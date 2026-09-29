# Run report — `20260928T081536Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T081536Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `corporate_records_specialist_v4` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 50 docs, seed 42 |
| timestamp | `2026-09-28T08:15:36+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T081536Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:20:09+00:00` |

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
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:15:36+00:00` |
| finished_at | `2026-09-28T08:20:09+00:00` |
| duration_s (wall) | 274.6000 |
| latency_ms_mean | 37071.5 |
| latency_ms_p95 | 97770.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4248 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4248** (sd 0.1574, min 0.2028, max 0.8021) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 274.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0376** USD |
| cost estimated (roster token rates) | **0.0376** USD |
| cost per document (actual) | 0.0008 USD |
| cost per document (estimated) | 0.0008 USD |
| latency e2e / p50 / p95 / max | 274.6000 / 31.2934 / 97.7706 / 123.4042 s |
| prompt / completion / total tokens | 569885 / 157683 / 727568 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1853.6 s vs wall = 274.6 s -> wall/serial factor 6.75x at concurrency 8.

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
| `corporate_records_specialist` | 59 | 569885 | 157683 | 727568 | 0.0376 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1853.6 s over wall 274.6 s = **6.75×** effective parallelism at c8 (84% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` (indenture) 123.4 s = 45% of wall — p95/p50 = 3.12×.
- **Prompt length vs latency:** Pearson r = 0.89 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3154 tok/doc, mean prompt 11398 tok/doc.
- **Subclass spread:** best `powers_of_attorney` 0.671 (n=1), worst `officer_certificate` 0.284 (n=6).
- **Field-level extraction:** 30/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 13 | 0.2970 |
| indenture | 7 | 0.3321 |
| officer_certificate | 6 | 0.2835 |
| subsidiary_list | 6 | 0.5031 |
| articles_of_incorporation | 5 | 0.6002 |
| bylaws | 4 | 0.6638 |
| rights_instrument | 4 | 0.6144 |
| board_resolution | 3 | 0.3325 |
| other | 1 | 0.5536 |
| powers_of_attorney | 1 | 0.6708 |
| **total** | **50** | **0.4248** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2028 | 0.0000 | 34.9822 | 20070 | 2538 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6250 | 0.2500 | 13.4247 | 21131 | 988 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.5165 | 0.1667 | 41.5978 | 1982 | 3700 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3262 | 0.0000 | 29.4575 | 1904 | 2474 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6714 | 0.2500 | 26.6545 | 2727 | 2278 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.5678 | 0.2352 | 33.5935 | 14648 | 2884 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.5857 | 0.2352 | 32.7254 | 8021 | 2918 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.5136 | 0.1667 | 27.9975 | 1608 | 2204 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2437 | 0.0000 | 41.2893 | 10272 | 3424 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.6708 | 0.2666 | 50.8425 | 3697 | 4684 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.8021 | 0.5000 | 33.1201 | 3626 | 2815 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3214 | 0.0000 | 38.6589 | 2262 | 3206 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.2731 | 0.0000 | 34.9421 | 1809 | 3247 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.2230 | 0.0000 | 44.3094 | 1801 | 3450 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 97.7706 | 75108 | 7784 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2437 | 0.0000 | 29.2590 | 5879 | 2491 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 41.0462 | 6939 | 3526 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 24.8760 | 2283 | 2144 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 36.9004 | 3445 | 3043 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3526 | 0.0000 | 31.5413 | 4776 | 2512 | — |
| 21 | `corpus:ground_truth:train:0001214659-18-006586_ex3_3.htm` | board_resolution | 0.5014 | 0.1250 | 31.7768 | 1852 | 2774 | — |
| 22 | `corpus:ground_truth:train:0000950168-02-001563_dex211.txt` | subsidiary_list | 0.4776 | 0.2857 | 23.5076 | 1560 | 1925 | — |
| 23 | `corpus:ground_truth:train:0001493152-22-014997_ex3-2.htm` | charter_amendment | 0.2345 | 0.0000 | 28.7532 | 2346 | 2642 | — |
| 24 | `corpus:ground_truth:train:0000721748-14-000223_ex3_2bylaws.htm` | bylaws | 0.6312 | 0.2500 | 17.9357 | 13289 | 1555 | — |
| 25 | `corpus:ground_truth:train:0001193125-10-049079_dex341.htm` | charter_amendment | 0.2591 | 0.0000 | 27.3578 | 3964 | 2404 | — |
| 26 | `corpus:ground_truth:train:0001213900-20-012863_ea122016ex3-1iv_lantern.htm` | charter_amendment | 0.3673 | 0.0000 | 22.9466 | 2223 | 2093 | — |
| 27 | `corpus:ground_truth:train:0001079974-10-000369_bulkstors1ex32_72110.htm` | articles_of_incorporation | 0.5367 | 0.0000 | 25.5518 | 8537 | 2123 | — |
| 28 | `corpus:ground_truth:train:0001683168-24-006658_cloudastructure_ex0302.htm` | bylaws | 0.6625 | 0.2666 | 28.4373 | 13738 | 2205 | — |
| 29 | `corpus:ground_truth:train:0001571049-17-008060_t1702546_ex4-3.htm` | rights_instrument | 0.6208 | 0.2666 | 39.3363 | 2936 | 3557 | — |
| 30 | `corpus:ground_truth:train:0001547903-13-000020_a41specimenclassacommonsto.htm` | articles_of_incorporation | 0.4882 | 0.0000 | 23.9704 | 2234 | 2140 | — |
| 31 | `corpus:ground_truth:train:0001193125-07-225925_dex211.htm` | subsidiary_list | 0.5927 | 0.1819 | 33.5821 | 1633 | 2788 | — |
| 32 | `corpus:ground_truth:train:0000950123-09-074380_g20855a1exv3w10.htm` | officer_certificate | 0.2437 | 0.0000 | 30.1604 | 2787 | 2795 | — |
| 33 | `corpus:ground_truth:train:0001104659-20-105312_tm2024520d5_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 25.4356 | 4360 | 2272 | — |
| 34 | `corpus:ground_truth:train:0001193125-09-061115_dex32.htm` | bylaws | 0.7364 | 0.2857 | 26.2203 | 19077 | 2088 | — |
| 35 | `corpus:ground_truth:train:0001193125-09-252452_dex34.htm` | charter_amendment | 0.3530 | 0.0000 | 28.9288 | 2216 | 2727 | — |
| 36 | `corpus:ground_truth:train:0001047469-09-009128_a2194825zex-3_4.htm` | charter_amendment | 0.2864 | 0.0000 | 31.2934 | 2123 | 2685 | — |
| 37 | `corpus:ground_truth:train:0001398432-09-000149_exh4_10.htm` | rights_instrument | 0.5976 | 0.2352 | 28.8111 | 2167 | 2552 | — |
| 38 | `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` | indenture | 0.3973 | 0.0000 | 123.4042 | 94806 | 9917 | — |
| 39 | `corpus:ground_truth:train:0001193125-04-072642_dex211.htm` | subsidiary_list | 0.4548 | 0.1667 | 31.6956 | 1579 | 2745 | — |
| 40 | `corpus:ground_truth:train:0001553350-15-001174_aqua_ex3z1c.htm` | officer_certificate | 0.3161 | 0.0000 | 27.2730 | 5449 | 2583 | — |
| 41 | `corpus:ground_truth:train:0000950137-02-005662_c71678a2exv4w1.txt` | indenture | 0.3914 | 0.0000 | 94.2417 | 72723 | 7912 | — |
| 42 | `corpus:ground_truth:train:0001615774-14-000417_s100510_ex3-1.htm` | other | 0.5536 | 0.1819 | 29.0829 | 21070 | 2504 | — |
| 43 | `corpus:ground_truth:train:0000950144-06-006066_g01711a1exv4w7.txt` | indenture | 0.3212 | 0.0000 | 101.7460 | 64784 | 8275 | — |
| 44 | `corpus:ground_truth:train:0001193125-15-005780_d789569dex49.htm` | indenture | 0.3414 | 0.0000 | 27.8902 | 3080 | 2489 | — |
| 45 | `corpus:ground_truth:train:0001829126-25-005032_picardmedical_ex3-3.htm` | charter_amendment | 0.2845 | 0.0000 | 31.2100 | 2146 | 2807 | — |
| 46 | `corpus:ground_truth:train:0001193125-10-012980_dex211.htm` | subsidiary_list | 0.4636 | 0.1667 | 32.0430 | 1596 | 2824 | — |
| 47 | `corpus:ground_truth:train:0001193125-14-025241_d593074dex313.htm` | charter_amendment | 0.2829 | 0.0000 | 24.7289 | 2662 | 2113 | — |
| 48 | `corpus:ground_truth:train:0001099574-13-000003_exh32amendmentstocertificate.htm` | charter_amendment | 0.2887 | 0.0000 | 42.9823 | 4308 | 3879 | — |
| 49 | `corpus:ground_truth:train:0001193125-08-114390_dex3150.htm` | articles_of_incorporation | 0.5885 | 0.2352 | 29.8965 | 2344 | 2722 | — |
| 50 | `corpus:ground_truth:train:0001213900-19-025668_fs12019a1ex3-7_sgblocksinc.htm` | officer_certificate | 0.3014 | 0.0000 | 38.3885 | 12308 | 3278 | — |

- scored rows: 50/50; min=0.2028 max=0.8021 mean=0.4248

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 50 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T081536Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T081536Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T081536Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T081536Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T081536Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/corporate_records/RUN-50-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
