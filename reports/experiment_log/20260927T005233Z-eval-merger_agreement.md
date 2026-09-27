## 20260927T005233Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / merger_agreement_specialist_v1 |
| trace backend | braintrust |
| git | commit: 533b371 · dirty: True |
| started / finished | 2026-09-27T00:52:33+00:00 → 2026-09-27T01:09:03+00:00 |
| duration_s | 900 |
| comparison report | — |
| error | Interrupted 3/20: unchunked ~350k-char merger text truncate… |

### Run configuration

| Param | Value |
|---|---|
| decode_profile | qwen3-8b |
| sample | 20 |
| seed | 42 |

### Dataset

| Key | Value |
|---|---|
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| subset | class:merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 1 |
| n | 3 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0392 |
| cost_usd_total | 0.0392 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 247912.7333 |
| latency_ms_p95 | 289547.9 |
| tokens_completion_total | 24585 |
| tokens_prompt_total | 239586 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 3 | 239586 | 24585 | 264171 | 0.0392 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 234100.5 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt |  | 220089.8 | ValueError: Exceeds the limit (4300 digits) for integer str… |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 289547.9 | — |
