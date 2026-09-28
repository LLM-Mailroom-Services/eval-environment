## 20260928T054828Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T05:48:28+00:00 → 2026-09-28T05:58:14+00:00 |
| duration_s | 588.3 |
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
| subset_manifest_jsonl | data/experiments/20260928T054828Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260928T054828Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.4625 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0713 |
| cost_usd_total | 0.0713 |
| latency_ms_mean | 83996.47 |
| latency_ms_p95 | 190489.7 |
| tokens_completion_total | 380795 |
| tokens_prompt_total | 727681 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 59 | 727681 | 380795 | 1108476 | 0.0713 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.3067 · needs_judge_review: False · n_expec… | 54002.9 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.5416 · needs_judge_review: False · n_expec… | 70555 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.5926 · needs_judge_review: False · n_expec… | 56872.4 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.6429 · needs_judge_review: False · n_expec… | 72593.1 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.56 · needs_judge_review: False · n_expecte… | 151995.6 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.6818 · needs_judge_review: False · n_expec… | 46528.6 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.5333 · needs_judge_review: False · n_expec… | 64182.3 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.5703 · needs_judge_review: False · n_expec… | 149219.8 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 44445.2 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 49150.1 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 135523.2 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.6406 · needs_judge_review: False · n_expec… | 53294.6 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.5862 · needs_judge_review: False · n_expec… | 72096.1 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 88583.6 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 34466.5 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 216789.2 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.3688 · needs_judge_review: False · n_expec… | 73227.1 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.75 · needs_judge_review: True · n_expected… | 50598 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.5294 · needs_judge_review: False · n_expec… | 148412.1 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 147415.8 | — |
| corpus:ground_truth:train:MTITECHNOLOGYCORP_11_16_2004-EX-1… | overall_score: 0.6389 · needs_judge_review: False · n_expec… | 74475.5 | — |
| corpus:ground_truth:train:0001193125-14-242205_d623882dex10… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 72633.3 | — |
| corpus:ground_truth:train:TELEGLOBEINTERNATIONALHOLDINGSLTD… | overall_score: 0.5484 · needs_judge_review: False · n_expec… | 79548.7 | — |
| corpus:ground_truth:train:ADUROBIOTECH,INC_06_02_2020-EX-10… | overall_score: 0.6562 · needs_judge_review: False · n_expec… | 49904.8 | — |
| corpus:ground_truth:train:0001564590-21-028164_ck7045120534… | overall_score: 0.3369 · needs_judge_review: False · n_expec… | 50664.3 | — |
| corpus:ground_truth:train:DYNAMEXINC_06_06_1996-EX-10.4-TRA… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 161995.6 | — |
| corpus:ground_truth:train:CANOPETROLEUM,INC_12_13_2007-EX-1… | overall_score: 0.5357 · needs_judge_review: False · n_expec… | 63701.3 | — |
| corpus:ground_truth:train:SPHERE3DCORP_06_24_2020-EX-10.12-… | overall_score: 0.5416 · needs_judge_review: False · n_expec… | 75480 | — |
| corpus:ground_truth:train:PRECIGEN,INC_01_22_2020-EX-99.1-J… | overall_score: 0.2222 · needs_judge_review: False · n_expec… | 40593.3 | — |
| corpus:ground_truth:train:XYBERNAUTCORP_07_12_2002-EX-4-SPO… | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 73833.1 | — |
| corpus:ground_truth:train:CcRealEstateIncomeFundadv_2018120… | overall_score: 0.5715 · needs_judge_review: False · n_expec… | 59006.4 | — |
| corpus:ground_truth:train:GpaqAcquisitionHoldingsInc_202001… | overall_score: 0.3599 · needs_judge_review: False · n_expec… | 67497.4 | — |
| corpus:ground_truth:train:0001213900-23-083790_ea187099ex10… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 59750.4 | — |
| corpus:ground_truth:train:GAINSCOINC_01_21_2010-EX-10.41-SP… | overall_score: 0.5961 · needs_judge_review: False · n_expec… | 69431.1 | — |
| corpus:ground_truth:train:0001493152-17-012423_ex10-25.htm | overall_score: 0.4672 · needs_judge_review: False · n_expec… | 64513 | — |
| corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018… | overall_score: 0.5722 · needs_judge_review: False · n_expec… | 212378.9 | — |
| corpus:ground_truth:train:XENCORINC_10_25_2013-EX-10.24-COL… | overall_score: 0.5076 · needs_judge_review: False · n_expec… | 190489.7 | — |
| corpus:ground_truth:train:AudibleInc_20001113_10-Q_EX-10.32… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 79364.9 | — |
| corpus:ground_truth:train:AIRTECHINTERNATIONALGROUPINC_05_0… | overall_score: 0.5715 · needs_judge_review: False · n_expec… | 79306.6 | — |
| corpus:ground_truth:train:PHREESIA,INC_05_28_2019-EX-10.18-… | overall_score: 0.5588 · needs_judge_review: False · n_expec… | 110725 | — |
| corpus:ground_truth:train:SUMMAFOURINC_06_19_1998-EX-10.3-S… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 93469.3 | — |
| corpus:ground_truth:train:0001213900-25-051717_ea024476901e… | overall_score: 0.3359 · needs_judge_review: False · n_expec… | 48268.6 | — |
| corpus:ground_truth:train:SimplicityEsportsGamingCompany_20… | overall_score: 0.574 · needs_judge_review: False · n_expect… | 80284.7 | — |
| corpus:ground_truth:train:MARTINMIDSTREAMPARTNERSLP_01_23_2… | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 61565.4 | — |
| corpus:ground_truth:train:RemarkHoldingsInc_20081114_10-Q_E… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 84696.1 | — |
| corpus:ground_truth:train:GSVINC_05_15_1998-EX-10-SPONSORSH… | overall_score: 0.6363 · needs_judge_review: False · n_expec… | 80124.9 | — |
| corpus:ground_truth:train:SPIENERGYCO,LTD_07_10_2014-EX-10-… | overall_score: 0.5 · needs_judge_review: False · n_expected… | 38236.1 | — |
| corpus:ground_truth:train:BANUESTRAFINANCIALCORP_09_08_2006… | overall_score: 0.625 · needs_judge_review: False · n_expect… | 52984.3 | — |
| corpus:ground_truth:train:0000950123-09-046709_y01981a3exv1… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 82911.5 | — |
| corpus:ground_truth:train:GlobalTechnologiesGroupInc_200509… | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 62038.1 | — |
