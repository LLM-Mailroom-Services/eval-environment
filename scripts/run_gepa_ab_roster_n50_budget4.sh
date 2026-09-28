#!/usr/bin/env bash
# DEPRECATED: use run_gepa_ab_roster_n50_budget2.sh ($2 cap). Kept for explicit override only.
set -euo pipefail
echo "Use ./scripts/run_gepa_ab_roster_n50_budget2.sh (default \$2 cap)." >&2
echo "Higher budget requires confirmation: GEPA_AB_BUDGET_USD=<amount> $0" >&2
exit 1
