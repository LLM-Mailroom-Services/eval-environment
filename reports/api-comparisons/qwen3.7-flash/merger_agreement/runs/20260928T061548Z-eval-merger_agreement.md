# Run report — `20260928T061548Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T061548Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `merger_agreement_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 50 docs, seed 42 |
| timestamp | `2026-09-28T06:15:48+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T061548Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:22:43+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T061548Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T06:15:48+00:00` |
| finished_at | `2026-09-28T06:22:43+00:00` |
| duration_s (wall) | 416.2000 |
| latency_ms_mean | 57687.1 |
| latency_ms_p95 | 95775.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4909 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4909** (sd 0.2281, min 0.0000, max 0.8823) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 416.2000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.1603** USD |
| cost estimated (roster token rates) | **0.1603** USD |
| cost per document (actual) | 0.0032 USD |
| cost per document (estimated) | 0.0032 USD |
| latency e2e / p50 / p95 / max | 416.2000 / 52.5481 / 95.7759 / 110.8695 s |
| prompt / completion / total tokens | 3864191 / 341008 / 4205199 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2884.4 s vs wall = 416.2 s -> wall/serial factor 6.93x at concurrency 8.

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
| `merger_agreement_specialist` | 53 | 3864191 | 341008 | 4205199 | 0.1603 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2884.4 s over wall 416.2 s = **6.93×** effective parallelism at c8 (87% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_2_merger_agreement.txt` (other) 110.9 s = 27% of wall — p95/p50 = 1.82×.
- **Prompt length vs latency:** Pearson r = 0.40 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 6820 tok/doc, mean prompt 77284 tok/doc.
- **Subclass spread:** best `all_cash` 0.667 (n=16), worst `other` 0.224 (n=18).
- **Field-level extraction:** 19/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 18 | 0.2236 |
| all_cash | 16 | 0.6665 |
| all_stock | 9 | 0.6402 |
| mixed_cash_stock | 6 | 0.5789 |
| mixed_cash_stock_election | 1 | 0.6177 |
| **total** | **50** | **0.4909** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.2633 | 0.0000 | 52.6038 | 81147 | 7937 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.2986 | 0.0000 | 50.4505 | 75974 | 6623 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.6000 | 0.1818 | 54.6643 | 81697 | 7256 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.1751 | 0.0000 | 48.6103 | 73297 | 6341 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.6177 | 0.1818 | 46.7994 | 95573 | 4966 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.2045 | 0.0000 | 45.6206 | 79550 | 6006 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.6177 | 0.1667 | 49.6831 | 84637 | 6032 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.7222 | 0.2000 | 52.5481 | 67958 | 7197 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.1867 | 0.0000 | 44.1883 | 92602 | 5431 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.1718 | 0.0000 | 54.2346 | 84796 | 7516 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.5250 | 0.0000 | 55.7515 | 86824 | 7452 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5555 | 0.0000 | 40.3356 | 56512 | 5414 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.6111 | 0.1428 | 48.4840 | 72696 | 6457 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.5882 | 0.1818 | 60.8653 | 94186 | 8112 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.1578 | 0.0000 | 47.7467 | 82219 | 6556 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.5882 | 0.1333 | 49.8380 | 92882 | 6506 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.1578 | 0.0000 | 44.2175 | 97664 | 5236 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.6250 | 0.1667 | 46.3945 | 57111 | 6268 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.1494 | 0.0000 | 60.0283 | 72647 | 7432 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.5750 | 0.1818 | 48.5625 | 81035 | 5204 | — |
| 21 | `corpus:ground_truth:train:contract_126_merger_agreement.txt` | mixed_cash_stock | 0.5882 | 0.1818 | 54.2481 | 81927 | 5353 | — |
| 22 | `corpus:ground_truth:train:contract_75_merger_agreement.txt` | all_cash | 0.6666 | 0.1818 | 46.1538 | 60164 | 6612 | — |
| 23 | `corpus:ground_truth:train:contract_112_merger_agreement.txt` | all_stock | 0.6562 | 0.1818 | 39.8537 | 52187 | 5501 | — |
| 24 | `corpus:ground_truth:train:contract_141_merger_agreement.txt` | other | 0.3306 | 0.0000 | 90.0583 | 61975 | 6998 | — |
| 25 | `corpus:ground_truth:train:contract_73_merger_agreement.txt` | other | 0.1578 | 0.0000 | 82.7415 | 110306 | 10367 | — |
| 26 | `corpus:ground_truth:train:contract_1_merger_agreement.txt` | all_cash | 0.5834 | 0.2000 | 50.5449 | 73674 | 5997 | — |
| 27 | `corpus:ground_truth:train:contract_144_merger_agreement.txt` | all_cash | 0.7500 | 0.1667 | 91.7274 | 72394 | 7406 | — |
| 28 | `corpus:ground_truth:train:contract_134_merger_agreement.txt` | all_cash | 0.7647 | 0.1667 | 50.5907 | 76610 | 5491 | — |
| 29 | `corpus:ground_truth:train:contract_78_merger_agreement.txt` | all_cash | 0.6471 | 0.1538 | 53.7367 | 58960 | 7364 | — |
| 30 | `corpus:ground_truth:train:contract_17_merger_agreement.txt` | other | 0.0000 | 0.0000 | 64.9796 | 77204 | 8190 | — |
| 31 | `corpus:ground_truth:train:contract_137_merger_agreement.txt` | all_stock | 0.7000 | 0.1428 | 62.4271 | 68917 | 7275 | — |
| 32 | `corpus:ground_truth:train:contract_54_merger_agreement.txt` | all_stock | 0.6875 | 0.1818 | 57.6621 | 85429 | 6614 | — |
| 33 | `corpus:ground_truth:train:contract_3_merger_agreement.txt` | all_cash | 0.7059 | 0.1667 | 54.7337 | 67168 | 6023 | — |
| 34 | `corpus:ground_truth:train:contract_2_merger_agreement.txt` | other | 0.7333 | 0.1538 | 110.8695 | 85174 | 7046 | — |
| 35 | `corpus:ground_truth:train:contract_23_merger_agreement.txt` | all_stock | 0.6666 | 0.1667 | 57.1898 | 85325 | 6454 | — |
| 36 | `corpus:ground_truth:train:contract_57_merger_agreement.txt` | other | 0.2865 | 0.0000 | 60.5136 | 90836 | 7887 | — |
| 37 | `corpus:ground_truth:train:contract_81_merger_agreement.txt` | all_stock | 0.6539 | 0.1538 | 95.7759 | 110046 | 11834 | — |
| 38 | `corpus:ground_truth:train:contract_24_merger_agreement.txt` | all_stock | 0.6666 | 0.1538 | 54.3249 | 105719 | 7211 | — |
| 39 | `corpus:ground_truth:train:contract_101_merger_agreement.txt` | all_cash | 0.6471 | 0.1818 | 45.6251 | 65094 | 5951 | — |
| 40 | `corpus:ground_truth:train:contract_28_merger_agreement.txt` | all_cash | 0.8823 | 0.1818 | 85.2320 | 75212 | 6039 | — |
| 41 | `corpus:ground_truth:train:contract_83_merger_agreement.txt` | all_cash | 0.6177 | 0.1818 | 40.0689 | 59714 | 4981 | — |
| 42 | `corpus:ground_truth:train:contract_85_merger_agreement.txt` | all_stock | 0.6177 | 0.1538 | 50.8523 | 61457 | 6621 | — |
| 43 | `corpus:ground_truth:train:contract_119_merger_agreement.txt` | other | 0.3221 | 0.0000 | 48.4317 | 45341 | 7271 | — |
| 44 | `corpus:ground_truth:train:contract_35_merger_agreement.txt` | mixed_cash_stock | 0.6000 | 0.1667 | 51.7235 | 74531 | 6531 | — |
| 45 | `corpus:ground_truth:train:contract_77_merger_agreement.txt` | other | 0.1578 | 0.0000 | 58.7419 | 68183 | 7082 | — |
| 46 | `corpus:ground_truth:train:contract_27_merger_agreement.txt` | mixed_cash_stock | 0.5666 | 0.1667 | 110.7099 | 106953 | 10831 | — |
| 47 | `corpus:ground_truth:train:contract_43_merger_agreement.txt` | all_cash | 0.5294 | 0.1538 | 51.7070 | 53390 | 6396 | — |
| 48 | `corpus:ground_truth:train:contract_47_merger_agreement.txt` | all_cash | 0.6945 | 0.1667 | 49.1256 | 60485 | 6282 | — |
| 49 | `corpus:ground_truth:train:contract_20_merger_agreement.txt` | other | 0.0000 | 0.0000 | 67.5155 | 88525 | 8190 | — |
| 50 | `corpus:ground_truth:train:contract_7_merger_agreement.txt` | other | 0.2725 | 0.0000 | 44.8637 | 70284 | 5268 | — |

- scored rows: 50/50; min=0.0000 max=0.8823 mean=0.4909

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 50 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T061548Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T061548Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T061548Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T061548Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T061548Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/merger_agreement/RUN-50-MERGER_AGREEMENT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
