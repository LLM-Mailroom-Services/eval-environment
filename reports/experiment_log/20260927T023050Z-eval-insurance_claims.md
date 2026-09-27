## 20260927T023050Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:30:50+00:00 → 2026-09-27T02:33:44+00:00 |
| duration_s | 175.6 |
| comparison report | /workspace/reports/api-comparisons/qwen3-8b/RUN-20-INSURANC… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
| decode_budget_applied | sampling_injected: False · max_tokens_by_agent: {'contracts… |
| decode_call_timeout_s | 600 |
| decode_profile | qwen3-8b |
| decode_sampling | — |
| dry_run | ✗ |
| n | — |
| resumed_from | — |
| sample | 20 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Cost cap

| Key | Value |
|---|---|
| cap_usd | 1.5 |
| cost_usd_est | 0.0192 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:pde:233384494245864.txt, corpus:g… |
| config | ground_truth |
| filenames | pde:233384494245864.txt, insurbias-624.txt, carrier:8874733… |
| n_selected | 20 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260927T023050Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260927T023050Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.202 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0192 |
| cost_usd_total | 0.0192 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 34087.465 |
| latency_ms_p95 | 155975.6 |
| tokens_completion_total | 31824 |
| tokens_prompt_total | 40696 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 40696 | 31824 | 72520 | 0.0192 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14192.7 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8428 · needs_judge_review: False · n_expec… | 27512 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 11072 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15367.8 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 155975.6 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.7034 · needs_judge_review: True · n_expect… | 21359.7 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 15778.7 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14478.1 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 9325.9 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 158081.2 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 8805.9 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8424 · needs_judge_review: False · n_expec… | 15052.8 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8182 · needs_judge_review: False · n_expec… | 17154.5 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 8780.8 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15097.6 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 11298.6 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18761 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 6566.8 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 126405.9 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 10681.7 | — |
