## 20260927T065622Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: 1d9f8d2 · dirty: True |
| started / finished | 2026-09-27T06:56:22+00:00 → 2026-09-27T07:04:48+00:00 |
| duration_s | 508.6 |
| comparison report | reports/api-comparisons/granite-4.2-8b/corporate_records/RU… |
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
| cost_usd_est | 0.0436 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… |
| config | ground_truth |
| filenames | 0001047469-12-006895_a2210011zex-4_10.htm, 0001047469-03-03… |
| n_selected | 20 |
| n_total | 403 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:corporate_record |
| subset_manifest_jsonl | data/experiments/20260927T065622Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260927T065622Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4156 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0436 |
| cost_usd_total | 0.0436 |
| expected_cost_usd | 0.8 |
| latency_ms_mean | 95147.26 |
| latency_ms_p95 | 205019.6 |
| tokens_completion_total | 127441 |
| tokens_prompt_total | 196299 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 22 | 196299 | 127441 | 323740 | 0.0436 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.2545 · needs_judge_review: False · n_expec… | 86230.7 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 3602.8 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 10050.1 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.2762 · needs_judge_review: False · n_expec… | 117122.5 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.6691 · needs_judge_review: False · n_expec… | 49059.7 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.6214 · needs_judge_review: False · n_expec… | 205019.6 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.675 · needs_judge_review: True · n_expecte… | 3895.4 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.4636 · needs_judge_review: False · n_expec… | 113266.2 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.3372 · needs_judge_review: False · n_expec… | 2433.1 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.5708 · needs_judge_review: False · n_expec… | 197213.4 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.7063 · needs_judge_review: True · n_expect… | 75910.5 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.3098 · needs_judge_review: False · n_expec… | 89875.7 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.4234 · needs_judge_review: False · n_expec… | 64867.1 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.4098 · needs_judge_review: False · n_expec… | 76268.4 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.3589 · needs_judge_review: True · n_expect… | 412907.5 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2294 · needs_judge_review: False · n_expec… | 99594.2 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.2521 · needs_judge_review: False · n_expec… | 163842.1 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.591 · needs_judge_review: True · n_expecte… | 2411.1 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.3115 · needs_judge_review: False · n_expec… | 126870.7 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.3025 · needs_judge_review: False · n_expec… | 2504.4 | — |
