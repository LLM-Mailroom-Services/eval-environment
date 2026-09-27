## 20260927T033031Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: 4b973b7 · dirty: True |
| started / finished | 2026-09-27T03:30:31+00:00 → 2026-09-27T03:50:59+00:00 |
| duration_s | 1230.1 |
| comparison report | /workspace/reports/api-comparisons/qwen3-8b/RUN-20-CORRESPO… |
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
| cost_usd_est | 0.0604 |
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
| subset_manifest_jsonl | data/experiments/20260927T033031Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T033031Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.513 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0604 |
| cost_usd_total | 0.0604 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 128861.32 |
| latency_ms_p95 | 150933.7 |
| tokens_completion_total | 110287 |
| tokens_prompt_total | 87002 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 39 | 87002 | 110287 | 197289 | 0.0604 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.4013 · needs_judge_review: False · n_expec… | 99043.5 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 128665.8 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.5577 · needs_judge_review: False · n_expec… | 39379.1 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.419 · needs_judge_review: False · n_expect… | 106303.8 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4354 · needs_judge_review: False · n_expec… | 150933.7 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 134271 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 55458.9 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.7 · needs_judge_review: True · n_expected_… | 48333.9 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 23353.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 32837.6 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.3566 · needs_judge_review: False · n_expec… | 136725.8 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 44942.1 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 108990.5 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.6572 · needs_judge_review: False · n_expec… | 49599.1 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.4496 · needs_judge_review: False · n_expec… | 69641.2 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.6 · needs_judge_review: False · n_expected… | 84155 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 28686.4 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 1086942.8 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 47420.2 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 101542.5 | — |
