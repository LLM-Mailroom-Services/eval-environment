## 20260928T055822Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / contracts_specialist_v2 |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T05:58:22+00:00 → 2026-09-28T06:09:11+00:00 |
| duration_s | 651.2 |
| comparison report | reports/api-comparisons/qwen3.7-flash/contracts/runs/202609… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
| decode_budget_applied | sampling_injected: False · max_tokens_by_agent: {} |
| decode_profile | — |
| dry_run | ✗ |
| n | — |
| resumed_from | — |
| sample | 50 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… |
| class_counts | contract: 50 |
| config | ground_truth |
| filenames | MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PD… |
| n_selected | 50 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 50 |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260928T055822Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260928T055822Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5277 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.07 |
| cost_usd_total | 0.07 |
| latency_ms_mean | 89440.694 |
| latency_ms_p95 | 218906 |
| tokens_completion_total | 368531 |
| tokens_prompt_total | 736712 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 60 | 736712 | 368531 | 1105243 | 0.07 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.3623 · needs_judge_review: False · n_expec… | 86548.7 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.625 · needs_judge_review: False · n_expect… | 136387.3 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.6297 · needs_judge_review: False · n_expec… | 61202.8 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.6785 · needs_judge_review: False · n_expec… | 63053.7 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.5466 · needs_judge_review: False · n_expec… | 116650.9 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.6818 · needs_judge_review: False · n_expec… | 74861.4 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.5444 · needs_judge_review: False · n_expec… | 62558.5 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.5469 · needs_judge_review: False · n_expec… | 124302.6 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 44090.1 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 39915.4 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.5606 · needs_judge_review: False · n_expec… | 76156.1 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 91658.6 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.6035 · needs_judge_review: False · n_expec… | 61760.4 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.5869 · needs_judge_review: False · n_expec… | 76116.5 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 41640 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.5535 · needs_judge_review: False · n_expec… | 157906.5 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.272 · needs_judge_review: False · n_expect… | 82366.3 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.7916 · needs_judge_review: True · n_expect… | 78397.8 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.6764 · needs_judge_review: False · n_expec… | 229018.9 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.6429 · needs_judge_review: False · n_expec… | 58871.7 | — |
| corpus:ground_truth:train:MTITECHNOLOGYCORP_11_16_2004-EX-1… | overall_score: 0.75 · needs_judge_review: True · n_expected… | 81583 | — |
| corpus:ground_truth:train:0001193125-14-242205_d623882dex10… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 46018.6 | — |
| corpus:ground_truth:train:TELEGLOBEINTERNATIONALHOLDINGSLTD… | overall_score: 0.5484 · needs_judge_review: False · n_expec… | 73585.6 | — |
| corpus:ground_truth:train:ADUROBIOTECH,INC_06_02_2020-EX-10… | overall_score: 0.6875 · needs_judge_review: False · n_expec… | 58172.4 | — |
| corpus:ground_truth:train:0001564590-21-028164_ck7045120534… | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 58893.3 | — |
| corpus:ground_truth:train:DYNAMEXINC_06_06_1996-EX-10.4-TRA… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 127741.2 | — |
| corpus:ground_truth:train:CANOPETROLEUM,INC_12_13_2007-EX-1… | overall_score: 0.75 · needs_judge_review: True · n_expected… | 67276.4 | — |
| corpus:ground_truth:train:SPHERE3DCORP_06_24_2020-EX-10.12-… | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 76453.5 | — |
| corpus:ground_truth:train:PRECIGEN,INC_01_22_2020-EX-99.1-J… | overall_score: 0.3472 · needs_judge_review: False · n_expec… | 36194.6 | — |
| corpus:ground_truth:train:XYBERNAUTCORP_07_12_2002-EX-4-SPO… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 92128 | — |
| corpus:ground_truth:train:CcRealEstateIncomeFundadv_2018120… | overall_score: 0.6429 · needs_judge_review: False · n_expec… | 61561.6 | — |
| corpus:ground_truth:train:GpaqAcquisitionHoldingsInc_202001… | overall_score: 0.3956 · needs_judge_review: False · n_expec… | 159833.2 | — |
| corpus:ground_truth:train:0001213900-23-083790_ea187099ex10… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 62517.7 | — |
| corpus:ground_truth:train:GAINSCOINC_01_21_2010-EX-10.41-SP… | overall_score: 0.7116 · needs_judge_review: False · n_expec… | 174032.8 | — |
| corpus:ground_truth:train:0001493152-17-012423_ex10-25.htm | overall_score: 0.2667 · needs_judge_review: False · n_expec… | 48962.4 | — |
| corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018… | overall_score: 0.5928 · needs_judge_review: False · n_expec… | 284287.8 | — |
| corpus:ground_truth:train:XENCORINC_10_25_2013-EX-10.24-COL… | overall_score: 0.5454 · needs_judge_review: False · n_expec… | 108629.2 | — |
| corpus:ground_truth:train:AudibleInc_20001113_10-Q_EX-10.32… | overall_score: 0.3204 · needs_judge_review: False · n_expec… | 92717.1 | — |
| corpus:ground_truth:train:AIRTECHINTERNATIONALGROUPINC_05_0… | overall_score: 0.6429 · needs_judge_review: False · n_expec… | 80806.9 | — |
| corpus:ground_truth:train:PHREESIA,INC_05_28_2019-EX-10.18-… | overall_score: 0.5294 · needs_judge_review: False · n_expec… | 218906 | — |
| corpus:ground_truth:train:SUMMAFOURINC_06_19_1998-EX-10.3-S… | overall_score: 0.2878 · needs_judge_review: False · n_expec… | 76470.8 | — |
| corpus:ground_truth:train:0001213900-25-051717_ea024476901e… | overall_score: 0.3359 · needs_judge_review: False · n_expec… | 49865.1 | — |
| corpus:ground_truth:train:SimplicityEsportsGamingCompany_20… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 86895.8 | — |
| corpus:ground_truth:train:MARTINMIDSTREAMPARTNERSLP_01_23_2… | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 95870.2 | — |
| corpus:ground_truth:train:RemarkHoldingsInc_20081114_10-Q_E… | overall_score: 0.5463 · needs_judge_review: False · n_expec… | 74896.5 | — |
| corpus:ground_truth:train:GSVINC_05_15_1998-EX-10-SPONSORSH… | overall_score: 0.6363 · needs_judge_review: False · n_expec… | 85749.1 | — |
| corpus:ground_truth:train:SPIENERGYCO,LTD_07_10_2014-EX-10-… | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 46655.8 | — |
| corpus:ground_truth:train:BANUESTRAFINANCIALCORP_09_08_2006… | overall_score: 0.625 · needs_judge_review: False · n_expect… | 46459.8 | — |
| corpus:ground_truth:train:0000950123-09-046709_y01981a3exv1… | overall_score: 0.2667 · needs_judge_review: False · n_expec… | 68397 | — |
| corpus:ground_truth:train:GlobalTechnologiesGroupInc_200509… | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 67009.1 | — |
