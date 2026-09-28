# GEPA specialist A/B comparisons (Qwen 3.7 Flash, seed 42)

OpenRouter model `qwen/qwen3.7-flash`, paired bootstrap on `overall_score` (`compare_runs.py --record`).

## N=50 roster (v1 frozen vs v2 mutation)

| Task | Baseline | Candidate (v2) | Accepted (CI lo > 0) |
|------|----------|----------------|----------------------|
| correspondence | `20260928T052606Z-eval-correspondence` | `20260928T053010Z-eval-correspondence` | no (Δ +0.0114, CI lo −0.0023) |
| insurance_claims | `20260928T053903Z-eval-insurance_claims` | `20260928T054349Z-eval-insurance_claims` | no (Δ −0.0034, CI lo −0.0124) |
| contracts | `20260928T054828Z-eval-contracts` | `20260928T055822Z-eval-contracts` | no (Δ +0.0652, CI lo −0.0036) |
| merger_agreement | `20260928T060919Z-eval-merger_agreement` | `20260928T061548Z-eval-merger_agreement` | no (Δ −0.0176, CI lo −0.0434) |
| corporate_records | `20260928T062251Z-eval-corporate_records` | `20260928T062755Z-eval-corporate_records` | no (Δ −0.0026, CI lo −0.0146) |

Summary JSON: `reports/gepa/gepa_ab_roster_summary.json`. Comparison records are appended to `reports/experiment_log.jsonl` as `comparison_result` rows.

## N=20 v1 vs v2 (seed 42, all five specialists)

| Task | Baseline | Candidate (v2) | Δ | CI lo | Accepted |
|------|----------|----------------|---|-------|----------|
| correspondence | `20260928T050127Z` | `20260928T050325Z` | −0.0026 | −0.0257 | no |
| insurance_claims | `20260928T051701Z` | `20260928T051905Z` | −0.0039 | −0.0223 | no |
| contracts | `20260928T075346Z` | `20260928T075959Z` | −0.0297 | −0.1337 | no |
| merger_agreement | `20260928T080542Z` | `20260928T080826Z` | −0.0101 | −0.0759 | no |
| corporate_records | `20260928T074850Z` | `20260928T075116Z` | +0.0110 | −0.0131 | no |

Cross-model check (DeepSeek v4.1, GEPA-best mutations @ N=20): [deepseek-v4.1-flash/README.md](deepseek-v4.1-flash/README.md).

## Promotions (accepted comparisons)

| Specialist | Version | n | CI lo | Run pair |
|------------|---------|---|-------|----------|
| contracts | v3 | 50 | +0.0216 | `20260928T054828Z` vs `20260928T063713Z` |

## Budget

**~$1.36 / $2.00** estimated OpenRouter spend on 2026-09-28 GEPA runs. Details: `reports/gepa/gepa_ab_budget_status.md` and `reports/gepa/gepa_ab_final_report.md`.

## N=20 v2 (completed for all five)

Contracts, merger, and corporate N=20 pairs were recorded on 2026-09-28 (`20260928T074850Z`–`20260928T080826Z` baselines). Correspondence and insurance N=20 pairs were recorded earlier the same day.

Correspondence v2 at **N=100** (same seed): REJECT (Δ −0.0084, CI lo −0.0193) — `20260928T072519Z` vs `20260928T073402Z`.

## Post-roster follow-ups (stopped 2026-09-28)

| Pair | Result |
|------|--------|
| Qwen v6 correspondence vs v1 @ N=50 | REJECT (Δ −0.0091, CI lo −0.0351) |
| DeepSeek merger v2 vs v1 @ N=50 | REJECT (Δ −0.2077, CI lo −0.3155) |

**No further paid evals** without explicit approval — see `reports/gepa/gepa_ab_budget_status.md`.
