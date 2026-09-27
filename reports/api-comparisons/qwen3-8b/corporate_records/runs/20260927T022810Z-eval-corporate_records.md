# Run report — `20260927T022810Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T022810Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 20 docs, seed 42 |
| timestamp | `2026-09-27T02:28:10+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T022810Z-eval-corporate_records/subset_manifest.json` |
| eval git | `fd6a220` |
| finished | `2026-09-27T02:33:59+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | qwen3-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T022810Z-eval-corporate_records', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T02:28:10+00:00` |
| finished_at | `2026-09-27T02:33:59+00:00` |
| duration_s (wall) | 352.0000 |
| latency_ms_mean | 50674.8 |
| latency_ms_p95 | 240418.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.1824 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 352.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0403** USD |
| cost estimated (roster token rates) | **0.0403** USD |
| cost per document (actual) | 0.0020 USD |
| cost per document (estimated) | 0.0020 USD |
| latency e2e / p50 / p95 / max | 352.0000 / 22.5707 / 240.4187 / 318.8127 s |
| prompt / completion / total tokens | 190774 / 39458 / 230232 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1013.5 s vs wall = 352.0 s -> wall/serial factor 2.88x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `none (pipeline posture)` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 8192, "corporate_records_specialist": 8192, "correspondence_specialist": 4096, "insurance_claims_specialist": 6144, "merger_agreement_specialist": 16384}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `corporate_records_specialist` | 22 | 190774 | 39458 | 230232 | 0.0403 | qwen/qwen3-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.0000 | 0.0000 | 26.6834 | 19904 | 904 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.5500 | 0.2666 | 36.3365 | 20844 | 999 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.0000 | 0.0000 | 7.8022 | 1920 | 356 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.0000 | 0.0000 | 22.5707 | 1840 | 846 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.5976 | 0.2352 | 22.1094 | 2657 | 816 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.0000 | 0.0000 | 13.4852 | 14339 | 381 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.5857 | 0.2352 | 17.6945 | 7922 | 607 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.0000 | 0.0000 | 18.6039 | 1557 | 1096 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2295 | 0.0000 | 20.0458 | 10163 | 665 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.0000 | 0.0000 | 49.3670 | 3614 | 2150 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.0000 | 0.0000 | 17.4741 | 3567 | 950 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.2521 | 0.0000 | 21.6775 | 2190 | 698 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.0000 | 0.0000 | 240.4187 | 1747 | 9776 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.2230 | 0.0000 | 42.6869 | 1738 | 1979 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.4576 | 0.1250 | 318.8127 | 73994 | 11914 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2295 | 0.0000 | 36.1448 | 5789 | 855 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.0000 | 0.0000 | 47.0114 | 6747 | 2059 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2606 | 0.0000 | 10.3224 | 2216 | 637 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.2615 | 0.0000 | 25.7696 | 3340 | 925 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.0000 | 0.0000 | 18.4797 | 4686 | 845 | — |

- scored rows: 20/20; min=0.0000 max=0.5976 mean=0.1824

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
