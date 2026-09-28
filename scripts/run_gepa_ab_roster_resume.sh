#!/usr/bin/env bash
# Resume roster after correspondence + insurance_claims (manual compares recorded).
set -euo pipefail
cd "$(dirname "$0")/.."
export GEPA_AB_ROSTER_SKIP=2
export GEPA_AB_SEED_RESULTS=$'{"task":"correspondence","baseline":"20260928T050127Z-eval-correspondence","candidate":"20260928T050325Z-eval-correspondence","v2":"correspondence_specialist_v2","accepted":"no"}\n{"task":"insurance_claims","baseline":"20260928T051701Z-eval-insurance_claims","candidate":"20260928T051905Z-eval-insurance_claims","v2":"insurance_claims_specialist_v2","accepted":"no"}'
# Do not truncate log when resuming
export GEPA_AB_ROSTER_LOG="${GEPA_AB_ROSTER_LOG:-/tmp/gepa-ab-roster.log}"
export GEPA_AB_APPEND_LOG=1
exec ./scripts/run_gepa_ab_roster_n20.sh
