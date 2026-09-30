## 20260926T223154Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:54+00:00 → 2026-09-26T22:31:56+00:00 |
| duration_s | 2.5 |
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
| case_ids | corpus:ground_truth:train:carrier:887013387879564.txt, corp… |
| config | ground_truth |
| filenames | carrier:887013387879564.txt, carrier:887023387120037.txt |
| n_selected | 2 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260926T223154Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260926T223154Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.697 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| cost_usd_total | — |
| latency_ms_mean | 40 |
| latency_ms_p95 | 54.6 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:carrier:887013387879564.txt | overall_score: 0.697 · needs_judge_review: True · n_expecte… | 54.6 | — |
| corpus:ground_truth:train:carrier:887023387120037.txt | overall_score: 0.697 · needs_judge_review: True · n_expecte… | 25.4 | — |
