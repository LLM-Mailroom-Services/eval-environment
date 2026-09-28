## 20260928T081536Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / corporate_records_specialist_v4 |
| trace backend | none |
| git | commit: 6c4ac14 · dirty: True |
| started / finished | 2026-09-28T08:15:36+00:00 → 2026-09-28T08:20:09+00:00 |
| duration_s | 274.6 |
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
| subset_manifest_jsonl | data/experiments/20260928T081536Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260928T081536Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.4248 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0376 |
| cost_usd_total | 0.0376 |
| latency_ms_mean | 37071.538 |
| latency_ms_p95 | 97770.6 |
| tokens_completion_total | 157683 |
| tokens_prompt_total | 569885 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 59 | 569885 | 157683 | 727568 | 0.0376 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.2028 · needs_judge_review: False · n_expec… | 34982.2 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.625 · needs_judge_review: False · n_expect… | 13424.7 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.5165 · needs_judge_review: False · n_expec… | 41597.8 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.3262 · needs_judge_review: False · n_expec… | 29457.5 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.6714 · needs_judge_review: False · n_expec… | 26654.5 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.5678 · needs_judge_review: False · n_expec… | 33593.5 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 32725.4 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.5136 · needs_judge_review: False · n_expec… | 27997.5 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.2437 · needs_judge_review: False · n_expec… | 41289.3 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.6708 · needs_judge_review: True · n_expect… | 50842.5 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.8021 · needs_judge_review: False · n_expec… | 33120.1 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.3214 · needs_judge_review: False · n_expec… | 38658.9 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.2731 · needs_judge_review: False · n_expec… | 34942.1 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.223 · needs_judge_review: False · n_expect… | 44309.4 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.3589 · needs_judge_review: True · n_expect… | 97770.6 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2437 · needs_judge_review: False · n_expec… | 29259 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.2829 · needs_judge_review: False · n_expec… | 41046.2 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.2918 · needs_judge_review: False · n_expec… | 24876 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.3115 · needs_judge_review: False · n_expec… | 36900.4 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.3526 · needs_judge_review: False · n_expec… | 31541.3 | — |
| corpus:ground_truth:train:0001214659-18-006586_ex3_3.htm | overall_score: 0.5014 · needs_judge_review: False · n_expec… | 31776.8 | — |
| corpus:ground_truth:train:0000950168-02-001563_dex211.txt | overall_score: 0.4776 · needs_judge_review: False · n_expec… | 23507.6 | — |
| corpus:ground_truth:train:0001493152-22-014997_ex3-2.htm | overall_score: 0.2345 · needs_judge_review: False · n_expec… | 28753.2 | — |
| corpus:ground_truth:train:0000721748-14-000223_ex3_2bylaws.… | overall_score: 0.6312 · needs_judge_review: False · n_expec… | 17935.7 | — |
| corpus:ground_truth:train:0001193125-10-049079_dex341.htm | overall_score: 0.2591 · needs_judge_review: False · n_expec… | 27357.8 | — |
| corpus:ground_truth:train:0001213900-20-012863_ea122016ex3-… | overall_score: 0.3673 · needs_judge_review: True · n_expect… | 22946.6 | — |
| corpus:ground_truth:train:0001079974-10-000369_bulkstors1ex… | overall_score: 0.5367 · needs_judge_review: True · n_expect… | 25551.8 | — |
| corpus:ground_truth:train:0001683168-24-006658_cloudastruct… | overall_score: 0.6625 · needs_judge_review: False · n_expec… | 28437.3 | — |
| corpus:ground_truth:train:0001571049-17-008060_t1702546_ex4… | overall_score: 0.6208 · needs_judge_review: False · n_expec… | 39336.3 | — |
| corpus:ground_truth:train:0001547903-13-000020_a41specimenc… | overall_score: 0.4882 · needs_judge_review: True · n_expect… | 23970.4 | — |
| corpus:ground_truth:train:0001193125-07-225925_dex211.htm | overall_score: 0.5927 · needs_judge_review: True · n_expect… | 33582.1 | — |
| corpus:ground_truth:train:0000950123-09-074380_g20855a1exv3… | overall_score: 0.2437 · needs_judge_review: False · n_expec… | 30160.4 | — |
| corpus:ground_truth:train:0001104659-20-105312_tm2024520d5_… | overall_score: 0.2829 · needs_judge_review: False · n_expec… | 25435.6 | — |
| corpus:ground_truth:train:0001193125-09-061115_dex32.htm | overall_score: 0.7364 · needs_judge_review: True · n_expect… | 26220.3 | — |
| corpus:ground_truth:train:0001193125-09-252452_dex34.htm | overall_score: 0.353 · needs_judge_review: False · n_expect… | 28928.8 | — |
| corpus:ground_truth:train:0001047469-09-009128_a2194825zex-… | overall_score: 0.2864 · needs_judge_review: False · n_expec… | 31293.4 | — |
| corpus:ground_truth:train:0001398432-09-000149_exh4_10.htm | overall_score: 0.5976 · needs_judge_review: False · n_expec… | 28811.1 | — |
| corpus:ground_truth:train:0000950120-07-000199_exhibit4_1.h… | overall_score: 0.3973 · needs_judge_review: False · n_expec… | 123404.2 | — |
| corpus:ground_truth:train:0001193125-04-072642_dex211.htm | overall_score: 0.4548 · needs_judge_review: False · n_expec… | 31695.6 | — |
| corpus:ground_truth:train:0001553350-15-001174_aqua_ex3z1c.… | overall_score: 0.3161 · needs_judge_review: False · n_expec… | 27273 | — |
| corpus:ground_truth:train:0000950137-02-005662_c71678a2exv4… | overall_score: 0.3914 · needs_judge_review: True · n_expect… | 94241.7 | — |
| corpus:ground_truth:train:0001615774-14-000417_s100510_ex3-… | overall_score: 0.5536 · needs_judge_review: True · n_expect… | 29082.9 | — |
| corpus:ground_truth:train:0000950144-06-006066_g01711a1exv4… | overall_score: 0.3212 · needs_judge_review: False · n_expec… | 101746 | — |
| corpus:ground_truth:train:0001193125-15-005780_d789569dex49… | overall_score: 0.3414 · needs_judge_review: False · n_expec… | 27890.2 | — |
| corpus:ground_truth:train:0001829126-25-005032_picardmedica… | overall_score: 0.2845 · needs_judge_review: False · n_expec… | 31210 | — |
| corpus:ground_truth:train:0001193125-10-012980_dex211.htm | overall_score: 0.4636 · needs_judge_review: False · n_expec… | 32043 | — |
| corpus:ground_truth:train:0001193125-14-025241_d593074dex31… | overall_score: 0.2829 · needs_judge_review: False · n_expec… | 24728.9 | — |
| corpus:ground_truth:train:0001099574-13-000003_exh32amendme… | overall_score: 0.2887 · needs_judge_review: False · n_expec… | 42982.3 | — |
| corpus:ground_truth:train:0001193125-08-114390_dex3150.htm | overall_score: 0.5885 · needs_judge_review: False · n_expec… | 29896.5 | — |
| corpus:ground_truth:train:0001213900-19-025668_fs12019a1ex3… | overall_score: 0.3014 · needs_judge_review: False · n_expec… | 38388.5 | — |
