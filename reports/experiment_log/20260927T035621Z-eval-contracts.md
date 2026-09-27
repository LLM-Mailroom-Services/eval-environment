## 20260927T035621Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: a3506e2 · dirty: True |
| started / finished | 2026-09-27T03:56:21+00:00 → 2026-09-27T04:20:36+00:00 |
| duration_s | 1457.5 |
| error | — |

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
| subset_manifest_jsonl | data/experiments/20260927T035621Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260927T035621Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.6169 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1141 |
| latency_ms_mean | 177560.88 |
| latency_ms_p95 | 285038.9 |
| tokens_completion_total | 110286 |
| tokens_prompt_total | 546225 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 44 | 546225 | 110286 | 656511 | 0.1141 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 139282.9 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.5139 · needs_judge_review: False · n_expec… | 85425.3 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.6482 · needs_judge_review: False · n_expec… | 53308.3 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.6429 · needs_judge_review: False · n_expec… | 110936.1 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.54 · needs_judge_review: False · n_expecte… | 200409 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.6363 · needs_judge_review: False · n_expec… | 76406.3 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 138952.9 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.5234 · needs_judge_review: False · n_expec… | 201456 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 51326 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 53575.2 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.5757 · needs_judge_review: False · n_expec… | 175812.5 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.5469 · needs_judge_review: False · n_expec… | 139284.8 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.5689 · needs_judge_review: False · n_expec… | 82921 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.5652 · needs_judge_review: False · n_expec… | 74188.2 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 72778.6 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.6012 · needs_judge_review: False · n_expec… | 211723.7 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.5806 · needs_judge_review: False · n_expec… | 1244619.2 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.75 · needs_judge_review: True · n_expected… | 48101.4 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.5736 · needs_judge_review: False · n_expec… | 285038.9 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.5535 · needs_judge_review: False · n_expec… | 105671.3 | — |
