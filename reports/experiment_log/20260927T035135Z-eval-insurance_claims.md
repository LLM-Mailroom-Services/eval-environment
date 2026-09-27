## 20260927T035135Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: bd43f66 · dirty: True |
| started / finished | 2026-09-27T03:51:35+00:00 → 2026-09-27T03:54:57+00:00 |
| duration_s | 203.3 |
| error | — |

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
| subset_manifest_jsonl | data/experiments/20260927T035135Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260927T035135Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.7488 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.032 |
| latency_ms_mean | 50681.595 |
| latency_ms_p95 | 147490.1 |
| tokens_completion_total | 50885 |
| tokens_prompt_total | 75955 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 37 | 75955 | 50885 | 126840 | 0.032 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 27438.6 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8556 · needs_judge_review: False · n_expec… | 39907.7 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7512 · needs_judge_review: False · n_expec… | 27076.5 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.7209 · needs_judge_review: True · n_expect… | 145889.5 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 23580.6 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 25049.2 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 19644.4 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.7583 · needs_judge_review: False · n_expec… | 14831.3 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9 · needs_judge_review: False · n_expected… | 33817.7 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 147490.1 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 21485 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8408 · needs_judge_review: False · n_expec… | 14622.3 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8423 · needs_judge_review: False · n_expec… | 38177.8 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 20600.4 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 18637.4 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.63 · needs_judge_review: True · n_expected… | 27120.2 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.7535 · needs_judge_review: False · n_expec… | 144598.8 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 19430.5 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 150612.8 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.6768 · needs_judge_review: False · n_expec… | 53621.1 | — |
