## 20260927T053647Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: 1d9f8d2 · dirty: True |
| started / finished | 2026-09-27T05:36:47+00:00 → 2026-09-27T05:41:17+00:00 |
| duration_s | 272.3 |
| comparison report | reports/api-comparisons/granite-4.2-8b/correspondence/runs/… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
| decode_budget_applied | sampling_injected: True · max_tokens_by_agent: {'contracts_… |
| decode_call_timeout_s | 600 |
| decode_profile | granite-4.2-8b |
| decode_sampling | temperature: 1.0 · top_p: 0.95 · seed: 42 |
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
| cost_usd_est | 0.0292 |
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
| subset_manifest_jsonl | data/experiments/20260927T053647Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T053647Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

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
| cost_usd_est_total | 0.0292 |
| cost_usd_total | 0.0292 |
| expected_cost_usd | 0.8 |
| latency_ms_mean | 76726.235 |
| latency_ms_p95 | 146506.5 |
| tokens_completion_total | 104315 |
| tokens_prompt_total | 51943 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 20 | 51943 | 104315 | 156258 | 0.0292 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.3513 · needs_judge_review: False · n_expec… | 60276.6 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 104109.3 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.5769 · needs_judge_review: False · n_expec… | 59383.5 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.419 · needs_judge_review: False · n_expect… | 87643.7 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 840.7 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 2548.2 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 98034.9 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.7 · needs_judge_review: True · n_expected_… | 89946.4 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 38935.3 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 135225.2 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.5625 · needs_judge_review: False · n_expec… | 98063.8 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 36895.5 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 79899.5 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.3887 · needs_judge_review: False · n_expec… | 124658.4 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.3259 · needs_judge_review: False · n_expec… | 146506.5 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 115562.4 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 577.3 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.6833 · needs_judge_review: False · n_expec… | 165931.6 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.452 · needs_judge_review: False · n_expect… | 2013.1 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 87472.8 | — |
