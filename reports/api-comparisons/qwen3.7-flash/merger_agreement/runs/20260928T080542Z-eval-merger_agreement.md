# Run report — `20260928T080542Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T080542Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-28T08:05:43+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T080542Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:08:19+00:00` |

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
| prompt source / lineage | frozen / frozen |
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:05:43+00:00` |
| finished_at | `2026-09-28T08:08:19+00:00` |
| duration_s (wall) | 158.2000 |
| latency_ms_mean | 50590.9 |
| latency_ms_p95 | 97363.0 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4065 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4065** (sd 0.2134, min 0.0000, max 0.7353) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 158.2000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0646** USD |
| cost estimated (roster token rates) | **0.0646** USD |
| cost per document (actual) | 0.0032 USD |
| cost per document (estimated) | 0.0032 USD |
| latency e2e / p50 / p95 / max | 158.2000 / 45.6275 / 97.3630 / 98.2677 s |
| prompt / completion / total tokens | 1610639 / 125255 / 1735894 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1011.8 s vs wall = 158.2 s -> wall/serial factor 6.40x at concurrency 8.

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
| `merger_agreement_specialist` | 20 | 1610639 | 125255 | 1735894 | 0.0646 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1011.8 s over wall 158.2 s = **6.40×** effective parallelism at c8 (80% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_100_merger_agreement.txt` (all_stock) 98.3 s = 62% of wall — p95/p50 = 2.13×.
- **Prompt length vs latency:** Pearson r = 0.07 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 6263 tok/doc, mean prompt 80532 tok/doc.
- **Subclass spread:** best `mixed_cash_stock_election` 0.735 (n=1), worst `other` 0.234 (n=9).
- **Field-level extraction:** 11/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 9 | 0.2344 |
| all_cash | 5 | 0.6123 |
| mixed_cash_stock | 3 | 0.5451 |
| all_stock | 2 | 0.2941 |
| mixed_cash_stock_election | 1 | 0.7353 |
| **total** | **20** | **0.4065** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.3222 | 0.0000 | 97.3630 | 81134 | 7584 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.4057 | 0.0000 | 58.9939 | 75955 | 8190 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.6000 | 0.1818 | 38.4623 | 81678 | 4358 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.2046 | 0.0000 | 47.2783 | 73278 | 6268 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.7353 | 0.1818 | 46.1886 | 95554 | 5863 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.2928 | 0.0000 | 43.4334 | 79531 | 5884 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.6177 | 0.1818 | 43.8201 | 84618 | 5700 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.6389 | 0.1818 | 43.9435 | 67939 | 6267 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.1867 | 0.0000 | 50.8252 | 92583 | 6636 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.1441 | 0.0000 | 34.9028 | 84777 | 4436 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.0000 | 0.0000 | 98.2677 | 86811 | 8192 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.4722 | 0.0000 | 43.8273 | 56493 | 6562 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.6111 | 0.1667 | 51.5424 | 72677 | 7150 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.5882 | 0.1818 | 46.7990 | 94167 | 6112 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.1873 | 0.0000 | 36.7025 | 82200 | 5225 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.5882 | 0.1667 | 39.2031 | 92863 | 4966 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.1873 | 0.0000 | 45.2828 | 97645 | 5693 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.5938 | 0.1667 | 45.6275 | 57092 | 7136 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.1789 | 0.0000 | 42.1115 | 72628 | 5423 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.5750 | 0.1818 | 57.2424 | 81016 | 7610 | — |

- scored rows: 20/20; min=0.0000 max=0.7353 mean=0.4065

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 20 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T080542Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T080542Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T080542Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T080542Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T080542Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/merger_agreement/RUN-20-MERGER_AGREEMENT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
