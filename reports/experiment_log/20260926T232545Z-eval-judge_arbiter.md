## 20260926T232545Z-eval-judge_arbiter

| Key | Value |
|---|---|
| family / task | eval / judge_arbiter |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:45+00:00 → 2026-09-26T23:25:45+00:00 |
| duration_s | 0.6 |
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
| scorer | judge |
| seed | 42 |
| skipped_already_run | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T232545Z-eval-judge_arbiter/subset… |
| subset_manifest_path | data/experiments/20260926T232545Z-eval-judge_arbiter/subset… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| judge_agrees | 0.5 |
| judge_score | 1 |
| n | 2 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0 |
| cost_usd_total | 0 |
| latency_ms_mean | 0.95 |
| latency_ms_p95 | 1.4 |
| tokens_completion_total | 130 |
| tokens_prompt_total | 250 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 2 | 240 | 120 | 360 | 0 | qwen/qwen3.7-flash |
| judge | 1 | 10 | 10 | 20 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | judge_label: complete · judge_score: 1.0 · judge_agrees: 0 | 1.4 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | judge_label: skipped · judge_score: None · judge_agrees: 1 | 0.5 | — |
