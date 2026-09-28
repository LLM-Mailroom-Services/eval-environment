# Run report — `20260928T070803Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T070803Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `merger_agreement_specialist_v3` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 50 docs, seed 42 |
| timestamp | `2026-09-28T07:08:03+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T070803Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T07:16:10+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 50 / None |
| scorer | extraction |
| decode profile | — |
| prompt source / lineage | frozen / mutation |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T070803Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T07:08:03+00:00` |
| finished_at | `2026-09-28T07:16:10+00:00` |
| duration_s (wall) | 488.0000 |
| latency_ms_mean | 55020.0 |
| latency_ms_p95 | 99717.0 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5213 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5213** (sd 0.2287, min 0.0000, max 0.8611) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 488.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.1611** USD |
| cost estimated (roster token rates) | **0.1611** USD |
| cost per document (actual) | 0.0032 USD |
| cost per document (estimated) | 0.0032 USD |
| latency e2e / p50 / p95 / max | 488.0000 / 51.0362 / 99.7170 / 110.7878 s |
| prompt / completion / total tokens | 3864179 / 347846 / 4212025 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2751.0 s vs wall = 488.0 s -> wall/serial factor 5.64x at concurrency 8.

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
| `merger_agreement_specialist` | 53 | 3864179 | 347846 | 4212025 | 0.1611 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2751.0 s over wall 488.0 s = **5.64×** effective parallelism at c8 (70% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_27_merger_agreement.txt` (mixed_cash_stock) 110.8 s = 23% of wall — p95/p50 = 1.95×.
- **Prompt length vs latency:** Pearson r = 0.57 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 6957 tok/doc, mean prompt 77284 tok/doc.
- **Subclass spread:** best `all_stock` 0.716 (n=9), worst `other` 0.277 (n=18).
- **Field-level extraction:** 20/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 18 | 0.2774 |
| all_cash | 16 | 0.6452 |
| all_stock | 9 | 0.7160 |
| mixed_cash_stock | 6 | 0.6098 |
| mixed_cash_stock_election | 1 | 0.6471 |
| **total** | **50** | **0.5213** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.2339 | 0.0000 | 46.1362 | 81147 | 5904 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.3343 | 0.0000 | 53.0563 | 75974 | 6923 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.6000 | 0.1818 | 61.4727 | 81697 | 7554 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.2045 | 0.0000 | 53.4923 | 73297 | 7510 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.6471 | 0.2000 | 54.8322 | 95573 | 6395 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.2633 | 0.0000 | 60.5319 | 79550 | 7439 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.6177 | 0.1538 | 60.6571 | 84637 | 7916 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.6389 | 0.2000 | 42.5159 | 67958 | 6105 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.3201 | 0.0000 | 48.2199 | 92602 | 6009 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.1718 | 0.0000 | 54.5967 | 84796 | 7243 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.6250 | 0.0000 | 53.7095 | 86824 | 6893 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5278 | 0.0000 | 46.3283 | 56512 | 6511 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.6111 | 0.1667 | 43.6154 | 72696 | 5682 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.7353 | 0.2000 | 57.0261 | 94186 | 6169 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.1873 | 0.0000 | 47.5364 | 82219 | 6510 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.6177 | 0.1538 | 44.3635 | 92882 | 5396 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.1578 | 0.0000 | 50.4566 | 97664 | 6205 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.6250 | 0.1667 | 47.0152 | 57111 | 6418 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.3260 | 0.0000 | 47.5610 | 72647 | 6250 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.6000 | 0.2000 | 51.0588 | 81035 | 6860 | — |
| 21 | `corpus:ground_truth:train:contract_126_merger_agreement.txt` | mixed_cash_stock | 0.5882 | 0.1818 | 48.9991 | 81927 | 6146 | — |
| 22 | `corpus:ground_truth:train:contract_75_merger_agreement.txt` | all_cash | 0.6666 | 0.1667 | 42.2784 | 60164 | 5670 | — |
| 23 | `corpus:ground_truth:train:contract_112_merger_agreement.txt` | all_stock | 0.7500 | 0.2000 | 47.4828 | 52187 | 5926 | — |
| 24 | `corpus:ground_truth:train:contract_141_merger_agreement.txt` | other | 0.2591 | 0.0000 | 53.6399 | 61969 | 6689 | — |
| 25 | `corpus:ground_truth:train:contract_73_merger_agreement.txt` | other | 0.2755 | 0.0000 | 93.6811 | 110306 | 12910 | — |
| 26 | `corpus:ground_truth:train:contract_1_merger_agreement.txt` | all_cash | 0.8611 | 0.1667 | 76.5863 | 73680 | 6537 | — |
| 27 | `corpus:ground_truth:train:contract_144_merger_agreement.txt` | all_cash | 0.6875 | 0.1818 | 44.9239 | 72388 | 5712 | — |
| 28 | `corpus:ground_truth:train:contract_134_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 62.6486 | 76610 | 8190 | — |
| 29 | `corpus:ground_truth:train:contract_78_merger_agreement.txt` | all_cash | 0.7353 | 0.1667 | 47.7227 | 58960 | 6422 | — |
| 30 | `corpus:ground_truth:train:contract_17_merger_agreement.txt` | other | 0.2965 | 0.0000 | 57.0769 | 77204 | 6892 | — |
| 31 | `corpus:ground_truth:train:contract_137_merger_agreement.txt` | all_stock | 0.7333 | 0.1818 | 40.1498 | 68917 | 5113 | — |
| 32 | `corpus:ground_truth:train:contract_54_merger_agreement.txt` | all_stock | 0.6562 | 0.1818 | 54.8980 | 85429 | 7782 | — |
| 33 | `corpus:ground_truth:train:contract_3_merger_agreement.txt` | all_cash | 0.6764 | 0.1538 | 52.7232 | 67168 | 7533 | — |
| 34 | `corpus:ground_truth:train:contract_2_merger_agreement.txt` | other | 0.2657 | 0.0000 | 46.3517 | 85168 | 5418 | — |
| 35 | `corpus:ground_truth:train:contract_23_merger_agreement.txt` | all_stock | 0.7778 | 0.1818 | 51.0362 | 85325 | 6831 | — |
| 36 | `corpus:ground_truth:train:contract_57_merger_agreement.txt` | other | 0.7812 | 0.1428 | 99.7170 | 90842 | 12999 | — |
| 37 | `corpus:ground_truth:train:contract_81_merger_agreement.txt` | all_stock | 0.7308 | 0.1667 | 105.9544 | 110046 | 14863 | — |
| 38 | `corpus:ground_truth:train:contract_24_merger_agreement.txt` | all_stock | 0.7000 | 0.2000 | 52.0873 | 105719 | 5454 | — |
| 39 | `corpus:ground_truth:train:contract_101_merger_agreement.txt` | all_cash | 0.7059 | 0.1667 | 43.9848 | 65094 | 5017 | — |
| 40 | `corpus:ground_truth:train:contract_28_merger_agreement.txt` | all_cash | 0.7353 | 0.1667 | 57.0376 | 75206 | 6892 | — |
| 41 | `corpus:ground_truth:train:contract_83_merger_agreement.txt` | all_cash | 0.7941 | 0.1667 | 50.5561 | 59714 | 6131 | — |
| 42 | `corpus:ground_truth:train:contract_85_merger_agreement.txt` | all_stock | 0.7353 | 0.1667 | 48.0492 | 61457 | 6350 | — |
| 43 | `corpus:ground_truth:train:contract_119_merger_agreement.txt` | other | 0.2633 | 0.0000 | 44.8912 | 45341 | 6051 | — |
| 44 | `corpus:ground_truth:train:contract_35_merger_agreement.txt` | mixed_cash_stock | 0.6250 | 0.1818 | 54.8610 | 74531 | 5128 | — |
| 45 | `corpus:ground_truth:train:contract_77_merger_agreement.txt` | other | 0.1873 | 0.0000 | 48.0625 | 68183 | 6406 | — |
| 46 | `corpus:ground_truth:train:contract_27_merger_agreement.txt` | mixed_cash_stock | 0.7000 | 0.1818 | 110.7878 | 106953 | 11391 | — |
| 47 | `corpus:ground_truth:train:contract_43_merger_agreement.txt` | all_cash | 0.6177 | 0.1667 | 54.3126 | 53390 | 7299 | — |
| 48 | `corpus:ground_truth:train:contract_47_merger_agreement.txt` | all_cash | 0.7500 | 0.2000 | 48.7533 | 60485 | 6550 | — |
| 49 | `corpus:ground_truth:train:contract_20_merger_agreement.txt` | other | 0.1303 | 0.0000 | 50.6647 | 88525 | 6421 | — |
| 50 | `corpus:ground_truth:train:contract_7_merger_agreement.txt` | other | 0.3350 | 0.0000 | 36.8982 | 70284 | 5231 | — |

- scored rows: 50/50; min=0.0000 max=0.8611 mean=0.5213

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 50 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T070803Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T070803Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T070803Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T070803Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T070803Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/merger_agreement/RUN-50-MERGER_AGREEMENT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
