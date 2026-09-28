#!/usr/bin/env bash
# GEPA mutations on DeepSeek v4.1 Flash — N=20 seed-42, candidate-only vs frozen v1 baselines.
# Reuses 20260927 DeepSeek v1 runs (same draw as SAND-027 Leg B). Records compare_runs --record.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
export BRAINTRUST_PROJECT="${BRAINTRUST_PROJECT:-Mailroom-Evals}"
export GEPA_AB_MODEL="${GEPA_AB_MODEL:-deepseek/deepseek-v4.1-flash}"
export GEPA_AB_SEED="${GEPA_AB_SEED:-42}"
export GEPA_AB_SAMPLE="${GEPA_AB_SAMPLE:-20}"
export GEPA_AB_CONCURRENCY="${GEPA_AB_CONCURRENCY:-8}"

set -a
# shellcheck disable=SC1091
[ -f .env ] && source .env
set +a

LOG="${GEPA_DEEPSEEK_MUT_LOG:-/tmp/gepa-deepseek41-mutations-n20.log}"
REPORT_DIR="${GEPA_DEEPSEEK_REPORT_DIR:-reports/gepa-comparisons/deepseek-v4.1-flash}"
mkdir -p "$REPORT_DIR" reports/gepa

# task class baseline_run_id prompt_version_key
declare -a SPECS=(
  "eval:correspondence correspondence 20260927T105317Z-eval-correspondence correspondence_specialist_v2"
  "eval:insurance_claims insurance_claim 20260927T105400Z-eval-insurance_claims insurance_claims_specialist_v2"
  "eval:contracts contract 20260927T105549Z-eval-contracts contracts_specialist_v3"
  "eval:merger_agreement merger_agreement 20260927T110153Z-eval-merger_agreement merger_agreement_specialist_v2"
  "eval:corporate_records corporate_record 20260927T110828Z-eval-corporate_records corporate_records_specialist_v2"
)

run_candidate() {
  local task="$1" class="$2" prompt_ver="$3"
  {
    echo "=== CAND task=${task} prompt=${prompt_ver} model=${GEPA_AB_MODEL} n=${GEPA_AB_SAMPLE} seed=${GEPA_AB_SEED} ==="
    uv run python -u scripts/run_evals.py \
      --task "$task" \
      --real \
      --subset "class:${class}" \
      --sample "$GEPA_AB_SAMPLE" \
      --seed "$GEPA_AB_SEED" \
      --model "$GEPA_AB_MODEL" \
      --prompt-version "$prompt_ver" \
      --require-trace-sink \
      --prompt-source frozen \
      --trace-backend braintrust \
      --concurrency "$GEPA_AB_CONCURRENCY"
  } >>"$LOG" 2>&1
  uv run python -c "
from evals import experiment_log
task = '${task#eval:}'
model = '${GEPA_AB_MODEL}'
pv = '${prompt_ver}'
sample = int('${GEPA_AB_SAMPLE}')
runs = [r for r in experiment_log.load_runs() if r.get('task')==task and r.get('mode')=='real' and r.get('model')==model and r.get('prompt_version')==pv]
runs = [r for r in runs if (r.get('params') or {}).get('sample') == sample or (r.get('dataset') or {}).get('n_selected') == sample]
print(runs[-1]['run_id'] if runs else '')
" 2>/dev/null | grep -E '^[0-9]{8}T[0-9]{6}Z-eval-' | tail -1 | tr -d '\r'
}

if [[ -z "${GEPA_DEEPSEEK_APPEND_LOG:-}" ]]; then
  : >"$LOG"
fi
RESULT_LINES=()

for spec in "${SPECS[@]}"; do
  # shellcheck disable=SC2086
  set -- $spec
  TASK="$1"; CLASS="$2"; BASELINE="$3"; PROMPT="$4"
  echo "======== DEEPSEEK GEPA ${TASK} ${PROMPT} ========" | tee -a "$LOG"
  CAND_RUN="$(run_candidate "$TASK" "$CLASS" "$PROMPT")"
  echo "baseline=${BASELINE} candidate=${CAND_RUN}" | tee -a "$LOG"
  if [[ -z "$CAND_RUN" ]]; then
    echo "SKIP compare — missing candidate run_id" | tee -a "$LOG"
    continue
  fi
  CMP_JSON="$(mktemp)"
  uv run python scripts/compare_runs.py --a "$BASELINE" --b "$CAND_RUN" --record --json --md "$REPORT_DIR" >"$CMP_JSON" 2>>"$LOG"
  cat "$CMP_JSON" >>"$LOG"
  ACCEPTED="$(CMP_JSON="$CMP_JSON" uv run python -c "
import json, os
d = json.load(open(os.environ['CMP_JSON']))
p = d.get('paired_case_deltas') or {}
v = next(iter(p.values()), {})
print('yes' if (v.get('ci_lo') or 0) > 0 else 'no')
" 2>/dev/null || echo "unknown")"
  rm -f "$CMP_JSON"
  RESULT_LINES+=("{\"task\":\"${TASK#eval:}\",\"baseline\":\"$BASELINE\",\"candidate\":\"$CAND_RUN\",\"mutation\":\"$PROMPT\",\"accepted\":\"$ACCEPTED\"}")
done

uv run python -c "
import json
from pathlib import Path
lines = '''$(printf '%s\n' "${RESULT_LINES[@]}")'''.strip().splitlines()
rows = [json.loads(l) for l in lines if l.strip()]
Path('reports/gepa/gepa_deepseek41_mutations_summary.json').write_text(json.dumps({
    'model': '$GEPA_AB_MODEL', 'seed': $GEPA_AB_SEED, 'n': $GEPA_AB_SAMPLE,
    'baselines': '20260927 DeepSeek v1 frozen (seed 42)',
    'results': rows,
}, indent=2))
print('summary → reports/gepa/gepa_deepseek41_mutations_summary.json')
"

echo "=== DEEPSEEK GEPA MUTATIONS N=20 DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
