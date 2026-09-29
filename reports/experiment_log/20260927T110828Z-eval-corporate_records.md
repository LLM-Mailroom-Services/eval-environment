## 20260927T110828Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / None |
| trace backend | braintrust |
| git | commit: 3c2c95c · dirty: True |
| started / finished | 2026-09-27T11:08:28+00:00 → 2026-09-27T11:09:57+00:00 |
| duration_s | 91.6 |
| comparison report | reports/api-comparisons/deepseek-v4.1-flash/corporate_recor… |
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
| subset_manifest_jsonl | data/experiments/20260927T110828Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260927T110828Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4415 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0197 |
| cost_usd_total | 0.0197 |
| latency_ms_mean | 10693.665 |
| latency_ms_p95 | 16931.3 |
| tokens_completion_total | 45325 |
| tokens_prompt_total | 186564 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 21 | 186564 | 45325 | 231889 | 0.0197 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.2528 · needs_judge_review: False · n_expec… | 5126.4 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.65 · needs_judge_review: False · n_expecte… | 3030.7 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.4666 · needs_judge_review: False · n_expec… | 4194.5 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.3679 · needs_judge_review: False · n_expec… | 5822.9 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.6214 · needs_judge_review: False · n_expec… | 6936.4 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.6214 · needs_judge_review: False · n_expec… | 11409.6 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.725 · needs_judge_review: True · n_expecte… | 6893.7 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.4636 · needs_judge_review: False · n_expec… | 4777 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.2437 · needs_judge_review: False · n_expec… | 16931.3 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.7333 · needs_judge_review: True · n_expect… | 7345.3 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.7688 · needs_judge_review: False · n_expec… | 5010.1 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.3099 · needs_judge_review: False · n_expec… | 6426.5 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.4597 · needs_judge_review: False · n_expec… | 2973 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.4348 · needs_judge_review: False · n_expec… | 8171.1 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.3589 · needs_judge_review: True · n_expect… | 10188.9 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2437 · needs_judge_review: False · n_expec… | 14729.1 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.2829 · needs_judge_review: False · n_expec… | 71977.7 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.2137 · needs_judge_review: False · n_expec… | 9564.3 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.3431 · needs_judge_review: False · n_expec… | 7721.1 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.2682 · needs_judge_review: False · n_expec… | 4643.7 | — |
