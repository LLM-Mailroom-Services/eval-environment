## 20260928T085148Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / contracts_specialist_v3 |
| trace backend | braintrust |
| git | commit: eabeab5 · dirty: True |
| started / finished | 2026-09-28T08:51:48+00:00 → 2026-09-28T08:54:15+00:00 |
| duration_s | 148.3 |
| comparison report | reports/api-comparisons/deepseek-v4.1-flash/contracts/runs/… |
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
| sample | 20 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… |
| class_counts | contract: 20 |
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
| subset_manifest_jsonl | data/experiments/20260928T085148Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260928T085148Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.6219 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0456 |
| cost_usd_total | 0.0456 |
| latency_ms_mean | 29340.05 |
| latency_ms_p95 | 62363.3 |
| tokens_completion_total | 121079 |
| tokens_prompt_total | 300981 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 22 | 300981 | 121079 | 422060 | 0.0456 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.8334 · needs_judge_review: True · n_expect… | 22533.4 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.6805 · needs_judge_review: False · n_expec… | 17973.3 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.6852 · needs_judge_review: False · n_expec… | 14898.6 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.7857 · needs_judge_review: True · n_expect… | 27762.4 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.6134 · needs_judge_review: False · n_expec… | 10844.4 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.8637 · needs_judge_review: True · n_expect… | 18389.8 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.7 · needs_judge_review: False · n_expected… | 23556.8 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.5703 · needs_judge_review: False · n_expec… | 33943.9 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 0.3515 · needs_judge_review: False · n_expec… | 15353.4 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 14080.7 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 100235 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.6562 · needs_judge_review: False · n_expec… | 62363.3 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.7069 · needs_judge_review: False · n_expec… | 16036.8 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.6956 · needs_judge_review: False · n_expec… | 58351.2 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.3515 · needs_judge_review: False · n_expec… | 6458.1 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.5476 · needs_judge_review: False · n_expec… | 52819.3 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.3365 · needs_judge_review: False · n_expec… | 18581.4 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.7916 · needs_judge_review: True · n_expect… | 13709.3 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.6618 · needs_judge_review: False · n_expec… | 15940.5 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.6071 · needs_judge_review: False · n_expec… | 42969.4 | — |
