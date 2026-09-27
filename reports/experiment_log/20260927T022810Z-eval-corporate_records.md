## 20260927T022810Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:28:10+00:00 → 2026-09-27T02:33:59+00:00 |
| duration_s | 352 |
| comparison report | reports/api-comparisons/qwen3-8b/corporate_records/runs/202… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
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
| cost_usd_est | 0.0403 |
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
| subset_manifest_jsonl | data/experiments/20260927T022810Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260927T022810Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.1824 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0403 |
| cost_usd_total | 0.0403 |
| expected_cost_usd | 0.12 |
| latency_ms_mean | 50674.82 |
| latency_ms_p95 | 240418.7 |
| tokens_completion_total | 39458 |
| tokens_prompt_total | 190774 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 22 | 190774 | 39458 | 230232 | 0.0403 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 26683.4 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 36336.5 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 7802.2 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 22570.7 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.5976 · needs_judge_review: False · n_expec… | 22109.4 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 13485.2 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 17694.5 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18603.9 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.2295 · needs_judge_review: False · n_expec… | 20045.8 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.0 · needs_judge_review: False · n_expected… | 49367 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 17474.1 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.2521 · needs_judge_review: False · n_expec… | 21677.5 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 240418.7 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.223 · needs_judge_review: False · n_expect… | 42686.9 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.4576 · needs_judge_review: False · n_expec… | 318812.7 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2295 · needs_judge_review: False · n_expec… | 36144.8 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 47011.4 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.2606 · needs_judge_review: False · n_expec… | 10322.4 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.2615 · needs_judge_review: False · n_expec… | 25769.6 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18479.7 | — |
