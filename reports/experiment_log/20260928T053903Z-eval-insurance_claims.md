## 20260928T053903Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T05:39:03+00:00 → 2026-09-28T05:43:42+00:00 |
| duration_s | 281.4 |
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
| sample | 50 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:pde:233384494245864.txt, corpus:g… |
| class_counts | insurance_claim: 50 |
| config | ground_truth |
| filenames | pde:233384494245864.txt, insurbias-624.txt, carrier:8874733… |
| n_selected | 50 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 50 |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260928T053903Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260928T053903Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.7846 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0264 |
| cost_usd_total | 0.0264 |
| latency_ms_mean | 40475.264 |
| latency_ms_p95 | 50805.6 |
| tokens_completion_total | 176597 |
| tokens_prompt_total | 114073 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 50 | 114073 | 176597 | 290670 | 0.0264 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 30668.9 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8583 · needs_judge_review: False · n_expec… | 36026.6 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 45666.2 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.6317 · needs_judge_review: True · n_expect… | 38113.2 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 33327.6 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 31308.4 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.9221 · needs_judge_review: True · n_expect… | 44746.2 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8702 · needs_judge_review: True · n_expect… | 34018.2 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9779 · needs_judge_review: True · n_expect… | 34321.4 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 30198.3 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 39199.2 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8464 · needs_judge_review: False · n_expec… | 35052.4 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8469 · needs_judge_review: False · n_expec… | 26351.5 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.9268 · needs_judge_review: True · n_expect… | 32106.5 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 44520.9 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 40854.9 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.7978 · needs_judge_review: False · n_expec… | 36886.6 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.9213 · needs_judge_review: True · n_expect… | 36865.6 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 48914.1 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.7343 · needs_judge_review: True · n_expect… | 47281.5 | — |
| corpus:ground_truth:train:auto:CLM-000355.txt | overall_score: 0.9223 · needs_judge_review: True · n_expect… | 39446 | — |
| corpus:ground_truth:train:insurbias-535.txt | overall_score: 0.8508 · needs_judge_review: False · n_expec… | 35045.7 | — |
| corpus:ground_truth:train:pde:233734492807320.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 48868.7 | — |
| corpus:ground_truth:train:property:268405870.txt | overall_score: 0.6689 · needs_judge_review: True · n_expect… | 48391.5 | — |
| corpus:ground_truth:train:outpatient:542762281171383:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 36012 | — |
| corpus:ground_truth:train:property:261716804.txt | overall_score: 0.7437 · needs_judge_review: True · n_expect… | 56822.8 | — |
| corpus:ground_truth:train:carrier:887263386589340.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 35408.1 | — |
| corpus:ground_truth:train:outpatient:542062281218793:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 32175.3 | — |
| corpus:ground_truth:train:insurbias-1222.txt | overall_score: 0.8576 · needs_judge_review: False · n_expec… | 44164.7 | — |
| corpus:ground_truth:train:inpatient:196401177008033:1.txt | overall_score: 0.7353 · needs_judge_review: True · n_expect… | 42805.1 | — |
| corpus:ground_truth:train:property:269879669.txt | overall_score: 0.8485 · needs_judge_review: False · n_expec… | 59994.9 | — |
| corpus:ground_truth:train:pde:233024489630762.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 44879.9 | — |
| corpus:ground_truth:train:insurbias-976.txt | overall_score: 0.8738 · needs_judge_review: True · n_expect… | 35137.1 | — |
| corpus:ground_truth:train:insurbias-914.txt | overall_score: 0.8854 · needs_judge_review: True · n_expect… | 37147 | — |
| corpus:ground_truth:train:pde:233654491978707.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 35556.9 | — |
| corpus:ground_truth:train:property:267944087.txt | overall_score: 0.7434 · needs_judge_review: True · n_expect… | 40285.5 | — |
| corpus:ground_truth:train:inpatient:196451176994433:1.txt | overall_score: 0.8127 · needs_judge_review: True · n_expect… | 39551.5 | — |
| corpus:ground_truth:train:pde:233634491375303.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 37602 | — |
| corpus:ground_truth:train:outpatient:542712281056440:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 36896.8 | — |
| corpus:ground_truth:train:auto:CLM-000809.txt | overall_score: 0.8762 · needs_judge_review: False · n_expec… | 41069.9 | — |
| corpus:ground_truth:train:inpatient:196991176968589:1.txt | overall_score: 0.7766 · needs_judge_review: False · n_expec… | 42590.4 | — |
| corpus:ground_truth:train:outpatient:542922281376960:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 47920.7 | — |
| corpus:ground_truth:train:outpatient:542472281487558:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 41827.5 | — |
| corpus:ground_truth:train:carrier:887393389256013.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 46334.1 | — |
| corpus:ground_truth:train:property:262548994.txt | overall_score: 0.6539 · needs_judge_review: False · n_expec… | 50646 | — |
| corpus:ground_truth:train:property:261515174.txt | overall_score: 0.8728 · needs_judge_review: True · n_expect… | 49462.2 | — |
| corpus:ground_truth:train:insurbias-969.txt | overall_score: 0.854 · needs_judge_review: False · n_expect… | 40719.7 | — |
| corpus:ground_truth:train:auto:CLM-000249.txt | overall_score: 0.886 · needs_judge_review: True · n_expecte… | 37736.5 | — |
| corpus:ground_truth:train:property:263266666.txt | overall_score: 0.8488 · needs_judge_review: True · n_expect… | 50805.6 | — |
| corpus:ground_truth:train:inpatient:196781176972873:1.txt | overall_score: 0.7859 · needs_judge_review: True · n_expect… | 42030.9 | — |
