## 20260928T080826Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / merger_agreement_specialist_v2 |
| trace backend | none |
| git | commit: 6c4ac14 · dirty: True |
| started / finished | 2026-09-28T08:08:26+00:00 → 2026-09-28T08:11:11+00:00 |
| duration_s | 166.1 |
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
| subset_manifest_jsonl | data/experiments/20260928T080826Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T080826Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.3964 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.065 |
| cost_usd_total | 0.065 |
| latency_ms_mean | 49937.56 |
| latency_ms_p95 | 61809.5 |
| tokens_completion_total | 127971 |
| tokens_prompt_total | 1611013 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 20 | 1611013 | 127971 | 1738984 | 0.065 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.2339 · needs_judge_review: False · n_expec… | 55007.6 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 101943.6 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 50107.4 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.2045 · needs_judge_review: False · n_expec… | 47288.4 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.6471 · needs_judge_review: False · n_expec… | 45597.2 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.2339 · needs_judge_review: False · n_expec… | 45503.8 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.5588 · needs_judge_review: False · n_expec… | 58979 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 42478.4 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.1867 · needs_judge_review: False · n_expec… | 43899 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1718 · needs_judge_review: False · n_expec… | 56138.1 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.5917 · needs_judge_review: True · n_expect… | 41477.1 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.4445 · needs_judge_review: True · n_expect… | 45401.2 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.5834 · needs_judge_review: False · n_expec… | 44482 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.5882 · needs_judge_review: False · n_expec… | 46111.3 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.1578 · needs_judge_review: False · n_expec… | 40222.8 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.6471 · needs_judge_review: False · n_expec… | 45295.4 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.1285 · needs_judge_review: False · n_expec… | 46301.7 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.5312 · needs_judge_review: False · n_expec… | 39515.2 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.2083 · needs_judge_review: False · n_expec… | 41192.5 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.6 · needs_judge_review: False · n_expected… | 61809.5 | — |
