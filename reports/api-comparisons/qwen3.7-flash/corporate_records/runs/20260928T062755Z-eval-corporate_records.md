# Run report — `20260928T062755Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T062755Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `corporate_records_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 50 docs, seed 42 |
| timestamp | `2026-09-28T06:27:55+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T062755Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:33:08+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T062755Z-eval-corporate_records', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T06:27:55+00:00` |
| finished_at | `2026-09-28T06:33:08+00:00` |
| duration_s (wall) | 314.0000 |
| latency_ms_mean | 44464.9 |
| latency_ms_p95 | 107836.2 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4159 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4159** (sd 0.1560, min 0.2028, max 0.8021) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 314.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0391** USD |
| cost estimated (roster token rates) | **0.0391** USD |
| cost per document (actual) | 0.0008 USD |
| cost per document (estimated) | 0.0008 USD |
| latency e2e / p50 / p95 / max | 314.0000 / 38.6559 / 107.8362 / 121.7607 s |
| prompt / completion / total tokens | 568823 / 169671 / 738494 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2223.2 s vs wall = 314.0 s -> wall/serial factor 7.08x at concurrency 8.

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
| `corporate_records_specialist` | 59 | 568823 | 169671 | 738494 | 0.0391 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2223.2 s over wall 314.0 s = **7.08×** effective parallelism at c8 (89% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` (indenture) 121.8 s = 39% of wall — p95/p50 = 2.79×.
- **Prompt length vs latency:** Pearson r = 0.86 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3393 tok/doc, mean prompt 11376 tok/doc.
- **Subclass spread:** best `powers_of_attorney` 0.671 (n=1), worst `officer_certificate` 0.275 (n=6).
- **Field-level extraction:** 31/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 13 | 0.2999 |
| indenture | 7 | 0.3072 |
| officer_certificate | 6 | 0.2752 |
| subsidiary_list | 6 | 0.5024 |
| articles_of_incorporation | 5 | 0.6102 |
| bylaws | 4 | 0.6519 |
| rights_instrument | 4 | 0.6144 |
| board_resolution | 3 | 0.3325 |
| other | 1 | 0.2966 |
| powers_of_attorney | 1 | 0.6708 |
| **total** | **50** | **0.4159** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2028 | 0.0000 | 31.4106 | 20052 | 2713 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6250 | 0.2500 | 40.5939 | 21113 | 2695 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4666 | 0.1538 | 38.4134 | 1964 | 3252 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3887 | 0.0000 | 28.9514 | 1886 | 2427 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6714 | 0.2500 | 37.5688 | 2709 | 3246 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.5678 | 0.2352 | 46.7454 | 14630 | 4447 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.6357 | 0.2500 | 29.1654 | 8003 | 2194 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.5136 | 0.1667 | 37.7568 | 1590 | 2579 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2437 | 0.0000 | 30.9299 | 10254 | 2215 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.6708 | 0.2666 | 81.2323 | 3679 | 6081 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.8021 | 0.5000 | 48.5491 | 3608 | 3973 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3214 | 0.0000 | 34.7223 | 2244 | 2927 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.2731 | 0.0000 | 26.7795 | 1791 | 2173 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.4098 | 0.1250 | 42.5566 | 1783 | 3114 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3397 | 0.0000 | 121.6224 | 75054 | 8901 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2937 | 0.0000 | 42.0513 | 5861 | 3138 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 46.9365 | 6921 | 3975 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 40.4038 | 2265 | 2914 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 42.4732 | 3427 | 3146 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3026 | 0.0000 | 39.5891 | 4758 | 2950 | — |
| 21 | `corpus:ground_truth:train:0001214659-18-006586_ex3_3.htm` | board_resolution | 0.3147 | 0.0000 | 31.0701 | 1834 | 2686 | — |
| 22 | `corpus:ground_truth:train:0000950168-02-001563_dex211.txt` | subsidiary_list | 0.5276 | 0.2857 | 29.9294 | 1542 | 2140 | — |
| 23 | `corpus:ground_truth:train:0001493152-22-014997_ex3-2.htm` | charter_amendment | 0.2345 | 0.0000 | 48.2111 | 2328 | 3416 | — |
| 24 | `corpus:ground_truth:train:0000721748-14-000223_ex3_2bylaws.htm` | bylaws | 0.6937 | 0.2500 | 28.2231 | 13271 | 2006 | — |
| 25 | `corpus:ground_truth:train:0001193125-10-049079_dex341.htm` | charter_amendment | 0.2591 | 0.0000 | 35.7195 | 3946 | 2700 | — |
| 26 | `corpus:ground_truth:train:0001213900-20-012863_ea122016ex3-1iv_lantern.htm` | charter_amendment | 0.3673 | 0.0000 | 31.8751 | 2205 | 2557 | — |
| 27 | `corpus:ground_truth:train:0001079974-10-000369_bulkstors1ex32_72110.htm` | articles_of_incorporation | 0.5367 | 0.0000 | 27.5672 | 8519 | 1764 | — |
| 28 | `corpus:ground_truth:train:0001683168-24-006658_cloudastructure_ex0302.htm` | bylaws | 0.6208 | 0.2666 | 29.7908 | 13720 | 2442 | — |
| 29 | `corpus:ground_truth:train:0001571049-17-008060_t1702546_ex4-3.htm` | rights_instrument | 0.6208 | 0.2666 | 45.5559 | 2918 | 3217 | — |
| 30 | `corpus:ground_truth:train:0001547903-13-000020_a41specimenclassacommonsto.htm` | articles_of_incorporation | 0.4882 | 0.0000 | 31.9680 | 2216 | 2633 | — |
| 31 | `corpus:ground_truth:train:0001193125-07-225925_dex211.htm` | subsidiary_list | 0.5427 | 0.1819 | 43.5526 | 1615 | 3129 | — |
| 32 | `corpus:ground_truth:train:0000950123-09-074380_g20855a1exv3w10.htm` | officer_certificate | 0.2437 | 0.0000 | 45.5646 | 2769 | 3233 | — |
| 33 | `corpus:ground_truth:train:0001104659-20-105312_tm2024520d5_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 36.8882 | 4342 | 2573 | — |
| 34 | `corpus:ground_truth:train:0001193125-09-061115_dex32.htm` | bylaws | 0.6682 | 0.2857 | 33.4737 | 19059 | 2260 | — |
| 35 | `corpus:ground_truth:train:0001193125-09-252452_dex34.htm` | charter_amendment | 0.3530 | 0.0000 | 39.1446 | 2198 | 3044 | — |
| 36 | `corpus:ground_truth:train:0001047469-09-009128_a2194825zex-3_4.htm` | charter_amendment | 0.2864 | 0.0000 | 38.6559 | 2105 | 2720 | — |
| 37 | `corpus:ground_truth:train:0001398432-09-000149_exh4_10.htm` | rights_instrument | 0.5976 | 0.2352 | 56.2482 | 2149 | 4382 | — |
| 38 | `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` | indenture | 0.3456 | 0.0000 | 121.7607 | 94734 | 8951 | — |
| 39 | `corpus:ground_truth:train:0001193125-04-072642_dex211.htm` | subsidiary_list | 0.5003 | 0.1667 | 33.7260 | 1561 | 2770 | — |
| 40 | `corpus:ground_truth:train:0001553350-15-001174_aqua_ex3z1c.htm` | officer_certificate | 0.2661 | 0.0000 | 40.7406 | 5431 | 3663 | — |
| 41 | `corpus:ground_truth:train:0000950137-02-005662_c71678a2exv4w1.txt` | indenture | 0.3397 | 0.0000 | 100.7104 | 72669 | 7470 | — |
| 42 | `corpus:ground_truth:train:0001615774-14-000417_s100510_ex3-1.htm` | other | 0.2966 | 0.0000 | 46.0335 | 21052 | 3210 | — |
| 43 | `corpus:ground_truth:train:0000950144-06-006066_g01711a1exv4w7.txt` | indenture | 0.3212 | 0.0000 | 107.8362 | 64730 | 7575 | — |
| 44 | `corpus:ground_truth:train:0001193125-15-005780_d789569dex49.htm` | indenture | 0.2897 | 0.0000 | 51.9711 | 3062 | 3668 | — |
| 45 | `corpus:ground_truth:train:0001829126-25-005032_picardmedical_ex3-3.htm` | charter_amendment | 0.2845 | 0.0000 | 36.4691 | 2128 | 2634 | — |
| 46 | `corpus:ground_truth:train:0001193125-10-012980_dex211.htm` | subsidiary_list | 0.4636 | 0.1667 | 24.2982 | 1578 | 2039 | — |
| 47 | `corpus:ground_truth:train:0001193125-14-025241_d593074dex313.htm` | charter_amendment | 0.2829 | 0.0000 | 30.4647 | 2644 | 2548 | — |
| 48 | `corpus:ground_truth:train:0001099574-13-000003_exh32amendmentstocertificate.htm` | charter_amendment | 0.2637 | 0.0000 | 42.2057 | 4290 | 3693 | — |
| 49 | `corpus:ground_truth:train:0001193125-08-114390_dex3150.htm` | articles_of_incorporation | 0.5885 | 0.2352 | 26.6932 | 2326 | 2341 | — |
| 50 | `corpus:ground_truth:train:0001213900-19-025668_fs12019a1ex3-7_sgblocksinc.htm` | officer_certificate | 0.3014 | 0.0000 | 38.4441 | 12290 | 3147 | — |

- scored rows: 50/50; min=0.2028 max=0.8021 mean=0.4159

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 50 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T062755Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T062755Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T062755Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T062755Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T062755Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/corporate_records/RUN-50-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
