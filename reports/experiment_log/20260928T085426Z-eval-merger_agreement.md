## 20260928T085426Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / merger_agreement_specialist_… |
| trace backend | braintrust |
| git | commit: eabeab5 · dirty: True |
| started / finished | 2026-09-28T08:54:26+00:00 → 2026-09-28T08:58:11+00:00 |
| duration_s | 225.6 |
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
| sample | 20 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
| class_counts | merger_agreement: 20 |
| config | ground_truth |
| filenames | contract_128_merger_agreement.txt, contract_31_merger_agree… |
| n_selected | 20 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260928T085426Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T085426Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4284 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1448 |
| cost_usd_total | 0.1448 |
| latency_ms_mean | 55767.625 |
| latency_ms_p95 | 130738.9 |
| tokens_completion_total | 213524 |
| tokens_prompt_total | 2367475 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 29 | 2367475 | 213524 | 2580999 | 0.1448 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.1751 · needs_judge_review: False · n_expec… | 51336.1 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.62 · needs_judge_review: False · n_expecte… | 78390.1 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 92713.7 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.2927 · needs_judge_review: False · n_expec… | 45590.5 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 82104 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.3516 · needs_judge_review: False · n_expec… | 49939 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 130738.9 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 45155.7 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.3867 · needs_judge_review: True · n_expect… | 25457.7 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 25656.9 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.6583 · needs_judge_review: True · n_expect… | 156197.9 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5834 · needs_judge_review: True · n_expect… | 55371.9 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.7222 · needs_judge_review: False · n_expec… | 28448.1 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 22361.2 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.3049 · needs_judge_review: False · n_expec… | 75291.3 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 16120.2 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.599 · needs_judge_review: False · n_expect… | 27227.5 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.7188 · needs_judge_review: False · n_expec… | 35506.6 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 42321.9 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.95 · needs_judge_review: False · n_expecte… | 29423.3 | — |
