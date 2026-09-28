#!/usr/bin/env bash
# GEPA EVALUATE — full specialist roster: v1 vs v2 on identical seed-42 N=20 draws.
# Same OpenRouter model both arms (default qwen/qwen3.7-flash). Records accept/reject.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
export BRAINTRUST_PROJECT="${BRAINTRUST_PROJECT:-Mailroom-Evals}"
export GEPA_AB_MODEL="${GEPA_AB_MODEL:-qwen/qwen3.7-flash}"
export GEPA_AB_SEED="${GEPA_AB_SEED:-42}"
export GEPA_AB_SAMPLE="${GEPA_AB_SAMPLE:-20}"
export GEPA_AB_CONCURRENCY="${GEPA_AB_CONCURRENCY:-8}"

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

run_arm() {
  local task="$1" class="$2" prompt_ver="${3:-}"
  local extra=()
  if [[ -n "$prompt_ver" ]]; then
    extra=(--prompt-version "$prompt_ver")
  fi
  echo "=== ARM task=${task} prompt=${prompt_ver:-v1_frozen} model=${GEPA_AB_MODEL} ===" | tee -a "$LOG"
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
    --concurrency "$GEPA_AB_CONCURRENCY" \
    2>&1 | tee -a "$LOG"
  uv run python -c "
from evals import experiment_log
task = '${task#eval:}'
pv = '${prompt_ver}' or None
runs = [r for r in experiment_log.load_runs() if r.get('task')==task and r.get('mode')=='real']
if pv:
    runs = [r for r in runs if r.get('prompt_version')==pv]
else:
    runs = [r for r in runs if not r.get('prompt_version')]
print(runs[-1]['run_id'] if runs else '')
"
}

: >"$LOG"
RESULT_LINES=()

for spec in "${SPECS[@]}"; do
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
Path('$SUMMARY').write_text(json.dumps({'model': '$GEPA_AB_MODEL', 'seed': $GEPA_AB_SEED, 'n': $GEPA_AB_SAMPLE, 'results': rows}, indent=2))
print('summary → $SUMMARY')
"

echo "=== ROSTER A/B COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
