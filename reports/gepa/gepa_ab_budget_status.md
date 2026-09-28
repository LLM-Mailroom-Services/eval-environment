# GEPA A/B budget status (2026-09-28)

**Cap:** $2.00 OpenRouter (`GEPA_AB_BUDGET_USD`)  
**Estimated spend (20260928 real eval runs):** **~$1.08**  
**Runway:** **~$0.92** — insufficient for another merger-scale pair (~$0.32) plus contracts-scale pair (~$0.14) without explicit approval.

## Promotions (acceptance rule: paired `overall_score`, CI lo > 0)

| Specialist | Promoted version | Evidence |
|------------|------------------|----------|
| **contracts** | **`contracts_specialist_v3`** | `20260928T054828Z` vs `20260928T063713Z`, n=50, Δ +0.0837, CI lo **+0.0216** |
| correspondence | — | v2 N=50 CI lo −0.0023; N=100 v2 **REJECT** (Δ −0.0084, CI lo −0.0193) |
| insurance_claims | — | v2/v3 N=50 REJECT |
| merger_agreement | — | v2/v3 N=50 REJECT |
| corporate_records | — | v2/v3 N=50 REJECT |

**Score: 1 / 5** toward the ≥3/5 promotion goal.

## Completed work

- N=20 v1 vs v2 + `--record`: correspondence, insurance_claims.
- N=50 v1 vs v2 roster (seed 42, qwen/qwen3.7-flash): all five specialists.
- v3 follow-ups (contracts ACCEPT; others REJECT).
- Artifacts: `reports/gepa-comparisons/`, `reports/gepa/gepa_ab_roster_summary.json`, experiment log `comparison_result` rows.

## Tracing

Braintrust monthly score quota exceeded (11k/11k); local logging and experiment log unaffected.

## Recommendation

**Pause paid mutation A/B** until budget or success criteria are revised. Next marginal spend: targeted v4 on correspondence/corporate only (~$0.08–0.15), not full roster.
