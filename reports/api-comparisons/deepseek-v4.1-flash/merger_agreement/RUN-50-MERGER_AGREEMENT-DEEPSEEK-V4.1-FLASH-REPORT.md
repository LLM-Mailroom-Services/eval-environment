# Run report — `20260928T093403Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T093403Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `merger_agreement_specialist_v2` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 50 docs, seed 42 |
| timestamp | `2026-09-28T09:34:03+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T093403Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T09:42:02+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T093403Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T09:34:03+00:00` |
| finished_at | `2026-09-28T09:42:02+00:00` |
| duration_s (wall) | 479.6000 |
| latency_ms_mean | 59467.6 |
| latency_ms_p95 | 137533.1 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4217 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4217** (sd 0.3708, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 479.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.3713** USD |
| cost estimated (roster token rates) | **0.3713** USD |
| cost per document (actual) | 0.0074 USD |
| cost per document (estimated) | 0.0074 USD |
| latency e2e / p50 / p95 / max | 479.6000 / 51.0450 / 137.5331 / 181.7963 s |
| prompt / completion / total tokens | 5728402 / 589096 / 6317498 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2973.4 s vs wall = 479.6 s -> wall/serial factor 6.20x at concurrency 8.

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
| `merger_agreement_specialist` | 77 | 5728402 | 589096 | 6317498 | 0.3713 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2973.4 s over wall 479.6 s = **6.20×** effective parallelism at c8 (77% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_83_merger_agreement.txt` (all_cash) 181.8 s = 38% of wall — p95/p50 = 2.69×.
- **Prompt length vs latency:** Pearson r = 0.55 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 11782 tok/doc, mean prompt 114568 tok/doc.
- **Subclass spread:** best `all_stock` 0.725 (n=9), worst `other` 0.161 (n=18).
- **Field-level extraction:** 28/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 18 | 0.1609 |
| all_cash | 16 | 0.4826 |
| all_stock | 9 | 0.7253 |
| mixed_cash_stock | 6 | 0.5387 |
| mixed_cash_stock_election | 1 | 0.7059 |
| **total** | **50** | **0.4217** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.3221 | 0.0000 | 42.2548 | 81629 | 7497 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.0000 | 0.0000 | 56.4456 | 155273 | 16384 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.7667 | 0.1667 | 54.4935 | 168815 | 15741 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.3221 | 0.0000 | 53.2897 | 149553 | 15729 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.7059 | 0.1428 | 28.3439 | 97194 | 7371 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.3221 | 0.0000 | 87.3436 | 79937 | 7791 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.7647 | 0.1818 | 54.6254 | 172277 | 15383 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 52.9136 | 138909 | 16384 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.0000 | 0.0000 | 141.3054 | 189381 | 16384 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.3385 | 0.0000 | 17.5511 | 86841 | 5656 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.9250 | 0.1250 | 137.5331 | 175643 | 14145 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5555 | 0.0000 | 49.4036 | 116183 | 14788 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 52.8032 | 146801 | 16384 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.7941 | 0.2223 | 27.6618 | 102438 | 8192 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.0000 | 0.0000 | 96.4892 | 167509 | 16384 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.7059 | 0.1428 | 23.6912 | 94929 | 7275 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.0000 | 0.0000 | 48.8676 | 201845 | 16384 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.7500 | 0.1538 | 21.6642 | 58314 | 6615 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.0000 | 0.0000 | 49.0967 | 148013 | 16384 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.0000 | 0.0000 | 51.0450 | 82572 | 8192 | — |
| 21 | `corpus:ground_truth:train:contract_126_merger_agreement.txt` | mixed_cash_stock | 0.9706 | 0.1250 | 33.0705 | 83064 | 6768 | — |
| 22 | `corpus:ground_truth:train:contract_75_merger_agreement.txt` | all_cash | 0.7500 | 0.1818 | 20.9224 | 62740 | 7144 | — |
| 23 | `corpus:ground_truth:train:contract_112_merger_agreement.txt` | all_stock | 0.6875 | 0.1428 | 101.6848 | 108213 | 14863 | — |
| 24 | `corpus:ground_truth:train:contract_141_merger_agreement.txt` | other | 0.0000 | 0.0000 | 38.5443 | 62959 | 8192 | — |
| 25 | `corpus:ground_truth:train:contract_73_merger_agreement.txt` | other | 0.3638 | 0.0000 | 41.7397 | 110878 | 13393 | — |
| 26 | `corpus:ground_truth:train:contract_1_merger_agreement.txt` | all_cash | 0.7500 | 0.1818 | 23.3504 | 74677 | 7555 | — |
| 27 | `corpus:ground_truth:train:contract_144_merger_agreement.txt` | all_cash | 0.7188 | 0.1428 | 31.1975 | 73580 | 6914 | — |
| 28 | `corpus:ground_truth:train:contract_134_merger_agreement.txt` | all_cash | 0.7647 | 0.1667 | 23.1291 | 75866 | 8095 | — |
| 29 | `corpus:ground_truth:train:contract_78_merger_agreement.txt` | all_cash | 0.7353 | 0.1667 | 54.6167 | 59210 | 7840 | — |
| 30 | `corpus:ground_truth:train:contract_17_merger_agreement.txt` | other | 0.3553 | 0.0000 | 23.4251 | 78436 | 6904 | — |
| 31 | `corpus:ground_truth:train:contract_137_merger_agreement.txt` | all_stock | 0.0000 | 0.0000 | 49.8598 | 138365 | 16384 | — |
| 32 | `corpus:ground_truth:train:contract_54_merger_agreement.txt` | all_stock | 0.7500 | 0.1667 | 26.6761 | 86665 | 8192 | — |
| 33 | `corpus:ground_truth:train:contract_3_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 116.5992 | 141593 | 16384 | — |
| 34 | `corpus:ground_truth:train:contract_2_merger_agreement.txt` | other | 0.0000 | 0.0000 | 104.5142 | 173543 | 16384 | — |
| 35 | `corpus:ground_truth:train:contract_23_merger_agreement.txt` | all_stock | 0.7222 | 0.1538 | 23.8034 | 87439 | 7953 | — |
| 36 | `corpus:ground_truth:train:contract_57_merger_agreement.txt` | other | 0.0000 | 0.0000 | 71.3625 | 184945 | 16384 | — |
| 37 | `corpus:ground_truth:train:contract_81_merger_agreement.txt` | all_stock | 0.8846 | 0.1250 | 64.0995 | 111084 | 15419 | — |
| 38 | `corpus:ground_truth:train:contract_24_merger_agreement.txt` | all_stock | 1.0000 | 0.2105 | 37.2657 | 105917 | 6209 | — |
| 39 | `corpus:ground_truth:train:contract_101_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 19.4153 | 66094 | 8192 | — |
| 40 | `corpus:ground_truth:train:contract_28_merger_agreement.txt` | all_cash | 0.9706 | 0.1333 | 85.8178 | 153609 | 15519 | — |
| 41 | `corpus:ground_truth:train:contract_83_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 181.7963 | 119717 | 16384 | — |
| 42 | `corpus:ground_truth:train:contract_85_merger_agreement.txt` | all_stock | 0.7647 | 0.1818 | 104.2081 | 125175 | 14233 | — |
| 43 | `corpus:ground_truth:train:contract_119_merger_agreement.txt` | other | 0.0000 | 0.0000 | 93.9348 | 91765 | 16384 | — |
| 44 | `corpus:ground_truth:train:contract_35_merger_agreement.txt` | mixed_cash_stock | 0.0000 | 0.0000 | 21.3533 | 75913 | 8192 | — |
| 45 | `corpus:ground_truth:train:contract_77_merger_agreement.txt` | other | 0.3049 | 0.0000 | 108.5624 | 141887 | 13467 | — |
| 46 | `corpus:ground_truth:train:contract_27_merger_agreement.txt` | mixed_cash_stock | 1.0000 | 0.2501 | 69.6675 | 108403 | 10613 | — |
| 47 | `corpus:ground_truth:train:contract_43_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 112.2347 | 109979 | 16384 | — |
| 48 | `corpus:ground_truth:train:contract_47_merger_agreement.txt` | all_cash | 0.7500 | 0.1667 | 18.8742 | 60836 | 6930 | — |
| 49 | `corpus:ground_truth:train:contract_20_merger_agreement.txt` | other | 0.5678 | 0.0000 | 17.4944 | 96029 | 6374 | — |
| 50 | `corpus:ground_truth:train:contract_7_merger_agreement.txt` | other | 0.0000 | 0.0000 | 107.3403 | 145765 | 16384 | — |

- scored rows: 50/50; min=0.0000 max=1.0000 mean=0.4217

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 50 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T093403Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T093403Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T093403Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T093403Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T093403Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/merger_agreement/RUN-50-MERGER_AGREEMENT-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
