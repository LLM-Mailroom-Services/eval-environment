## 20260928T085028Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / insurance_claims_specialist_… |
| trace backend | braintrust |
| git | commit: eabeab5 · dirty: True |
| started / finished | 2026-09-28T08:50:28+00:00 → 2026-09-28T08:51:39+00:00 |
| duration_s | 72 |
| comparison report | reports/api-comparisons/deepseek-v4.1-flash/insurance_claim… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
| decode_budget_applied | sampling_injected: False · max_tokens_by_agent: {} |
| decode_profile | — |
| dry_run | ✗ |
| n | — |
| resumed_from | — |
| sample | 20 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:pde:233384494245864.txt, corpus:g… |
| class_counts | insurance_claim: 20 |
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
| subset_manifest_jsonl | data/experiments/20260928T085028Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260928T085028Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.7912 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0135 |
| cost_usd_total | 0.0135 |
| latency_ms_mean | 10424.78 |
| latency_ms_p95 | 19177.7 |
| tokens_completion_total | 41616 |
| tokens_prompt_total | 41068 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 41068 | 41616 | 82684 | 0.0135 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.6839 · needs_judge_review: False · n_expec… | 17065 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8625 · needs_judge_review: False · n_expec… | 13078.8 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7511 · needs_judge_review: False · n_expec… | 3312.7 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.7511 · needs_judge_review: False · n_expec… | 9856.4 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 4230.5 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.7034 · needs_judge_review: True · n_expect… | 8667.9 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8838 · needs_judge_review: True · n_expect… | 5248.7 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8685 · needs_judge_review: True · n_expect… | 11164.4 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.967 · needs_judge_review: True · n_expecte… | 10475.1 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.6943 · needs_judge_review: False · n_expec… | 18420.3 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 4565.3 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8754 · needs_judge_review: True · n_expect… | 6403.4 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8703 · needs_judge_review: True · n_expect… | 13808.2 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.9647 · needs_judge_review: True · n_expect… | 3192.2 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.7034 · needs_judge_review: True · n_expect… | 10814.8 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7208 · needs_judge_review: True · n_expect… | 19716 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.7535 · needs_judge_review: False · n_expec… | 4581.4 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.9714 · needs_judge_review: True · n_expect… | 19177.7 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.6943 · needs_judge_review: False · n_expec… | 8132.4 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.6463 · needs_judge_review: False · n_expec… | 16584.4 | — |
