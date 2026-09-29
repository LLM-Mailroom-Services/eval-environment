#!/usr/bin/env bash
# DeepSeek v4.1-Flash — SAND-027 Leg B N=20 specialist suite (sequential tasks).
# Same seed-42 class draws as qwen3-8b / Granite; concurrency 8 within each task.
# One coverage call per document (no source chunking); max 2 LLM calls/doc (retry).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
export BRAINTRUST_PROJECT="${BRAINTRUST_PROJECT:-Mailroom-Evals}"
set -a
# shellcheck disable=SC1091
[ -f .env ] && source .env
set +a

MODEL="deepseek/deepseek-v4.1-flash"
LOG="${DEEPSEEK41_N20_LOG:-/tmp/deepseek41-n20-specialists.log}"

run_wave() {
  local cls="$1" task="$2"
  echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) class=${cls} task=${task} model=${MODEL} ===" | tee -a "$LOG"
  uv run python -u scripts/run_evals.py \
    --task "$task" \
    --real \
    --subset "class:${cls}" \
    --sample 20 \
    --seed 42 \
    --model "$MODEL" \
    --require-trace-sink \
    --prompt-source frozen \
    --trace-backend braintrust \
    --concurrency 8 \
    2>&1 | tee -a "$LOG"
}

SPECS=(
  "correspondence eval:correspondence"
  "insurance_claim eval:insurance_claims"
  "contract eval:contracts"
  "merger_agreement eval:merger_agreement"
  "corporate_record eval:corporate_records"
)

: >"$LOG"
for spec in "${SPECS[@]}"; do
  # shellcheck disable=SC2086
  set -- $spec
  run_wave "$1" "$2"
done
echo "=== ALL DEEPSEEK V4.1 N=20 SPECIALISTS DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
