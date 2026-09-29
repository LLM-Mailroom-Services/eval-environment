# Run report — `20260928T074850Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T074850Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 20 docs, seed 42 |
| timestamp | `2026-09-28T07:48:50+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T074850Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T07:51:08+00:00` |

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
| started_at | `2026-09-28T07:48:50+00:00` |
| finished_at | `2026-09-28T07:51:08+00:00` |
| duration_s (wall) | 140.2000 |
| latency_ms_mean | 36904.2 |
| latency_ms_p95 | 46624.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4093 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4093** (sd 0.1516, min 0.2028, max 0.6476) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 140.2000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0141** USD |
| cost estimated (roster token rates) | **0.0141** USD |
| cost per document (actual) | 0.0007 USD |
| cost per document (estimated) | 0.0007 USD |
| latency e2e / p50 / p95 / max | 140.2000 / 33.9051 / 46.6247 / 95.1377 s |
| prompt / completion / total tokens | 193492 / 64000 / 257492 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 738.1 s vs wall = 140.2 s -> wall/serial factor 5.26x at concurrency 8.

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
| `corporate_records_specialist` | 22 | 193492 | 64000 | 257492 | 0.0141 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 738.1 s over wall 140.2 s = **5.26×** effective parallelism at c8 (66% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` (indenture) 95.1 s = 68% of wall — p95/p50 = 1.38×.
- **Prompt length vs latency:** Pearson r = 0.85 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 3200 tok/doc, mean prompt 9675 tok/doc.
- **Subclass spread:** best `bylaws` 0.625 (n=1), worst `board_resolution` 0.248 (n=2).
- **Field-level extraction:** 12/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 4 | 0.3052 |
| indenture | 3 | 0.2911 |
| officer_certificate | 3 | 0.3133 |
| articles_of_incorporation | 2 | 0.6249 |
| board_resolution | 2 | 0.2480 |
| rights_instrument | 2 | 0.6077 |
| subsidiary_list | 2 | 0.4722 |
| bylaws | 1 | 0.6250 |
| powers_of_attorney | 1 | 0.6208 |
| **total** | **20** | **0.4093** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2028 | 0.0000 | 35.2982 | 20051 | 2782 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6250 | 0.2500 | 28.9634 | 21112 | 2345 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4308 | 0.1538 | 33.9051 | 1963 | 2898 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3054 | 0.0000 | 30.2358 | 1885 | 2655 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6476 | 0.2500 | 39.6259 | 2708 | 3445 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.5678 | 0.2352 | 34.0735 | 14629 | 2859 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.6357 | 0.2500 | 32.2014 | 8002 | 2780 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.5136 | 0.1667 | 37.0354 | 1589 | 3096 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2937 | 0.0000 | 32.9697 | 10247 | 2555 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.6208 | 0.2500 | 46.6247 | 3672 | 4604 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.6140 | 0.2857 | 29.9563 | 3601 | 2696 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3214 | 0.0000 | 27.8438 | 2237 | 2297 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.2731 | 0.0000 | 39.2558 | 1790 | 3524 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.2230 | 0.0000 | 40.5234 | 1776 | 3712 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 95.1377 | 75033 | 8144 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2937 | 0.0000 | 29.8585 | 5854 | 2755 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.3022 | 0.0000 | 37.5958 | 6914 | 3456 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 30.9837 | 2258 | 2882 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 33.8481 | 3420 | 2744 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3526 | 0.0000 | 22.1468 | 4751 | 1771 | — |

- scored rows: 20/20; min=0.2028 max=0.6476 mean=0.4093

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 20 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T074850Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T074850Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T074850Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T074850Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T074850Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/corporate_records/RUN-20-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
