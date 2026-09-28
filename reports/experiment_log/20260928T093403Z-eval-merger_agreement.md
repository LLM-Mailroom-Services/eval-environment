## 20260928T093403Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | deepseek/deepseek-v4.1-flash / merger_agreement_specialist_… |
| trace backend | braintrust |
| git | commit: 9d993e0 · dirty: True |
| started / finished | 2026-09-28T09:34:03+00:00 → 2026-09-28T09:42:02+00:00 |
| duration_s | 479.6 |
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
| subset_manifest_jsonl | data/experiments/20260928T093403Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260928T093403Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.4217 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.3713 |
| cost_usd_total | 0.3713 |
| latency_ms_mean | 59467.644 |
| latency_ms_p95 | 137533.1 |
| tokens_completion_total | 589096 |
| tokens_prompt_total | 5728402 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 77 | 5728402 | 589096 | 6317498 | 0.3713 | deepseek/deepseek-v4.1-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.3221 · needs_judge_review: False · n_expec… | 42254.8 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 56445.6 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.7667 · needs_judge_review: True · n_expect… | 54493.5 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.3221 · needs_judge_review: False · n_expec… | 53289.7 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 28343.9 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.3221 · needs_judge_review: False · n_expec… | 87343.6 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 54625.4 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 52913.6 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 141305.4 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.3385 · needs_judge_review: False · n_expec… | 17551.1 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.925 · needs_judge_review: True · n_expecte… | 137533.1 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5555 · needs_judge_review: True · n_expect… | 49403.6 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 52803.2 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.7941 · needs_judge_review: True · n_expect… | 27661.8 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 96489.2 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.7059 · needs_judge_review: False · n_expec… | 23691.2 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 48867.6 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 21664.2 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 49096.7 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 51045 | — |
| corpus:ground_truth:train:contract_126_merger_agreement.txt | overall_score: 0.9706 · needs_judge_review: False · n_expec… | 33070.5 | — |
| corpus:ground_truth:train:contract_75_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 20922.4 | — |
| corpus:ground_truth:train:contract_112_merger_agreement.txt | overall_score: 0.6875 · needs_judge_review: False · n_expec… | 101684.8 | — |
| corpus:ground_truth:train:contract_141_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 38544.3 | — |
| corpus:ground_truth:train:contract_73_merger_agreement.txt | overall_score: 0.3638 · needs_judge_review: True · n_expect… | 41739.7 | — |
| corpus:ground_truth:train:contract_1_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 23350.4 | — |
| corpus:ground_truth:train:contract_144_merger_agreement.txt | overall_score: 0.7188 · needs_judge_review: False · n_expec… | 31197.5 | — |
| corpus:ground_truth:train:contract_134_merger_agreement.txt | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 23129.1 | — |
| corpus:ground_truth:train:contract_78_merger_agreement.txt | overall_score: 0.7353 · needs_judge_review: False · n_expec… | 54616.7 | — |
| corpus:ground_truth:train:contract_17_merger_agreement.txt | overall_score: 0.3553 · needs_judge_review: False · n_expec… | 23425.1 | — |
| corpus:ground_truth:train:contract_137_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 49859.8 | — |
| corpus:ground_truth:train:contract_54_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 26676.1 | — |
| corpus:ground_truth:train:contract_3_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 116599.2 | — |
| corpus:ground_truth:train:contract_2_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 104514.2 | — |
| corpus:ground_truth:train:contract_23_merger_agreement.txt | overall_score: 0.7222 · needs_judge_review: False · n_expec… | 23803.4 | — |
| corpus:ground_truth:train:contract_57_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 71362.5 | — |
| corpus:ground_truth:train:contract_81_merger_agreement.txt | overall_score: 0.8846 · needs_judge_review: True · n_expect… | 64099.5 | — |
| corpus:ground_truth:train:contract_24_merger_agreement.txt | overall_score: 1.0 · needs_judge_review: False · n_expected… | 37265.7 | — |
| corpus:ground_truth:train:contract_101_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 19415.3 | — |
| corpus:ground_truth:train:contract_28_merger_agreement.txt | overall_score: 0.9706 · needs_judge_review: False · n_expec… | 85817.8 | — |
| corpus:ground_truth:train:contract_83_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 181796.3 | — |
| corpus:ground_truth:train:contract_85_merger_agreement.txt | overall_score: 0.7647 · needs_judge_review: True · n_expect… | 104208.1 | — |
| corpus:ground_truth:train:contract_119_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 93934.8 | — |
| corpus:ground_truth:train:contract_35_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 21353.3 | — |
| corpus:ground_truth:train:contract_77_merger_agreement.txt | overall_score: 0.3049 · needs_judge_review: False · n_expec… | 108562.4 | — |
| corpus:ground_truth:train:contract_27_merger_agreement.txt | overall_score: 1.0 · needs_judge_review: False · n_expected… | 69667.5 | — |
| corpus:ground_truth:train:contract_43_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 112234.7 | — |
| corpus:ground_truth:train:contract_47_merger_agreement.txt | overall_score: 0.75 · needs_judge_review: True · n_expected… | 18874.2 | — |
| corpus:ground_truth:train:contract_20_merger_agreement.txt | overall_score: 0.5678 · needs_judge_review: False · n_expec… | 17494.4 | — |
| corpus:ground_truth:train:contract_7_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 107340.3 | — |
