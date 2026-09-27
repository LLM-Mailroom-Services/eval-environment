## 20260927T051729Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / mock |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | none |
| git | commit: 5b9d25b · dirty: True |
| started / finished | 2026-09-27T05:17:29+00:00 → 2026-09-27T05:17:29+00:00 |
| duration_s | 2.8 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm |
| n_selected | 1 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260927T051729Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260927T051729Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 1 |
| scorer_errors | 0 |
| subclass_accuracy | 0.0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0001 |
| latency_ms_mean | 171.7 |
| latency_ms_p95 | 171.7 |
| tokens_completion_total | 180 |
| tokens_prompt_total | 360 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 3 | 360 | 180 | 540 | 0.0001 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | predicted_doc_class: contract · expected_doc_class: corpora… | 171.7 | — |
