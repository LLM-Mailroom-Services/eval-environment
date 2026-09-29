## 20260928T101150Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 5b7bc5a · dirty: False |
| started / finished | 2026-09-28T10:11:50+00:00 → 2026-09-28T10:11:51+00:00 |
| duration_s | 3.4 |
| comparison report | — |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 1 |
| decode_budget_applied | sampling_injected: False · max_tokens_by_agent: {} |
| decode_profile | — |
| dry_run | ✗ |
| n | 3 |
| resumed_from | — |
| sample | — |
| scorer | classification |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| class_counts | corporate_record: 3 |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 3 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | /tmp/claude-501/-Users-luciusjmorningstar-Downloads-local-m… |
| subset_manifest_path | /tmp/claude-501/-Users-luciusjmorningstar-Downloads-local-m… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 3 |
| scorer_errors | 0 |
| subclass_accuracy | 0.0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0001 |
| cost_usd_total | 0.0001 |
| latency_ms_mean | 52.6667 |
| latency_ms_p95 | 144.3 |
| tokens_completion_total | 420 |
| tokens_prompt_total | 840 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 7 | 840 | 420 | 1260 | 0.0001 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | predicted_doc_class: contract · expected_doc_class: corpora… | 144.3 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | predicted_doc_class: contract · expected_doc_class: corpora… | 7.5 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | predicted_doc_class: contract · expected_doc_class: corpora… | 6.2 | — |
