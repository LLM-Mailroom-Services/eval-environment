## 20260926T232540Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:40+00:00 → 2026-09-26T23:25:41+00:00 |
| duration_s | 1.4 |
| comparison report | — |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 1 |
| dry_run | ✗ |
| n | 2 |
| resumed_from | — |
| sample | — |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:allen-p/deleted_items/65., corpus… |
| config | ground_truth |
| filenames | allen-p/deleted_items/65., arnold-j/deleted_items/395. |
| n_selected | 2 |
| n_total | 915 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:correspondence |
| subset_manifest_jsonl | data/experiments/20260926T232540Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260926T232540Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| cost_usd_total | — |
| latency_ms_mean | 48.95 |
| latency_ms_p95 | 79.7 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:allen-p/deleted_items/65. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 79.7 | — |
| corpus:ground_truth:train:arnold-j/deleted_items/395. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18.2 | — |
