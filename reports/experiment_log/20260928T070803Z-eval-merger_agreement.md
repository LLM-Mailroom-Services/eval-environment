## 20260928T070803Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / merger_agreement_specialist_v3 |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T07:08:03+00:00 → 2026-09-28T07:16:10+00:00 |
| duration_s | 488 |
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
| subset_manifest_jsonl | data/experiments/20260928T070803Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T070803Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5213 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1611 |
| cost_usd_total | 0.1611 |
| latency_ms_mean | 55019.966 |
| latency_ms_p95 | 99717 |
| tokens_completion_total | 347846 |
| tokens_prompt_total | 3864179 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 53 | 3864179 | 347846 | 4212025 | 0.1611 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.2339 · needs_judge_review: False · n_expec… | 46136.2 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.3343 · needs_judge_review: False · n_expec… | 53056.3 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 61472.7 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.2045 · needs_judge_review: False · n_expec… | 53492.3 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.6471 · needs_judge_review: False · n_expec… | 54832.2 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.2633 · needs_judge_review: False · n_expec… | 60531.9 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 60657.1 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.6389 · needs_judge_review: False · n_expec… | 42515.9 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.3201 · needs_judge_review: False · n_expec… | 48219.9 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1718 · needs_judge_review: False · n_expec… | 54596.7 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.625 · needs_judge_review: True · n_expecte… | 53709.5 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5278 · needs_judge_review: True · n_expect… | 46328.3 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 43615.4 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 57026.1 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.1873 · needs_judge_review: False · n_expec… | 47536.4 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 44363.5 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.1578 · needs_judge_review: False · n_expec… | 50456.6 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.625 · needs_judge_review: False · n_expect… | 47015.2 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.326 · needs_judge_review: False · n_expect… | 47561 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 51058.8 | — |
| corpus:ground_truth:train:contract_126_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 48999.1 | — |
| corpus:ground_truth:train:contract_75_merger_agreement.txt | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 42278.4 | — |
| corpus:ground_truth:train:contract_112_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 47482.8 | — |
| corpus:ground_truth:train:contract_141_merger_agreement.txt | overall_score: 0.2591 · needs_judge_review: False · n_expec… | 53639.9 | — |
| corpus:ground_truth:train:contract_73_merger_agreement.txt | overall_score: 0.2755 · needs_judge_review: False · n_expec… | 93681.1 | — |
| corpus:ground_truth:train:contract_1_merger_agreement.txt | overall_score: 0.8611 · needs_judge_review: True · n_expect… | 76586.3 | — |
| corpus:ground_truth:train:contract_144_merger_agreement.txt | overall_score: 0.6875 · needs_judge_review: False · n_expec… | 44923.9 | — |
| corpus:ground_truth:train:contract_134_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 62648.6 | — |
| corpus:ground_truth:train:contract_78_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 47722.7 | — |
| corpus:ground_truth:train:contract_17_merger_agreement.txt | overall_score: 0.2965 · needs_judge_review: False · n_expec… | 57076.9 | — |
| corpus:ground_truth:train:contract_137_merger_agreement.txt | overall_score: 0.7333 · needs_judge_review: False · n_expec… | 40149.8 | — |
| corpus:ground_truth:train:contract_54_merger_agreement.txt | overall_score: 0.6562 · needs_judge_review: False · n_expec… | 54898 | — |
| corpus:ground_truth:train:contract_3_merger_agreement.txt | overall_score: 0.6764 · needs_judge_review: False · n_expec… | 52723.2 | — |
| corpus:ground_truth:train:contract_2_merger_agreement.txt | overall_score: 0.2657 · needs_judge_review: False · n_expec… | 46351.7 | — |
| corpus:ground_truth:train:contract_23_merger_agreement.txt | overall_score: 0.7778 · needs_judge_review: True · n_expect… | 51036.2 | — |
| corpus:ground_truth:train:contract_57_merger_agreement.txt | overall_score: 0.7812 · needs_judge_review: True · n_expect… | 99717 | — |
| corpus:ground_truth:train:contract_81_merger_agreement.txt | overall_score: 0.7308 · needs_judge_review: False · n_expec… | 105954.4 | — |
| corpus:ground_truth:train:contract_24_merger_agreement.txt | overall_score: 0.7 · needs_judge_review: False · n_expected… | 52087.3 | — |
| corpus:ground_truth:train:contract_101_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 43984.8 | — |
| corpus:ground_truth:train:contract_28_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 57037.6 | — |
| corpus:ground_truth:train:contract_83_merger_agreement.txt | overall_score: 0.7941 · needs_judge_review: True · n_expect… | 50556.1 | — |
| corpus:ground_truth:train:contract_85_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 48049.2 | — |
| corpus:ground_truth:train:contract_119_merger_agreement.txt | overall_score: 0.2633 · needs_judge_review: False · n_expec… | 44891.2 | — |
| corpus:ground_truth:train:contract_35_merger_agreement.txt | overall_score: 0.625 · needs_judge_review: False · n_expect… | 54861 | — |
| corpus:ground_truth:train:contract_77_merger_agreement.txt | overall_score: 0.1873 · needs_judge_review: False · n_expec… | 48062.5 | — |
| corpus:ground_truth:train:contract_27_merger_agreement.txt | overall_score: 0.7 · needs_judge_review: False · n_expected… | 110787.8 | — |
| corpus:ground_truth:train:contract_43_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 54312.6 | — |
| corpus:ground_truth:train:contract_47_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 48753.3 | — |
| corpus:ground_truth:train:contract_20_merger_agreement.txt | overall_score: 0.1303 · needs_judge_review: False · n_expec… | 50664.7 | — |
| corpus:ground_truth:train:contract_7_merger_agreement.txt | overall_score: 0.335 · needs_judge_review: False · n_expect… | 36898.2 | — |
