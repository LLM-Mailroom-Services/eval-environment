## 20260927T054211Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: 1d9f8d2 · dirty: True |
| started / finished | 2026-09-27T05:42:11+00:00 → 2026-09-27T05:45:37+00:00 |
| duration_s | 208.1 |
| comparison report | reports/api-comparisons/granite-4.2-8b/insurance_claims/RUN… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
| decode_budget_applied | sampling_injected: True · max_tokens_by_agent: {'contracts_… |
| decode_call_timeout_s | 600 |
| decode_profile | granite-4.2-8b |
| decode_sampling | temperature: 1.0 · top_p: 0.95 · seed: 42 |
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
| cost_usd_est | 0.0247 |
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
| subset_manifest_jsonl | data/experiments/20260927T054211Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260927T054211Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.7135 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0247 |
| cost_usd_total | 0.0247 |
| expected_cost_usd | 0.8 |
| latency_ms_mean | 58454.34 |
| latency_ms_p95 | 121582.6 |
| tokens_completion_total | 88363 |
| tokens_prompt_total | 43656 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 43656 | 88363 | 132019 | 0.0247 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.7286 · needs_judge_review: True · n_expect… | 101588.2 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8537 · needs_judge_review: False · n_expec… | 98830.4 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.63 · needs_judge_review: True · n_expected… | 3966 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 879.9 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.662 · needs_judge_review: False · n_expect… | 3896.6 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.567 · needs_judge_review: False · n_expect… | 4406.7 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8833 · needs_judge_review: True · n_expect… | 78205.9 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.7911 · needs_judge_review: True · n_expect… | 3930.7 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9664 · needs_judge_review: True · n_expect… | 116300.2 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.6902 · needs_judge_review: False · n_expec… | 107096.1 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.649 · needs_judge_review: False · n_expect… | 3504.8 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.862 · needs_judge_review: False · n_expect… | 110557.3 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.848 · needs_judge_review: False · n_expect… | 132341.3 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.8826 · needs_judge_review: True · n_expect… | 75576.9 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.567 · needs_judge_review: False · n_expect… | 3623.1 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7013 · needs_judge_review: True · n_expect… | 121582.6 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.6626 · needs_judge_review: False · n_expec… | 4390.9 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.8844 · needs_judge_review: True · n_expect… | 55740.9 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.6981 · needs_judge_review: False · n_expec… | 62954.6 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.7422 · needs_judge_review: False · n_expec… | 79713.7 | — |
