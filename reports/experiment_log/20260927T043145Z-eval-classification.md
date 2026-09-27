## 20260927T043145Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: 782ddeb · dirty: True |
| started / finished | 2026-09-27T04:31:45+00:00 → 2026-09-27T04:34:57+00:00 |
| duration_s | 194.3 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:property:261501663.txt, corpus:gr… |
| config | ground_truth |
| filenames | property:261501663.txt, inpatient:196841176990879:1.txt, in… |
| n_selected | 20 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260927T043145Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260927T043145Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.7 |
| errors | 0 |
| n | 20 |
| scorer_errors | 0 |
| subclass_accuracy | 0.05 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.1493 |
| latency_ms_mean | 33056.525 |
| latency_ms_p95 | 133971.5 |
| tokens_completion_total | 16132 |
| tokens_prompt_total | 1213021 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 150 | 1213021 | 16132 | 1229153 | 0.1493 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:property:261501663.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 5656.4 | — |
| corpus:ground_truth:train:inpatient:196841176990879:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 4870.5 | — |
| corpus:ground_truth:train:insurbias-425.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 4674 | — |
| corpus:ground_truth:train:brawner-s/all_documents/59. | predicted_doc_class: correspondence · expected_doc_class: c… | 4966.8 | — |
| corpus:ground_truth:train:0000912057-01-507164_a2041839zex-… | predicted_doc_class: contract · expected_doc_class: corpora… | 9131 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/9309. | predicted_doc_class: correspondence · expected_doc_class: c… | 5079.1 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/9178. | predicted_doc_class: correspondence · expected_doc_class: c… | 5620.5 | — |
| corpus:ground_truth:train:0000950130-01-502904_dex211.txt | predicted_doc_class: corporate_record · expected_doc_class:… | 5333.8 | — |
| corpus:ground_truth:train:inpatient:196091177001318:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 4526.6 | — |
| corpus:ground_truth:train:inpatient:196831176969260:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 4084.8 | — |
| corpus:ground_truth:train:0001193125-14-273392_d715499dex41… | predicted_doc_class: contract · expected_doc_class: corpora… | 5529.6 | — |
| corpus:ground_truth:train:contract_117_merger_agreement.txt | predicted_doc_class: contract · expected_doc_class: merger_… | 131706.1 | — |
| corpus:ground_truth:train:property:262952775.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 9217.7 | — |
| corpus:ground_truth:train:0000950123-03-010752_y88696a1exv4… | predicted_doc_class: contract · expected_doc_class: corpora… | 133971.5 | — |
| corpus:ground_truth:train:contract_4_merger_agreement.txt | predicted_doc_class: contract · expected_doc_class: merger_… | 125820.9 | — |
| corpus:ground_truth:train:carrier:887493388020303.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 3213.8 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | predicted_doc_class: contract · expected_doc_class: merger_… | 180824.6 | — |
| corpus:ground_truth:train:inpatient:196641176967981:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 4657.4 | — |
| corpus:ground_truth:train:0001047469-06-011763_a2173128zex-… | predicted_doc_class: corporate_record · expected_doc_class:… | 7876.7 | — |
| corpus:ground_truth:train:outpatient:542502281397875:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 4368.7 | — |
