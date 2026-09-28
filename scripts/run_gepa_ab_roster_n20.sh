#!/usr/bin/env bash
# GEPA EVALUATE — full specialist roster: v1 vs v2 on identical seed-42 draws.
# Same OpenRouter model both arms (default qwen/qwen3.7-flash). Records accept/reject.
# Override sample: GEPA_AB_SAMPLE (default 50 for CI surface). Hard cap: GEPA_AB_BUDGET_USD.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
export BRAINTRUST_PROJECT="${BRAINTRUST_PROJECT:-Mailroom-Evals}"
export GEPA_AB_MODEL="${GEPA_AB_MODEL:-qwen/qwen3.7-flash}"
export GEPA_AB_SEED="${GEPA_AB_SEED:-42}"
export GEPA_AB_SAMPLE="${GEPA_AB_SAMPLE:-50}"
export GEPA_AB_CONCURRENCY="${GEPA_AB_CONCURRENCY:-8}"
export GEPA_AB_BUDGET_USD="${GEPA_AB_BUDGET_USD:-4.00}"
export GEPA_AB_SPENT_PRIOR_USD="${GEPA_AB_SPENT_PRIOR_USD:-0.037}"
GEPA_AB_SPENT_FILE="${GEPA_AB_SPENT_FILE:-/tmp/gepa-ab-roster-spent.txt}"
echo "${GEPA_AB_SPENT_PRIOR_USD}" >"$GEPA_AB_SPENT_FILE"

set -a
# shellcheck disable=SC1091
[ -f .env ] && source .env
set +a

LOG="${GEPA_AB_ROSTER_LOG:-/tmp/gepa-ab-roster.log}"
SUMMARY="${GEPA_AB_SUMMARY:-reports/gepa/gepa_ab_roster_summary.json}"
mkdir -p reports/gepa reports/gepa-comparisons

declare -a SPECS=(
  "eval:correspondence correspondence correspondence_specialist_v2"
  "eval:insurance_claims insurance_claim insurance_claims_specialist_v2"
  "eval:contracts contract contracts_specialist_v2"
  "eval:merger_agreement merger_agreement merger_agreement_specialist_v2"
  "eval:corporate_records corporate_record corporate_records_specialist_v2"
)

run_arm_cost_usd() {
  local run_id="$1"
  uv run python -c "
from evals import experiment_log
rid = '''$run_id'''
for r in experiment_log.load_runs():
    if r.get('run_id') == rid:
        perf = r.get('performance') or {}
        print(perf.get('cost_usd_est_total') or r.get('cost_usd_est_total') or 0)
        break
else:
    print(0)
"
}

budget_ok_or_stop() {
  local spent
  spent="$(awk '{s+=$1} END {printf \"%.4f\", s+0}' "$GEPA_AB_SPENT_FILE" 2>/dev/null || echo 0)"
  if awk -v s="$spent" -v cap="$GEPA_AB_BUDGET_USD" 'BEGIN { exit (s <= cap + 0.0001) ? 0 : 1 }'; then
    echo "budget ok: spent=\$${spent} cap=\$${GEPA_AB_BUDGET_USD}" | tee -a "$LOG"
    return 0
  fi
  echo "BUDGET STOP: spent=\$${spent} exceeds cap=\$${GEPA_AB_BUDGET_USD}" | tee -a "$LOG"
  exit 2
}

