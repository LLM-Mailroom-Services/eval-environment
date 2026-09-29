## 20260927T105400Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / None |
| trace backend | braintrust |
| git | commit: 3c2c95c · dirty: True |
| started / finished | 2026-09-27T10:54:00+00:00 → 2026-09-27T10:55:45+00:00 |
| duration_s | 107.3 |
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
| subset_manifest_jsonl | data/experiments/20260927T105400Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260927T105400Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.7974 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0135 |
| cost_usd_total | 0.0135 |
| latency_ms_mean | 15101.91 |
| latency_ms_p95 | 79745 |
| tokens_completion_total | 41615 |
| tokens_prompt_total | 40636 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 40636 | 41615 | 82251 | 0.0135 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.6883 · needs_judge_review: False · n_expec… | 5517.4 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8651 · needs_judge_review: True · n_expect… | 7237.2 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7512 · needs_judge_review: False · n_expec… | 7435.2 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.7209 · needs_judge_review: True · n_expect… | 6874 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 8226.8 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.7489 · needs_judge_review: False · n_expec… | 9651.2 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.9167 · needs_judge_review: False · n_expec… | 10140.6 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8794 · needs_judge_review: True · n_expect… | 2607.7 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9666 · needs_judge_review: True · n_expect… | 14654.8 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.6943 · needs_judge_review: False · n_expec… | 9910.7 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 5013.6 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8754 · needs_judge_review: True · n_expect… | 7994 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.867 · needs_judge_review: True · n_expecte… | 11063.7 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.9607 · needs_judge_review: True · n_expect… | 2560.2 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.6943 · needs_judge_review: False · n_expec… | 3338.2 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7209 · needs_judge_review: True · n_expect… | 92083.4 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.8227 · needs_judge_review: True · n_expect… | 3483.8 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.9631 · needs_judge_review: True · n_expect… | 10770.8 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.7034 · needs_judge_review: True · n_expect… | 3729.9 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.6515 · needs_judge_review: False · n_expec… | 79745 | — |
