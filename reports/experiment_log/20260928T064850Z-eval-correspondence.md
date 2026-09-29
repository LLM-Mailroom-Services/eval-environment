## 20260928T064850Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / correspondence_specialist_v3 |
| trace backend | braintrust |
| git | commit: b6b6683 · dirty: True |
| started / finished | 2026-09-28T06:48:50+00:00 → 2026-09-28T06:53:08+00:00 |
| duration_s | 259.7 |
| comparison report | reports/api-comparisons/qwen3.7-flash/correspondence/runs/2… |
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
| case_ids | corpus:ground_truth:train:blair-l/meetings/608., corpus:gro… |
| class_counts | correspondence: 50 |
| config | ground_truth |
| filenames | blair-l/meetings/608., lokey-t/inbox/250., kean-s/all_docum… |
| n_selected | 50 |
| n_total | 915 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 50 |
| seed | 42 |
| split | train |
| subset | class:correspondence |
| subset_manifest_jsonl | data/experiments/20260928T064850Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260928T064850Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5087 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.022 |
| cost_usd_total | 0.022 |
| latency_ms_mean | 35531.792 |
| latency_ms_p95 | 48428.9 |
| tokens_completion_total | 143770 |
| tokens_prompt_total | 110785 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 50 | 110785 | 143770 | 254555 | 0.022 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.3513 · needs_judge_review: False · n_expec… | 38359.7 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 34997.1 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.4118 · needs_judge_review: False · n_expec… | 35519.7 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 35953.4 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4582 · needs_judge_review: False · n_expec… | 36582.8 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 40562.2 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 38911.2 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.6833 · needs_judge_review: True · n_expect… | 32251.7 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.3322 · needs_judge_review: False · n_expec… | 27869.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 38211 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.5625 · needs_judge_review: False · n_expec… | 35297.7 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 30256.3 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 30052.7 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.6572 · needs_judge_review: False · n_expec… | 59650.5 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.6269 · needs_judge_review: False · n_expec… | 48428.9 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 31791.3 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 22873.7 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 43350.4 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.502 · needs_judge_review: False · n_expect… | 34948.1 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 29638.5 | — |
| corpus:ground_truth:train:campbell-l/inbox/488. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 46805.9 | — |
| corpus:ground_truth:train:lay-k/deleted_items/67. | overall_score: 0.5542 · needs_judge_review: True · n_expect… | 37894 | — |
| corpus:ground_truth:train:shackleton-s/all_documents/4886. | overall_score: 0.825 · needs_judge_review: True · n_expecte… | 31020.2 | — |
| corpus:ground_truth:train:farmer-d/all_documents/2959. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 43879.4 | — |
| corpus:ground_truth:train:jones-t/inbox/61. | overall_score: 0.3864 · needs_judge_review: True · n_expect… | 25096.2 | — |
| corpus:ground_truth:train:holst-k/inbox/99. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 22200.7 | — |
| corpus:ground_truth:train:skilling-j/inbox/31. | overall_score: 0.4071 · needs_judge_review: False · n_expec… | 32096 | — |
| corpus:ground_truth:train:kaminski-v/_sent_mail/1015. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 40196.1 | — |
| corpus:ground_truth:train:hendrickson-s/deleted_items/120. | overall_score: 0.6136 · needs_judge_review: False · n_expec… | 27081.4 | — |
| corpus:ground_truth:train:hain-m/all_documents/675. | overall_score: 0.875 · needs_judge_review: True · n_expecte… | 35249.2 | — |
| corpus:ground_truth:train:jones-t/all_documents/10848. | overall_score: 0.3674 · needs_judge_review: False · n_expec… | 32615.9 | — |
| corpus:ground_truth:train:cash-m/all_documents/552. | overall_score: 0.3868 · needs_judge_review: False · n_expec… | 26860.6 | — |
| corpus:ground_truth:train:lewis-a/deleted_items/747. | overall_score: 0.1662 · needs_judge_review: False · n_expec… | 40649.3 | — |
| corpus:ground_truth:train:haedicke-m/all_documents/4969. | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 37543.3 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/184. | overall_score: 0.4118 · needs_judge_review: False · n_expec… | 33956.8 | — |
| corpus:ground_truth:train:schoolcraft-d/deleted_items/689. | overall_score: 0.5417 · needs_judge_review: False · n_expec… | 36375.4 | — |
| corpus:ground_truth:train:taylor-m/inbox/219. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 28250.4 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/2276. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 32012.4 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/1330. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 39157.1 | — |
| corpus:ground_truth:train:buy-r/inbox/411. | overall_score: 0.4763 · needs_judge_review: True · n_expect… | 31530.8 | — |
| corpus:ground_truth:train:shankman-j/all_documents/94. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 39821.6 | — |
| corpus:ground_truth:train:baughman-d/deleted_items/292. | overall_score: 0.184 · needs_judge_review: False · n_expect… | 43256.8 | — |
| corpus:ground_truth:train:mann-k/_sent_mail/3284. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 37108.9 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/28332. | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 19954.9 | — |
| corpus:ground_truth:train:rapp-b/inbox/251. | overall_score: 0.3672 · needs_judge_review: False · n_expec… | 46567.2 | — |
| corpus:ground_truth:train:smith-m/_sent_mail/70. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 35249.8 | — |
| corpus:ground_truth:train:hain-m/all_documents/641. | overall_score: 0.4127 · needs_judge_review: False · n_expec… | 33951.6 | — |
| corpus:ground_truth:train:skilling-j/inbox/1231. | overall_score: 0.3231 · needs_judge_review: False · n_expec… | 56273.3 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/11714. | overall_score: 0.7987 · needs_judge_review: False · n_expec… | 26445.4 | — |
| corpus:ground_truth:train:bailey-s/deleted_items/59. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 31982.6 | — |