run_arm() {
  local task="$1" class="$2" prompt_ver="${3:-}"
  budget_ok_or_stop
  local extra=()
  if [[ -n "$prompt_ver" ]]; then
    extra=(--prompt-version "$prompt_ver")
  fi
  {
    echo "=== ARM task=${task} prompt=${prompt_ver:-v1_frozen} model=${GEPA_AB_MODEL} ==="
    uv run python -u scripts/run_evals.py \
      --task "$task" \
      --real \
      --subset "class:${class}" \
      --sample "$GEPA_AB_SAMPLE" \
      --seed "$GEPA_AB_SEED" \
      --model "$GEPA_AB_MODEL" \
      "${extra[@]}" \
      --require-trace-sink \
      --prompt-source frozen \
      --trace-backend braintrust \
      --concurrency "$GEPA_AB_CONCURRENCY"
  } >>"$LOG" 2>&1
  local run_id
  run_id="$(uv run python -c "
from evals import experiment_log
task = '${task#eval:}'
model = '${GEPA_AB_MODEL}'
sample = int('${GEPA_AB_SAMPLE}')
pv = '${prompt_ver}' or None
runs = [r for r in experiment_log.load_runs() if r.get('task')==task and r.get('mode')=='real' and r.get('model')==model]
runs = [r for r in runs if (r.get('params') or {}).get('sample') == sample or (r.get('dataset') or {}).get('n_selected') == sample]
runs = [r for r in runs if (r.get('prompt_version')==pv if pv else not r.get('prompt_version'))]
print(runs[-1]['run_id'] if runs else '')
")"
  if [[ -n "$run_id" ]]; then
    cost="$(run_arm_cost_usd "$run_id")"
    echo "$cost" >>"$GEPA_AB_SPENT_FILE"
    echo "arm cost run_id=$run_id usd=$cost" >>"$LOG"
  fi
  echo "$run_id"
}

if [[ -z "${GEPA_AB_APPEND_LOG:-}" ]]; then
  : >"$LOG"
fi
RESULT_LINES=()
if [[ -n "${GEPA_AB_SEED_RESULTS:-}" ]]; then
  while IFS= read -r line; do
    [[ -n "$line" ]] && RESULT_LINES+=("$line")
  done <<< "$GEPA_AB_SEED_RESULTS"
fi
# Optional resume: skip first N roster entries (after fixing run_arm / manual compares).
GEPA_AB_ROSTER_SKIP="${GEPA_AB_ROSTER_SKIP:-0}"

idx=0
for spec in "${SPECS[@]}"; do
  if (( idx < GEPA_AB_ROSTER_SKIP )); then
    idx=$((idx + 1))
    continue
  fi
  idx=$((idx + 1))
  # shellcheck disable=SC2086
  set -- $spec
  TASK="$1"; CLASS="$2"; V2="$3"
  echo "======== ROSTER A/B ${TASK} ========" | tee -a "$LOG"
  BASE_RUN="$(run_arm "$TASK" "$CLASS" "")"
  CAND_RUN="$(run_arm "$TASK" "$CLASS" "$V2")"
  echo "baseline=${BASE_RUN} candidate=${CAND_RUN}" | tee -a "$LOG"
  if [[ -z "$BASE_RUN" || -z "$CAND_RUN" ]]; then
    echo "SKIP compare — missing run_id" | tee -a "$LOG"
    continue
  fi
  CMP_OUT="$(uv run python scripts/compare_runs.py --a "$BASE_RUN" --b "$CAND_RUN" --record --json 2>&1 | tee -a "$LOG")"
  ACCEPTED="$(echo "$CMP_OUT" | uv run python -c "import sys,json; d=json.load(sys.stdin); p=(d.get('paired_case_deltas') or {}); v=next(iter(p.values()),{}); print('yes' if v.get('ci_lo',0)>0 else 'no')" 2>/dev/null || echo "unknown")"
  RESULT_LINES+=("{\"task\":\"${TASK#eval:}\",\"baseline\":\"$BASE_RUN\",\"candidate\":\"$CAND_RUN\",\"v2\":\"$V2\",\"accepted\":\"$ACCEPTED\"}")
done

uv run python -c "
import json
from pathlib import Path
lines = '''$(printf '%s\n' "${RESULT_LINES[@]}")'''.strip().splitlines()
rows = [json.loads(l) for l in lines if l.strip()]
spent = float('''$(awk '{s+=$1} END {print s+0}' "$GEPA_AB_SPENT_FILE" 2>/dev/null || echo 0)''')
Path('$SUMMARY').write_text(json.dumps({
    'model': '$GEPA_AB_MODEL', 'seed': $GEPA_AB_SEED, 'n': $GEPA_AB_SAMPLE,
    'budget_usd_cap': float('$GEPA_AB_BUDGET_USD'),
    'spent_usd_est': spent,
    'results': rows,
}, indent=2))
print('summary → $SUMMARY')
"

echo "=== ROSTER A/B COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
