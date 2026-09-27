#!/usr/bin/env bash
# SAND-027 Leg B: N=20 probe waves (handoff docs/handoff/HANDOFF.md)
set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
cd "$(dirname "$0")/.."
set -a
# shellcheck disable=SC1091
source .env
set +a

LOG="reports/api-comparisons/sand027-n20-run.log"
mkdir -p reports/api-comparisons
touch "$LOG"

run_wave() {
  local cls="$1" task="$2" model="$3" profile="$4"
  echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) class=${cls} model=${model} profile=${profile} ===" | tee -a "$LOG"
  uv run python scripts/run_evals.py \
    --task "$task" \
    --real \
    --subset "class:${cls}" \
    --sample 20 \
    --seed 42 \
    --model "$model" \
    --decode-profile "$profile" \
    --require-trace-sink \
    --prompt-source frozen \
    --trace-backend auto \
    2>&1 | tee -a "$LOG"
}

SPECS=(
  "correspondence eval:correspondence"
  "insurance_claim eval:insurance_claims"
  "contract eval:contracts"
  "merger_agreement eval:merger_agreement"
  "corporate_record eval:corporate_records"
)

echo "=== Qwen leg $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
for spec in "${SPECS[@]}"; do
  # shellcheck disable=SC2086
  set -- $spec
  run_wave "$1" "$2" "qwen/qwen3-8b" "qwen3-8b"
done

echo "=== Granite leg $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
for spec in "${SPECS[@]}"; do
  # shellcheck disable=SC2086
  set -- $spec
  run_wave "$1" "$2" "ibm-granite/granite-4.2-8b" "granite-4.2-8b"
done

echo "=== ALL WAVES DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
