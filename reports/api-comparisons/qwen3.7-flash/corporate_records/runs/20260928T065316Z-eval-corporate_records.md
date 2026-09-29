# Run report — `20260928T065316Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T065316Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `corporate_records_specialist_v3` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 50 docs, seed 42 |
| timestamp | `2026-09-28T06:53:16+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T065316Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:58:13+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T065316Z-eval-corporate_records', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T06:53:16+00:00` |
| finished_at | `2026-09-28T06:58:13+00:00` |
| duration_s (wall) | 298.3000 |
| latency_ms_mean | 40389.6 |
| latency_ms_p95 | 101156.3 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4156 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4156** (sd 0.1478, min 0.2028, max 0.7208) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 298.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0384** USD |
| cost estimated (roster token rates) | **0.0384** USD |
| cost per document (actual) | 0.0008 USD |
| cost per document (estimated) | 0.0008 USD |
| latency e2e / p50 / p95 / max | 298.3000 / 34.7602 / 101.1563 / 135.5589 s |
| prompt / completion / total tokens | 569944 / 163898 / 733842 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2019.5 s vs wall = 298.3 s -> wall/serial factor 6.77x at concurrency 8.

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
| `corporate_records_specialist` | 59 | 569944 | 163898 | 733842 | 0.0384 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2019.5 s over wall 298.3 s = **6.77×** effective parallelism at c8 (85% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` (indenture) 135.6 s = 45% of wall — p95/p50 = 2.91×.
- **Prompt length vs latency:** Pearson r = 0.90 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3278 tok/doc, mean prompt 11399 tok/doc.
- **Subclass spread:** best `bylaws` 0.636 (n=4), worst `charter_amendment` 0.289 (n=13).
- **Field-level extraction:** 30/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 13 | 0.2894 |
| indenture | 7 | 0.3118 |
| officer_certificate | 6 | 0.2919 |
| subsidiary_list | 6 | 0.5070 |
| articles_of_incorporation | 5 | 0.5840 |
| bylaws | 4 | 0.6363 |
| rights_instrument | 4 | 0.6144 |
| board_resolution | 3 | 0.3948 |
| other | 1 | 0.3156 |
| powers_of_attorney | 1 | 0.6208 |
| **total** | **50** | **0.4156** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2028 | 0.0000 | 34.4690 | 20071 | 2919 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6250 | 0.2500 | 29.0061 | 21132 | 2643 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4666 | 0.1538 | 39.0024 | 1983 | 2906 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3262 | 0.0000 | 42.8728 | 1905 | 3144 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6714 | 0.2500 | 35.2593 | 2728 | 2686 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.5678 | 0.2352 | 35.7593 | 14649 | 3030 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.5857 | 0.2352 | 37.1124 | 8022 | 2778 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.5136 | 0.1667 | 35.2599 | 1609 | 2816 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2437 | 0.0000 | 28.3140 | 10273 | 2350 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.6208 | 0.2500 | 53.5802 | 3698 | 4590 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.7208 | 0.4444 | 28.2892 | 3627 | 2552 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3214 | 0.0000 | 43.9016 | 2263 | 3948 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.2731 | 0.0000 | 28.8223 | 1810 | 1966 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.4098 | 0.1250 | 34.7602 | 1802 | 2645 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 105.7204 | 75111 | 8498 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2937 | 0.0000 | 29.7698 | 5880 | 2756 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 56.4841 | 6940 | 4614 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 24.5019 | 2284 | 1942 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 37.2001 | 3446 | 3256 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3526 | 0.0000 | 26.8922 | 4777 | 2340 | — |
| 21 | `corpus:ground_truth:train:0001214659-18-006586_ex3_3.htm` | board_resolution | 0.5014 | 0.1250 | 34.2377 | 1853 | 3107 | — |
| 22 | `corpus:ground_truth:train:0000950168-02-001563_dex211.txt` | subsidiary_list | 0.5276 | 0.2857 | 26.1884 | 1561 | 1903 | — |
| 23 | `corpus:ground_truth:train:0001493152-22-014997_ex3-2.htm` | charter_amendment | 0.2345 | 0.0000 | 27.0298 | 2347 | 2493 | — |
| 24 | `corpus:ground_truth:train:0000721748-14-000223_ex3_2bylaws.htm` | bylaws | 0.6312 | 0.2500 | 19.2691 | 13290 | 1471 | — |
| 25 | `corpus:ground_truth:train:0001193125-10-049079_dex341.htm` | charter_amendment | 0.2591 | 0.0000 | 40.1362 | 3965 | 3187 | — |
| 26 | `corpus:ground_truth:train:0001213900-20-012863_ea122016ex3-1iv_lantern.htm` | charter_amendment | 0.3173 | 0.0000 | 32.9258 | 2224 | 2709 | — |
| 27 | `corpus:ground_truth:train:0001079974-10-000369_bulkstors1ex32_72110.htm` | articles_of_incorporation | 0.5367 | 0.0000 | 26.4705 | 8538 | 2014 | — |
| 28 | `corpus:ground_truth:train:0001683168-24-006658_cloudastructure_ex0302.htm` | bylaws | 0.6208 | 0.2666 | 20.3369 | 13739 | 1589 | — |
| 29 | `corpus:ground_truth:train:0001571049-17-008060_t1702546_ex4-3.htm` | rights_instrument | 0.6208 | 0.2666 | 41.7499 | 2937 | 3083 | — |
| 30 | `corpus:ground_truth:train:0001547903-13-000020_a41specimenclassacommonsto.htm` | articles_of_incorporation | 0.4882 | 0.0000 | 32.9325 | 2235 | 2900 | — |
| 31 | `corpus:ground_truth:train:0001193125-07-225925_dex211.htm` | subsidiary_list | 0.5427 | 0.1819 | 42.6901 | 1634 | 4038 | — |
| 32 | `corpus:ground_truth:train:0000950123-09-074380_g20855a1exv3w10.htm` | officer_certificate | 0.2437 | 0.0000 | 27.6964 | 2788 | 2060 | — |
| 33 | `corpus:ground_truth:train:0001104659-20-105312_tm2024520d5_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 30.0452 | 4361 | 2792 | — |
| 34 | `corpus:ground_truth:train:0001193125-09-061115_dex32.htm` | bylaws | 0.6682 | 0.2857 | 28.0520 | 19078 | 2057 | — |
| 35 | `corpus:ground_truth:train:0001193125-09-252452_dex34.htm` | charter_amendment | 0.3530 | 0.0000 | 31.7762 | 2217 | 2646 | — |
| 36 | `corpus:ground_truth:train:0001047469-09-009128_a2194825zex-3_4.htm` | charter_amendment | 0.2864 | 0.0000 | 38.9617 | 2124 | 2956 | — |
| 37 | `corpus:ground_truth:train:0001398432-09-000149_exh4_10.htm` | rights_instrument | 0.5976 | 0.2352 | 29.9342 | 2168 | 2520 | — |
| 38 | `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` | indenture | 0.3456 | 0.0000 | 135.5589 | 94810 | 10270 | — |
| 39 | `corpus:ground_truth:train:0001193125-04-072642_dex211.htm` | subsidiary_list | 0.4776 | 0.1667 | 32.1025 | 1580 | 2391 | — |
| 40 | `corpus:ground_truth:train:0001553350-15-001174_aqua_ex3z1c.htm` | officer_certificate | 0.2661 | 0.0000 | 42.9578 | 5450 | 4067 | — |
| 41 | `corpus:ground_truth:train:0000950137-02-005662_c71678a2exv4w1.txt` | indenture | 0.3914 | 0.0000 | 101.1563 | 72726 | 7995 | — |
| 42 | `corpus:ground_truth:train:0001615774-14-000417_s100510_ex3-1.htm` | other | 0.3156 | 0.0000 | 46.2918 | 21071 | 3421 | — |
| 43 | `corpus:ground_truth:train:0000950144-06-006066_g01711a1exv4w7.txt` | indenture | 0.3212 | 0.0000 | 95.6561 | 64787 | 7640 | — |
| 44 | `corpus:ground_truth:train:0001193125-15-005780_d789569dex49.htm` | indenture | 0.2512 | 0.0000 | 43.3363 | 3081 | 3331 | — |
| 45 | `corpus:ground_truth:train:0001829126-25-005032_picardmedical_ex3-3.htm` | charter_amendment | 0.2845 | 0.0000 | 37.6556 | 2147 | 2980 | — |
| 46 | `corpus:ground_truth:train:0001193125-10-012980_dex211.htm` | subsidiary_list | 0.5136 | 0.1819 | 33.5595 | 1597 | 3056 | — |
| 47 | `corpus:ground_truth:train:0001193125-14-025241_d593074dex313.htm` | charter_amendment | 0.2829 | 0.0000 | 25.9872 | 2663 | 2304 | — |
| 48 | `corpus:ground_truth:train:0001099574-13-000003_exh32amendmentstocertificate.htm` | charter_amendment | 0.2387 | 0.0000 | 41.9333 | 4309 | 3175 | — |
| 49 | `corpus:ground_truth:train:0001193125-08-114390_dex3150.htm` | articles_of_incorporation | 0.5885 | 0.2352 | 29.5397 | 2345 | 2541 | — |
| 50 | `corpus:ground_truth:train:0001213900-19-025668_fs12019a1ex3-7_sgblocksinc.htm` | officer_certificate | 0.3514 | 0.0000 | 36.3367 | 12309 | 2823 | — |

- scored rows: 50/50; min=0.2028 max=0.7208 mean=0.4156

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 50 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T065316Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T065316Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T065316Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T065316Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T065316Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/corporate_records/RUN-50-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
