## 20260927T082404Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: b66e30f · dirty: True |
| started / finished | 2026-09-27T08:24:04+00:00 → 2026-09-27T08:44:30+00:00 |
| duration_s | 1228 |
| comparison report | reports/api-comparisons/granite-4.2-8b/merger_agreement/run… |
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
| cost_usd_est | 0.1774 |
| cost_usd_total | 0.1774 |
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
| subset_manifest_jsonl | data/experiments/20260927T082404Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T082404Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.4548 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1774 |
| cost_usd_total | 0.1774 |
| expected_cost_usd | 0.8 |
| latency_ms_mean | 383811.575 |
| latency_ms_p95 | 580299.4 |
| tokens_completion_total | 306796 |
| tokens_prompt_total | 1678904 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 38 | 1678904 | 306796 | 1985700 | 0.1774 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 423301.1 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 440920.4 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 655539.1 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 292294.4 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.5588 · needs_judge_review: False · n_expec… | 573646.4 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 526408.8 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 508224.5 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 419153.5 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 219868.6 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 142930.6 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 580299.4 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 143997 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 457459.4 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.3315 · needs_judge_review: True · n_expect… | 313721.1 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 212152.5 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 293511 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.099 · needs_judge_review: False · n_expect… | 517898.1 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.5625 · needs_judge_review: False · n_expec… | 223610.3 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: False · n_expected… | 248759.1 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.625 · needs_judge_review: False · n_expect… | 482536.2 | — |
