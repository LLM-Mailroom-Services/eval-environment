## 20260928T080542Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 6c4ac14 · dirty: True |
| started / finished | 2026-09-28T08:05:43+00:00 → 2026-09-28T08:08:19+00:00 |
| duration_s | 158.2 |
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
| subset_manifest_jsonl | data/experiments/20260928T080542Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T080542Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4065 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0646 |
| cost_usd_total | 0.0646 |
| latency_ms_mean | 50590.865 |
| latency_ms_p95 | 97363 |
| tokens_completion_total | 125255 |
| tokens_prompt_total | 1610639 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 20 | 1610639 | 125255 | 1735894 | 0.0646 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.3222 · needs_judge_review: False · n_expec… | 97363 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.4057 · needs_judge_review: True · n_expect… | 58993.9 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 38462.3 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.2046 · needs_judge_review: False · n_expec… | 47278.3 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 46188.6 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.2928 · needs_judge_review: False · n_expec… | 43433.4 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 43820.1 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.6389 · needs_judge_review: False · n_expec… | 43943.5 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.1867 · needs_judge_review: False · n_expec… | 50825.2 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1441 · needs_judge_review: False · n_expec… | 34902.8 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 98267.7 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.4722 · needs_judge_review: True · n_expect… | 43827.3 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 51542.4 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 46799 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.1873 · needs_judge_review: False · n_expec… | 36702.5 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 39203.1 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.1873 · needs_judge_review: False · n_expec… | 45282.8 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 45627.5 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.1789 · needs_judge_review: False · n_expec… | 42111.5 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.575 · needs_judge_review: False · n_expect… | 57242.4 | — |
