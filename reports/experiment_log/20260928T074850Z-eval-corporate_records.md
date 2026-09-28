## 20260928T074850Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 6c4ac14 · dirty: True |
| started / finished | 2026-09-28T07:48:50+00:00 → 2026-09-28T07:51:08+00:00 |
| duration_s | 140.2 |
| comparison report | reports/api-comparisons/qwen3.7-flash/corporate_records/run… |
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
| case_ids | corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… |
| class_counts | corporate_record: 20 |
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
| subset_manifest_jsonl | data/experiments/20260928T074850Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260928T074850Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4093 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0141 |
| cost_usd_total | 0.0141 |
| latency_ms_mean | 36904.15 |
| latency_ms_p95 | 46624.7 |
| tokens_completion_total | 64000 |
| tokens_prompt_total | 193492 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 22 | 193492 | 64000 | 257492 | 0.0141 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.2028 · needs_judge_review: False · n_expec… | 35298.2 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.625 · needs_judge_review: False · n_expect… | 28963.4 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.4308 · needs_judge_review: False · n_expec… | 33905.1 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.3054 · needs_judge_review: False · n_expec… | 30235.8 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.6476 · needs_judge_review: False · n_expec… | 39625.9 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.5678 · needs_judge_review: False · n_expec… | 34073.5 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.6357 · needs_judge_review: False · n_expec… | 32201.4 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.5136 · needs_judge_review: False · n_expec… | 37035.4 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.2937 · needs_judge_review: False · n_expec… | 32969.7 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.6208 · needs_judge_review: False · n_expec… | 46624.7 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.614 · needs_judge_review: False · n_expect… | 29956.3 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.3214 · needs_judge_review: False · n_expec… | 27843.8 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.2731 · needs_judge_review: False · n_expec… | 39255.8 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.223 · needs_judge_review: False · n_expect… | 40523.4 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.3589 · needs_judge_review: True · n_expect… | 95137.7 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2937 · needs_judge_review: False · n_expec… | 29858.5 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.3022 · needs_judge_review: False · n_expec… | 37595.8 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.2918 · needs_judge_review: False · n_expec… | 30983.7 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.3115 · needs_judge_review: False · n_expec… | 33848.1 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.3526 · needs_judge_review: False · n_expec… | 22146.8 | — |
