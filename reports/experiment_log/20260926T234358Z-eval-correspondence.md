## 20260926T234358Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fe120a8 · dirty: True |
| started / finished | 2026-09-26T23:43:58+00:00 → 2026-09-26T23:46:00+00:00 |
| duration_s | 123.4 |
| comparison report | reports/api-comparisons/qwen3-8b/correspondence/runs/202609… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 1 |
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
| cost_usd_est | 0.0077 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:blair-l/meetings/608., corpus:gro… |
| config | ground_truth |
| filenames | blair-l/meetings/608., lokey-t/inbox/250., kean-s/all_docum… |
| n_selected | 20 |
| n_total | 915 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:correspondence |
| subset_manifest_jsonl | data/experiments/20260926T234358Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260926T234358Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.3179 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0077 |
| cost_usd_total | 0.0077 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 3861.845 |
| latency_ms_p95 | 5505.8 |
| tokens_completion_total | 3197 |
| tokens_prompt_total | 53521 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 20 | 53521 | 3197 | 56718 | 0.0077 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.4058 · needs_judge_review: True · n_expect… | 3953.3 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.3857 · needs_judge_review: False · n_expec… | 3065.9 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.3269 · needs_judge_review: False · n_expec… | 5018 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.2789 · needs_judge_review: False · n_expec… | 3020.5 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4409 · needs_judge_review: False · n_expec… | 4114.6 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.2607 · needs_judge_review: False · n_expec… | 4915.6 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.3244 · needs_judge_review: False · n_expec… | 4357.5 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.5552 · needs_judge_review: True · n_expect… | 3938.2 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.1109 · needs_judge_review: False · n_expec… | 2214.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.1947 · needs_judge_review: False · n_expec… | 3407.5 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.1872 · needs_judge_review: False · n_expec… | 3819.6 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.3143 · needs_judge_review: False · n_expec… | 2544.6 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.3558 · needs_judge_review: True · n_expect… | 3638.3 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.5783 · needs_judge_review: True · n_expect… | 4548.2 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.3464 · needs_judge_review: True · n_expect… | 5505.8 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.3909 · needs_judge_review: False · n_expec… | 3360.8 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.1109 · needs_judge_review: False · n_expec… | 2531 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.1683 · needs_judge_review: False · n_expec… | 6838.4 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.4465 · needs_judge_review: False · n_expec… | 3502.1 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.1752 · needs_judge_review: False · n_expec… | 2942.5 | — |
