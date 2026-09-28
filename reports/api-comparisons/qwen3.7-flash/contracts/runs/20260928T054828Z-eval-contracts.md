# Run report — `20260928T054828Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T054828Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 50 docs, seed 42 |
| timestamp | `2026-09-28T05:48:28+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T054828Z-eval-contracts/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:58:14+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T054828Z-eval-contracts', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:48:28+00:00` |
| finished_at | `2026-09-28T05:58:14+00:00` |
| duration_s (wall) | 588.3000 |
| latency_ms_mean | 83996.5 |
| latency_ms_p95 | 190489.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4625 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4625** (sd 0.2639, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 588.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0713** USD |
| cost estimated (roster token rates) | **0.0713** USD |
| cost per document (actual) | 0.0014 USD |
| cost per document (estimated) | 0.0014 USD |
| latency e2e / p50 / p95 / max | 588.3000 / 72.5931 / 190.4897 / 216.7892 s |
| prompt / completion / total tokens | 727681 / 380795 / 1108476 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 4199.8 s vs wall = 588.3 s -> wall/serial factor 7.14x at concurrency 8.

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
| `contracts_specialist` | 59 | 727681 | 380795 | 1108476 | 0.0713 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 4199.8 s over wall 588.3 s = **7.14×** effective parallelism at c8 (89% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` (Franchise) 216.8 s = 37% of wall — p95/p50 = 2.62×.
- **Prompt length vs latency:** Pearson r = 0.87 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 7616 tok/doc, mean prompt 14554 tok/doc.
- **Subclass spread:** best `Supply` 0.668 (n=2), worst `Development` 0.000 (n=1).
- **Field-level extraction:** 18/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Consulting Agreements | 6 | 0.6108 |
| Sponsorship | 5 | 0.6076 |
| Strategic Alliance | 5 | 0.6045 |
| Franchise | 4 | 0.4294 |
| Collaboration | 3 | 0.5225 |
| Distributor | 3 | 0.3913 |
| IP | 3 | 0.3466 |
| License_Agreements | 3 | 0.3920 |
| Maintenance | 3 | 0.3782 |
| Marketing | 3 | 0.3134 |
| Joint Venture _ Filing | 2 | 0.1111 |
| Supply | 2 | 0.6680 |
| Transportation | 2 | 0.2941 |
| Agency Agreements | 1 | 0.6250 |
| Development | 1 | 0.0000 |
| Endorsement | 1 | 0.3067 |
| Promotion | 1 | 0.5703 |
| Reseller | 1 | 0.6389 |
| Service | 1 | 0.3599 |
| **total** | **50** | **0.4625** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.3067 | 0.0000 | 54.0029 | 5971 | 4367 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5416 | 0.2500 | 70.5550 | 14319 | 7000 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.5926 | 0.2857 | 56.8724 | 6107 | 5194 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6429 | 0.2857 | 72.5931 | 15701 | 6525 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.5600 | 0.2857 | 151.9956 | 44725 | 13743 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.6818 | 0.2223 | 46.5286 | 4173 | 4423 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.5333 | 0.2223 | 64.1823 | 10858 | 5857 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5703 | 0.2223 | 149.2198 | 42711 | 14140 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3514 | 0.0000 | 44.4452 | 3558 | 3957 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2501 | 49.1501 | 3558 | 4224 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.0000 | 0.0000 | 135.5232 | 16452 | 11972 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.6406 | 0.2000 | 53.2946 | 6859 | 5084 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.5862 | 0.2500 | 72.0961 | 14195 | 7077 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.0000 | 0.0000 | 88.5836 | 5808 | 8190 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3514 | 0.0000 | 34.4665 | 2620 | 2875 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.0000 | 0.0000 | 216.7892 | 38996 | 21971 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.3688 | 0.0000 | 73.2271 | 9312 | 7224 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.7500 | 0.2000 | 50.5980 | 5081 | 4981 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5294 | 0.2857 | 148.4121 | 31083 | 13924 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.0000 | 0.0000 | 147.4158 | 17549 | 8192 | — |
| 21 | `corpus:ground_truth:train:MTITECHNOLOGYCORP_11_16_2004-EX-10.102-Reseller Agreement Premier Addendum.PDF` | Reseller | 0.6389 | 0.2223 | 74.4755 | 9307 | 6762 | — |
| 22 | `corpus:ground_truth:train:0001193125-14-242205_d623882dex1023.htm` | Supply | 1.0000 | 0.2222 | 72.6333 | 4177 | 7355 | — |
| 23 | `corpus:ground_truth:train:TELEGLOBEINTERNATIONALHOLDINGSLTD_03_29_2004-EX-10.10-CONSTRUCTION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.5484 | 0.2223 | 79.5487 | 22561 | 7212 | — |
| 24 | `corpus:ground_truth:train:ADUROBIOTECH,INC_06_02_2020-EX-10.7-CONSULTING AGREEMENT(1).PDF` | Consulting Agreements | 0.6562 | 0.2500 | 49.9048 | 4854 | 4549 | — |
| 25 | `corpus:ground_truth:train:0001564590-21-028164_ck7045120534-ex108_276.htm` | IP | 0.3369 | 0.0000 | 50.6643 | 13016 | 4328 | — |
| 26 | `corpus:ground_truth:train:DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.PDF` | Transportation | 0.0000 | 0.0000 | 161.9956 | 24404 | 16384 | — |
| 27 | `corpus:ground_truth:train:CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.PDF` | Sponsorship | 0.5357 | 0.2223 | 63.7013 | 4457 | 5897 | — |
| 28 | `corpus:ground_truth:train:SPHERE3DCORP_06_24_2020-EX-10.12-CONSULTING AGREEMENT.PDF` | Consulting Agreements | 0.5416 | 0.2223 | 75.4800 | 4875 | 6755 | — |
| 29 | `corpus:ground_truth:train:PRECIGEN,INC_01_22_2020-EX-99.1-JOINT FILING AGREEMENT.PDF` | Joint Venture _ Filing | 0.2222 | 0.0000 | 40.5933 | 2780 | 3428 | — |
| 30 | `corpus:ground_truth:train:XYBERNAUTCORP_07_12_2002-EX-4-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.5882 | 0.2500 | 73.8331 | 13128 | 7223 | — |
| 31 | `corpus:ground_truth:train:CcRealEstateIncomeFundadv_20181205_POS 8C_EX-99.(H)(3)_11447739_EX-99.(H)(3)_Marketing Agreement.pdf` | Marketing | 0.5715 | 0.2500 | 59.0064 | 8891 | 5175 | — |
| 32 | `corpus:ground_truth:train:GpaqAcquisitionHoldingsInc_20200123_S-4A_EX-10.8_11951679_EX-10.8_Service Agreement.pdf` | Service | 0.3599 | 0.0000 | 67.4974 | 14161 | 6742 | — |
| 33 | `corpus:ground_truth:train:0001213900-23-083790_ea187099ex10-23_perfect.htm` | Consulting Agreements | 1.0000 | 0.2858 | 59.7504 | 3545 | 5551 | — |
| 34 | `corpus:ground_truth:train:GAINSCOINC_01_21_2010-EX-10.41-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.5961 | 0.2223 | 69.4311 | 5803 | 6775 | — |
| 35 | `corpus:ground_truth:train:0001493152-17-012423_ex10-25.htm` | Consulting Agreements | 0.4672 | 0.0000 | 64.5130 | 4561 | 5106 | — |
| 36 | `corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018-EX-10.6-Franchise Agreement.PDF` | Franchise | 0.5722 | 0.2223 | 212.3789 | 74056 | 19544 | — |
| 37 | `corpus:ground_truth:train:XENCORINC_10_25_2013-EX-10.24-COLLABORATION AGREEMENT (3).PDF` | Collaboration | 0.5076 | 0.3333 | 190.4897 | 40105 | 11777 | — |
| 38 | `corpus:ground_truth:train:AudibleInc_20001113_10-Q_EX-10.32_2599586_EX-10.32_Co-Branding Agreement_ Marketing Agreement_ Investment Distribution Agreement.pdf` | Marketing | 0.0000 | 0.0000 | 79.3649 | 18546 | 8190 | — |
| 39 | `corpus:ground_truth:train:AIRTECHINTERNATIONALGROUPINC_05_08_2000-EX-10.4-FRANCHISE AGREEMENT.PDF` | Franchise | 0.5715 | 0.2223 | 79.3066 | 18200 | 8186 | — |
| 40 | `corpus:ground_truth:train:PHREESIA,INC_05_28_2019-EX-10.18-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5588 | 0.2000 | 110.7250 | 29904 | 9740 | — |
| 41 | `corpus:ground_truth:train:SUMMAFOURINC_06_19_1998-EX-10.3-SOFTWARE LICENSE AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.0000 | 0.0000 | 93.4693 | 24276 | 8190 | — |
| 42 | `corpus:ground_truth:train:0001213900-25-051717_ea024476901ex10-38_natures.htm` | Supply | 0.3359 | 0.0000 | 48.2686 | 6793 | 4333 | — |
| 43 | `corpus:ground_truth:train:SimplicityEsportsGamingCompany_20181130_8-K_EX-10.1_11444071_EX-10.1_Franchise Agreement.pdf` | Franchise | 0.5740 | 0.2500 | 80.2847 | 8635 | 7482 | — |
| 44 | `corpus:ground_truth:train:MARTINMIDSTREAMPARTNERSLP_01_23_2004-EX-10.3-TRANSPORTATION SERVICES AGREEMENT.PDF` | Transportation | 0.5882 | 0.2223 | 61.5654 | 5324 | 5440 | — |
| 45 | `corpus:ground_truth:train:RemarkHoldingsInc_20081114_10-Q_EX-10.24_2895649_EX-10.24_Content License Agreement.pdf` | License_Agreements | 0.0000 | 0.0000 | 84.6961 | 15648 | 8190 | — |
| 46 | `corpus:ground_truth:train:GSVINC_05_15_1998-EX-10-SPONSORSHIP AGREEMENT.PDF` | Sponsorship | 0.6363 | 0.2500 | 80.1249 | 10953 | 8089 | — |
| 47 | `corpus:ground_truth:train:SPIENERGYCO,LTD_07_10_2014-EX-10-Cooperation Agreement of 50MWp Photovoltaic Grid-connected Power Generation Project in Yangqiao of~1.PDF` | Collaboration | 0.5000 | 0.3333 | 38.2361 | 3025 | 3233 | — |
| 48 | `corpus:ground_truth:train:BANUESTRAFINANCIALCORP_09_08_2006-EX-10.16-AGENCY AGREEMENT.PDF` | Agency Agreements | 0.6250 | 0.2857 | 52.9843 | 11773 | 4349 | — |
| 49 | `corpus:ground_truth:train:0000950123-09-046709_y01981a3exv10w15.htm` | Consulting Agreements | 0.0000 | 0.0000 | 82.9115 | 9422 | 8190 | — |
| 50 | `corpus:ground_truth:train:GlobalTechnologiesGroupInc_20050928_10KSB_EX-10.9_4148808_EX-10.9_Content License Agreement.pdf` | License_Agreements | 0.5834 | 0.2000 | 62.0381 | 10865 | 5700 | — |

- scored rows: 50/50; min=0.0000 max=1.0000 mean=0.4625

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 50 --seed 42 --concurrency 8 --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260928T054828Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T054828Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T054828Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T054828Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T054828Z-eval-contracts.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/contracts/RUN-50-CONTRACT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
