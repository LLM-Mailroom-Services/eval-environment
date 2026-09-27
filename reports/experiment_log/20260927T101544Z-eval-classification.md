## 20260927T101544Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / real |
| model / prompt | deepseek/deepseek-v4.1-flash / None |
| trace backend | braintrust |
| git | commit: 53a9d88 · dirty: True |
| started / finished | 2026-09-27T10:45:45+00:00 → 2026-09-27T10:46:33+00:00 |
| duration_s | 4.8 |
| comparison report | reports/api-comparisons/deepseek-deepseek-v4.1-flash/classi… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 1 |
| decode_budget_applied | sampling_injected: False · max_tokens_by_agent: {} |
| decode_profile | — |
| dry_run | ✗ |
| n | — |
| resumed_from | — |
| sample | 100 |
| scorer | classification |
| seed | 42 |
| skipped_already_run | 99 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:property:261501663.txt, corpus:gr… |
| config | ground_truth |
| filenames | property:261501663.txt, inpatient:196841176990879:1.txt, in… |
| n_selected | 100 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 100 |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260927T101544Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260927T101544Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.95 |
| errors | 0 |
| n | 100 |
| scorer_errors | 0 |
| subclass_accuracy | 0.64 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1001 |
| cost_usd_total | 0.1001 |
| latency_ms_mean | 6666.522 |
| latency_ms_p95 | 31993.5 |
| tokens_completion_total | 51008 |
| tokens_prompt_total | 2437786 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 329 | 2437786 | 51008 | 2488794 | 0.1001 | deepseek/deepseek-v4.1-flash |
