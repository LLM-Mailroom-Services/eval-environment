## 20260927T014814Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: 4b25a4e · dirty: True |
| started / finished | 2026-09-27T01:48:14+00:00 → 2026-09-27T01:56:35+00:00 |
| duration_s | 503 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
| config | ground_truth |
| filenames | contract_128_merger_agreement.txt, contract_31_merger_agree… |
| n_selected | 2 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 2 |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260927T014814Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T014814Z-eval-merger_agreement/sub… |
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
| cost_usd_est_total | 0.0259 |
| latency_ms_mean | 249440.15 |
| latency_ms_p95 | 253967.8 |
| tokens_completion_total | 16390 |
| tokens_prompt_total | 157754 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 2 | 157754 | 16390 | 174144 | 0.0259 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 253967.8 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 244912.5 | — |
