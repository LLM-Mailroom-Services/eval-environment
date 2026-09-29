## 20260927T105317Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / None |
| trace backend | braintrust |
| git | commit: 7712588 · dirty: True |
| started / finished | 2026-09-27T10:53:17+00:00 → 2026-09-27T10:53:56+00:00 |
| duration_s | 40.3 |
| comparison report | reports/api-comparisons/deepseek-v4.1-flash/correspondence/… |
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
| case_ids | corpus:ground_truth:train:blair-l/meetings/608., corpus:gro… |
| class_counts | correspondence: 20 |
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
| subset_manifest_jsonl | data/experiments/20260927T105317Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T105317Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4419 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0121 |
| cost_usd_total | 0.0121 |
| latency_ms_mean | 7393.465 |
| latency_ms_p95 | 14399.5 |
| tokens_completion_total | 35712 |
| tokens_prompt_total | 48744 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 20 | 48744 | 35712 | 84456 | 0.0121 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.4013 · needs_judge_review: False · n_expec… | 4802 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.2179 · needs_judge_review: False · n_expec… | 8084.5 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.6731 · needs_judge_review: True · n_expect… | 14399.5 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 5832.5 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4582 · needs_judge_review: False · n_expec… | 10078.6 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.2502 · needs_judge_review: False · n_expec… | 9382.1 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 11872.2 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.7333 · needs_judge_review: True · n_expect… | 5375.6 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 1501.2 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.3068 · needs_judge_review: True · n_expect… | 9554.8 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.5625 · needs_judge_review: False · n_expec… | 3451 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.3368 · needs_judge_review: False · n_expec… | 944.1 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 6446.7 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.4959 · needs_judge_review: False · n_expec… | 8591.2 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.3066 · needs_judge_review: False · n_expec… | 5012.6 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.575 · needs_judge_review: False · n_expect… | 7674.5 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 1459.4 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.234 · needs_judge_review: False · n_expect… | 10531.9 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.4798 · needs_judge_review: True · n_expect… | 18720.2 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 4154.7 | — |
