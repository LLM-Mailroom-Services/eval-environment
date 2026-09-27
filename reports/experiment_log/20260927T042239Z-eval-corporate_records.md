## 20260927T042239Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: b949149 · dirty: True |
| started / finished | 2026-09-27T04:22:39+00:00 → 2026-09-27T04:29:53+00:00 |
| duration_s | 436.5 |
| error | — |

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
| subset_manifest_jsonl | data/experiments/20260927T042239Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260927T042239Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4004 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0602 |
| latency_ms_mean | 81193.54 |
| latency_ms_p95 | 337727.3 |
| tokens_completion_total | 54703 |
| tokens_prompt_total | 301916 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 34 | 301916 | 54703 | 356619 | 0.0602 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.3605 · needs_judge_review: False · n_expec… | 65579.3 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 32597.6 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.4808 · needs_judge_review: False · n_expec… | 337727.3 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.2554 · needs_judge_review: False · n_expec… | 30866.8 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.4599 · needs_judge_review: False · n_expec… | 13010.6 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.5678 · needs_judge_review: False · n_expec… | 37420.2 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 28675 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.4636 · needs_judge_review: False · n_expec… | 30869 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.1602 · needs_judge_review: False · n_expec… | 18804.6 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 64008.9 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.75 · needs_judge_review: False · n_expecte… | 242776.6 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.2521 · needs_judge_review: False · n_expec… | 14995.1 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.4098 · needs_judge_review: False · n_expec… | 397685.4 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.3484 · needs_judge_review: False · n_expec… | 27742.4 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.5392 · needs_judge_review: False · n_expec… | 130368.7 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2294 · needs_judge_review: False · n_expec… | 32521.2 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.2329 · needs_judge_review: False · n_expec… | 47372.9 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.2606 · needs_judge_review: False · n_expec… | 10660 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.3115 · needs_judge_review: False · n_expec… | 30491.8 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.241 · needs_judge_review: False · n_expect… | 29697.4 | — |
