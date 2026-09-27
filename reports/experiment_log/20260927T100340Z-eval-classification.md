## 20260927T100340Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: 53a9d88 · dirty: True |
| started / finished | 2026-09-27T10:03:40+00:00 → 2026-09-27T10:08:33+00:00 |
| duration_s | 294.8 |
| comparison report | reports/api-comparisons/granite-4.2-8b/classification/runs/… |
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
| sample | 100 |
| scorer | classification |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Cost cap

| Key | Value |
|---|---|
| cap_usd | 1.5 |
| cost_usd_est | 0.1506 |
| cost_usd_total | 0.1506 |
| status | under_cap |

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
| subset_manifest_jsonl | data/experiments/20260927T100340Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260927T100340Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.94 |
| errors | 0 |
| n | 100 |
| scorer_errors | 0 |
| subclass_accuracy | 0.49 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1506 |
| cost_usd_total | 0.1506 |
| expected_cost_usd | 4 |
| latency_ms_mean | 14845.835 |
| latency_ms_p95 | 75382.4 |
| tokens_completion_total | 74141 |
| tokens_prompt_total | 2201847 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 291 | 2201847 | 74141 | 2275988 | 0.1506 | ibm-granite/granite-4.2-8b |
