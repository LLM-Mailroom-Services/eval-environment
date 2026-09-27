## 20260926T223151Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:51+00:00 → 2026-09-26T22:31:52+00:00 |
| duration_s | 1.3 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 403 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:corporate_record |
| subset_manifest_jsonl | data/experiments/20260926T223151Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260926T223151Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

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
| latency_ms_mean | 34.15 |
| latency_ms_p95 | 51.8 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 51.8 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | overall_score: 0.0 · needs_judge_review: False · n_expected… | 16.5 | — |
