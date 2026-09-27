## 20260926T232610Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:26:10+00:00 → 2026-09-26T23:26:32+00:00 |
| duration_s | 24 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 1 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T232610Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T232610Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.7167 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0005 |
| latency_ms_mean | 13026.6 |
| latency_ms_p95 | 13026.6 |
| tokens_completion_total | 1405 |
| tokens_prompt_total | 10825 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 1 | 10825 | 1405 | 12230 | 0.0005 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… | overall_score: 0.7167 · needs_judge_review: False · n_expec… | 13026.6 | — |
