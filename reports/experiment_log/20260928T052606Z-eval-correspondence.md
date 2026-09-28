## 20260928T052606Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: b2058f9 · dirty: True |
| started / finished | 2026-09-28T05:26:06+00:00 → 2026-09-28T05:30:04+00:00 |
| duration_s | 240 |
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
| subset_manifest_jsonl | data/experiments/20260928T052606Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260928T052606Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5022 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0221 |
| cost_usd_total | 0.0221 |
| latency_ms_mean | 34356.266 |
| latency_ms_p95 | 49371.7 |
| tokens_completion_total | 144601 |
| tokens_prompt_total | 108735 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 50 | 108735 | 144601 | 253336 | 0.0221 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.4013 · needs_judge_review: False · n_expec… | 34172.6 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 38984 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.4118 · needs_judge_review: False · n_expec… | 39882.2 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 26447.8 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4582 · needs_judge_review: False · n_expec… | 33571 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.278 · needs_judge_review: False · n_expect… | 37786.6 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 38361.6 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.6833 · needs_judge_review: True · n_expect… | 31997.2 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 20033.9 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 39702.5 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.6125 · needs_judge_review: False · n_expec… | 34619.7 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 22265.1 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 27774.4 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.4959 · needs_judge_review: False · n_expec… | 49371.7 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.6462 · needs_judge_review: False · n_expec… | 47740.4 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 31368.5 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 32649.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 43353.5 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.502 · needs_judge_review: False · n_expect… | 28770.9 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 25015.7 | — |
| corpus:ground_truth:train:campbell-l/inbox/488. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 27552.4 | — |
| corpus:ground_truth:train:lay-k/deleted_items/67. | overall_score: 0.5542 · needs_judge_review: True · n_expect… | 25896.5 | — |
| corpus:ground_truth:train:shackleton-s/all_documents/4886. | overall_score: 0.925 · needs_judge_review: True · n_expecte… | 36306.1 | — |
| corpus:ground_truth:train:farmer-d/all_documents/2959. | overall_score: 0.5227 · needs_judge_review: False · n_expec… | 29635.9 | — |
| corpus:ground_truth:train:jones-t/inbox/61. | overall_score: 0.3864 · needs_judge_review: True · n_expect… | 25459 | — |
| corpus:ground_truth:train:holst-k/inbox/99. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 30974.1 | — |
| corpus:ground_truth:train:skilling-j/inbox/31. | overall_score: 0.4071 · needs_judge_review: False · n_expec… | 30612.5 | — |
| corpus:ground_truth:train:kaminski-v/_sent_mail/1015. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 33862.8 | — |
| corpus:ground_truth:train:hendrickson-s/deleted_items/120. | overall_score: 0.6136 · needs_judge_review: False · n_expec… | 35536.4 | — |
| corpus:ground_truth:train:hain-m/all_documents/675. | overall_score: 0.748 · needs_judge_review: True · n_expecte… | 34021.5 | — |
| corpus:ground_truth:train:jones-t/all_documents/10848. | overall_score: 0.3673 · needs_judge_review: False · n_expec… | 44470.1 | — |
| corpus:ground_truth:train:cash-m/all_documents/552. | overall_score: 0.4702 · needs_judge_review: False · n_expec… | 28160.1 | — |
| corpus:ground_truth:train:lewis-a/deleted_items/747. | overall_score: 0.1966 · needs_judge_review: False · n_expec… | 33303 | — |
| corpus:ground_truth:train:haedicke-m/all_documents/4969. | overall_score: 0.5714 · needs_judge_review: False · n_expec… | 47924.6 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/184. | overall_score: 0.3618 · needs_judge_review: False · n_expec… | 35307.4 | — |
| corpus:ground_truth:train:schoolcraft-d/deleted_items/689. | overall_score: 0.3826 · needs_judge_review: False · n_expec… | 41717.8 | — |
| corpus:ground_truth:train:taylor-m/inbox/219. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 34322.8 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/2276. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 27153.7 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/1330. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 49906.7 | — |
| corpus:ground_truth:train:buy-r/inbox/411. | overall_score: 0.4763 · needs_judge_review: True · n_expect… | 52804.3 | — |
| corpus:ground_truth:train:shankman-j/all_documents/94. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 30624.1 | — |
| corpus:ground_truth:train:baughman-d/deleted_items/292. | overall_score: 0.4066 · needs_judge_review: False · n_expec… | 33743.3 | — |
| corpus:ground_truth:train:mann-k/_sent_mail/3284. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 40402 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/28332. | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 15507.6 | — |
| corpus:ground_truth:train:rapp-b/inbox/251. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 46741.6 | — |
| corpus:ground_truth:train:smith-m/_sent_mail/70. | overall_score: 0.3357 · needs_judge_review: False · n_expec… | 33510.7 | — |
| corpus:ground_truth:train:hain-m/all_documents/641. | overall_score: 0.4127 · needs_judge_review: False · n_expec… | 34859.2 | — |
| corpus:ground_truth:train:skilling-j/inbox/1231. | overall_score: 0.323 · needs_judge_review: False · n_expect… | 38771.9 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/11714. | overall_score: 0.7987 · needs_judge_review: False · n_expec… | 30070.5 | — |
| corpus:ground_truth:train:bailey-s/deleted_items/59. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 24785.9 | — |
