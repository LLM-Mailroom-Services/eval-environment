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

Compare JSON/MD files land in this directory after the wave completes.
