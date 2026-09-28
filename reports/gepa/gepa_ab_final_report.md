# GEPA specialist mutation campaign — final report

**Date:** 2026-09-28  
**Model:** `qwen/qwen3.7-flash` (OpenRouter)  
**Draw:** seed **42**, class subsets per specialist  
**Accept rule:** paired `overall_score`, bootstrap **CI lo > 0** (`compare_runs.py --record`)

## Executive summary

- **Spend:** ~**$1.36** estimated OpenRouter (under $2 cap, but over the intended mutation budget).
- **Promotions:** **1 / 5** — **`contracts_specialist_v3`** accepted vs frozen v1 baseline.
- **Deliverables:** full comparison archive, experiment-log records, mutation lineage, automation fixes, draft PR **#64**.

## Accepted promotion

| Baseline run | Candidate run | Version | n | Mean Δ | CI lo | CI hi |
|--------------|---------------|---------|---|--------|-------|-------|
| `20260928T054828Z-eval-contracts` | `20260928T063713Z-eval-contracts` | `contracts_specialist_v3` | 50 | +0.0837 | +0.0216 | +0.1501 |

**Mutation note:** v2 added CUAD `cuad_clauses` / parties guidance (+0.0652 mean at N=50 but CI crossed 0). v3 tightened: no invented Atticus labels; party names in `parties[]` only.

## v2 A/B results (frozen v1 vs `*_specialist_v2`)

| Specialist | N=20 recorded | N=50 recorded | v2 paired Δ (best) | CI lo (best) |
|------------|---------------|---------------|--------------------|--------------|
| correspondence | yes | yes | +0.0114 | −0.0023 |
| insurance_claims | yes | yes | −0.0034 | −0.0124 |
| contracts | yes | yes | +0.0652 | −0.0036 |
| merger_agreement | yes | yes | −0.0176 | −0.0434 |
| corporate_records | yes | yes | −0.0026 | −0.0146 |

Merger and corporate **v2** mutations were **drafted, Gate-5-validated, and exercised** on real evals (objective satisfied for “draft and test”).

## Follow-on iterations (v3/v4, N=100)

Documented in experiment log; all **REJECT** except contracts v3 above. Notable: correspondence v2 **did not** improve at N=100; corporate v4 reached CI lo **−0.0064** (still reject).

## Where to look

| Artifact | Purpose |
|----------|---------|
| [reports/gepa-comparisons/README.md](../gepa-comparisons/README.md) | Index of paired compares |
| [reports/gepa/gepa_ab_roster_summary.json](gepa_ab_roster_summary.json) | N=50 v2 roster JSON |
| [reports/experiment_log.jsonl](../experiment_log.jsonl) | Append-only run + `comparison_result` rows |
| [prompts/mutations.json](../../prompts/mutations.json) | Registered mutation texts |
| `data/experiments/<run_id>/` | Case-level rows for OBSERVE / re-score |

## Goal checklist

| Requirement | Met? |
|-------------|------|
| N=20 seed-42 v1 vs v2, all five specialists, `--record` | **Yes** |
| Cost-efficient Qwen 3.7 Flash | **Yes** |
| Merger/corporate v2 drafted & tested | **Yes** |
| Gate 5 (+120 chars specialists) | **Yes** |
| Publish `reports/gepa-comparisons` + log records | **Yes** |
| Commit via PR to main | **PR #64** (CI green; rebase onto main in progress) |
| **≥3/5 promotions** | **No (1/5)** |

## Recommended next steps (no spend implied)

1. **Merge PR #64** to land artifacts and `contracts_specialist_v3` lineage.
2. **Promote contracts v3** in pipeline config when product is ready (comparison already logged).
3. For correspondence/corporate, use **failure exports** + OBSERVE before any new paid A/B.
4. Re-open budget only with a **per-specialist cap** (merger/contracts dominate cost).
