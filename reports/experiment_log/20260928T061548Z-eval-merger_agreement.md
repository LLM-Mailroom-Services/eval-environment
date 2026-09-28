## 20260928T061548Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / merger_agreement_specialist_v2 |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T06:15:48+00:00 → 2026-09-28T06:22:43+00:00 |
| duration_s | 416.2 |
| comparison report | reports/api-comparisons/qwen3.7-flash/merger_agreement/runs… |
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
| subset_manifest_jsonl | data/experiments/20260928T061548Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T061548Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.4909 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1603 |
| cost_usd_total | 0.1603 |
| latency_ms_mean | 57687.106 |
| latency_ms_p95 | 95775.9 |
| tokens_completion_total | 341008 |
| tokens_prompt_total | 3864191 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 53 | 3864191 | 341008 | 4205199 | 0.1603 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.2633 · needs_judge_review: False · n_expec… | 52603.8 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.2986 · needs_judge_review: False · n_expec… | 50450.5 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 54664.3 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.1751 · needs_judge_review: False · n_expec… | 48610.3 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 46799.4 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.2045 · needs_judge_review: False · n_expec… | 45620.6 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 49683.1 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.7222 · needs_judge_review: False · n_expec… | 52548.1 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.1867 · needs_judge_review: False · n_expec… | 44188.3 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1718 · needs_judge_review: False · n_expec… | 54234.6 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.525 · needs_judge_review: True · n_expecte… | 55751.5 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5555 · needs_judge_review: True · n_expect… | 40335.6 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 48484 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 60865.3 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.1578 · needs_judge_review: False · n_expec… | 47746.7 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 49838 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.1578 · needs_judge_review: False · n_expec… | 44217.5 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.625 · needs_judge_review: False · n_expect… | 46394.5 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.1494 · needs_judge_review: False · n_expec… | 60028.3 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.575 · needs_judge_review: False · n_expect… | 48562.5 | — |
| corpus:ground_truth:train:contract_126_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 54248.1 | — |
| corpus:ground_truth:train:contract_75_merger_agreement.txt | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 46153.8 | — |
| corpus:ground_truth:train:contract_112_merger_agreement.txt | overall_score: 0.6562 · needs_judge_review: False · n_expec… | 39853.7 | — |
| corpus:ground_truth:train:contract_141_merger_agreement.txt | overall_score: 0.3306 · needs_judge_review: False · n_expec… | 90058.3 | — |
| corpus:ground_truth:train:contract_73_merger_agreement.txt | overall_score: 0.1578 · needs_judge_review: False · n_expec… | 82741.5 | — |
| corpus:ground_truth:train:contract_1_merger_agreement.txt | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 50544.9 | — |
| corpus:ground_truth:train:contract_144_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 91727.4 | — |
| corpus:ground_truth:train:contract_134_merger_agreement.txt | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 50590.7 | — |
| corpus:ground_truth:train:contract_78_merger_agreement.txt | overall_score: 0.6471 · needs_judge_review: False · n_expec… | 53736.7 | — |
| corpus:ground_truth:train:contract_17_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 64979.6 | — |
| corpus:ground_truth:train:contract_137_merger_agreement.txt | overall_score: 0.7 · needs_judge_review: False · n_expected… | 62427.1 | — |
| corpus:ground_truth:train:contract_54_merger_agreement.txt | overall_score: 0.6875 · needs_judge_review: False · n_expec… | 57662.1 | — |
| corpus:ground_truth:train:contract_3_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 54733.7 | — |
| corpus:ground_truth:train:contract_2_merger_agreement.txt | overall_score: 0.7333 · needs_judge_review: False · n_expec… | 110869.5 | — |
| corpus:ground_truth:train:contract_23_merger_agreement.txt | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 57189.8 | — |
| corpus:ground_truth:train:contract_57_merger_agreement.txt | overall_score: 0.2865 · needs_judge_review: False · n_expec… | 60513.6 | — |
| corpus:ground_truth:train:contract_81_merger_agreement.txt | overall_score: 0.6539 · needs_judge_review: False · n_expec… | 95775.9 | — |
| corpus:ground_truth:train:contract_24_merger_agreement.txt | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 54324.9 | — |
| corpus:ground_truth:train:contract_101_merger_agreement.txt | overall_score: 0.6471 · needs_judge_review: False · n_expec… | 45625.1 | — |
| corpus:ground_truth:train:contract_28_merger_agreement.txt | overall_score: 0.8823 · needs_judge_review: True · n_expect… | 85232 | — |
| corpus:ground_truth:train:contract_83_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 40068.9 | — |
| corpus:ground_truth:train:contract_85_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 50852.3 | — |
| corpus:ground_truth:train:contract_119_merger_agreement.txt | overall_score: 0.3221 · needs_judge_review: False · n_expec… | 48431.7 | — |
| corpus:ground_truth:train:contract_35_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 51723.5 | — |
| corpus:ground_truth:train:contract_77_merger_agreement.txt | overall_score: 0.1578 · needs_judge_review: False · n_expec… | 58741.9 | — |
| corpus:ground_truth:train:contract_27_merger_agreement.txt | overall_score: 0.5666 · needs_judge_review: False · n_expec… | 110709.9 | — |
| corpus:ground_truth:train:contract_43_merger_agreement.txt | overall_score: 0.5294 · needs_judge_review: False · n_expec… | 51707 | — |
| corpus:ground_truth:train:contract_47_merger_agreement.txt | overall_score: 0.6945 · needs_judge_review: False · n_expec… | 49125.6 | — |
| corpus:ground_truth:train:contract_20_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 67515.5 | — |
| corpus:ground_truth:train:contract_7_merger_agreement.txt | overall_score: 0.2725 · needs_judge_review: False · n_expec… | 44863.7 | — |
