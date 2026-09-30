## 20260927T110153Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / None |
| trace backend | braintrust |
| git | commit: 3c2c95c · dirty: True |
| started / finished | 2026-09-27T11:01:53+00:00 → 2026-09-27T11:08:24+00:00 |
| duration_s | 392.7 |
| comparison report | reports/api-comparisons/deepseek-v4.1-flash/merger_agreemen… |
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
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
| class_counts | merger_agreement: 20 |
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
| subset_manifest_jsonl | data/experiments/20260927T110153Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T110153Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.2423 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0752 |
| cost_usd_total | 0.0752 |
| latency_ms_mean | 41119.41 |
| latency_ms_p95 | 63886.6 |
| tokens_completion_total | 111149 |
| tokens_prompt_total | 1228920 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 15 | 1228920 | 111149 | 1340069 | 0.0752 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.6162 · needs_judge_review: False · n_expec… | 23210.5 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.37 · needs_judge_review: True · n_expected… | 29992.2 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.7333 · needs_judge_review: False · n_expec… | 26549.4 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.3221 · needs_judge_review: False · n_expec… | 56774.6 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 63886.6 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.3516 · needs_judge_review: False · n_expec… | 388527.8 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 30093.8 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 26964.9 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 29913.6 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.3385 · needs_judge_review: False · n_expec… | 29374.5 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.6583 · needs_judge_review: True · n_expect… | 33818.4 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 38224.2 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 35644.6 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 850.9 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 1266.9 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 1316.6 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 1922.1 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 1899.4 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 1315.8 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 841.4 | — |
