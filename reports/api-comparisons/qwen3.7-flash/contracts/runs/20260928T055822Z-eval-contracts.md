# Run report — `20260928T055822Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T055822Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `contracts_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 50 docs, seed 42 |
| timestamp | `2026-09-28T05:58:22+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T055822Z-eval-contracts/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:09:11+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T055822Z-eval-contracts', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:58:22+00:00` |
| finished_at | `2026-09-28T06:09:11+00:00` |
| duration_s (wall) | 651.2000 |
| latency_ms_mean | 89440.7 |
| latency_ms_p95 | 218906.0 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5277 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5277** (sd 0.2353, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 651.2000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0700** USD |
| cost estimated (roster token rates) | **0.0700** USD |
| cost per document (actual) | 0.0014 USD |
| cost per document (estimated) | 0.0014 USD |
| latency e2e / p50 / p95 / max | 651.2000 / 76.1561 / 218.9060 / 284.2878 s |
| prompt / completion / total tokens | 736712 / 368531 / 1105243 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 4472.0 s vs wall = 651.2 s -> wall/serial factor 6.87x at concurrency 8.

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
| `contracts_specialist` | 60 | 736712 | 368531 | 1105243 | 0.0700 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 4472.0 s over wall 651.2 s = **6.87×** effective parallelism at c8 (86% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018-EX-10.6-Franchise Agreement.PDF` (Franchise) 284.3 s = 44% of wall — p95/p50 = 2.87×.
- **Prompt length vs latency:** Pearson r = 0.76 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 7371 tok/doc, mean prompt 14734 tok/doc.
- **Subclass spread:** best `Reseller` 0.750 (n=1), worst `IP` 0.351 (n=3).
- **Field-level extraction:** 16/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Consulting Agreements | 6 | 0.6479 |
| Sponsorship | 5 | 0.5559 |
| Strategic Alliance | 5 | 0.6602 |
| Franchise | 4 | 0.4473 |
| Collaboration | 3 | 0.5585 |
| Distributor | 3 | 0.3771 |
| IP | 3 | 0.3514 |
| License_Agreements | 3 | 0.5865 |
| Maintenance | 3 | 0.4799 |
| Marketing | 3 | 0.4118 |
| Joint Venture _ Filing | 2 | 0.4950 |
| Supply | 2 | 0.6680 |
| Transportation | 2 | 0.3824 |
| Agency Agreements | 1 | 0.6250 |
| Development | 1 | 0.5606 |
| Endorsement | 1 | 0.3623 |
| Promotion | 1 | 0.5469 |
| Reseller | 1 | 0.7500 |
| Service | 1 | 0.3956 |
| **total** | **50** | **0.5277** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.3623 | 0.0000 | 86.5487 | 5992 | 6455 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6250 | 0.2857 | 136.3873 | 14346 | 7608 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.6297 | 0.2857 | 61.2028 | 6128 | 5812 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6785 | 0.2500 | 63.0537 | 15722 | 5718 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.5466 | 0.2857 | 116.6509 | 44767 | 10621 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.6818 | 0.2223 | 74.8614 | 4194 | 6952 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.5444 | 0.2223 | 62.5585 | 10879 | 6047 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5469 | 0.2857 | 124.3026 | 42753 | 12133 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3514 | 0.0000 | 44.0901 | 3579 | 3636 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2501 | 39.9154 | 3579 | 3602 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.5606 | 0.2500 | 76.1561 | 16467 | 6803 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.0000 | 0.0000 | 91.6586 | 6880 | 8190 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.6035 | 0.2500 | 61.7604 | 14216 | 6003 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.5869 | 0.2000 | 76.1165 | 5829 | 7033 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3514 | 0.0000 | 41.6400 | 2641 | 3748 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.5535 | 0.1818 | 157.9065 | 39026 | 15231 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.2720 | 0.0000 | 82.3663 | 9333 | 7560 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.7916 | 0.2223 | 78.3978 | 5102 | 7196 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6764 | 0.2000 | 229.0189 | 31131 | 14194 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.6429 | 0.2223 | 58.8717 | 17564 | 5569 | — |
| 21 | `corpus:ground_truth:train:MTITECHNOLOGYCORP_11_16_2004-EX-10.102-Reseller Agreement Premier Addendum.PDF` | Reseller | 0.7500 | 0.2000 | 81.5830 | 9328 | 7376 | — |
| 22 | `corpus:ground_truth:train:0001193125-14-242205_d623882dex1023.htm` | Supply | 1.0000 | 0.2222 | 46.0186 | 4198 | 3982 | — |
| 23 | `corpus:ground_truth:train:TELEGLOBEINTERNATIONALHOLDINGSLTD_03_29_2004-EX-10.10-CONSTRUCTION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.5484 | 0.2857 | 73.5856 | 22582 | 5966 | — |
| 24 | `corpus:ground_truth:train:ADUROBIOTECH,INC_06_02_2020-EX-10.7-CONSULTING AGREEMENT(1).PDF` | Consulting Agreements | 0.6875 | 0.2500 | 58.1724 | 4875 | 5532 | — |
| 25 | `corpus:ground_truth:train:0001564590-21-028164_ck7045120534-ex108_276.htm` | IP | 0.3514 | 0.0000 | 58.8933 | 13037 | 4489 | — |
| 26 | `corpus:ground_truth:train:DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.PDF` | Transportation | 0.0000 | 0.0000 | 127.7412 | 12226 | 8192 | — |
| 27 | `corpus:ground_truth:train:CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.PDF` | Sponsorship | 0.7500 | 0.2223 | 67.2764 | 4478 | 6328 | — |
| 28 | `corpus:ground_truth:train:SPHERE3DCORP_06_24_2020-EX-10.12-CONSULTING AGREEMENT.PDF` | Consulting Agreements | 0.6666 | 0.2000 | 76.4535 | 4896 | 7644 | — |
| 29 | `corpus:ground_truth:train:PRECIGEN,INC_01_22_2020-EX-99.1-JOINT FILING AGREEMENT.PDF` | Joint Venture _ Filing | 0.3472 | 0.0000 | 36.1946 | 2801 | 3035 | — |
| 30 | `corpus:ground_truth:train:XYBERNAUTCORP_07_12_2002-EX-4-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.0000 | 0.0000 | 92.1280 | 13149 | 8190 | — |
| 31 | `corpus:ground_truth:train:CcRealEstateIncomeFundadv_20181205_POS 8C_EX-99.(H)(3)_11447739_EX-99.(H)(3)_Marketing Agreement.pdf` | Marketing | 0.6429 | 0.2500 | 61.5616 | 8912 | 5538 | — |
| 32 | `corpus:ground_truth:train:GpaqAcquisitionHoldingsInc_20200123_S-4A_EX-10.8_11951679_EX-10.8_Service Agreement.pdf` | Service | 0.3956 | 0.0000 | 159.8332 | 28370 | 15429 | — |
| 33 | `corpus:ground_truth:train:0001213900-23-083790_ea187099ex10-23_perfect.htm` | Consulting Agreements | 1.0000 | 0.2501 | 62.5177 | 3566 | 5445 | — |
| 34 | `corpus:ground_truth:train:GAINSCOINC_01_21_2010-EX-10.41-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.7116 | 0.2223 | 174.0328 | 11654 | 15790 | — |
| 35 | `corpus:ground_truth:train:0001493152-17-012423_ex10-25.htm` | Consulting Agreements | 0.2667 | 0.0000 | 48.9624 | 4582 | 3964 | — |
| 36 | `corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018-EX-10.6-Franchise Agreement.PDF` | Franchise | 0.5928 | 0.2000 | 284.2878 | 74125 | 17597 | — |
| 37 | `corpus:ground_truth:train:XENCORINC_10_25_2013-EX-10.24-COLLABORATION AGREEMENT (3).PDF` | Collaboration | 0.5454 | 0.2223 | 108.6292 | 40141 | 8758 | — |
| 38 | `corpus:ground_truth:train:AudibleInc_20001113_10-Q_EX-10.32_2599586_EX-10.32_Co-Branding Agreement_ Marketing Agreement_ Investment Distribution Agreement.pdf` | Marketing | 0.3204 | 0.0000 | 92.7171 | 18567 | 7835 | — |
| 39 | `corpus:ground_truth:train:AIRTECHINTERNATIONALGROUPINC_05_08_2000-EX-10.4-FRANCHISE AGREEMENT.PDF` | Franchise | 0.6429 | 0.2223 | 80.8069 | 18221 | 6955 | — |
| 40 | `corpus:ground_truth:train:PHREESIA,INC_05_28_2019-EX-10.18-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5294 | 0.3333 | 218.9060 | 29952 | 12156 | — |
| 41 | `corpus:ground_truth:train:SUMMAFOURINC_06_19_1998-EX-10.3-SOFTWARE LICENSE AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.2878 | 0.0000 | 76.4708 | 24297 | 6141 | — |
| 42 | `corpus:ground_truth:train:0001213900-25-051717_ea024476901ex10-38_natures.htm` | Supply | 0.3359 | 0.0000 | 49.8651 | 6814 | 3818 | — |
| 43 | `corpus:ground_truth:train:SimplicityEsportsGamingCompany_20181130_8-K_EX-10.1_11444071_EX-10.1_Franchise Agreement.pdf` | Franchise | 0.0000 | 0.0000 | 86.8958 | 8656 | 8190 | — |
| 44 | `corpus:ground_truth:train:MARTINMIDSTREAMPARTNERSLP_01_23_2004-EX-10.3-TRANSPORTATION SERVICES AGREEMENT.PDF` | Transportation | 0.7647 | 0.2223 | 95.8702 | 5345 | 7858 | — |
| 45 | `corpus:ground_truth:train:RemarkHoldingsInc_20081114_10-Q_EX-10.24_2895649_EX-10.24_Content License Agreement.pdf` | License_Agreements | 0.5463 | 0.2857 | 74.8965 | 15669 | 6151 | — |
| 46 | `corpus:ground_truth:train:GSVINC_05_15_1998-EX-10-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.6363 | 0.2223 | 85.7491 | 10974 | 6881 | — |
| 47 | `corpus:ground_truth:train:SPIENERGYCO,LTD_07_10_2014-EX-10-Cooperation Agreement of 50MWp Photovoltaic Grid-connected Power Generation Project in Yangqiao of~1.PDF` | Collaboration | 0.5834 | 0.3333 | 46.6558 | 3046 | 3882 | — |
| 48 | `corpus:ground_truth:train:BANUESTRAFINANCIALCORP_09_08_2006-EX-10.16-AGENCY AGREEMENT.PDF` | Agency Agreements | 0.6250 | 0.3333 | 46.4598 | 11794 | 3507 | — |
| 49 | `corpus:ground_truth:train:0000950123-09-046709_y01981a3exv10w15.htm` | Consulting Agreements | 0.2667 | 0.0000 | 68.3970 | 9443 | 5952 | — |
| 50 | `corpus:ground_truth:train:GlobalTechnologiesGroupInc_20050928_10KSB_EX-10.9_4148808_EX-10.9_Content License Agreement.pdf` | License_Agreements | 0.5834 | 0.2223 | 67.0091 | 10886 | 5839 | — |

- scored rows: 50/50; min=0.0000 max=1.0000 mean=0.5277

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 50 --seed 42 --concurrency 8 --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260928T055822Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T055822Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T055822Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T055822Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T055822Z-eval-contracts.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/contracts/RUN-50-CONTRACT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
