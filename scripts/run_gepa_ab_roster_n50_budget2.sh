#!/usr/bin/env bash
# Full GEPA roster at N=50 (seed 42), Qwen 3.7 Flash, $2 hard budget (incl. prior spend).
# Skips correspondence (N=50 pair already recorded). To raise cap: export GEPA_AB_BUDGET_USD after confirmation.
set -euo pipefail
cd "$(dirname "$0")/.."
export GEPA_AB_SAMPLE=50
export GEPA_AB_BUDGET_USD=2.00
# N=20 pair (~0.037) + correspondence N=50 v1/v2 (~0.044)
export GEPA_AB_SPENT_PRIOR_USD="${GEPA_AB_SPENT_PRIOR_USD:-0.081}"
export GEPA_AB_ROSTER_SKIP=1
export GEPA_AB_SEED_RESULTS='{"task":"correspondence","baseline":"20260928T052606Z-eval-correspondence","candidate":"20260928T053010Z-eval-correspondence","v2":"correspondence_specialist_v2","accepted":"no"}'
export GEPA_AB_APPEND_LOG=1
exec ./scripts/run_gepa_ab_roster_n20.sh
