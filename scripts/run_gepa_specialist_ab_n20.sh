#!/usr/bin/env bash
# GEPA EVALUATE — N=20 paired A/B for one specialist mutation vs frozen v1 baseline.
# Same class draw as SAND-027 (seed 42). Default eval model: Qwen 3.7 Flash (override via GEPA_AB_MODEL).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
export BRAINTRUST_PROJECT="${BRAINTRUST_PROJECT:-Mailroom-Evals}"

MODEL="${GEPA_AB_MODEL:-qwen/qwen3.7-flash}"
SEED="${GEPA_AB_SEED:-42}"
SAMPLE="${GEPA_AB_SAMPLE:-20}"
CONCURRENCY="${GEPA_AB_CONCURRENCY:-8}"

usage() {
  echo "Usage: $0 <eval_task> <class_subset> <prompt_version_key> [baseline_run_id]" >&2
  echo "  eval_task: eval:correspondence | eval:insurance_claims | eval:contracts | eval:merger_agreement | eval:corporate_records" >&2
  exit 1
}

TASK="${1:-}"; CLASS="${2:-}"; PROMPT_VER="${3:-}"; BASELINE="${4:-}"
[[ -n "$TASK" && -n "$CLASS" && -n "$PROMPT_VER" ]] || usage

set -a
# shellcheck disable=SC1091
[ -f .env ] && source .env
set +a

LOG="${GEPA_AB_LOG:-/tmp/gepa-specialist-ab.log}"
echo "=== GEPA A/B $(date -u +%Y-%m-%dT%H:%M:%SZ) task=${TASK} prompt=${PROMPT_VER} model=${MODEL} ===" | tee -a "$LOG"

uv run python -u scripts/run_evals.py \
  --task "$TASK" \
  --real \
  --subset "class:${CLASS}" \
  --sample "$SAMPLE" \
  --seed "$SEED" \
  --model "$MODEL" \
  --prompt-version "$PROMPT_VER" \
  --require-trace-sink \
  --prompt-source frozen \
  --trace-backend braintrust \
  --concurrency "$CONCURRENCY" \
  2>&1 | tee -a "$LOG"

CAND_RUN="$(grep -E '^run_id:' "$LOG" | tail -1 | awk '{print $2}')"
if [[ -z "$CAND_RUN" ]]; then
  CAND_RUN="$(grep -E 'run_id=' "$LOG" | tail -1 | sed 's/.*run_id=//')"
fi
# Runner prints summary line; parse latest eval run from experiment log if needed
if [[ -z "$CAND_RUN" ]]; then
  CAND_RUN="$(uv run python -c "
from evals import experiment_log
runs = [r for r in experiment_log.load_runs() if r.get('task')=='${TASK#eval:}' and r.get('prompt_version')=='${PROMPT_VER}']
print(runs[-1]['run_id'] if runs else '')
")"
fi

echo "candidate run_id: ${CAND_RUN:-unknown}" | tee -a "$LOG"

if [[ -n "$BASELINE" && -n "$CAND_RUN" ]]; then
  REPORT_DIR="reports/gepa-comparisons"
  mkdir -p "$REPORT_DIR"
  uv run python scripts/compare_runs.py \
    --a "$BASELINE" \
    --b "$CAND_RUN" \
    --md "$REPORT_DIR" \
    --record \
    2>&1 | tee -a "$LOG"
fi

echo "=== GEPA A/B DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
