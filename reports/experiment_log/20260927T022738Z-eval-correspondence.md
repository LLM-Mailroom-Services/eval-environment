## 20260927T022738Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:27:38+00:00 → 2026-09-27T02:30:47+00:00 |
| duration_s | 191 |
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
| cost_usd_est | 0.0287 |
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
| subset_manifest_jsonl | data/experiments/20260927T022738Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T022738Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0287 |
| cost_usd_total | 0.0287 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 56321.215 |
| latency_ms_p95 | 133521.6 |
| tokens_completion_total | 50672 |
| tokens_prompt_total | 48452 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 20 | 48452 | 50672 | 99124 | 0.0287 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15188 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 13655.3 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15726.7 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 98922.4 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 19837.6 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 16800 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18517.7 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 92858.7 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14052.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 123945.1 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 25086.7 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 11648.6 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 99540.6 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 147604.4 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 50105.2 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 118640.7 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 12548.1 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 133521.6 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15670 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 82554.4 | — |
