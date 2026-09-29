## 20260928T054349Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / insurance_claims_specialist_v2 |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T05:43:49+00:00 → 2026-09-28T05:48:20+00:00 |
| duration_s | 272.3 |
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
| subset_manifest_jsonl | data/experiments/20260928T054349Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260928T054349Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.7812 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0259 |
| cost_usd_total | 0.0259 |
| latency_ms_mean | 39429.332 |
| latency_ms_p95 | 51438.1 |
| tokens_completion_total | 172751 |
| tokens_prompt_total | 115273 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 50 | 115273 | 172751 | 288024 | 0.0259 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 31911.8 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8585 · needs_judge_review: False · n_expec… | 39816.8 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 51426.6 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.6317 · needs_judge_review: True · n_expect… | 47111.9 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 36642 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 31905.2 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.9221 · needs_judge_review: True · n_expect… | 38055.1 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8791 · needs_judge_review: True · n_expect… | 43530.5 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9752 · needs_judge_review: True · n_expect… | 44685.1 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 46280.8 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 33761.2 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8588 · needs_judge_review: False · n_expec… | 38952.3 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8469 · needs_judge_review: False · n_expec… | 36152.1 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.9268 · needs_judge_review: True · n_expect… | 32589.4 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 42705.3 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 39802.1 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.7978 · needs_judge_review: False · n_expec… | 34786.4 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.9213 · needs_judge_review: True · n_expect… | 43057.8 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 33918.9 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.7353 · needs_judge_review: True · n_expect… | 48202.7 | — |
| corpus:ground_truth:train:auto:CLM-000355.txt | overall_score: 0.9223 · needs_judge_review: True · n_expect… | 32929.2 | — |
| corpus:ground_truth:train:insurbias-535.txt | overall_score: 0.8508 · needs_judge_review: False · n_expec… | 34893.8 | — |
| corpus:ground_truth:train:pde:233734492807320.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 35528.3 | — |
| corpus:ground_truth:train:property:268405870.txt | overall_score: 0.6698 · needs_judge_review: True · n_expect… | 51696.1 | — |
| corpus:ground_truth:train:outpatient:542762281171383:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 32331.6 | — |
| corpus:ground_truth:train:property:261716804.txt | overall_score: 0.7336 · needs_judge_review: True · n_expect… | 41131 | — |
| corpus:ground_truth:train:carrier:887263386589340.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 51438.1 | — |
| corpus:ground_truth:train:outpatient:542062281218793:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 32580.1 | — |
| corpus:ground_truth:train:insurbias-1222.txt | overall_score: 0.8576 · needs_judge_review: False · n_expec… | 32468.7 | — |
| corpus:ground_truth:train:inpatient:196401177008033:1.txt | overall_score: 0.7353 · needs_judge_review: True · n_expect… | 38686.9 | — |
| corpus:ground_truth:train:property:269879669.txt | overall_score: 0.7576 · needs_judge_review: False · n_expec… | 45430.2 | — |
| corpus:ground_truth:train:pde:233024489630762.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 36857.8 | — |
| corpus:ground_truth:train:insurbias-976.txt | overall_score: 0.8652 · needs_judge_review: True · n_expect… | 35723.9 | — |
| corpus:ground_truth:train:insurbias-914.txt | overall_score: 0.8855 · needs_judge_review: True · n_expect… | 36244.3 | — |
| corpus:ground_truth:train:pde:233654491978707.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 31744.3 | — |
| corpus:ground_truth:train:property:267944087.txt | overall_score: 0.7434 · needs_judge_review: True · n_expect… | 46139.1 | — |
| corpus:ground_truth:train:inpatient:196451176994433:1.txt | overall_score: 0.813 · needs_judge_review: True · n_expecte… | 36661.2 | — |
| corpus:ground_truth:train:pde:233634491375303.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 32724.2 | — |
| corpus:ground_truth:train:outpatient:542712281056440:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 32070.4 | — |
| corpus:ground_truth:train:auto:CLM-000809.txt | overall_score: 0.8762 · needs_judge_review: False · n_expec… | 31337.1 | — |
| corpus:ground_truth:train:inpatient:196991176968589:1.txt | overall_score: 0.7535 · needs_judge_review: False · n_expec… | 42814.1 | — |
| corpus:ground_truth:train:outpatient:542922281376960:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 42864.4 | — |
| corpus:ground_truth:train:outpatient:542472281487558:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 36795.6 | — |
| corpus:ground_truth:train:carrier:887393389256013.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 44645.7 | — |
| corpus:ground_truth:train:property:262548994.txt | overall_score: 0.6356 · needs_judge_review: True · n_expect… | 51776.5 | — |
| corpus:ground_truth:train:property:261515174.txt | overall_score: 0.8431 · needs_judge_review: True · n_expect… | 48562.6 | — |
| corpus:ground_truth:train:insurbias-969.txt | overall_score: 0.8521 · needs_judge_review: False · n_expec… | 39541.7 | — |
| corpus:ground_truth:train:auto:CLM-000249.txt | overall_score: 0.886 · needs_judge_review: True · n_expecte… | 37810.7 | — |
| corpus:ground_truth:train:property:263266666.txt | overall_score: 0.8488 · needs_judge_review: True · n_expect… | 44152 | — |
| corpus:ground_truth:train:inpatient:196781176972873:1.txt | overall_score: 0.7779 · needs_judge_review: True · n_expect… | 38593 | — |
