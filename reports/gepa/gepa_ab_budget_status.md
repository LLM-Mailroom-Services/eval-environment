# GEPA A/B budget status (final snapshot 2026-09-28)

**Configured cap:** $2.00 OpenRouter (`GEPA_AB_BUDGET_USD`)  
**Estimated spend:** **~$1.36** (29 real `qwen/qwen3.7-flash` eval runs on 2026-09-28, sum of `cost_usd_est_total`)  
**Status:** **STOP — no further `--real` evals** without explicit operator approval (2026-09-28).

**Experiment-log rollup (estimated `cost_usd_est_total`, all real runs):** ~**$4.52** across 79 runs (2026-09-26–28). OpenRouter dashboard totals may differ (retries, unlogged probes, estimate error). The GEPA Qwen wave alone was ~$1.36 of that; DeepSeek/Granite/N=50 follow-ups and merger re-runs account for most of the rest.

## Promotions (CI lo > 0 on paired `overall_score`)

| Specialist | Promoted version | n | Δ | CI lo |
|------------|------------------|---|---|-------|
| **contracts** | **`contracts_specialist_v3`** | 50 | +0.0837 | **+0.0216** |

**1 / 5** vs ≥3/5 goal.

## v2 roster (seed 42, primary objective)

All five specialists: N=20 and/or N=50 v1 frozen vs v2, `--record` in experiment log. None of the **v2-only** promotions met acceptance; contracts required **v3**.

## Artifacts

- `reports/gepa-comparisons/` (README index)
- `reports/gepa/gepa_ab_roster_summary.json`
- `reports/experiment_log.jsonl` (`comparison_result` rows)
- `prompts/mutations.json` (v2–v4 specialist lineage, Gate 5 compliant)
- PR **#64** → merge to `main` when ready

## Tracing

Braintrust monthly score quota exceeded during wave; local experiment log and comparisons complete.
