## 20260927T004231Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: 5bdab8d · dirty: True |
| started / finished | 2026-09-27T00:42:31+00:00 → 2026-09-27T00:52:00+00:00 |
| duration_s | 420 |
| error | Interrupted after 1/20: completion budget 8192 truncated me… |

### Dataset

| Key | Value |
|---|---|
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| subset | class:merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0132 |
| latency_ms_mean | 268266.4 |
| latency_ms_p95 | 268266.4 |
| tokens_completion_total | 8195 |
| tokens_prompt_total | 81257 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 1 | 81257 | 8195 | 89452 | 0.0132 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 268266.4 | — |
