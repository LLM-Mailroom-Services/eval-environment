## 20260928T083627Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / corporate_records_specialist_v5 |
| trace backend | braintrust |
| git | commit: a5325b9 · dirty: True |
| started / finished | 2026-09-28T08:36:27+00:00 → 2026-09-28T08:42:13+00:00 |
| duration_s | 347.3 |
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
| sample | 50 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… |
| class_counts | corporate_record: 50 |
| config | ground_truth |
| filenames | 0001047469-12-006895_a2210011zex-4_10.htm, 0001047469-03-03… |
| n_selected | 50 |
| n_total | 403 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 50 |
| seed | 42 |
| split | train |
| subset | class:corporate_record |
| subset_manifest_jsonl | data/experiments/20260928T083627Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260928T083627Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.4178 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0393 |
| cost_usd_total | 0.0393 |
| latency_ms_mean | 39336.862 |
| latency_ms_p95 | 97541.5 |
| tokens_completion_total | 170711 |
| tokens_prompt_total | 569472 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 59 | 569472 | 170711 | 740183 | 0.0393 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.2028 · needs_judge_review: False · n_expec… | 30345.3 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.625 · needs_judge_review: False · n_expect… | 27507.4 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.4666 · needs_judge_review: False · n_expec… | 29459 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.3887 · needs_judge_review: True · n_expect… | 35657.2 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.6214 · needs_judge_review: False · n_expec… | 49065.1 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.5678 · needs_judge_review: False · n_expec… | 38192.1 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 28356.8 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.5136 · needs_judge_review: False · n_expec… | 31624.2 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.2437 · needs_judge_review: False · n_expec… | 30058.3 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.7125 · needs_judge_review: True · n_expect… | 46912.3 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.7854 · needs_judge_review: False · n_expec… | 37155.5 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.3214 · needs_judge_review: False · n_expec… | 27367.6 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.2731 · needs_judge_review: False · n_expec… | 30936.7 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.223 · needs_judge_review: False · n_expect… | 30711.9 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.3589 · needs_judge_review: True · n_expect… | 116666.4 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2937 · needs_judge_review: False · n_expec… | 43869.6 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.3022 · needs_judge_review: False · n_expec… | 44451.7 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.2918 · needs_judge_review: False · n_expec… | 24029.1 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.3115 · needs_judge_review: False · n_expec… | 34381.6 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.3025 · needs_judge_review: False · n_expec… | 27661.6 | — |
| corpus:ground_truth:train:0001214659-18-006586_ex3_3.htm | overall_score: 0.5014 · needs_judge_review: False · n_expec… | 42560.4 | — |
| corpus:ground_truth:train:0000950168-02-001563_dex211.txt | overall_score: 0.4776 · needs_judge_review: False · n_expec… | 24500.3 | — |
| corpus:ground_truth:train:0001493152-22-014997_ex3-2.htm | overall_score: 0.2345 · needs_judge_review: False · n_expec… | 34325.2 | — |
| corpus:ground_truth:train:0000721748-14-000223_ex3_2bylaws.… | overall_score: 0.6937 · needs_judge_review: False · n_expec… | 26796.1 | — |
| corpus:ground_truth:train:0001193125-10-049079_dex341.htm | overall_score: 0.2591 · needs_judge_review: False · n_expec… | 29497.5 | — |
| corpus:ground_truth:train:0001213900-20-012863_ea122016ex3-… | overall_score: 0.3673 · needs_judge_review: True · n_expect… | 32424.5 | — |
| corpus:ground_truth:train:0001079974-10-000369_bulkstors1ex… | overall_score: 0.5367 · needs_judge_review: True · n_expect… | 24088.1 | — |
| corpus:ground_truth:train:0001683168-24-006658_cloudastruct… | overall_score: 0.6625 · needs_judge_review: False · n_expec… | 28939.7 | — |
| corpus:ground_truth:train:0001571049-17-008060_t1702546_ex4… | overall_score: 0.6208 · needs_judge_review: False · n_expec… | 25536.3 | — |
| corpus:ground_truth:train:0001547903-13-000020_a41specimenc… | overall_score: 0.4882 · needs_judge_review: True · n_expect… | 33243.8 | — |
| corpus:ground_truth:train:0001193125-07-225925_dex211.htm | overall_score: 0.5427 · needs_judge_review: True · n_expect… | 39291.7 | — |
| corpus:ground_truth:train:0000950123-09-074380_g20855a1exv3… | overall_score: 0.2437 · needs_judge_review: False · n_expec… | 35940.4 | — |
| corpus:ground_truth:train:0001104659-20-105312_tm2024520d5_… | overall_score: 0.2829 · needs_judge_review: False · n_expec… | 32089.2 | — |
| corpus:ground_truth:train:0001193125-09-061115_dex32.htm | overall_score: 0.7364 · needs_judge_review: True · n_expect… | 22941.9 | — |
| corpus:ground_truth:train:0001193125-09-252452_dex34.htm | overall_score: 0.353 · needs_judge_review: False · n_expect… | 33000.5 | — |
| corpus:ground_truth:train:0001047469-09-009128_a2194825zex-… | overall_score: 0.2864 · needs_judge_review: False · n_expec… | 29026.5 | — |
| corpus:ground_truth:train:0001398432-09-000149_exh4_10.htm | overall_score: 0.5976 · needs_judge_review: False · n_expec… | 31632.4 | — |
| corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.h… | overall_score: 0.3456 · needs_judge_review: False · n_expec… | 151834 | — |
| corpus:ground_truth:train:0001193125-04-072642_dex211.htm | overall_score: 0.4776 · needs_judge_review: False · n_expec… | 32792.3 | — |
| corpus:ground_truth:train:0001553350-15-001174_aqua_ex3z1c.… | overall_score: 0.2661 · needs_judge_review: False · n_expec… | 37888.1 | — |
| corpus:ground_truth:train:0000950137-02-005662_c71678a2exv4… | overall_score: 0.3397 · needs_judge_review: True · n_expect… | 97541.5 | — |
| corpus:ground_truth:train:0001615774-14-000417_s100510_ex3-… | overall_score: 0.3156 · needs_judge_review: False · n_expec… | 35677.3 | — |
| corpus:ground_truth:train:0000950144-06-006066_g01711a1exv4… | overall_score: 0.3212 · needs_judge_review: False · n_expec… | 92414.7 | — |
| corpus:ground_truth:train:0001193125-15-005780_d789569dex49… | overall_score: 0.2897 · needs_judge_review: False · n_expec… | 38166.9 | — |
| corpus:ground_truth:train:0001829126-25-005032_picardmedica… | overall_score: 0.2345 · needs_judge_review: False · n_expec… | 30291.9 | — |
| corpus:ground_truth:train:0001193125-10-012980_dex211.htm | overall_score: 0.5136 · needs_judge_review: False · n_expec… | 27999 | — |
| corpus:ground_truth:train:0001193125-14-025241_d593074dex31… | overall_score: 0.2829 · needs_judge_review: False · n_expec… | 23045.8 | — |
| corpus:ground_truth:train:0001099574-13-000003_exh32amendme… | overall_score: 0.2887 · needs_judge_review: False · n_expec… | 42357.7 | — |
| corpus:ground_truth:train:0001193125-08-114390_dex3150.htm | overall_score: 0.5885 · needs_judge_review: False · n_expec… | 42664.5 | — |
| corpus:ground_truth:train:0001213900-19-025668_fs12019a1ex3… | overall_score: 0.3513 · needs_judge_review: False · n_expec… | 23925.5 | — |
