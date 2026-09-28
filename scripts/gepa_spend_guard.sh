#!/usr/bin/env bash
# GEPA paid-eval gate — sourced by run_gepa_*.sh before any --real invoke.
gepa_require_spend_approval() {
  if [[ "${GEPA_SPEND_APPROVED:-}" != "1" ]]; then
    echo "REFUSED: paid GEPA evals require explicit approval." >&2
    echo "  export GEPA_SPEND_APPROVED=1" >&2
    echo "  export GEPA_AB_BUDGET_USD=<usd_cap>   # hard cap for roster scripts" >&2
    echo "See reports/gepa/gepa_ab_budget_status.md" >&2
    exit 2
  fi
  export EVALS_SPEND_APPROVED=1
}
