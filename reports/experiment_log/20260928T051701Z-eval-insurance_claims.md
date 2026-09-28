## 20260928T051701Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: ac3b77f · dirty: True |
| started / finished | 2026-09-28T05:17:01+00:00 → 2026-09-28T05:19:00+00:00 |
| duration_s | 121 |
| comparison report | reports/api-comparisons/qwen3.7-flash/insurance_claims/runs… |
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
| subset_manifest_jsonl | data/experiments/20260928T051701Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260928T051701Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.7894 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0099 |
| cost_usd_total | 0.0099 |
| latency_ms_mean | 37009.215 |
| latency_ms_p95 | 40900.7 |
| tokens_completion_total | 66346 |
| tokens_prompt_total | 41452 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 41452 | 66346 | 107798 | 0.0099 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 40730.1 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8585 · needs_judge_review: False · n_expec… | 37530.2 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 37874.3 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 35831.5 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 40757.9 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 37229.5 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.9221 · needs_judge_review: True · n_expect… | 40074.4 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8714 · needs_judge_review: True · n_expect… | 33363.7 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9785 · needs_judge_review: True · n_expect… | 34168.8 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 29287.4 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 38061.3 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8588 · needs_judge_review: False · n_expec… | 33500.4 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8469 · needs_judge_review: False · n_expec… | 29968.2 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.9268 · needs_judge_review: True · n_expect… | 39268.8 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 40063.2 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 38180.9 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.7535 · needs_judge_review: False · n_expec… | 36782.3 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.9213 · needs_judge_review: True · n_expect… | 32940.1 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 40900.7 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.7532 · needs_judge_review: False · n_expec… | 43670.6 | — |
