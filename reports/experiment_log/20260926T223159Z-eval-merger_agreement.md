## 20260926T223159Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:59+00:00 → 2026-09-26T22:32:00+00:00 |
| duration_s | 1.4 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_0_merger_agreement.txt, … |
| config | ground_truth |
| filenames | contract_0_merger_agreement.txt, contract_100_merger_agreem… |
| n_selected | 2 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260926T223159Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260926T223159Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

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
| cost_usd_est_total | 0.0001 |
| latency_ms_mean | 49.8 |
| latency_ms_p95 | 75.4 |
| tokens_completion_total | 540 |
| tokens_prompt_total | 1080 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 9 | 1080 | 540 | 1620 | 0.0001 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_0_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 75.4 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 24.2 | — |
