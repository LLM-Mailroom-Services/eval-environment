## 20260927T020724Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: 53ffee5 · dirty: True |
| started / finished | 2026-09-27T02:07:24+00:00 → 2026-09-27T02:09:08+00:00 |
| duration_s | 106.5 |
| comparison report | /workspace/reports/api-comparisons/qwen3-8b/RUN-2-MERGER_AG… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 1 |
| decode_budget_applied | sampling_injected: False · max_tokens_by_agent: {'contracts… |
| decode_call_timeout_s | 600 |
| decode_profile | qwen3-8b |
| decode_sampling | — |
| dry_run | ✗ |
| n | — |
| resumed_from | — |
| sample | 2 |
| scorer | extraction |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Cost cap

| Key | Value |
|---|---|
| cap_usd | 1.5 |
| cost_usd_est | 0.0064 |
| status | under_cap |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
| config | ground_truth |
| filenames | contract_128_merger_agreement.txt, contract_31_merger_agree… |
| n_selected | 2 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 2 |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260927T020724Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T020724Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.346 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0064 |
| cost_usd_total | 0.0064 |
| expected_cost_usd | 0.012 |
| latency_ms_mean | 46870 |
| latency_ms_p95 | 47783.9 |
| tokens_completion_total | 13016 |
| tokens_prompt_total | 157083 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 2 | 157083 | 13016 | 170099 | 0.0064 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.3221 · needs_judge_review: False · n_expec… | 45956.1 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.37 · needs_judge_review: True · n_expected… | 47783.9 | — |
