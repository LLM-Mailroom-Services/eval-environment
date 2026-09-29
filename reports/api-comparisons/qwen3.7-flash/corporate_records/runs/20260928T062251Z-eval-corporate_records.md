# Run report — `20260928T062251Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T062251Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 50 docs, seed 42 |
| timestamp | `2026-09-28T06:22:51+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T062251Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:27:48+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T062251Z-eval-corporate_records', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T06:22:51+00:00` |
| finished_at | `2026-09-28T06:27:48+00:00` |
| duration_s (wall) | 299.1000 |
| latency_ms_mean | 40759.7 |
| latency_ms_p95 | 105988.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4186 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4186** (sd 0.1456, min 0.2028, max 0.7396) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 299.1000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0387** USD |
| cost estimated (roster token rates) | **0.0387** USD |
| cost per document (actual) | 0.0008 USD |
| cost per document (estimated) | 0.0008 USD |
| latency e2e / p50 / p95 / max | 299.1000 / 34.6555 / 105.9884 / 121.9464 s |
| prompt / completion / total tokens | 568410 / 166233 / 734643 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2038.0 s vs wall = 299.1 s -> wall/serial factor 6.81x at concurrency 8.

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
| `corporate_records_specialist` | 59 | 568410 | 166233 | 734643 | 0.0387 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2038.0 s over wall 299.1 s = **6.81×** effective parallelism at c8 (85% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` (indenture) 121.9 s = 41% of wall — p95/p50 = 3.06×.
- **Prompt length vs latency:** Pearson r = 0.90 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3325 tok/doc, mean prompt 11368 tok/doc.
- **Subclass spread:** best `bylaws` 0.647 (n=4), worst `officer_certificate` 0.297 (n=6).
- **Field-level extraction:** 30/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 13 | 0.3009 |
| indenture | 7 | 0.3028 |
| officer_certificate | 6 | 0.2969 |
| subsidiary_list | 6 | 0.4986 |
| articles_of_incorporation | 5 | 0.5877 |
| bylaws | 4 | 0.6467 |
| rights_instrument | 4 | 0.6084 |
| board_resolution | 3 | 0.3948 |
| other | 1 | 0.3591 |
| powers_of_attorney | 1 | 0.6208 |
| **total** | **50** | **0.4186** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2028 | 0.0000 | 32.4159 | 20045 | 2716 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6250 | 0.2500 | 30.6884 | 21106 | 2168 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4666 | 0.1538 | 39.4663 | 1957 | 3510 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3262 | 0.0000 | 33.0611 | 1879 | 3039 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6476 | 0.2500 | 19.2239 | 2702 | 1776 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.5678 | 0.2352 | 31.0614 | 14623 | 2812 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.5857 | 0.2352 | 34.1117 | 7996 | 2708 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.5136 | 0.1667 | 42.1303 | 1583 | 3503 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2436 | 0.0000 | 38.8142 | 10247 | 2982 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.6208 | 0.2500 | 60.1764 | 3672 | 5370 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.7396 | 0.4000 | 41.8358 | 3601 | 3182 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3214 | 0.0000 | 35.0434 | 2237 | 3067 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.2731 | 0.0000 | 30.1988 | 1784 | 2759 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.4098 | 0.1250 | 36.8293 | 1776 | 3074 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 105.8174 | 75033 | 8311 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2936 | 0.0000 | 36.5042 | 5854 | 3211 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 41.9275 | 6914 | 3713 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 25.4513 | 2258 | 2247 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 34.4477 | 3420 | 2980 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3525 | 0.0000 | 31.8804 | 4751 | 2724 | — |
| 21 | `corpus:ground_truth:train:0001214659-18-006586_ex3_3.htm` | board_resolution | 0.5014 | 0.1250 | 38.8971 | 1827 | 2751 | — |
| 22 | `corpus:ground_truth:train:0000950168-02-001563_dex211.txt` | subsidiary_list | 0.4776 | 0.2857 | 28.9413 | 1535 | 2191 | — |
| 23 | `corpus:ground_truth:train:0001493152-22-014997_ex3-2.htm` | charter_amendment | 0.2845 | 0.0000 | 37.2288 | 2321 | 2914 | — |
| 24 | `corpus:ground_truth:train:0000721748-14-000223_ex3_2bylaws.htm` | bylaws | 0.6312 | 0.2500 | 20.8257 | 13264 | 1709 | — |
| 25 | `corpus:ground_truth:train:0001193125-10-049079_dex341.htm` | charter_amendment | 0.2591 | 0.0000 | 39.1116 | 3939 | 3448 | — |
| 26 | `corpus:ground_truth:train:0001213900-20-012863_ea122016ex3-1iv_lantern.htm` | charter_amendment | 0.3673 | 0.0000 | 35.4391 | 2198 | 2552 | — |
| 27 | `corpus:ground_truth:train:0001079974-10-000369_bulkstors1ex32_72110.htm` | articles_of_incorporation | 0.5367 | 0.0000 | 21.7951 | 8512 | 1891 | — |
| 28 | `corpus:ground_truth:train:0001683168-24-006658_cloudastructure_ex0302.htm` | bylaws | 0.6625 | 0.2666 | 43.3958 | 13713 | 3467 | — |
| 29 | `corpus:ground_truth:train:0001571049-17-008060_t1702546_ex4-3.htm` | rights_instrument | 0.6208 | 0.2666 | 34.4558 | 2911 | 2598 | — |
| 30 | `corpus:ground_truth:train:0001547903-13-000020_a41specimenclassacommonsto.htm` | articles_of_incorporation | 0.4882 | 0.0000 | 34.4872 | 2209 | 2958 | — |
| 31 | `corpus:ground_truth:train:0001193125-07-225925_dex211.htm` | subsidiary_list | 0.5927 | 0.1819 | 43.6430 | 1608 | 3567 | — |
| 32 | `corpus:ground_truth:train:0000950123-09-074380_g20855a1exv3w10.htm` | officer_certificate | 0.2436 | 0.0000 | 39.3251 | 2762 | 3055 | — |
| 33 | `corpus:ground_truth:train:0001104659-20-105312_tm2024520d5_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 37.4783 | 4335 | 3342 | — |
| 34 | `corpus:ground_truth:train:0001193125-09-061115_dex32.htm` | bylaws | 0.6682 | 0.2857 | 30.3415 | 19052 | 2264 | — |
| 35 | `corpus:ground_truth:train:0001193125-09-252452_dex34.htm` | charter_amendment | 0.3530 | 0.0000 | 29.1409 | 2191 | 2538 | — |
| 36 | `corpus:ground_truth:train:0001047469-09-009128_a2194825zex-3_4.htm` | charter_amendment | 0.2864 | 0.0000 | 30.9413 | 2098 | 2647 | — |
| 37 | `corpus:ground_truth:train:0001398432-09-000149_exh4_10.htm` | rights_instrument | 0.5976 | 0.2352 | 31.4141 | 2142 | 2310 | — |
| 38 | `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` | indenture | 0.3456 | 0.0000 | 121.9464 | 94706 | 9878 | — |
| 39 | `corpus:ground_truth:train:0001193125-04-072642_dex211.htm` | subsidiary_list | 0.4776 | 0.1667 | 34.6555 | 1554 | 2617 | — |
| 40 | `corpus:ground_truth:train:0001553350-15-001174_aqua_ex3z1c.htm` | officer_certificate | 0.3161 | 0.0000 | 27.2726 | 5424 | 2470 | — |
| 41 | `corpus:ground_truth:train:0000950137-02-005662_c71678a2exv4w1.txt` | indenture | 0.2897 | 0.0000 | 115.1421 | 72648 | 8728 | — |
| 42 | `corpus:ground_truth:train:0001615774-14-000417_s100510_ex3-1.htm` | other | 0.3591 | 0.0000 | 31.3267 | 21045 | 2243 | — |
| 43 | `corpus:ground_truth:train:0000950144-06-006066_g01711a1exv4w7.txt` | indenture | 0.3212 | 0.0000 | 105.9884 | 64709 | 8705 | — |
| 44 | `corpus:ground_truth:train:0001193125-15-005780_d789569dex49.htm` | indenture | 0.2897 | 0.0000 | 38.2175 | 3055 | 2975 | — |
| 45 | `corpus:ground_truth:train:0001829126-25-005032_picardmedical_ex3-3.htm` | charter_amendment | 0.2845 | 0.0000 | 31.8049 | 2121 | 2297 | — |
| 46 | `corpus:ground_truth:train:0001193125-10-012980_dex211.htm` | subsidiary_list | 0.4636 | 0.1667 | 34.6893 | 1571 | 2940 | — |
| 47 | `corpus:ground_truth:train:0001193125-14-025241_d593074dex313.htm` | charter_amendment | 0.2829 | 0.0000 | 25.1207 | 2637 | 1793 | — |
| 48 | `corpus:ground_truth:train:0001099574-13-000003_exh32amendmentstocertificate.htm` | charter_amendment | 0.2887 | 0.0000 | 46.4325 | 4283 | 4004 | — |
| 49 | `corpus:ground_truth:train:0001193125-08-114390_dex3150.htm` | articles_of_incorporation | 0.5885 | 0.2352 | 32.8953 | 2319 | 2363 | — |
| 50 | `corpus:ground_truth:train:0001213900-19-025668_fs12019a1ex3-7_sgblocksinc.htm` | officer_certificate | 0.3321 | 0.0000 | 34.5455 | 12283 | 3166 | — |

- scored rows: 50/50; min=0.2028 max=0.7396 mean=0.4186

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 50 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T062251Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T062251Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T062251Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T062251Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T062251Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/corporate_records/RUN-50-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
