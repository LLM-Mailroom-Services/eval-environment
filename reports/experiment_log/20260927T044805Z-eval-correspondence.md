## 20260927T044805Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: 8a4a1c4 · dirty: True |
| started / finished | 2026-09-27T04:48:05+00:00 → 2026-09-27T04:51:09+00:00 |
| duration_s | 185.8 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:blair-l/meetings/608., corpus:gro… |
| config | ground_truth |
| filenames | blair-l/meetings/608., lokey-t/inbox/250., kean-s/all_docum… |
| n_selected | 20 |
| n_total | 915 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:correspondence |
| subset_manifest_jsonl | data/experiments/20260927T044805Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T044805Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.0999 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0358 |
| latency_ms_mean | 64418.015 |
| latency_ms_p95 | 88638.8 |
| tokens_completion_total | 120989 |
| tokens_prompt_total | 93101 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 34 | 93101 | 120989 | 214090 | 0.0358 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 87175.6 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 86054.5 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 87315.2 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 1895.7 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 78518.8 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.3057 · needs_judge_review: False · n_expec… | 3177.1 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 87207.3 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 87331.3 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 30551.7 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 86344.1 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 85680.9 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.3368 · needs_judge_review: False · n_expec… | 35309.1 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 89756.2 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 88546.2 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 88638.8 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 88628.5 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 227.8 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 88591.4 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 1389.8 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 86020.3 | — |
