## 20260928T060919Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T06:09:19+00:00 → 2026-09-28T06:15:39+00:00 |
| duration_s | 381.6 |
| comparison report | reports/api-comparisons/qwen3.7-flash/merger_agreement/runs… |
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
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
| class_counts | merger_agreement: 50 |
| config | ground_truth |
| filenames | contract_128_merger_agreement.txt, contract_31_merger_agree… |
| n_selected | 50 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 50 |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260928T060919Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T060919Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5085 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1583 |
| cost_usd_total | 0.1583 |
| latency_ms_mean | 53755.614 |
| latency_ms_p95 | 86529.7 |
| tokens_completion_total | 326444 |
| tokens_prompt_total | 3863166 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 53 | 3863166 | 326444 | 4189610 | 0.1583 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.2633 · needs_judge_review: False · n_expec… | 49997.1 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.37 · needs_judge_review: True · n_expected… | 52516.9 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 53710.1 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.2045 · needs_judge_review: False · n_expec… | 50872.9 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.6764 · needs_judge_review: False · n_expec… | 55295.9 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.2927 · needs_judge_review: False · n_expec… | 41204.1 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.6764 · needs_judge_review: False · n_expec… | 52187.7 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.6389 · needs_judge_review: False · n_expec… | 60766.4 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.3201 · needs_judge_review: False · n_expec… | 55588.5 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1441 · needs_judge_review: False · n_expec… | 50906.4 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.725 · needs_judge_review: True · n_expecte… | 58984.6 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: True · n_expected_… | 47162 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.6389 · needs_judge_review: False · n_expec… | 57151.4 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 52658 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.1578 · needs_judge_review: False · n_expec… | 46867.4 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.6471 · needs_judge_review: False · n_expec… | 56898.6 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.1873 · needs_judge_review: False · n_expec… | 53744.5 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 34279.8 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.2965 · needs_judge_review: False · n_expec… | 47314.3 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 52624.7 | — |
| corpus:ground_truth:train:contract_126_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 55019.1 | — |
| corpus:ground_truth:train:contract_75_merger_agreement.txt | overall_score: 0.6945 · needs_judge_review: False · n_expec… | 57245.8 | — |
| corpus:ground_truth:train:contract_112_merger_agreement.txt | overall_score: 0.7188 · needs_judge_review: False · n_expec… | 43545.3 | — |
| corpus:ground_truth:train:contract_141_merger_agreement.txt | overall_score: 0.2234 · needs_judge_review: False · n_expec… | 46010.5 | — |
| corpus:ground_truth:train:contract_73_merger_agreement.txt | overall_score: 0.2167 · needs_judge_review: False · n_expec… | 72798.6 | — |
| corpus:ground_truth:train:contract_1_merger_agreement.txt | overall_score: 0.7222 · needs_judge_review: False · n_expec… | 57388.9 | — |
| corpus:ground_truth:train:contract_144_merger_agreement.txt | overall_score: 0.8438 · needs_judge_review: True · n_expect… | 101055.6 | — |
| corpus:ground_truth:train:contract_134_merger_agreement.txt | overall_score: 0.6764 · needs_judge_review: False · n_expec… | 52317.8 | — |
| corpus:ground_truth:train:contract_78_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 52578.3 | — |
| corpus:ground_truth:train:contract_17_merger_agreement.txt | overall_score: 0.2377 · needs_judge_review: False · n_expec… | 50975.3 | — |
| corpus:ground_truth:train:contract_137_merger_agreement.txt | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 49316.1 | — |
| corpus:ground_truth:train:contract_54_merger_agreement.txt | overall_score: 0.625 · needs_judge_review: False · n_expect… | 40447.8 | — |
| corpus:ground_truth:train:contract_3_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 46802.5 | — |
| corpus:ground_truth:train:contract_2_merger_agreement.txt | overall_score: 0.2829 · needs_judge_review: False · n_expec… | 52176.1 | — |
| corpus:ground_truth:train:contract_23_merger_agreement.txt | overall_score: 0.6945 · needs_judge_review: False · n_expec… | 47486 | — |
| corpus:ground_truth:train:contract_57_merger_agreement.txt | overall_score: 0.2865 · needs_judge_review: False · n_expec… | 58395.6 | — |
| corpus:ground_truth:train:contract_81_merger_agreement.txt | overall_score: 0.7308 · needs_judge_review: False · n_expec… | 86529.7 | — |
| corpus:ground_truth:train:contract_24_merger_agreement.txt | overall_score: 0.7 · needs_judge_review: False · n_expected… | 45603.6 | — |
| corpus:ground_truth:train:contract_101_merger_agreement.txt | overall_score: 0.6764 · needs_judge_review: False · n_expec… | 40185.8 | — |
| corpus:ground_truth:train:contract_28_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 57975 | — |
| corpus:ground_truth:train:contract_83_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 62033.2 | — |
| corpus:ground_truth:train:contract_85_merger_agreement.txt | overall_score: 0.6471 · needs_judge_review: False · n_expec… | 46245.8 | — |
| corpus:ground_truth:train:contract_119_merger_agreement.txt | overall_score: 0.2633 · needs_judge_review: False · n_expec… | 35103.3 | — |
| corpus:ground_truth:train:contract_35_merger_agreement.txt | overall_score: 0.625 · needs_judge_review: False · n_expect… | 56750.5 | — |
| corpus:ground_truth:train:contract_77_merger_agreement.txt | overall_score: 0.2461 · needs_judge_review: False · n_expec… | 51454.7 | — |
| corpus:ground_truth:train:contract_27_merger_agreement.txt | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 105386.2 | — |
| corpus:ground_truth:train:contract_43_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 39390.9 | — |
| corpus:ground_truth:train:contract_47_merger_agreement.txt | overall_score: 0.6945 · needs_judge_review: False · n_expec… | 44273.7 | — |
| corpus:ground_truth:train:contract_20_merger_agreement.txt | overall_score: 0.1303 · needs_judge_review: False · n_expec… | 56244.3 | — |
| corpus:ground_truth:train:contract_7_merger_agreement.txt | overall_score: 0.2725 · needs_judge_review: False · n_expec… | 46313.4 | — |
