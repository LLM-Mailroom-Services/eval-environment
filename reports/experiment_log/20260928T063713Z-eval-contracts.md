## 20260928T063713Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / contracts_specialist_v3 |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T06:37:13+00:00 → 2026-09-28T06:48:42+00:00 |
| duration_s | 690.2 |
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
| subset_manifest_jsonl | data/experiments/20260928T063713Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260928T063713Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5462 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0739 |
| cost_usd_total | 0.0739 |
| latency_ms_mean | 95005.57 |
| latency_ms_p95 | 202765.2 |
| tokens_completion_total | 387157 |
| tokens_prompt_total | 786252 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 61 | 786252 | 387157 | 1173409 | 0.0739 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 73580.4 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 79081.5 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.5926 · needs_judge_review: False · n_expec… | 64904 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.5357 · needs_judge_review: False · n_expec… | 56810.1 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.5734 · needs_judge_review: False · n_expec… | 170549.3 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.6818 · needs_judge_review: False · n_expec… | 65214.3 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.5444 · needs_judge_review: False · n_expec… | 79782.9 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.5625 · needs_judge_review: False · n_expec… | 194005.8 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 71024.1 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 46531.9 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.5606 · needs_judge_review: False · n_expec… | 66148.9 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 79059.3 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.5862 · needs_judge_review: False · n_expec… | 68969.8 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.6087 · needs_judge_review: False · n_expec… | 78901.6 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 42202 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 157209.2 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.2881 · needs_judge_review: False · n_expec… | 73175.2 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.75 · needs_judge_review: True · n_expected… | 157603.2 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.6618 · needs_judge_review: False · n_expec… | 231469.3 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.5715 · needs_judge_review: False · n_expec… | 86222.3 | — |
| corpus:ground_truth:train:MTITECHNOLOGYCORP_11_16_2004-EX-1… | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 77916.6 | — |
| corpus:ground_truth:train:0001193125-14-242205_d623882dex10… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 63083.7 | — |
| corpus:ground_truth:train:TELEGLOBEINTERNATIONALHOLDINGSLTD… | overall_score: 0.5484 · needs_judge_review: False · n_expec… | 146461.4 | — |
| corpus:ground_truth:train:ADUROBIOTECH,INC_06_02_2020-EX-10… | overall_score: 0.75 · needs_judge_review: True · n_expected… | 72662.7 | — |
| corpus:ground_truth:train:0001564590-21-028164_ck7045120534… | overall_score: 0.3369 · needs_judge_review: False · n_expec… | 63879.5 | — |
| corpus:ground_truth:train:DYNAMEXINC_06_06_1996-EX-10.4-TRA… | overall_score: 0.5454 · needs_judge_review: False · n_expec… | 84013.5 | — |
| corpus:ground_truth:train:CANOPETROLEUM,INC_12_13_2007-EX-1… | overall_score: 0.6429 · needs_judge_review: False · n_expec… | 62771.2 | — |
| corpus:ground_truth:train:SPHERE3DCORP_06_24_2020-EX-10.12-… | overall_score: 0.75 · needs_judge_review: True · n_expected… | 70678.2 | — |
| corpus:ground_truth:train:PRECIGEN,INC_01_22_2020-EX-99.1-J… | overall_score: 0.5 · needs_judge_review: False · n_expected… | 91572.3 | — |
| corpus:ground_truth:train:XYBERNAUTCORP_07_12_2002-EX-4-SPO… | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 78408.5 | — |
| corpus:ground_truth:train:CcRealEstateIncomeFundadv_2018120… | overall_score: 0.5715 · needs_judge_review: False · n_expec… | 64510.5 | — |
| corpus:ground_truth:train:GpaqAcquisitionHoldingsInc_202001… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 102642.4 | — |
| corpus:ground_truth:train:0001213900-23-083790_ea187099ex10… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 47676.1 | — |
| corpus:ground_truth:train:GAINSCOINC_01_21_2010-EX-10.41-SP… | overall_score: 0.5192 · needs_judge_review: False · n_expec… | 63664.3 | — |
| corpus:ground_truth:train:0001493152-17-012423_ex10-25.htm | overall_score: 0.2667 · needs_judge_review: False · n_expec… | 60743.8 | — |
| corpus:ground_truth:train:GOOSEHEADINSURANCE,INC_04_02_2018… | overall_score: 0.567 · needs_judge_review: False · n_expect… | 279891 | — |
| corpus:ground_truth:train:XENCORINC_10_25_2013-EX-10.24-COL… | overall_score: 0.5 · needs_judge_review: False · n_expected… | 202765.2 | — |
| corpus:ground_truth:train:AudibleInc_20001113_10-Q_EX-10.32… | overall_score: 0.2992 · needs_judge_review: False · n_expec… | 71062.5 | — |
| corpus:ground_truth:train:AIRTECHINTERNATIONALGROUPINC_05_0… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 84582.5 | — |
| corpus:ground_truth:train:PHREESIA,INC_05_28_2019-EX-10.18-… | overall_score: 0.6275 · needs_judge_review: False · n_expec… | 197950.3 | — |
| corpus:ground_truth:train:SUMMAFOURINC_06_19_1998-EX-10.3-S… | overall_score: 0.2731 · needs_judge_review: False · n_expec… | 89459.2 | — |
| corpus:ground_truth:train:0001213900-25-051717_ea024476901e… | overall_score: 0.3359 · needs_judge_review: False · n_expec… | 61058.1 | — |
| corpus:ground_truth:train:SimplicityEsportsGamingCompany_20… | overall_score: 0.6482 · needs_judge_review: False · n_expec… | 73136.7 | — |
| corpus:ground_truth:train:MARTINMIDSTREAMPARTNERSLP_01_23_2… | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 76788.7 | — |
| corpus:ground_truth:train:RemarkHoldingsInc_20081114_10-Q_E… | overall_score: 0.5926 · needs_judge_review: False · n_expec… | 141348.1 | — |
| corpus:ground_truth:train:GSVINC_05_15_1998-EX-10-SPONSORSH… | overall_score: 0.6363 · needs_judge_review: False · n_expec… | 67003.5 | — |
| corpus:ground_truth:train:SPIENERGYCO,LTD_07_10_2014-EX-10-… | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 49515.6 | — |
| corpus:ground_truth:train:BANUESTRAFINANCIALCORP_09_08_2006… | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 58859.3 | — |
| corpus:ground_truth:train:0000950123-09-046709_y01981a3exv1… | overall_score: 0.2667 · needs_judge_review: False · n_expec… | 123788 | — |
| corpus:ground_truth:train:GlobalTechnologiesGroupInc_200509… | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 79940 | — |
