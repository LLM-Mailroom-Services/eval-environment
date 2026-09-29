## 20260928T051905Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / insurance_claims_specialist_v2 |
| trace backend | braintrust |
| git | commit: ac3b77f · dirty: True |
| started / finished | 2026-09-28T05:19:05+00:00 → 2026-09-28T05:20:59+00:00 |
| duration_s | 115.3 |
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
| subset_manifest_jsonl | data/experiments/20260928T051905Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260928T051905Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.7855 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0094 |
| cost_usd_total | 0.0094 |
| latency_ms_mean | 34297.195 |
| latency_ms_p95 | 44322.9 |
| tokens_completion_total | 62525 |
| tokens_prompt_total | 41932 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 41932 | 62525 | 104457 | 0.0094 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 32029.7 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8583 · needs_judge_review: False · n_expec… | 33809.4 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 44570.4 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.6317 · needs_judge_review: True · n_expect… | 37422.7 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 35384.7 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 31911.8 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.9221 · needs_judge_review: True · n_expect… | 31154.1 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8714 · needs_judge_review: True · n_expect… | 31476.7 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9779 · needs_judge_review: True · n_expect… | 36002.3 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 28531.1 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 33775.5 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8464 · needs_judge_review: False · n_expec… | 30542.2 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8469 · needs_judge_review: False · n_expec… | 30746.4 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.9268 · needs_judge_review: True · n_expect… | 31085.4 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 31799.8 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 35648.1 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.7978 · needs_judge_review: False · n_expec… | 37053.8 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.9213 · needs_judge_review: True · n_expect… | 36215.9 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 32461 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.6434 · needs_judge_review: True · n_expect… | 44322.9 | — |
