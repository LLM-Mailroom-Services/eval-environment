## 20260927T060322Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: 1d9f8d2 · dirty: True |
| started / finished | 2026-09-27T06:03:22+00:00 → 2026-09-27T06:54:02+00:00 |
| duration_s | 3041.9 |
| comparison report | reports/api-comparisons/granite-4.2-8b/merger_agreement/RUN… |
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
| cost_usd_est | 0.4374 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
| config | ground_truth |
| filenames | contract_128_merger_agreement.txt, contract_31_merger_agree… |
| n_selected | 20 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260927T060322Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T060322Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.387 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.4374 |
| cost_usd_total | 0.4374 |
| expected_cost_usd | 0.8 |
| latency_ms_mean | 1065583.98 |
| latency_ms_p95 | 1748404.3 |
| tokens_completion_total | 1259169 |
| tokens_prompt_total | 2044275 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 170 | 2044275 | 1259169 | 3303444 | 0.4374 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 1247604.1 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 1112379.2 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.5333 · needs_judge_review: False · n_expec… | 1424451.1 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.1163 · needs_judge_review: False · n_expec… | 909993.6 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.5588 · needs_judge_review: False · n_expec… | 1748404.3 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 1004991.2 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.5588 · needs_judge_review: False · n_expec… | 1234822 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.7222 · needs_judge_review: False · n_expec… | 953902.7 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 1361030.7 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1441 · needs_judge_review: False · n_expec… | 893219.4 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 1950586.8 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 556902.3 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 1186225 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.3905 · needs_judge_review: True · n_expect… | 1256131.8 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 1017198.3 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 796078.7 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 870445.3 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.5312 · needs_judge_review: False · n_expec… | 430016.1 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 606595.9 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 750701.1 | — |
