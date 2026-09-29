# Run report — `20260928T090247Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T090247Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 50 docs, seed 42 |
| timestamp | `2026-09-28T09:02:47+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T090247Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T09:07:57+00:00` |

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
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T090247Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T09:02:47+00:00` |
| finished_at | `2026-09-28T09:07:57+00:00` |
| duration_s (wall) | 312.6000 |
| latency_ms_mean | 35142.6 |
| latency_ms_p95 | 68731.2 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.6294 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.6294** (sd 0.2733, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 312.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.2462** USD |
| cost estimated (roster token rates) | **0.2462** USD |
| cost per document (actual) | 0.0049 USD |
| cost per document (estimated) | 0.0049 USD |
| latency e2e / p50 / p95 / max | 312.6000 / 29.4190 / 68.7312 / 127.6027 s |
| prompt / completion / total tokens | 4090925 / 355317 / 4446242 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1757.1 s vs wall = 312.6 s -> wall/serial factor 5.62x at concurrency 8.

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
| `merger_agreement_specialist` | 55 | 4090925 | 355317 | 4446242 | 0.2462 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1757.1 s over wall 312.6 s = **5.62×** effective parallelism at c8 (70% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_120_merger_agreement.txt` (other) 127.6 s = 41% of wall — p95/p50 = 2.34×.
- **Prompt length vs latency:** Pearson r = 0.41 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 7106 tok/doc, mean prompt 81818 tok/doc.
- **Subclass spread:** best `mixed_cash_stock_election` 0.794 (n=1), worst `other` 0.448 (n=18).
- **Field-level extraction:** 17/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 18 | 0.4476 |
| all_cash | 16 | 0.6828 |
| all_stock | 9 | 0.7803 |
| mixed_cash_stock | 6 | 0.7788 |
| mixed_cash_stock_election | 1 | 0.7941 |
| **total** | **50** | **0.6294** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.3516 | 0.0000 | 26.0602 | 81609 | 5924 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.4415 | 0.0000 | 24.3115 | 77613 | 4828 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.7333 | 0.1428 | 25.2811 | 84384 | 5314 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.3222 | 0.0000 | 34.6841 | 74753 | 7787 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.7941 | 0.2000 | 31.8887 | 97174 | 6920 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.0000 | 0.0000 | 127.6027 | 159863 | 16384 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.7353 | 0.1667 | 62.5081 | 86115 | 7408 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 35.7751 | 69431 | 8192 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.4200 | 0.0000 | 27.0423 | 94667 | 6210 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.3108 | 0.0000 | 22.6640 | 86821 | 6277 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.9250 | 0.1333 | 17.4690 | 87820 | 4067 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5834 | 0.0000 | 29.4149 | 58068 | 8192 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 1.0000 | 0.2666 | 17.9753 | 73377 | 5155 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.7647 | 0.1667 | 27.8161 | 102418 | 7474 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.5991 | 0.1250 | 30.8646 | 83731 | 6365 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.7059 | 0.1428 | 21.7361 | 94909 | 5802 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.3344 | 0.0000 | 25.6627 | 100899 | 6969 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.7500 | 0.1667 | 13.3461 | 58294 | 3588 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.5907 | 0.0000 | 23.7744 | 73983 | 6081 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.7000 | 0.1538 | 68.7312 | 82552 | 7101 | — |
| 21 | `corpus:ground_truth:train:contract_126_merger_agreement.txt` | mixed_cash_stock | 1.0000 | 0.2501 | 31.3398 | 83044 | 6200 | — |
| 22 | `corpus:ground_truth:train:contract_75_merger_agreement.txt` | all_cash | 0.7222 | 0.1667 | 38.4632 | 62720 | 6507 | — |
| 23 | `corpus:ground_truth:train:contract_112_merger_agreement.txt` | all_stock | 0.7500 | 0.1667 | 28.3007 | 54083 | 7387 | — |
| 24 | `corpus:ground_truth:train:contract_141_merger_agreement.txt` | other | 0.3306 | 0.0000 | 21.6186 | 62939 | 5605 | — |
| 25 | `corpus:ground_truth:train:contract_73_merger_agreement.txt` | other | 0.5991 | 0.1333 | 53.3097 | 110838 | 12035 | — |
| 26 | `corpus:ground_truth:train:contract_1_merger_agreement.txt` | all_cash | 0.7778 | 0.1818 | 17.0151 | 74657 | 5145 | — |
| 27 | `corpus:ground_truth:train:contract_144_merger_agreement.txt` | all_cash | 0.7500 | 0.1667 | 29.1926 | 73560 | 6425 | — |
| 28 | `corpus:ground_truth:train:contract_134_merger_agreement.txt` | all_cash | 0.7647 | 0.1667 | 23.0365 | 75846 | 6319 | — |
| 29 | `corpus:ground_truth:train:contract_78_merger_agreement.txt` | all_cash | 0.7353 | 0.1538 | 30.2385 | 59190 | 6429 | — |
| 30 | `corpus:ground_truth:train:contract_17_merger_agreement.txt` | other | 0.6200 | 0.1333 | 24.7963 | 78416 | 6498 | — |
| 31 | `corpus:ground_truth:train:contract_137_merger_agreement.txt` | all_stock | 0.9667 | 0.1111 | 29.4190 | 69159 | 7669 | — |
| 32 | `corpus:ground_truth:train:contract_54_merger_agreement.txt` | all_stock | 1.0000 | 0.2501 | 28.9639 | 86645 | 7192 | — |
| 33 | `corpus:ground_truth:train:contract_3_merger_agreement.txt` | all_cash | 0.7353 | 0.1538 | 43.8280 | 70773 | 7906 | — |
| 34 | `corpus:ground_truth:train:contract_2_merger_agreement.txt` | other | 0.8000 | 0.1818 | 34.8619 | 86748 | 7022 | — |
| 35 | `corpus:ground_truth:train:contract_23_merger_agreement.txt` | all_stock | 0.7222 | 0.1667 | 21.8966 | 87419 | 6325 | — |
| 36 | `corpus:ground_truth:train:contract_57_merger_agreement.txt` | other | 0.7500 | 0.1538 | 28.0353 | 92449 | 8192 | — |
| 37 | `corpus:ground_truth:train:contract_81_merger_agreement.txt` | all_stock | 0.9231 | 0.1111 | 52.8120 | 111044 | 11114 | — |
| 38 | `corpus:ground_truth:train:contract_24_merger_agreement.txt` | all_stock | 0.0000 | 0.0000 | 29.4321 | 105897 | 8192 | — |
| 39 | `corpus:ground_truth:train:contract_101_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 57.3690 | 132155 | 16384 | — |
| 40 | `corpus:ground_truth:train:contract_28_merger_agreement.txt` | all_cash | 0.7353 | 0.1667 | 38.1063 | 76781 | 7036 | — |
| 41 | `corpus:ground_truth:train:contract_83_merger_agreement.txt` | all_cash | 1.0000 | 0.2352 | 78.3026 | 59846 | 8007 | — |
| 42 | `corpus:ground_truth:train:contract_85_merger_agreement.txt` | all_stock | 0.9706 | 0.1177 | 32.4425 | 62564 | 6976 | — |
| 43 | `corpus:ground_truth:train:contract_119_merger_agreement.txt` | other | 0.3516 | 0.0000 | 42.0305 | 45859 | 6158 | — |
| 44 | `corpus:ground_truth:train:contract_35_merger_agreement.txt` | mixed_cash_stock | 0.9500 | 0.1333 | 24.7622 | 75893 | 7226 | — |
| 45 | `corpus:ground_truth:train:contract_77_merger_agreement.txt` | other | 0.3638 | 0.0000 | 47.6204 | 70909 | 4614 | — |
| 46 | `corpus:ground_truth:train:contract_27_merger_agreement.txt` | mixed_cash_stock | 0.7333 | 0.1428 | 18.8827 | 108360 | 3937 | — |
| 47 | `corpus:ground_truth:train:contract_43_merger_agreement.txt` | all_cash | 0.7353 | 0.1538 | 38.1491 | 54966 | 6524 | — |
| 48 | `corpus:ground_truth:train:contract_47_merger_agreement.txt` | all_cash | 0.7500 | 0.1818 | 35.3791 | 60816 | 7515 | — |
| 49 | `corpus:ground_truth:train:contract_20_merger_agreement.txt` | other | 0.2866 | 0.0000 | 28.4461 | 96009 | 6571 | — |
| 50 | `corpus:ground_truth:train:contract_7_merger_agreement.txt` | other | 0.5850 | 0.0000 | 54.4702 | 72859 | 6169 | — |

- scored rows: 50/50; min=0.0000 max=1.0000 mean=0.6294

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 50 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T090247Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T090247Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T090247Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T090247Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T090247Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/merger_agreement/RUN-50-MERGER_AGREEMENT-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
