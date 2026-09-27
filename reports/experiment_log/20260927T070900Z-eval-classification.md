## 20260927T070900Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / real |
| model / prompt | ibm-granite/granite-4.2-8b / None |
| trace backend | braintrust |
| git | commit: 1d9f8d2 · dirty: True |
| started / finished | 2026-09-27T07:09:00+00:00 → 2026-09-27T07:12:02+00:00 |
| duration_s | 184.3 |
| comparison report | reports/api-comparisons/granite-4.2-8b/classification/RUN-2… |
| error | — |

### Run configuration

| Param | Value |
|---|---|
| concurrency | 8 |
| decode_budget_applied | sampling_injected: True · max_tokens_by_agent: {'contracts_… |
| decode_call_timeout_s | 600 |
| decode_profile | granite-4.2-8b |
| decode_sampling | temperature: 1.0 · top_p: 0.95 · seed: 42 |
| dry_run | ✗ |
| n | — |
| resumed_from | — |
| sample | 20 |
| scorer | classification |
| seed | 42 |
| skipped_already_run | 0 |
| thinking_recovered | 0 |

### Cost cap

| Key | Value |
|---|---|
| cap_usd | 1.5 |
| cost_usd_est | 0.0644 |
| status | under_cap |

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
| subset_manifest_jsonl | data/experiments/20260927T070900Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260927T070900Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.9 |
| errors | 0 |
| n | 20 |
| scorer_errors | 0 |
| subclass_accuracy | 0.6 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0644 |
| cost_usd_total | 0.0644 |
| expected_cost_usd | 0.8 |
| latency_ms_mean | 26860.855 |
| latency_ms_p95 | 111121.3 |
| tokens_completion_total | 33329 |
| tokens_prompt_total | 933912 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 118 | 933912 | 33329 | 967241 | 0.0644 | ibm-granite/granite-4.2-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:property:261501663.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 3669.6 | — |
| corpus:ground_truth:train:inpatient:196841176990879:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 9747.9 | — |
| corpus:ground_truth:train:insurbias-425.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 2856.4 | — |
| corpus:ground_truth:train:brawner-s/all_documents/59. | predicted_doc_class: correspondence · expected_doc_class: c… | 3899.3 | — |
| corpus:ground_truth:train:0000912057-01-507164_a2041839zex-… | predicted_doc_class: corporate_record · expected_doc_class:… | 6304.6 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/9309. | predicted_doc_class: correspondence · expected_doc_class: c… | 3205.4 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/9178. | predicted_doc_class: correspondence · expected_doc_class: c… | 2842.6 | — |
| corpus:ground_truth:train:0000950130-01-502904_dex211.txt | predicted_doc_class: corporate_record · expected_doc_class:… | 2702 | — |
| corpus:ground_truth:train:inpatient:196091177001318:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 2758.7 | — |
| corpus:ground_truth:train:inpatient:196831176969260:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 3111 | — |
| corpus:ground_truth:train:0001193125-14-273392_d715499dex41… | predicted_doc_class: corporate_record · expected_doc_class:… | 3100.9 | — |
| corpus:ground_truth:train:contract_117_merger_agreement.txt | predicted_doc_class: unknown · expected_doc_class: merger_a… | 111121.3 | — |
| corpus:ground_truth:train:property:262952775.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 5167.6 | — |
| corpus:ground_truth:train:0000950123-03-010752_y88696a1exv4… | predicted_doc_class: corporate_record · expected_doc_class:… | 97546.6 | — |
| corpus:ground_truth:train:contract_4_merger_agreement.txt | predicted_doc_class: unknown · expected_doc_class: merger_a… | 92120.1 | — |
| corpus:ground_truth:train:carrier:887493388020303.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 2421.2 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | predicted_doc_class: merger_agreement · expected_doc_class:… | 174013.2 | — |
| corpus:ground_truth:train:inpatient:196641176967981:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 2624.8 | — |
| corpus:ground_truth:train:0001047469-06-011763_a2173128zex-… | predicted_doc_class: corporate_record · expected_doc_class:… | 4998.6 | — |
| corpus:ground_truth:train:outpatient:542502281397875:1.txt | predicted_doc_class: insurance_claim · expected_doc_class: … | 3005.3 | — |
