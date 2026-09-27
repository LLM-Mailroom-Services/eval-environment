## 20260927T011209Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / merger_agreement_specialist_v1 |
| trace backend | braintrust |
| git | commit: f75ccd9 · dirty: True |
| started / finished | 2026-09-27T01:12:09+00:00 → 2026-09-27T01:25:51+00:00 |
| duration_s | 780 |
| error | Interrupted 1/20: 8 chunks still returned unparseable JSON … |

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
| cost_usd_est_total | 0.0221 |
| latency_ms_mean | 669067.9 |
| latency_ms_p95 | 669067.9 |
| tokens_completion_total | 22641 |
| tokens_prompt_total | 100682 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 8 | 100682 | 22641 | 123323 | 0.0221 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 669067.9 | — |
