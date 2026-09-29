#!/usr/bin/env bash
# Complete N=20 seed-42 v1 vs v2 for contracts/merger/corporate; v4 candidate compares (budget-conscious).
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source scripts/gepa_spend_guard.sh
gepa_require_spend_approval
export PYTHONUNBUFFERED=1
set -a; [ -f .env ] && source .env; set +a
LOG=/tmp/gepa-n20-v4.log
: >"$LOG"
MODEL=qwen/qwen3.7-flash
SEED=42

run_eval() {
  local task=$1 class=$2 sample=$3 pv=${4:-}
  local extra=()
  [[ -n "$pv" ]] && extra=(--prompt-version "$pv")
  uv run python -u scripts/run_evals.py --task "$task" --real --subset "class:$class" \
    --sample "$sample" --seed "$SEED" --model "$MODEL" "${extra[@]}" \
    --prompt-source frozen --trace-backend none --concurrency 8 >>"$LOG" 2>&1
}

last_run() {
  local task=$1 sample=$2 pv=${3:-}
  uv run python -c "
from evals import experiment_log
task='${task#eval:}'
sample=$sample
pv='${pv}'
runs=[r for r in experiment_log.load_runs() if r.get('task')==task and r.get('mode')=='real' and r.get('model')=='$MODEL']
runs=[r for r in runs if (r.get('params') or {}).get('sample')==sample]
if pv:
  runs=[r for r in runs if r.get('prompt_version')==pv]
else:
  runs=[r for r in runs if not r.get('prompt_version')]
print(runs[-1]['run_id'] if runs else '')
" 2>/dev/null | grep -E '^[0-9]{8}T[0-9]{6}Z-eval-' | tail -1
}

ab_n20() {
  local task=$1 class=$2 pv=$3
  echo "=== N=20 $task v1 vs $pv ===" | tee -a "$LOG"
  run_eval "$task" "$class" 20 ""
  base=$(last_run "$task" 20 "")
  run_eval "$task" "$class" 20 "$pv"
  cand=$(last_run "$task" 20 "$pv")
  uv run python scripts/compare_runs.py --a "$base" --b "$cand" --md reports/gepa-comparisons --record >>"$LOG" 2>&1
}

ab_n20 eval:corporate_records corporate_record corporate_records_specialist_v2
ab_n20 eval:contracts contract contracts_specialist_v2
ab_n20 eval:merger_agreement merger_agreement merger_agreement_specialist_v2

echo "=== v4 N=50 candidates ===" | tee -a "$LOG"
run_eval eval:correspondence correspondence 50 correspondence_specialist_v4
corr=$(last_run eval:correspondence 50 correspondence_specialist_v4)
uv run python scripts/compare_runs.py --a 20260928T052606Z-eval-correspondence --b "$corr" --md reports/gepa-comparisons --record >>"$LOG" 2>&1

run_eval eval:corporate_records corporate_record 50 corporate_records_specialist_v4
corp=$(last_run eval:corporate_records 50 corporate_records_specialist_v4)
uv run python scripts/compare_runs.py --a 20260928T062251Z-eval-corporate_records --b "$corp" --md reports/gepa-comparisons --record >>"$LOG" 2>&1

echo "=== COMPLETE ===" | tee -a "$LOG"
