## 20260926T223149Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:49+00:00 → 2026-09-26T22:31:49+00:00 |
| duration_s | 3.1 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260926T223149Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260926T223149Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |
| subclass_accuracy | 0.0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0001 |
| latency_ms_mean | 33.45 |
| latency_ms_p95 | 52.2 |
| tokens_completion_total | 360 |
| tokens_prompt_total | 720 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 6 | 720 | 360 | 1080 | 0.0001 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | predicted_doc_class: contract · expected_doc_class: corpora… | 52.2 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | predicted_doc_class: contract · expected_doc_class: corpora… | 14.7 | — |
