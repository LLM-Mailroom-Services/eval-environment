## 20260926T234603Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fe120a8 · dirty: True |
| started / finished | 2026-09-26T23:46:03+00:00 → 2026-09-26T23:49:16+00:00 |
| duration_s | 195 |
| comparison report | reports/api-comparisons/qwen3-8b/insurance_claims/runs/2026… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 1 |
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
| cost_usd_est | 0.0095 |
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
| subset_manifest_jsonl | data/experiments/20260926T234603Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260926T234603Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.8056 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0095 |
| cost_usd_total | 0.0095 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 8608.955 |
| latency_ms_p95 | 11533 |
| tokens_completion_total | 7641 |
| tokens_prompt_total | 51248 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 51248 | 7641 | 58889 | 0.0095 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.728 · needs_judge_review: True · n_expecte… | 7084.4 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8537 · needs_judge_review: False · n_expec… | 6526.5 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7548 · needs_judge_review: True · n_expect… | 7953.5 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.7482 · needs_judge_review: True · n_expect… | 7621.3 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7994 · needs_judge_review: True · n_expect… | 8042.5 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.7327 · needs_judge_review: True · n_expect… | 7325.3 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8822 · needs_judge_review: True · n_expect… | 10141.2 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8882 · needs_judge_review: True · n_expect… | 7510.6 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9804 · needs_judge_review: True · n_expect… | 6857.3 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.7288 · needs_judge_review: True · n_expect… | 11016.1 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7272 · needs_judge_review: True · n_expect… | 7443.6 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.864 · needs_judge_review: True · n_expecte… | 6167.4 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8742 · needs_judge_review: True · n_expect… | 10884.9 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.8887 · needs_judge_review: True · n_expect… | 7756.3 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.7058 · needs_judge_review: True · n_expect… | 6114.1 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7491 · needs_judge_review: True · n_expect… | 7683.6 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.8238 · needs_judge_review: True · n_expect… | 21420.3 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.8889 · needs_judge_review: True · n_expect… | 6561.2 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.7277 · needs_judge_review: True · n_expect… | 6536 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.767 · needs_judge_review: True · n_expecte… | 11533 | — |
