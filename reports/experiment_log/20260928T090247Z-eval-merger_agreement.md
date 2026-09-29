## 20260928T090247Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / None |
| trace backend | braintrust |
| git | commit: 9d993e0 · dirty: True |
| started / finished | 2026-09-28T09:02:47+00:00 → 2026-09-28T09:07:57+00:00 |
| duration_s | 312.6 |
| comparison report | reports/api-comparisons/deepseek-v4.1-flash/merger_agreemen… |
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
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
| class_counts | merger_agreement: 50 |
| config | ground_truth |
| filenames | contract_128_merger_agreement.txt, contract_31_merger_agree… |
| n_selected | 50 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 50 |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260928T090247Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T090247Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.6294 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.2462 |
| cost_usd_total | 0.2462 |
| latency_ms_mean | 35142.574 |
| latency_ms_p95 | 68731.2 |
| tokens_completion_total | 355317 |
| tokens_prompt_total | 4090925 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 55 | 4090925 | 355317 | 4446242 | 0.2462 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.3516 · needs_judge_review: False · n_expec… | 26060.2 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.4415 · needs_judge_review: True · n_expect… | 24311.5 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.7333 · needs_judge_review: False · n_expec… | 25281.1 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.3222 · needs_judge_review: False · n_expec… | 34684.1 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.7941 · needs_judge_review: True · n_expect… | 31888.7 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 127602.7 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 62508.1 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 35775.1 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.42 · needs_judge_review: True · n_expected… | 27042.3 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.3108 · needs_judge_review: False · n_expec… | 22664 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.925 · needs_judge_review: True · n_expecte… | 17469 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5834 · needs_judge_review: True · n_expect… | 29414.9 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 1.0 · needs_judge_review: False · n_expected… | 17975.3 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 27816.1 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.5991 · needs_judge_review: False · n_expec… | 30864.6 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 21736.1 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.3344 · needs_judge_review: False · n_expec… | 25662.7 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 13346.1 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.5907 · needs_judge_review: False · n_expec… | 23774.4 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.7 · needs_judge_review: False · n_expected… | 68731.2 | — |
| corpus:ground_truth:train:contract_126_merger_agreement.txt | overall_score: 1.0 · needs_judge_review: False · n_expected… | 31339.8 | — |
| corpus:ground_truth:train:contract_75_merger_agreement.txt | overall_score: 0.7222 · needs_judge_review: False · n_expec… | 38463.2 | — |
| corpus:ground_truth:train:contract_112_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 28300.7 | — |
| corpus:ground_truth:train:contract_141_merger_agreement.txt | overall_score: 0.3306 · needs_judge_review: False · n_expec… | 21618.6 | — |
| corpus:ground_truth:train:contract_73_merger_agreement.txt | overall_score: 0.5991 · needs_judge_review: False · n_expec… | 53309.7 | — |
| corpus:ground_truth:train:contract_1_merger_agreement.txt | overall_score: 0.7778 · needs_judge_review: True · n_expect… | 17015.1 | — |
| corpus:ground_truth:train:contract_144_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 29192.6 | — |
| corpus:ground_truth:train:contract_134_merger_agreement.txt | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 23036.5 | — |
| corpus:ground_truth:train:contract_78_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 30238.5 | — |
| corpus:ground_truth:train:contract_17_merger_agreement.txt | overall_score: 0.62 · needs_judge_review: False · n_expecte… | 24796.3 | — |
| corpus:ground_truth:train:contract_137_merger_agreement.txt | overall_score: 0.9667 · needs_judge_review: False · n_expec… | 29419 | — |
| corpus:ground_truth:train:contract_54_merger_agreement.txt | overall_score: 1.0 · needs_judge_review: False · n_expected… | 28963.9 | — |
| corpus:ground_truth:train:contract_3_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 43828 | — |
| corpus:ground_truth:train:contract_2_merger_agreement.txt | overall_score: 0.8 · needs_judge_review: True · n_expected_… | 34861.9 | — |
| corpus:ground_truth:train:contract_23_merger_agreement.txt | overall_score: 0.7222 · needs_judge_review: False · n_expec… | 21896.6 | — |
| corpus:ground_truth:train:contract_57_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 28035.3 | — |
| corpus:ground_truth:train:contract_81_merger_agreement.txt | overall_score: 0.9231 · needs_judge_review: True · n_expect… | 52812 | — |
| corpus:ground_truth:train:contract_24_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 29432.1 | — |
| corpus:ground_truth:train:contract_101_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 57369 | — |
| corpus:ground_truth:train:contract_28_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 38106.3 | — |
| corpus:ground_truth:train:contract_83_merger_agreement.txt | overall_score: 1.0 · needs_judge_review: False · n_expected… | 78302.6 | — |
| corpus:ground_truth:train:contract_85_merger_agreement.txt | overall_score: 0.9706 · needs_judge_review: False · n_expec… | 32442.5 | — |
| corpus:ground_truth:train:contract_119_merger_agreement.txt | overall_score: 0.3516 · needs_judge_review: False · n_expec… | 42030.5 | — |
| corpus:ground_truth:train:contract_35_merger_agreement.txt | overall_score: 0.95 · needs_judge_review: False · n_expecte… | 24762.2 | — |
| corpus:ground_truth:train:contract_77_merger_agreement.txt | overall_score: 0.3638 · needs_judge_review: True · n_expect… | 47620.4 | — |
| corpus:ground_truth:train:contract_27_merger_agreement.txt | overall_score: 0.7333 · needs_judge_review: False · n_expec… | 18882.7 | — |
| corpus:ground_truth:train:contract_43_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 38149.1 | — |
| corpus:ground_truth:train:contract_47_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 35379.1 | — |
| corpus:ground_truth:train:contract_20_merger_agreement.txt | overall_score: 0.2866 · needs_judge_review: False · n_expec… | 28446.1 | — |
| corpus:ground_truth:train:contract_7_merger_agreement.txt | overall_score: 0.585 · needs_judge_review: False · n_expect… | 54470.2 | — |
