# DeepSeek v4.1 Flash × GEPA best mutations (N=20, seed 42)

Paired A/B: **frozen v1 baseline** (2026-09-27 DeepSeek Leg B runs) vs **GEPA-best mutation** per specialist on the **same** seed-42 class draw.

| Specialist | Mutation tested | v1 baseline run |
|------------|-----------------|-----------------|
| correspondence | `correspondence_specialist_v2` | `20260927T105317Z-eval-correspondence` |
| insurance_claims | `insurance_claims_specialist_v2` | `20260927T105400Z-eval-insurance_claims` |
| contracts | `contracts_specialist_v3` | `20260927T105549Z-eval-contracts` |
| merger_agreement | `merger_agreement_specialist_v2` | `20260927T110153Z-eval-merger_agreement` |
| corporate_records | `corporate_records_specialist_v2` | `20260927T110828Z-eval-corporate_records` |

**Runner:** `scripts/run_gepa_deepseek41_best_mutations_n20.sh`  
**Accept rule:** paired `overall_score`, bootstrap CI lo > 0 (`compare_runs.py --record`).

## Results (2026-09-28 wave)

| Specialist | Mutation | Δ | CI lo | Accepted |
|------------|----------|---|-------|----------|
| **corporate_records** | v2 | +0.0209 | **+0.0006** | **Yes** |
| merger_agreement | v2 | +0.1861 | −0.0525 | No |
| contracts | v3 | +0.1082 | −0.0354 | No |
| correspondence | v2 | −0.0172 | −0.0453 | No |
| insurance_claims | v2 | −0.0062 | −0.0166 | No |

Full write-up: [reports/gepa/gepa_deepseek41_mutations_report.md](../../gepa/gepa_deepseek41_mutations_report.md)
