## 20260927T023347Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:33:47+00:00 → 2026-09-27T02:40:49+00:00 |
| duration_s | 424.4 |
| comparison report | /workspace/reports/api-comparisons/qwen3-8b/RUN-20-CONTRACT… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
| decode_budget_applied | sampling_injected: False · max_tokens_by_agent: {'contracts… |
| decode_call_timeout_s | 600 |
| decode_profile | qwen3-8b |
| decode_sampling | — |
| dry_run | ✗ |
| n | — |
| resumed_from | — |
| sample | 20 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Cost cap

| Key | Value |
|---|---|
| cap_usd | 1.5 |
| cost_usd_est | 0.0498 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… |
| config | ground_truth |
| filenames | MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PD… |
| n_selected | 20 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260927T023347Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260927T023347Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.0762 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0498 |
| cost_usd_total | 0.0498 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 108632.14 |
| latency_ms_p95 | 365572.6 |
| tokens_completion_total | 48066 |
| tokens_prompt_total | 238475 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 21 | 238475 | 48066 | 286541 | 0.0498 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 41025.8 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 38844.1 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 365572.6 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 25336.3 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 72349.4 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 21737.4 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 266975 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 260779.7 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 30970.1 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 395455.6 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 61586.8 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 89018.8 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 17135.9 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 26165.1 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18878.5 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.5238 · needs_judge_review: False · n_expec… | 73212.6 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15677.4 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 8563.3 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 195448.8 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 147909.6 | — |
