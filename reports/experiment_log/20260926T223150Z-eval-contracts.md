## 20260926T223150Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:50+00:00 → 2026-09-26T22:31:51+00:00 |
| duration_s | 1.5 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 2 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T223150Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T223150Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

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
| cost_usd_est_total | 0 |
| latency_ms_mean | 38.95 |
| latency_ms_p95 | 63.1 |
| tokens_completion_total | 120 |
| tokens_prompt_total | 240 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 2 | 240 | 120 | 360 | 0 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 63.1 | — |
| corpus:ground_truth:train:ABILITYINC_06_15_2020-EX-4.25-SER… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14.8 | — |
