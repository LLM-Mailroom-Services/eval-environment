# Run report — `20260927T105549Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T105549Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `—` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 20 docs, seed 42 |
| timestamp | `2026-09-27T10:55:49+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T105549Z-eval-contracts/subset_manifest.json` |
| eval git | `3c2c95c` |
| finished | `2026-09-27T11:01:49+00:00` |

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
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T105549Z-eval-contracts', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T10:55:49+00:00` |
| finished_at | `2026-09-27T11:01:49+00:00` |
| duration_s (wall) | 361.6000 |
| latency_ms_mean | 73489.4 |
| latency_ms_p95 | 268776.2 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5137 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 361.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0502** USD |
| cost estimated (roster token rates) | **0.0502** USD |
| cost per document (actual) | 0.0025 USD |
| cost per document (estimated) | 0.0025 USD |
| latency e2e / p50 / p95 / max | 361.6000 / 18.0436 / 268.7762 / 341.0738 s |
| prompt / completion / total tokens | 334616 / 132835 / 467451 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1469.8 s vs wall = 361.6 s -> wall/serial factor 4.06x at concurrency 8.

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
| `contracts_specialist` | 23 | 334616 | 132835 | 467451 | 0.0502 | deepseek/deepseek-v4.1-flash |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.7778 | 0.2857 | 268.7762 | 5796 | 4679 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6666 | 0.2500 | 16.3030 | 13978 | 3225 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.7408 | 0.2857 | 12.8183 | 6085 | 4072 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.8572 | 0.2500 | 14.6747 | 15421 | 4805 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.5666 | 0.2857 | 341.0738 | 38673 | 6341 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.8637 | 0.2223 | 16.2712 | 4088 | 6050 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.6889 | 0.2223 | 16.2894 | 10825 | 6432 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5781 | 0.2223 | 18.0436 | 37812 | 5945 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3514 | 0.0000 | 14.8176 | 3400 | 4677 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2501 | 7.8967 | 3503 | 1933 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.7272 | 0.2223 | 148.1829 | 32489 | 13560 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.0000 | 0.0000 | 78.6799 | 13341 | 16384 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.6896 | 0.2500 | 13.8140 | 13747 | 5235 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.0000 | 0.0000 | 32.4056 | 5777 | 8192 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3514 | 0.0000 | 7.1432 | 2610 | 1696 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.0000 | 0.0000 | 159.5681 | 68665 | 16384 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.0000 | 0.0000 | 38.1291 | 9224 | 8192 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.0000 | 0.0000 | 37.7322 | 5037 | 8192 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6471 | 0.2000 | 12.5111 | 27094 | 2922 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.7678 | 0.1538 | 214.6574 | 17051 | 3919 | — |

- scored rows: 20/20; min=0.0000 max=1.0000 mean=0.5137

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
