# Run report — `20260928T083627Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T083627Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `corporate_records_specialist_v5` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 50 docs, seed 42 |
| timestamp | `2026-09-28T08:36:27+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T083627Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:42:13+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T083627Z-eval-corporate_records', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:36:27+00:00` |
| finished_at | `2026-09-28T08:42:13+00:00` |
| duration_s (wall) | 347.3000 |
| latency_ms_mean | 39336.9 |
| latency_ms_p95 | 97541.5 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4178 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4178** (sd 0.1587, min 0.2028, max 0.7854) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 347.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0393** USD |
| cost estimated (roster token rates) | **0.0393** USD |
| cost per document (actual) | 0.0008 USD |
| cost per document (estimated) | 0.0008 USD |
| latency e2e / p50 / p95 / max | 347.3000 / 32.4245 / 97.5415 / 151.8340 s |
| prompt / completion / total tokens | 569472 / 170711 / 740183 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1966.8 s vs wall = 347.3 s -> wall/serial factor 5.66x at concurrency 8.

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
| `corporate_records_specialist` | 59 | 569472 | 170711 | 740183 | 0.0393 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1966.8 s over wall 347.3 s = **5.66×** effective parallelism at c8 (71% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` (indenture) 151.8 s = 44% of wall — p95/p50 = 3.01×.
- **Prompt length vs latency:** Pearson r = 0.91 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3414 tok/doc, mean prompt 11389 tok/doc.
- **Subclass spread:** best `powers_of_attorney` 0.713 (n=1), worst `officer_certificate` 0.283 (n=6).
- **Field-level extraction:** 31/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 13 | 0.2995 |
| indenture | 7 | 0.3099 |
| officer_certificate | 6 | 0.2835 |
| subsidiary_list | 6 | 0.4986 |
| articles_of_incorporation | 5 | 0.5969 |
| bylaws | 4 | 0.6794 |
| rights_instrument | 4 | 0.6019 |
| board_resolution | 3 | 0.3325 |
| other | 1 | 0.3156 |
| powers_of_attorney | 1 | 0.7125 |
| **total** | **50** | **0.4178** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2028 | 0.0000 | 30.3453 | 20063 | 2349 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6250 | 0.2500 | 27.5074 | 21124 | 2323 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4666 | 0.1538 | 29.4590 | 1975 | 2478 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3887 | 0.0000 | 35.6572 | 1897 | 3020 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6214 | 0.2352 | 49.0651 | 2720 | 4433 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.5678 | 0.2352 | 38.1921 | 14641 | 3191 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.5857 | 0.2352 | 28.3568 | 8014 | 2317 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.5136 | 0.1667 | 31.6242 | 1601 | 2637 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2437 | 0.0000 | 30.0583 | 10265 | 2717 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.7125 | 0.2666 | 46.9123 | 3690 | 4648 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.7854 | 0.5000 | 37.1555 | 3619 | 3044 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3214 | 0.0000 | 27.3676 | 2255 | 2515 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.2731 | 0.0000 | 30.9367 | 1802 | 2685 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.2230 | 0.0000 | 30.7119 | 1794 | 2642 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 116.6664 | 75087 | 9958 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2937 | 0.0000 | 43.8696 | 5872 | 3891 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.3022 | 0.0000 | 44.4517 | 6932 | 4042 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 24.0291 | 2276 | 2021 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 34.3816 | 3438 | 3174 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3025 | 0.0000 | 27.6616 | 4769 | 2514 | — |
| 21 | `corpus:ground_truth:train:0001214659-18-006586_ex3_3.htm` | board_resolution | 0.5014 | 0.1250 | 42.5604 | 1845 | 3892 | — |
| 22 | `corpus:ground_truth:train:0000950168-02-001563_dex211.txt` | subsidiary_list | 0.4776 | 0.2857 | 24.5003 | 1553 | 1951 | — |
| 23 | `corpus:ground_truth:train:0001493152-22-014997_ex3-2.htm` | charter_amendment | 0.2345 | 0.0000 | 34.3252 | 2339 | 2962 | — |
| 24 | `corpus:ground_truth:train:0000721748-14-000223_ex3_2bylaws.htm` | bylaws | 0.6937 | 0.2500 | 26.7961 | 13282 | 2129 | — |
| 25 | `corpus:ground_truth:train:0001193125-10-049079_dex341.htm` | charter_amendment | 0.2591 | 0.0000 | 29.4975 | 3957 | 2644 | — |
| 26 | `corpus:ground_truth:train:0001213900-20-012863_ea122016ex3-1iv_lantern.htm` | charter_amendment | 0.3673 | 0.0000 | 32.4245 | 2216 | 2755 | — |
| 27 | `corpus:ground_truth:train:0001079974-10-000369_bulkstors1ex32_72110.htm` | articles_of_incorporation | 0.5367 | 0.0000 | 24.0881 | 8530 | 2031 | — |
| 28 | `corpus:ground_truth:train:0001683168-24-006658_cloudastructure_ex0302.htm` | bylaws | 0.6625 | 0.2666 | 28.9397 | 13731 | 2470 | — |
| 29 | `corpus:ground_truth:train:0001571049-17-008060_t1702546_ex4-3.htm` | rights_instrument | 0.6208 | 0.2666 | 25.5363 | 2929 | 2153 | — |
| 30 | `corpus:ground_truth:train:0001547903-13-000020_a41specimenclassacommonsto.htm` | articles_of_incorporation | 0.4882 | 0.0000 | 33.2438 | 2227 | 3009 | — |
| 31 | `corpus:ground_truth:train:0001193125-07-225925_dex211.htm` | subsidiary_list | 0.5427 | 0.1667 | 39.2917 | 1626 | 3220 | — |
| 32 | `corpus:ground_truth:train:0000950123-09-074380_g20855a1exv3w10.htm` | officer_certificate | 0.2437 | 0.0000 | 35.9404 | 2780 | 3161 | — |
| 33 | `corpus:ground_truth:train:0001104659-20-105312_tm2024520d5_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 32.0892 | 4353 | 2974 | — |
| 34 | `corpus:ground_truth:train:0001193125-09-061115_dex32.htm` | bylaws | 0.7364 | 0.2857 | 22.9419 | 19070 | 1570 | — |
| 35 | `corpus:ground_truth:train:0001193125-09-252452_dex34.htm` | charter_amendment | 0.3530 | 0.0000 | 33.0005 | 2209 | 3077 | — |
| 36 | `corpus:ground_truth:train:0001047469-09-009128_a2194825zex-3_4.htm` | charter_amendment | 0.2864 | 0.0000 | 29.0265 | 2116 | 2470 | — |
| 37 | `corpus:ground_truth:train:0001398432-09-000149_exh4_10.htm` | rights_instrument | 0.5976 | 0.2352 | 31.6324 | 2160 | 3102 | — |
| 38 | `corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.htm` | indenture | 0.3456 | 0.0000 | 151.8340 | 94778 | 12930 | — |
| 39 | `corpus:ground_truth:train:0001193125-04-072642_dex211.htm` | subsidiary_list | 0.4776 | 0.1819 | 32.7923 | 1572 | 2804 | — |
| 40 | `corpus:ground_truth:train:0001553350-15-001174_aqua_ex3z1c.htm` | officer_certificate | 0.2661 | 0.0000 | 37.8881 | 5442 | 3569 | — |
| 41 | `corpus:ground_truth:train:0000950137-02-005662_c71678a2exv4w1.txt` | indenture | 0.3397 | 0.0000 | 97.5415 | 72702 | 8406 | — |
| 42 | `corpus:ground_truth:train:0001615774-14-000417_s100510_ex3-1.htm` | other | 0.3156 | 0.0000 | 35.6773 | 21063 | 3065 | — |
| 43 | `corpus:ground_truth:train:0000950144-06-006066_g01711a1exv4w7.txt` | indenture | 0.3212 | 0.0000 | 92.4147 | 64763 | 7672 | — |
| 44 | `corpus:ground_truth:train:0001193125-15-005780_d789569dex49.htm` | indenture | 0.2897 | 0.0000 | 38.1669 | 3073 | 3048 | — |
| 45 | `corpus:ground_truth:train:0001829126-25-005032_picardmedical_ex3-3.htm` | charter_amendment | 0.2345 | 0.0000 | 30.2919 | 2139 | 2603 | — |
| 46 | `corpus:ground_truth:train:0001193125-10-012980_dex211.htm` | subsidiary_list | 0.5136 | 0.1819 | 27.9990 | 1589 | 2430 | — |
| 47 | `corpus:ground_truth:train:0001193125-14-025241_d593074dex313.htm` | charter_amendment | 0.2829 | 0.0000 | 23.0458 | 2655 | 2071 | — |
| 48 | `corpus:ground_truth:train:0001099574-13-000003_exh32amendmentstocertificate.htm` | charter_amendment | 0.2887 | 0.0000 | 42.3577 | 4301 | 3687 | — |
| 49 | `corpus:ground_truth:train:0001193125-08-114390_dex3150.htm` | articles_of_incorporation | 0.5885 | 0.2352 | 42.6645 | 2337 | 4150 | — |
| 50 | `corpus:ground_truth:train:0001213900-19-025668_fs12019a1ex3-7_sgblocksinc.htm` | officer_certificate | 0.3513 | 0.0000 | 23.9255 | 12301 | 2107 | — |

- scored rows: 50/50; min=0.2028 max=0.7854 mean=0.4178

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 50 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T083627Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T083627Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T083627Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T083627Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T083627Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/corporate_records/RUN-50-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
