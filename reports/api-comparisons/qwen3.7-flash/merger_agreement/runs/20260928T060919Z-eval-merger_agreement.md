# Run report — `20260928T060919Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T060919Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 50 docs, seed 42 |
| timestamp | `2026-09-28T06:09:19+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T060919Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:15:39+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T060919Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T06:09:19+00:00` |
| finished_at | `2026-09-28T06:15:39+00:00` |
| duration_s (wall) | 381.6000 |
| latency_ms_mean | 53755.6 |
| latency_ms_p95 | 86529.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5085 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5085** (sd 0.2071, min 0.1303, max 0.8438) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 381.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.1583** USD |
| cost estimated (roster token rates) | **0.1583** USD |
| cost per document (actual) | 0.0032 USD |
| cost per document (estimated) | 0.0032 USD |
| latency e2e / p50 / p95 / max | 381.6000 / 52.3178 / 86.5297 / 105.3862 s |
| prompt / completion / total tokens | 3863166 / 326444 / 4189610 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2687.8 s vs wall = 381.6 s -> wall/serial factor 7.04x at concurrency 8.

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
| `merger_agreement_specialist` | 53 | 3863166 | 326444 | 4189610 | 0.1583 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2687.8 s over wall 381.6 s = **7.04×** effective parallelism at c8 (88% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_27_merger_agreement.txt` (mixed_cash_stock) 105.4 s = 28% of wall — p95/p50 = 1.65×.
- **Prompt length vs latency:** Pearson r = 0.49 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 6529 tok/doc, mean prompt 77263 tok/doc.
- **Subclass spread:** best `all_stock` 0.677 (n=9), worst `other` 0.244 (n=18).
- **Field-level extraction:** 20/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 18 | 0.2442 |
| all_cash | 16 | 0.6666 |
| all_stock | 9 | 0.6769 |
| mixed_cash_stock | 6 | 0.5989 |
| mixed_cash_stock_election | 1 | 0.6764 |
| **total** | **50** | **0.5085** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.2633 | 0.0000 | 49.9971 | 81128 | 6675 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.3700 | 0.0000 | 52.5169 | 75955 | 7131 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.6333 | 0.1818 | 53.7101 | 81678 | 6200 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.2045 | 0.0000 | 50.8729 | 73278 | 6520 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.6764 | 0.1818 | 55.2959 | 95554 | 6413 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.2927 | 0.0000 | 41.2041 | 79531 | 5104 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.6764 | 0.1667 | 52.1877 | 84618 | 6979 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.6389 | 0.1818 | 60.7664 | 67939 | 8091 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.3201 | 0.0000 | 55.5885 | 92583 | 7297 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.1441 | 0.0000 | 50.9064 | 84777 | 6562 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.7250 | 0.0000 | 58.9846 | 86805 | 7559 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5000 | 0.0000 | 47.1620 | 56493 | 6329 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.6389 | 0.1818 | 57.1514 | 72677 | 6295 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.6177 | 0.2000 | 52.6580 | 94167 | 5880 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.1578 | 0.0000 | 46.8674 | 82200 | 5896 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.6471 | 0.1538 | 56.8986 | 92863 | 7353 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.1873 | 0.0000 | 53.7445 | 97645 | 7216 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.5938 | 0.1667 | 34.2798 | 57092 | 4854 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.2965 | 0.0000 | 47.3143 | 72628 | 6570 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.6000 | 0.1818 | 52.6247 | 81016 | 6133 | — |
| 21 | `corpus:ground_truth:train:contract_126_merger_agreement.txt` | mixed_cash_stock | 0.5882 | 0.1818 | 55.0191 | 81908 | 5900 | — |
| 22 | `corpus:ground_truth:train:contract_75_merger_agreement.txt` | all_cash | 0.6945 | 0.1818 | 57.2458 | 60145 | 7505 | — |
| 23 | `corpus:ground_truth:train:contract_112_merger_agreement.txt` | all_stock | 0.7188 | 0.1818 | 43.5453 | 52168 | 5964 | — |
| 24 | `corpus:ground_truth:train:contract_141_merger_agreement.txt` | other | 0.2234 | 0.0000 | 46.0105 | 61950 | 6241 | — |
| 25 | `corpus:ground_truth:train:contract_73_merger_agreement.txt` | other | 0.2167 | 0.0000 | 72.7986 | 110268 | 9841 | — |
| 26 | `corpus:ground_truth:train:contract_1_merger_agreement.txt` | all_cash | 0.7222 | 0.1818 | 57.3889 | 73655 | 7210 | — |
| 27 | `corpus:ground_truth:train:contract_144_merger_agreement.txt` | all_cash | 0.8438 | 0.1428 | 101.0556 | 72375 | 8149 | — |
| 28 | `corpus:ground_truth:train:contract_134_merger_agreement.txt` | all_cash | 0.6764 | 0.2000 | 52.3178 | 76591 | 6126 | — |
| 29 | `corpus:ground_truth:train:contract_78_merger_agreement.txt` | all_cash | 0.6177 | 0.1818 | 52.5783 | 58941 | 7539 | — |
| 30 | `corpus:ground_truth:train:contract_17_merger_agreement.txt` | other | 0.2377 | 0.0000 | 50.9753 | 77185 | 6228 | — |
| 31 | `corpus:ground_truth:train:contract_137_merger_agreement.txt` | all_stock | 0.6333 | 0.1538 | 49.3161 | 68898 | 5782 | — |
| 32 | `corpus:ground_truth:train:contract_54_merger_agreement.txt` | all_stock | 0.6250 | 0.1538 | 40.4478 | 85410 | 4701 | — |
| 33 | `corpus:ground_truth:train:contract_3_merger_agreement.txt` | all_cash | 0.6177 | 0.1667 | 46.8025 | 67149 | 6502 | — |
| 34 | `corpus:ground_truth:train:contract_2_merger_agreement.txt` | other | 0.2829 | 0.0000 | 52.1761 | 85149 | 5601 | — |
| 35 | `corpus:ground_truth:train:contract_23_merger_agreement.txt` | all_stock | 0.6945 | 0.1667 | 47.4860 | 85306 | 5930 | — |
| 36 | `corpus:ground_truth:train:contract_57_merger_agreement.txt` | other | 0.2865 | 0.0000 | 58.3956 | 90817 | 5798 | — |
| 37 | `corpus:ground_truth:train:contract_81_merger_agreement.txt` | all_stock | 0.7308 | 0.1667 | 86.5297 | 110008 | 10710 | — |
| 38 | `corpus:ground_truth:train:contract_24_merger_agreement.txt` | all_stock | 0.7000 | 0.2000 | 45.6036 | 105700 | 4871 | — |
| 39 | `corpus:ground_truth:train:contract_101_merger_agreement.txt` | all_cash | 0.6764 | 0.1818 | 40.1858 | 65075 | 4335 | — |
| 40 | `corpus:ground_truth:train:contract_28_merger_agreement.txt` | all_cash | 0.6177 | 0.1538 | 57.9750 | 75187 | 7385 | — |
| 41 | `corpus:ground_truth:train:contract_83_merger_agreement.txt` | all_cash | 0.7059 | 0.1818 | 62.0332 | 59695 | 7842 | — |
| 42 | `corpus:ground_truth:train:contract_85_merger_agreement.txt` | all_stock | 0.6471 | 0.1667 | 46.2458 | 61438 | 5845 | — |
| 43 | `corpus:ground_truth:train:contract_119_merger_agreement.txt` | other | 0.2633 | 0.0000 | 35.1033 | 45322 | 4577 | — |
| 44 | `corpus:ground_truth:train:contract_35_merger_agreement.txt` | mixed_cash_stock | 0.6250 | 0.1667 | 56.7505 | 74512 | 7100 | — |
| 45 | `corpus:ground_truth:train:contract_77_merger_agreement.txt` | other | 0.2461 | 0.0000 | 51.4547 | 68164 | 6308 | — |
| 46 | `corpus:ground_truth:train:contract_27_merger_agreement.txt` | mixed_cash_stock | 0.6333 | 0.1818 | 105.3862 | 106915 | 9328 | — |
| 47 | `corpus:ground_truth:train:contract_43_merger_agreement.txt` | all_cash | 0.6177 | 0.1667 | 39.3909 | 53371 | 4933 | — |
| 48 | `corpus:ground_truth:train:contract_47_merger_agreement.txt` | all_cash | 0.6945 | 0.2000 | 44.2737 | 60466 | 5193 | — |
| 49 | `corpus:ground_truth:train:contract_20_merger_agreement.txt` | other | 0.1303 | 0.0000 | 56.2443 | 88506 | 6046 | — |
| 50 | `corpus:ground_truth:train:contract_7_merger_agreement.txt` | other | 0.2725 | 0.0000 | 46.3134 | 70265 | 5897 | — |

- scored rows: 50/50; min=0.1303 max=0.8438 mean=0.5085

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 50 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T060919Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T060919Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T060919Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T060919Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T060919Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/merger_agreement/RUN-50-MERGER_AGREEMENT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
