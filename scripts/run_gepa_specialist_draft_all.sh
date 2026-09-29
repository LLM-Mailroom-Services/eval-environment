#!/usr/bin/env bash
# GEPA DRAFT — one v2 mutation per specialist from merged OBSERVE manifests.
set -euo pipefail
cd "$(dirname "$0")/.."

uv run python scripts/gepa_observe_specialists.py --all-defaults

declare -A PARENT=(
  [correspondence]=correspondence_specialist_v1
  [insurance_claims]=insurance_claims_specialist_v1
  [contracts]=contracts_specialist_v1
  [merger_agreement]=merger_agreement_specialist_v1
  [corporate_records]=corporate_records_specialist_v1
)

LOG="${GEPA_DRAFT_LOG:-/tmp/gepa-specialist-draft.log}"
: >"$LOG"

for task in correspondence insurance_claims contracts merger_agreement corporate_records; do
  manifest="data/manifests/gepa/${task}_merged.failures.jsonl"
  parent="${PARENT[$task]}"
  echo "=== DRAFT ${task} parent=${parent} ===" | tee -a "$LOG"
  uv run python scripts/prompt_engineer.py \
    --manifest "$manifest" \
    --parent "$parent" \
    --apply \
    2>&1 | tee -a "$LOG" || echo "DRAFT FAILED for ${task} (see log)" | tee -a "$LOG"
done

echo "=== ALL DRAFTS ATTEMPTED $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
