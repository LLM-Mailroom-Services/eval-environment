# GEPA objective status (Qwen 3.7 Flash, seed 42)

**Last updated:** 2026-09-28  
**Spend:** frozen — see [gepa_ab_budget_status.md](gepa_ab_budget_status.md) and preflight gates (#67).

## Success criterion: ≥3/5 promotions

| Specialist | v2 @ N=20 (recorded) | v2 @ N=50 CI lo | Accepted? |
|------------|----------------------|-----------------|-----------|
| correspondence | Δ −0.0026, CI lo −0.0257 | +0.0114, **−0.0023** | no |
| insurance_claims | Δ −0.0039, CI lo −0.0223 | −0.0034, −0.0124 | no |
| contracts | Δ −0.0297, CI lo −0.1337 | +0.0652, **−0.0036** | no (v3 **yes** @ N=50) |
| merger_agreement | Δ −0.0101, CI lo −0.0759 | −0.0176, −0.0434 | no |
| corporate_records | Δ +0.0110, CI lo −0.0131 | −0.0026, −0.0146 | no |

**Score:** **1 / 5** accepted on Qwen (`contracts_specialist_v3` only). Objective **not met**.

## Deliverables (on `main`)

- N=20 v1 vs v2, all five: experiment log `comparison_result` rows + [gepa-comparisons/README.md](../gepa-comparisons/README.md)
- Merger/corporate v2 in `prompts/mutations.json`
- PR #64 merged; spend gates PR #67 merged

## Case-level signal (N=50 v2 candidates vs v1 baselines)

Paired `overall_score` wins (candidate vs baseline, same seed-42 draw):

| Pair | Candidate wins | Baseline wins | Ties | Mean Δ |
|------|----------------|---------------|------|--------|
| correspondence v2 | 8 | 7 | 35 | +0.0114 |
| contracts v2 | 30 | 8 | 12 | +0.0652 |
| corporate v2 | 12 | 10 | 28 | −0.0026 |

Correspondence and contracts v2 show **positive mean** but **bootstrap CI lo ≤ 0** (high tie mass / variance). Promotion needs either tighter mutations on failure modes or larger n — **not attempted** after spend stop.

## Zero-cost OBSERVE (before any re-open)

Re-export failures (no LLM):

```bash
uv run python scripts/score_run.py --run-id 20260928T052606Z-eval-correspondence \
  --export-failures data/manifests/gepa_observe_correspondence_v1_n50.jsonl
uv run python scripts/score_run.py --run-id 20260928T055822Z-eval-contracts \
  --export-failures data/manifests/gepa_observe_contracts_v2_candidate_n50.jsonl
```

See [next_wave_observe.md](next_wave_observe.md).

## To resume paid work (operator only)

Unset `EVALS_REAL_RUNS_DISABLED`, set `GEPA_SPEND_APPROVED=1` and `GEPA_AB_BUDGET_USD`, keep **`GEPA_AB_SAMPLE=20`** if staying on the original v2 objective.
