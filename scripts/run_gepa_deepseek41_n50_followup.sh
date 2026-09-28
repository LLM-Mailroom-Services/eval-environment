#!/usr/bin/env bash
# DeepSeek v4.1 — N=50 paired follow-up for merger v2 + contracts v3 (seed 42).
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source scripts/gepa_spend_guard.sh
gepa_require_spend_approval
export PYTHONUNBUFFERED=1
export BRAINTRUST_PROJECT="${BRAINTRUST_PROJECT:-Mailroom-Evals}"
MODEL="${GEPA_AB_MODEL:-deepseek/deepseek-v4.1-flash}"
SEED="${GEPA_AB_SEED:-42}"
SAMPLE="${GEPA_AB_SAMPLE:-50}"
CONCURRENCY="${GEPA_AB_CONCURRENCY:-8}"
REPORT_DIR="reports/gepa-comparisons/deepseek-v4.1-flash"
LOG="${GEPA_DEEPSEEK_N50_LOG:-/tmp/gepa-deepseek41-n50-followup.log}"

set -a
# shellcheck disable=SC1091
[ -f .env ] && source .env
set +a

mkdir -p "$REPORT_DIR"
: >"$LOG"

run_arm() {
  local task="$1" class="$2" pv="${3:-}"
  local extra=()
  [[ -n "$pv" ]] && extra=(--prompt-version "$pv")
  echo "=== ARM task=$task pv=${pv:-v1} n=$SAMPLE ===" | tee -a "$LOG"
  uv run python -u scripts/run_evals.py \
    --task "$task" --real --subset "class:${class}" \
    --sample "$SAMPLE" --seed "$SEED" --model "$MODEL" \
    "${extra[@]}" --require-trace-sink --prompt-source frozen \
    --trace-backend braintrust --concurrency "$CONCURRENCY" >>"$LOG" 2>&1
  uv run python -c "
from evals import experiment_log
task='${task#eval:}'
pv='${pv}' or None
runs=[r for r in experiment_log.load_runs() if r.get('task')==task and r.get('mode')=='real' and r.get('model')=='${MODEL}']
runs=[r for r in runs if (r.get('prompt_version')==pv if pv else not r.get('prompt_version'))]
runs=[r for r in runs if (r.get('params') or {}).get('sample')==${SAMPLE} or (r.get('dataset') or {}).get('n_selected')==${SAMPLE})]
print(runs[-1]['run_id'] if runs else '')
" 2>/dev/null | grep -E '^[0-9]{8}T[0-9]{6}Z-eval-' | tail -1
}

pair_ab() {
  local task="$1" class="$2" pv="$3"
  echo "======== N=50 PAIR ${task} ${pv} ========" | tee -a "$LOG"
  base="$(run_arm "$task" "$class" "")"
  cand="$(run_arm "$task" "$class" "$pv")"
  echo "baseline=$base candidate=$cand" | tee -a "$LOG"
  uv run python scripts/compare_runs.py --a "$base" --b "$cand" --record --md "$REPORT_DIR" >>"$LOG" 2>&1
}

pair_ab "eval:merger_agreement" merger_agreement merger_agreement_specialist_v2
pair_ab "eval:contracts" contract contracts_specialist_v3

echo "=== DEEPSEEK N=50 FOLLOWUP DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
