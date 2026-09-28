## 20260928T053010Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / correspondence_specialist_v2 |
| trace backend | braintrust |
| git | commit: fdd8a5d · dirty: True |
| started / finished | 2026-09-28T05:30:10+00:00 → 2026-09-28T05:34:14+00:00 |
| duration_s | 245.3 |
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
| subset_manifest_jsonl | data/experiments/20260928T053010Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260928T053010Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5136 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0218 |
| cost_usd_total | 0.0218 |
| latency_ms_mean | 34499.32 |
| latency_ms_p95 | 49235.4 |
| tokens_completion_total | 142342 |
| tokens_prompt_total | 110235 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 50 | 110235 | 142342 | 252577 | 0.0218 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.3513 · needs_judge_review: False · n_expec… | 32071.5 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 34956.9 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.4118 · needs_judge_review: False · n_expec… | 35906.5 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 30837 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4582 · needs_judge_review: False · n_expec… | 41680 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.278 · needs_judge_review: False · n_expect… | 40829 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 36911.2 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.6833 · needs_judge_review: True · n_expect… | 27199.1 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 24389.2 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 37086.9 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.5625 · needs_judge_review: False · n_expec… | 37670.9 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 23361.9 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 30852.9 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.6572 · needs_judge_review: False · n_expec… | 55845.1 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.6269 · needs_judge_review: False · n_expec… | 50414.7 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 30712 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 20804.8 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 49235.4 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.502 · needs_judge_review: False · n_expect… | 33820.7 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 23777.5 | — |
| corpus:ground_truth:train:campbell-l/inbox/488. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 35452.8 | — |
| corpus:ground_truth:train:lay-k/deleted_items/67. | overall_score: 0.5542 · needs_judge_review: True · n_expect… | 25962.9 | — |
| corpus:ground_truth:train:shackleton-s/all_documents/4886. | overall_score: 0.8 · needs_judge_review: True · n_expected_… | 39078.5 | — |
| corpus:ground_truth:train:farmer-d/all_documents/2959. | overall_score: 0.5227 · needs_judge_review: False · n_expec… | 35743.6 | — |
| corpus:ground_truth:train:jones-t/inbox/61. | overall_score: 0.3864 · needs_judge_review: True · n_expect… | 23100.4 | — |
| corpus:ground_truth:train:holst-k/inbox/99. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 40171.7 | — |
| corpus:ground_truth:train:skilling-j/inbox/31. | overall_score: 0.4071 · needs_judge_review: False · n_expec… | 38552.6 | — |
| corpus:ground_truth:train:kaminski-v/_sent_mail/1015. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 38681.5 | — |
| corpus:ground_truth:train:hendrickson-s/deleted_items/120. | overall_score: 0.6136 · needs_judge_review: False · n_expec… | 32759.9 | — |
| corpus:ground_truth:train:hain-m/all_documents/675. | overall_score: 0.8611 · needs_judge_review: False · n_expec… | 30601 | — |
| corpus:ground_truth:train:jones-t/all_documents/10848. | overall_score: 0.5417 · needs_judge_review: False · n_expec… | 38602 | — |
| corpus:ground_truth:train:cash-m/all_documents/552. | overall_score: 0.4285 · needs_judge_review: False · n_expec… | 28758.6 | — |
| corpus:ground_truth:train:lewis-a/deleted_items/747. | overall_score: 0.1966 · needs_judge_review: False · n_expec… | 32275.6 | — |
| corpus:ground_truth:train:haedicke-m/all_documents/4969. | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 33461 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/184. | overall_score: 0.4618 · needs_judge_review: False · n_expec… | 34950.8 | — |
| corpus:ground_truth:train:schoolcraft-d/deleted_items/689. | overall_score: 0.5417 · needs_judge_review: False · n_expec… | 29374.4 | — |
| corpus:ground_truth:train:taylor-m/inbox/219. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 29308.8 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/2276. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 33936 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/1330. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 40391.2 | — |
| corpus:ground_truth:train:buy-r/inbox/411. | overall_score: 0.4763 · needs_judge_review: True · n_expect… | 37915.8 | — |
| corpus:ground_truth:train:shankman-j/all_documents/94. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 30598.3 | — |
| corpus:ground_truth:train:baughman-d/deleted_items/292. | overall_score: 0.4066 · needs_judge_review: False · n_expec… | 39051.6 | — |
| corpus:ground_truth:train:mann-k/_sent_mail/3284. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 37802.4 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/28332. | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 19792.4 | — |
| corpus:ground_truth:train:rapp-b/inbox/251. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 43015.4 | — |
| corpus:ground_truth:train:smith-m/_sent_mail/70. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 35630.5 | — |
| corpus:ground_truth:train:hain-m/all_documents/641. | overall_score: 0.4127 · needs_judge_review: False · n_expec… | 39148.5 | — |
| corpus:ground_truth:train:skilling-j/inbox/1231. | overall_score: 0.323 · needs_judge_review: False · n_expect… | 43443.2 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/11714. | overall_score: 0.7675 · needs_judge_review: True · n_expect… | 28644.8 | — |
| corpus:ground_truth:train:bailey-s/deleted_items/59. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 30396.6 | — |
