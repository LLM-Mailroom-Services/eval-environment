# Run report — `20260927T022750Z-eval-merger_agreement` (API leg)

> **Correction (2026-09-28):** this run is filed under `qwen3-8b` because that was its decode profile, but the model that served it was `qwen/qwen3.7-flash` (see the engine row and the per-agent models column). Do not compare it with Qwen3-8B results as the same model.

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T022750Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-27T02:27:50+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T022750Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `fd6a220` |
| finished | `2026-09-27T02:30:10+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | qwen3-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T022750Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T02:27:50+00:00` |
| finished_at | `2026-09-27T02:30:10+00:00` |
| duration_s (wall) | 142.0000 |
| latency_ms_mean | 45286.9 |
| latency_ms_p95 | 52445.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.3748 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.3748** (sd 0.2199, min 0.0000, max 0.6945) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 142.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0575** USD |
| cost estimated (roster token rates) | **0.0575** USD |
| cost per document (actual) | 0.0029 USD |
| cost per document (estimated) | 0.0029 USD |
| latency e2e / p50 / p95 / max | 142.0000 / 46.5884 / 52.4454 / 54.7646 s |
| prompt / completion / total tokens | 1422210 / 114281 / 1536491 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 905.7 s vs wall = 142.0 s -> wall/serial factor 6.38x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `none (pipeline posture)` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 8192, "corporate_records_specialist": 8192, "correspondence_specialist": 4096, "insurance_claims_specialist": 6144, "merger_agreement_specialist": 16384}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `merger_agreement_specialist` | 18 | 1422210 | 114281 | 1536491 | 0.0575 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 905.7 s over wall 142.0 s = **6.38×** effective parallelism at c8 (80% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_66_merger_agreement.txt` (all_stock) 54.8 s = 39% of wall — p95/p50 = 1.13×.
- **Prompt length vs latency:** Pearson r = 0.17 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 5714 tok/doc, mean prompt 71110 tok/doc.
- **Subclass spread:** best `all_cash` 0.630 (n=5), worst `mixed_cash_stock_election` 0.000 (n=1).
- **Field-level extraction:** 13/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 9 | 0.2327 |
| all_cash | 5 | 0.6301 |
| mixed_cash_stock | 3 | 0.3583 |
| all_stock | 2 | 0.5880 |
| mixed_cash_stock_election | 1 | 0.0000 |
| **total** | **20** | **0.3748** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.2633 | 0.0000 | 47.4188 | 81128 | 6932 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.2986 | 0.0000 | 37.7901 | 75955 | 4920 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.6333 | 0.1818 | 40.5727 | 81678 | 5248 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.1751 | 0.0000 | 37.7133 | 73278 | 5356 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.0000 | 0.0000 | 46.5884 | 0 | 0 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.2927 | 0.0000 | 47.0172 | 79531 | 7052 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.6177 | 0.1667 | 46.9872 | 84618 | 6561 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.6945 | 0.2000 | 51.7322 | 67939 | 7907 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.2201 | 0.0000 | 46.7235 | 92583 | 5196 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.1441 | 0.0000 | 48.9395 | 84777 | 7137 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.5584 | 0.0000 | 52.4454 | 86805 | 7641 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5000 | 0.0000 | 46.7546 | 56493 | 7471 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.6111 | 0.1667 | 40.3622 | 72677 | 6015 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.6177 | 0.2000 | 54.7646 | 94167 | 6583 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.1873 | 0.0000 | 41.0830 | 82200 | 5916 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.0000 | 0.0000 | 43.2483 | 0 | 0 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.2755 | 0.0000 | 45.0976 | 97645 | 5561 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.5938 | 0.1667 | 39.1423 | 57092 | 6273 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.2377 | 0.0000 | 46.5380 | 72628 | 6115 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.5750 | 0.1818 | 44.8187 | 81016 | 6397 | — |

- scored rows: 20/20; min=0.0000 max=0.6945 mean=0.3748

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 20 --seed 42 --concurrency 8 --decode-profile qwen3-8b --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260927T022750Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T022750Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T022750Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T022750Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T022750Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3-8b/merger_agreement/RUN-20-MERGER_AGREEMENT-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
