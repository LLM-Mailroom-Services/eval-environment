#!/usr/bin/env bash
# Full GEPA roster at N=50 (seed 42), Qwen 3.7 Flash, $2 hard budget (incl. prior spend).
# To raise the cap: export GEPA_AB_BUDGET_USD=<amount> only after explicit go-ahead.
set -euo pipefail
cd "$(dirname "$0")/.."
export GEPA_AB_SAMPLE=50
export GEPA_AB_BUDGET_USD=2.00
export GEPA_AB_SPENT_PRIOR_USD=0.037
export GEPA_AB_ROSTER_SKIP=0
export GEPA_AB_SEED_RESULTS=""
unset GEPA_AB_APPEND_LOG
exec ./scripts/run_gepa_ab_roster_n20.sh
