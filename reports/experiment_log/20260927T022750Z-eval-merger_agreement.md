## 20260927T022750Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:27:50+00:00 → 2026-09-27T02:30:10+00:00 |
| duration_s | 142 |
| comparison report | reports/api-comparisons/qwen3-8b/merger_agreement/runs/2026… |
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
| cost_usd_est | 0.0575 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
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
| subset_manifest_jsonl | data/experiments/20260927T022750Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T022750Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.3748 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0575 |
| cost_usd_total | 0.0575 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 45286.88 |
| latency_ms_p95 | 52445.4 |
| tokens_completion_total | 114281 |
| tokens_prompt_total | 1422210 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 18 | 1422210 | 114281 | 1536491 | 0.0575 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.2633 · needs_judge_review: False · n_expec… | 47418.8 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.2986 · needs_judge_review: False · n_expec… | 37790.1 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 40572.7 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.1751 · needs_judge_review: False · n_expec… | 37713.3 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 46588.4 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.2927 · needs_judge_review: False · n_expec… | 47017.2 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 46987.2 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.6945 · needs_judge_review: False · n_expec… | 51732.2 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.2201 · needs_judge_review: False · n_expec… | 46723.5 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1441 · needs_judge_review: False · n_expec… | 48939.5 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.5584 · needs_judge_review: True · n_expect… | 52445.4 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: True · n_expected_… | 46754.6 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 40362.2 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 54764.6 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.1873 · needs_judge_review: False · n_expec… | 41083 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 43248.3 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.2755 · needs_judge_review: False · n_expec… | 45097.6 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 39142.3 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.2377 · needs_judge_review: False · n_expec… | 46538 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.575 · needs_judge_review: False · n_expect… | 44818.7 | — |
