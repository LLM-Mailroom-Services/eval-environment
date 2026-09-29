# Run report — `20260928T063713Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T063713Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `contracts_specialist_v3` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 50 docs, seed 42 |
| timestamp | `2026-09-28T06:37:13+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T063713Z-eval-contracts/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:48:42+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T063713Z-eval-contracts', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T06:37:13+00:00` |
| finished_at | `2026-09-28T06:48:42+00:00` |
| duration_s (wall) | 690.2000 |
| latency_ms_mean | 95005.6 |
| latency_ms_p95 | 202765.2 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5462 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5462** (sd 0.1989, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 690.2000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0739** USD |
| cost estimated (roster token rates) | **0.0739** USD |
| cost per document (actual) | 0.0015 USD |
| cost per document (estimated) | 0.0015 USD |
| latency e2e / p50 / p95 / max | 690.2000 / 76.7887 / 202.7652 / 279.8910 s |
| prompt / completion / total tokens | 786252 / 387157 / 1173409 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 4750.3 s vs wall = 690.2 s -> wall/serial factor 6.88x at concurrency 8.

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
| `contracts_specialist` | 61 | 786252 | 387157 | 1173409 | 0.0739 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 4750.3 s over wall 690.2 s = **6.88×** effective parallelism at c8 (86% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018-EX-10.6-Franchise Agreement.PDF` (Franchise) 279.9 s = 41% of wall — p95/p50 = 2.64×.
- **Prompt length vs latency:** Pearson r = 0.90 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 7743 tok/doc, mean prompt 15725 tok/doc.
- **Subclass spread:** best `Consulting Agreements` 0.672 (n=6), worst `Service` 0.000 (n=1).
- **Field-level extraction:** 11/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Consulting Agreements | 6 | 0.6722 |
| Sponsorship | 5 | 0.6196 |
| Strategic Alliance | 5 | 0.6206 |
| Franchise | 4 | 0.4496 |
| Collaboration | 3 | 0.5523 |
| Distributor | 3 | 0.5823 |
| IP | 3 | 0.3466 |
| License_Agreements | 3 | 0.5895 |
| Maintenance | 3 | 0.4692 |
| Marketing | 3 | 0.3863 |
| Joint Venture _ Filing | 2 | 0.5357 |
| Supply | 2 | 0.6680 |
| Transportation | 2 | 0.5668 |
| Agency Agreements | 1 | 0.6666 |
| Development | 1 | 0.5606 |
| Endorsement | 1 | 0.5555 |
| Promotion | 1 | 0.5625 |
| Reseller | 1 | 0.6111 |
| Service | 1 | 0.0000 |
| **total** | **50** | **0.5462** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.5555 | 0.2857 | 73.5804 | 6009 | 6475 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5278 | 0.2857 | 79.0815 | 14357 | 7029 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.5926 | 0.2857 | 64.9040 | 6145 | 6311 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5357 | 0.2857 | 56.8101 | 15739 | 4946 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.5734 | 0.2223 | 170.5493 | 44801 | 14315 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.6818 | 0.2000 | 65.2143 | 4211 | 6153 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.5444 | 0.2223 | 79.7829 | 10896 | 5700 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5625 | 0.2000 | 194.0058 | 42787 | 15613 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3514 | 0.0000 | 71.0241 | 3596 | 5386 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2501 | 46.5319 | 3596 | 4127 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.5606 | 0.2500 | 66.1489 | 16484 | 6010 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.5938 | 0.2000 | 79.0593 | 6897 | 6230 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.5862 | 0.2500 | 68.9698 | 14233 | 5493 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.6087 | 0.2000 | 78.9016 | 5846 | 6370 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3514 | 0.0000 | 42.2020 | 2658 | 3284 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.5834 | 0.1818 | 157.2092 | 39060 | 13880 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.2881 | 0.0000 | 73.1752 | 9350 | 6238 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.7500 | 0.2223 | 157.6032 | 5125 | 7928 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6618 | 0.2500 | 231.4693 | 57709 | 27136 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.5715 | 0.1818 | 86.2223 | 17581 | 6840 | — |
| 21 | `corpus:ground_truth:train:MTITECHNOLOGYCORP_11_16_2004-EX-10.102-Reseller Agreement Premier Addendum.PDF` | Reseller | 0.6111 | 0.2223 | 77.9166 | 9345 | 7241 | — |
| 22 | `corpus:ground_truth:train:0001193125-14-242205_d623882dex1023.htm` | Supply | 1.0000 | 0.2222 | 63.0837 | 4215 | 5049 | — |
| 23 | `corpus:ground_truth:train:TELEGLOBEINTERNATIONALHOLDINGSLTD_03_29_2004-EX-10.10-CONSTRUCTION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.5484 | 0.2857 | 146.4614 | 22605 | 6561 | — |
| 24 | `corpus:ground_truth:train:ADUROBIOTECH,INC_06_02_2020-EX-10.7-CONSULTING AGREEMENT(1).PDF` | Consulting Agreements | 0.7500 | 0.2223 | 72.6627 | 4892 | 5578 | — |
| 25 | `corpus:ground_truth:train:0001564590-21-028164_ck7045120534-ex108_276.htm` | IP | 0.3369 | 0.0000 | 63.8795 | 13054 | 4917 | — |
| 26 | `corpus:ground_truth:train:DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.PDF` | Transportation | 0.5454 | 0.2223 | 84.0135 | 12237 | 8190 | — |
| 27 | `corpus:ground_truth:train:CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.PDF` | Sponsorship | 0.6429 | 0.2223 | 62.7712 | 4495 | 4591 | — |
| 28 | `corpus:ground_truth:train:SPHERE3DCORP_06_24_2020-EX-10.12-CONSULTING AGREEMENT.PDF` | Consulting Agreements | 0.7500 | 0.2000 | 70.6782 | 4913 | 6705 | — |
| 29 | `corpus:ground_truth:train:PRECIGEN,INC_01_22_2020-EX-99.1-JOINT FILING AGREEMENT.PDF` | Joint Venture _ Filing | 0.5000 | 0.3333 | 91.5723 | 2824 | 3564 | — |
| 30 | `corpus:ground_truth:train:XYBERNAUTCORP_07_12_2002-EX-4-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.6177 | 0.2000 | 78.4085 | 13166 | 7710 | — |
| 31 | `corpus:ground_truth:train:CcRealEstateIncomeFundadv_20181205_POS 8C_EX-99.(H)(3)_11447739_EX-99.(H)(3)_Marketing Agreement.pdf` | Marketing | 0.5715 | 0.2500 | 64.5105 | 8929 | 6125 | — |
| 32 | `corpus:ground_truth:train:GpaqAcquisitionHoldingsInc_20200123_S-4A_EX-10.8_11951679_EX-10.8_Service Agreement.pdf` | Service | 0.0000 | 0.0000 | 102.6424 | 14199 | 8190 | — |
| 33 | `corpus:ground_truth:train:0001213900-23-083790_ea187099ex10-23_perfect.htm` | Consulting Agreements | 1.0000 | 0.2858 | 47.6761 | 3583 | 3684 | — |
| 34 | `corpus:ground_truth:train:GAINSCOINC_01_21_2010-EX-10.41-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.5192 | 0.2223 | 63.6643 | 5841 | 6318 | — |
| 35 | `corpus:ground_truth:train:0001493152-17-012423_ex10-25.htm` | Consulting Agreements | 0.2667 | 0.0000 | 60.7438 | 4599 | 5241 | — |
| 36 | `corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018-EX-10.6-Franchise Agreement.PDF` | Franchise | 0.5670 | 0.1818 | 279.8910 | 74176 | 21545 | — |
| 37 | `corpus:ground_truth:train:XENCORINC_10_25_2013-EX-10.24-COLLABORATION AGREEMENT (3).PDF` | Collaboration | 0.5000 | 0.3333 | 202.7652 | 40181 | 10952 | — |
| 38 | `corpus:ground_truth:train:AudibleInc_20001113_10-Q_EX-10.32_2599586_EX-10.32_Co-Branding Agreement_ Marketing Agreement_ Investment Distribution Agreement.pdf` | Marketing | 0.2992 | 0.0000 | 71.0625 | 18584 | 7187 | — |
| 39 | `corpus:ground_truth:train:AIRTECHINTERNATIONALGROUPINC_05_08_2000-EX-10.4-FRANCHISE AGREEMENT.PDF` | Franchise | 0.0000 | 0.0000 | 84.5825 | 18238 | 8190 | — |
| 40 | `corpus:ground_truth:train:PHREESIA,INC_05_28_2019-EX-10.18-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6275 | 0.1667 | 197.9503 | 56304 | 17654 | — |
| 41 | `corpus:ground_truth:train:SUMMAFOURINC_06_19_1998-EX-10.3-SOFTWARE LICENSE AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.2731 | 0.0000 | 89.4592 | 24314 | 7146 | — |
| 42 | `corpus:ground_truth:train:0001213900-25-051717_ea024476901ex10-38_natures.htm` | Supply | 0.3359 | 0.0000 | 61.0581 | 6831 | 4261 | — |
| 43 | `corpus:ground_truth:train:SimplicityEsportsGamingCompany_20181130_8-K_EX-10.1_11444071_EX-10.1_Franchise Agreement.pdf` | Franchise | 0.6482 | 0.2857 | 73.1367 | 8673 | 5704 | — |
| 44 | `corpus:ground_truth:train:MARTINMIDSTREAMPARTNERSLP_01_23_2004-EX-10.3-TRANSPORTATION SERVICES AGREEMENT.PDF` | Transportation | 0.5882 | 0.2223 | 76.7887 | 5362 | 6302 | — |
| 45 | `corpus:ground_truth:train:RemarkHoldingsInc_20081114_10-Q_EX-10.24_2895649_EX-10.24_Content License Agreement.pdf` | License_Agreements | 0.5926 | 0.2223 | 141.3481 | 31378 | 13544 | — |
| 46 | `corpus:ground_truth:train:GSVINC_05_15_1998-EX-10-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.6363 | 0.2500 | 67.0035 | 10991 | 6595 | — |
| 47 | `corpus:ground_truth:train:SPIENERGYCO,LTD_07_10_2014-EX-10-Cooperation Agreement of 50MWp Photovoltaic Grid-connected Power Generation Project in Yangqiao of~1.PDF` | Collaboration | 0.5834 | 0.3333 | 49.5156 | 3063 | 3510 | — |
| 48 | `corpus:ground_truth:train:BANUESTRAFINANCIALCORP_09_08_2006-EX-10.16-AGENCY AGREEMENT.PDF` | Agency Agreements | 0.6666 | 0.2857 | 58.8593 | 11811 | 5095 | — |
| 49 | `corpus:ground_truth:train:0000950123-09-046709_y01981a3exv10w15.htm` | Consulting Agreements | 0.2667 | 0.0000 | 123.7880 | 9466 | 6683 | — |
| 50 | `corpus:ground_truth:train:GlobalTechnologiesGroupInc_20050928_10KSB_EX-10.9_4148808_EX-10.9_Content License Agreement.pdf` | License_Agreements | 0.5834 | 0.2223 | 79.9400 | 10903 | 7661 | — |

- scored rows: 50/50; min=0.0000 max=1.0000 mean=0.5462

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 50 --seed 42 --concurrency 8 --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260928T063713Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T063713Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T063713Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T063713Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T063713Z-eval-contracts.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/contracts/RUN-50-CONTRACT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
