## 20260927T051725Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / mock |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | none |
| git | commit: 5b9d25b · dirty: True |
| started / finished | 2026-09-27T05:17:25+00:00 → 2026-09-27T05:17:26+00:00 |
| duration_s | 2.5 |
| comparison report | reports/api-comparisons/granite-4.2-8b/correspondence/RUN-1… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 1 |
| decode_budget_applied | sampling_injected: True · max_tokens_by_agent: {'contracts_… |
| decode_call_timeout_s | 600 |
| decode_profile | granite-4.2-8b |
| decode_sampling | temperature: 1.0 · top_p: 0.95 · seed: 42 |
| dry_run | ✗ |
| n | 1 |
| resumed_from | — |
| sample | — |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Cost cap

| Key | Value |
|---|---|
| cap_usd | 1.5 |
| cost_usd_est | 0 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:allen-p/deleted_items/65. |
| config | ground_truth |
| filenames | allen-p/deleted_items/65. |
| n_selected | 1 |
| n_total | 915 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:correspondence |
| subset_manifest_jsonl | data/experiments/20260927T051725Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T051725Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0 |
| cost_usd_total | 0 |
| expected_cost_usd | 0.04 |
| latency_ms_mean | 0.8 |
| latency_ms_p95 | 0.8 |
| tokens_completion_total | 10 |
| tokens_prompt_total | 10 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 1 | 10 | 10 | 20 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:allen-p/deleted_items/65. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 0.8 | — |
