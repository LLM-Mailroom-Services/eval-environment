## 20260928T083110Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / correspondence_specialist_v5 |
| trace backend | braintrust |
| git | commit: a5325b9 · dirty: True |
| started / finished | 2026-09-28T08:31:10+00:00 → 2026-09-28T08:36:19+00:00 |
| duration_s | 309.7 |
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
| subset_manifest_jsonl | data/experiments/20260928T083110Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260928T083110Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 50 |
| overall_score | 0.5094 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0221 |
| cost_usd_total | 0.0221 |
| latency_ms_mean | 34288.09 |
| latency_ms_p95 | 45787.8 |
| tokens_completion_total | 144509 |
| tokens_prompt_total | 111485 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 50 | 111485 | 144509 | 255994 | 0.0221 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.4013 · needs_judge_review: False · n_expec… | 34651.8 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 36806 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.4118 · needs_judge_review: False · n_expec… | 38654.9 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 25794 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4354 · needs_judge_review: False · n_expec… | 33016.8 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.278 · needs_judge_review: False · n_expect… | 30981.9 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 34277.3 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.6833 · needs_judge_review: True · n_expect… | 27226 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 20781.6 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 37425.1 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.6125 · needs_judge_review: False · n_expec… | 42200 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 27536.7 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 26710.4 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.6572 · needs_judge_review: False · n_expec… | 42556.8 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.2874 · needs_judge_review: False · n_expec… | 51940.8 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.575 · needs_judge_review: False · n_expect… | 27145.8 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 24473.2 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 38987.2 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.5298 · needs_judge_review: True · n_expect… | 34583.2 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.3409 · needs_judge_review: False · n_expec… | 26575.3 | — |
| corpus:ground_truth:train:campbell-l/inbox/488. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 28201.6 | — |
| corpus:ground_truth:train:lay-k/deleted_items/67. | overall_score: 0.5542 · needs_judge_review: True · n_expect… | 32554.7 | — |
| corpus:ground_truth:train:shackleton-s/all_documents/4886. | overall_score: 0.925 · needs_judge_review: True · n_expecte… | 35166.4 | — |
| corpus:ground_truth:train:farmer-d/all_documents/2959. | overall_score: 0.5227 · needs_judge_review: False · n_expec… | 36702.3 | — |
| corpus:ground_truth:train:jones-t/inbox/61. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 21717.5 | — |
| corpus:ground_truth:train:holst-k/inbox/99. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 29090.1 | — |
| corpus:ground_truth:train:skilling-j/inbox/31. | overall_score: 0.4071 · needs_judge_review: False · n_expec… | 48938.9 | — |
| corpus:ground_truth:train:kaminski-v/_sent_mail/1015. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 44625.4 | — |
| corpus:ground_truth:train:hendrickson-s/deleted_items/120. | overall_score: 0.6136 · needs_judge_review: False · n_expec… | 34247.5 | — |
| corpus:ground_truth:train:hain-m/all_documents/675. | overall_score: 0.875 · needs_judge_review: True · n_expecte… | 29065.5 | — |
| corpus:ground_truth:train:jones-t/all_documents/10848. | overall_score: 0.5417 · needs_judge_review: False · n_expec… | 36795.4 | — |
| corpus:ground_truth:train:cash-m/all_documents/552. | overall_score: 0.4702 · needs_judge_review: False · n_expec… | 29073.4 | — |
| corpus:ground_truth:train:lewis-a/deleted_items/747. | overall_score: 0.1662 · needs_judge_review: False · n_expec… | 44774.6 | — |
| corpus:ground_truth:train:haedicke-m/all_documents/4969. | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 45595.6 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/184. | overall_score: 0.4118 · needs_judge_review: False · n_expec… | 30389.2 | — |
| corpus:ground_truth:train:schoolcraft-d/deleted_items/689. | overall_score: 0.3826 · needs_judge_review: False · n_expec… | 41391 | — |
| corpus:ground_truth:train:taylor-m/inbox/219. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 34148.3 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/2276. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 33450.6 | — |
| corpus:ground_truth:train:kaminski-v/deleted_items/1330. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 45787.8 | — |
| corpus:ground_truth:train:buy-r/inbox/411. | overall_score: 0.4763 · needs_judge_review: True · n_expect… | 38510 | — |
| corpus:ground_truth:train:shankman-j/all_documents/94. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 29282.8 | — |
| corpus:ground_truth:train:baughman-d/deleted_items/292. | overall_score: 0.4066 · needs_judge_review: False · n_expec… | 35345.1 | — |
| corpus:ground_truth:train:mann-k/_sent_mail/3284. | overall_score: 0.3611 · needs_judge_review: False · n_expec… | 33484.1 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/28332. | overall_score: 0.5278 · needs_judge_review: False · n_expec… | 22813.9 | — |
| corpus:ground_truth:train:rapp-b/inbox/251. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 42571.6 | — |
| corpus:ground_truth:train:smith-m/_sent_mail/70. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 23492.1 | — |
| corpus:ground_truth:train:hain-m/all_documents/641. | overall_score: 0.4127 · needs_judge_review: False · n_expec… | 40343.3 | — |
| corpus:ground_truth:train:skilling-j/inbox/1231. | overall_score: 0.323 · needs_judge_review: False · n_expect… | 45031.8 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/11714. | overall_score: 0.7987 · needs_judge_review: False · n_expec… | 25599.6 | — |
| corpus:ground_truth:train:bailey-s/deleted_items/59. | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 33889.6 | — |
