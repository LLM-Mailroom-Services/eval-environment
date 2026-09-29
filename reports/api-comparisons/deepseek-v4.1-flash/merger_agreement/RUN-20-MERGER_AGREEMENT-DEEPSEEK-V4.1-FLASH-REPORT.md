# Run report — `20260928T085426Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T085426Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `merger_agreement_specialist_v2` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-28T08:54:26+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T085426Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:58:11+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | — |
| prompt source / lineage | frozen / mutation |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T085426Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:54:26+00:00` |
| finished_at | `2026-09-28T08:58:11+00:00` |
| duration_s (wall) | 225.6000 |
| latency_ms_mean | 55767.6 |
| latency_ms_p95 | 130738.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4284 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4284** (sd 0.3076, min 0.0000, max 0.9500) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 225.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.1448** USD |
| cost estimated (roster token rates) | **0.1448** USD |
| cost per document (actual) | 0.0072 USD |
| cost per document (estimated) | 0.0072 USD |
| latency e2e / p50 / p95 / max | 225.6000 / 45.5905 / 130.7389 / 156.1979 s |
| prompt / completion / total tokens | 2367475 / 213524 / 2580999 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1115.4 s vs wall = 225.6 s -> wall/serial factor 4.94x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `none (pipeline posture)` |
| sampling injected on wire | False |
| per-agent completion budgets | `{}` |
| per-call timeout | pipeline default s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `merger_agreement_specialist` | 29 | 2367475 | 213524 | 2580999 | 0.1448 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1115.4 s over wall 225.6 s = **4.94×** effective parallelism at c8 (62% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_100_merger_agreement.txt` (all_stock) 156.2 s = 69% of wall — p95/p50 = 2.87×.
- **Prompt length vs latency:** Pearson r = 0.76 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 10676 tok/doc, mean prompt 118374 tok/doc.
- **Subclass spread:** best `mixed_cash_stock` 0.746 (n=3), worst `all_cash` 0.288 (n=5).
- **Field-level extraction:** 12/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 9 | 0.3033 |
| all_cash | 5 | 0.2882 |
| mixed_cash_stock | 3 | 0.7464 |
| all_stock | 2 | 0.7115 |
| mixed_cash_stock_election | 1 | 0.7353 |
| **total** | **20** | **0.4284** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.1751 | 0.0000 | 51.3361 | 81629 | 8192 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.6200 | 0.1177 | 78.3901 | 155273 | 14998 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 92.7137 | 168815 | 16384 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.2927 | 0.0000 | 45.5905 | 74773 | 7024 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.7353 | 0.1538 | 82.1040 | 194395 | 12769 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.3516 | 0.0000 | 49.9390 | 79937 | 7987 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 130.7389 | 172277 | 16384 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 45.1557 | 138909 | 16384 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.3867 | 0.0000 | 25.4577 | 94687 | 5303 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.0000 | 0.0000 | 25.6569 | 86841 | 8192 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.6583 | 0.0000 | 156.1979 | 175665 | 15792 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5834 | 0.0000 | 55.3719 | 116183 | 15828 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.7222 | 0.1538 | 28.4481 | 73397 | 7298 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.7647 | 0.1818 | 22.3612 | 102438 | 3833 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.3049 | 0.0000 | 75.2913 | 167509 | 13849 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.7059 | 0.1428 | 16.1202 | 94929 | 3993 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.5990 | 0.1333 | 27.2275 | 100919 | 7899 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.7188 | 0.1538 | 35.5066 | 58314 | 8192 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.0000 | 0.0000 | 42.3219 | 148013 | 16384 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.9500 | 0.1333 | 29.4233 | 82572 | 6839 | — |

- scored rows: 20/20; min=0.0000 max=0.9500 mean=0.4284

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 20 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T085426Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T085426Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T085426Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T085426Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T085426Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/merger_agreement/RUN-20-MERGER_AGREEMENT-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
