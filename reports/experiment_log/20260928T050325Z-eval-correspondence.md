## 20260928T050325Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / correspondence_specialist_v2 |
| trace backend | braintrust |
| git | commit: eddaccb · dirty: True |
| started / finished | 2026-09-28T05:03:25+00:00 → 2026-09-28T05:05:30+00:00 |
| duration_s | 125.1 |
| comparison report | reports/api-comparisons/qwen3.7-flash/correspondence/runs/2… |
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
| subset_manifest_jsonl | data/experiments/20260928T050325Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260928T050325Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.5104 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0089 |
| cost_usd_total | 0.0089 |
| latency_ms_mean | 35887.87 |
| latency_ms_p95 | 55219.8 |
| tokens_completion_total | 57329 |
| tokens_prompt_total | 49919 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 20 | 49919 | 57329 | 107248 | 0.0089 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.3513 · needs_judge_review: False · n_expec… | 34326.2 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 37560.3 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.4118 · needs_judge_review: False · n_expec… | 35517.6 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 26773.3 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4475 · needs_judge_review: False · n_expec… | 32887.5 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.278 · needs_judge_review: False · n_expect… | 35439 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 31499.7 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.6833 · needs_judge_review: True · n_expect… | 32109.6 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.3322 · needs_judge_review: False · n_expec… | 19948.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 87786.9 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.6125 · needs_judge_review: False · n_expec… | 36481.2 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 21017.8 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 40343.3 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.6572 · needs_judge_review: False · n_expec… | 37235.9 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.6654 · needs_judge_review: False · n_expec… | 55219.8 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.575 · needs_judge_review: False · n_expect… | 29792.6 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 25688.2 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 38394 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.4465 · needs_judge_review: False · n_expec… | 32942.4 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 26793.6 | — |
