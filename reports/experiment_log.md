# mailroom-evals — experiment log

| run_id | family | task | mode | model | subset | n | key metric | errors |
|---|---|---|---|---|---|---|---|---|
| 20260926T223144Z-eval-arbiter | eval | arbiter | mock | mock-model | fixtures | 2 | — | 0 |
| 20260926T223145Z-eval-archivist | eval | archivist | mock | — | fixtures | 2 | — | 0 |
| 20260926T223146Z-eval-boss | eval | boss | mock | mock-model | fixtures | 2 | — | 0 |
| 20260926T223149Z-eval-classification | eval | classification | mock | qwen/qwen3.7-flash | full | 2 | class_accuracy=0.0 | 0 |
| 20260926T223150Z-eval-contracts | eval | contracts | mock | qwen/qwen3.7-flash | class:contract | 2 | — | 0 |
| 20260926T223151Z-eval-corporate_records | eval | corporate_records | mock | mock-model | class:corporate_record | 2 | — | 0 |
| 20260926T223153Z-eval-correspondence | eval | correspondence | mock | mock-model | class:correspondence | 2 | — | 0 |
| 20260926T223154Z-eval-insurance_claims | eval | insurance_claims | mock | mock-model | class:insurance_claim | 2 | — | 0 |
| 20260926T223157Z-eval-intake | eval | intake | mock | mock-model | full | 2 | — | 0 |
| 20260926T223158Z-eval-judge_arbiter | eval | judge_arbiter | mock | qwen/qwen3.7-flash | fixtures | 2 | — | 0 |
| 20260926T223159Z-eval-merger_agreement | eval | merger_agreement | mock | qwen/qwen3.7-flash | class:merger_agreement | 2 | — | 0 |
| 20260926T223201Z-eval-pipeline_chain | eval | pipeline_chain | mock | qwen/qwen3.7-flash | pilot | 2 | class_accuracy=0.0 | 0 |
| 20260926T223211Z-eval-contracts | eval | contracts | real | — | class:contract | 0 | — | 0 |
| 20260926T223222Z-eval-contracts | eval | contracts | real | qwen/qwen3.7-flash | class:contract | 1 | — | 0 |
| 20260926T224038Z-eval-contracts | eval | contracts | real | qwen/qwen3.7-flash | class:contract | 1 | — | 0 |
| 20260926T232531Z-eval-arbiter | eval | arbiter | mock | mock-model | fixtures | 2 | — | 0 |
| 20260926T232531Z-eval-archivist | eval | archivist | mock | — | fixtures | 2 | — | 0 |
| 20260926T232533Z-eval-boss | eval | boss | mock | mock-model | fixtures | 2 | — | 0 |
| 20260926T232536Z-eval-classification | eval | classification | mock | qwen/qwen3.7-flash | full | 2 | class_accuracy=0.0 | 0 |
| 20260926T232538Z-eval-contracts | eval | contracts | mock | qwen/qwen3.7-flash | class:contract | 2 | — | 0 |
| 20260926T232539Z-eval-corporate_records | eval | corporate_records | mock | mock-model | class:corporate_record | 2 | — | 0 |
| 20260926T232540Z-eval-correspondence | eval | correspondence | mock | mock-model | class:correspondence | 2 | — | 0 |
| 20260926T232542Z-eval-insurance_claims | eval | insurance_claims | mock | mock-model | class:insurance_claim | 2 | — | 0 |
| 20260926T232544Z-eval-intake | eval | intake | mock | mock-model | full | 2 | — | 0 |
| 20260926T232545Z-eval-judge_arbiter | eval | judge_arbiter | mock | qwen/qwen3.7-flash | fixtures | 2 | — | 0 |
| 20260926T232546Z-eval-merger_agreement | eval | merger_agreement | mock | qwen/qwen3.7-flash | class:merger_agreement | 2 | — | 0 |
| 20260926T232547Z-eval-pipeline_chain | eval | pipeline_chain | mock | qwen/qwen3.7-flash | pilot | 2 | class_accuracy=0.0 | 0 |
| 20260926T232556Z-eval-contracts | eval | contracts | real | — | class:contract | 0 | — | 0 |
| 20260926T232610Z-eval-contracts | eval | contracts | real | qwen/qwen3.7-flash | class:contract | 1 | — | 0 |
| 20260926T234358Z-eval-correspondence | eval | correspondence | real | qwen/qwen3-8b | class:correspondence | 20 | — | 0 |
| 20260926T234603Z-eval-insurance_claims | eval | insurance_claims | real | qwen/qwen3-8b | class:insurance_claim | 20 | — | 0 |
| 20260926T235347Z-eval-contracts | eval | contracts | real | qwen/qwen3-8b | class:contract | 20 | — | 0 |
| 20260927T004231Z-eval-merger_agreement | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 1 | — | 0 |
| 20260927T005233Z-eval-merger_agreement | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 3 | — | 1 |
| 20260927T011209Z-eval-merger_agreement | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 1 | — | 0 |
| 20260927T014814Z-eval-merger_agreement | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 2 | — | 0 |
| 20260927T020724Z-eval-merger_agreement | eval | merger_agreement | real | qwen/qwen3.7-flash | class:merger_agreement | 2 | — | 0 |
| 20260927T022750Z-eval-merger_agreement | eval | merger_agreement | real | qwen/qwen3.7-flash | class:merger_agreement | 20 | — | 0 |
| 20260927T022738Z-eval-correspondence | eval | correspondence | real | qwen/qwen3-8b | class:correspondence | 20 | — | 0 |
| 20260927T023050Z-eval-insurance_claims | eval | insurance_claims | real | qwen/qwen3-8b | class:insurance_claim | 20 | — | 0 |
| 20260927T022810Z-eval-corporate_records | eval | corporate_records | real | qwen/qwen3-8b | class:corporate_record | 20 | — | 0 |
| 20260927T023347Z-eval-contracts | eval | contracts | real | qwen/qwen3-8b | class:contract | 20 | — | 0 |
| 20260927T033031Z-eval-correspondence | eval | correspondence | real | qwen/qwen3-8b | class:correspondence | 20 | — | 0 |
| 20260927T035135Z-eval-insurance_claims | eval | insurance_claims | real | qwen/qwen3-8b | class:insurance_claim | 20 | — | 0 |

---

## 20260926T223144Z-eval-arbiter

| Key | Value |
|---|---|
| family / task | eval / arbiter |
| invoke / mode | node / mock |
| model / prompt | mock-model / arbiter_v1 |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:44+00:00 → 2026-09-26T22:31:45+00:00 |
| duration_s | 4.1 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T223144Z-eval-arbiter/subset_manif… |
| subset_manifest_path | data/experiments/20260926T223144Z-eval-arbiter/subset_manif… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| decision_valid | 1 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 218.2 |
| latency_ms_p95 | 421.2 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| arbiter | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: human_review · decision_valid: 1 | 421.2 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: human_review · decision_valid: 1 | 15.2 | — |


## 20260926T223145Z-eval-archivist

| Key | Value |
|---|---|
| family / task | eval / archivist |
| invoke / mode | node / mock |
| model / prompt | None / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:45+00:00 → 2026-09-26T22:31:45+00:00 |
| duration_s | 0.9 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T223145Z-eval-archivist/subset_man… |
| subset_manifest_path | data/experiments/20260926T223145Z-eval-archivist/subset_man… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| archived_ok | 1 |
| audit_ok | 1 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |
| sha256_ok | 1 |
| stage_ok | 1 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 95.6 |
| latency_ms_p95 | 106.3 |
| tokens_completion_total | 0 |
| tokens_prompt_total | 0 |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | archived_ok: 1 · audit_ok: 1 · sha256_ok: 1 · stage_ok: 1 | 106.3 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | archived_ok: 1 · audit_ok: 1 · sha256_ok: 1 · stage_ok: 1 | 84.9 | — |


## 20260926T223146Z-eval-boss

| Key | Value |
|---|---|
| family / task | eval / boss |
| invoke / mode | node / mock |
| model / prompt | mock-model / boss_v1 |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:46+00:00 → 2026-09-26T22:31:46+00:00 |
| duration_s | 0.7 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T223146Z-eval-boss/subset_manifest… |
| subset_manifest_path | data/experiments/20260926T223146Z-eval-boss/subset_manifest… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| decision_agrees | 0.0 |
| decision_valid | 1 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 30.85 |
| latency_ms_p95 | 47.6 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| boss | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: approved · decision_valid: 1 · decision_agrees: 0 | 47.6 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: approved · decision_valid: 1 | 14.1 | — |


## 20260926T223149Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:49+00:00 → 2026-09-26T22:31:49+00:00 |
| duration_s | 3.1 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260926T223149Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260926T223149Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |
| subclass_accuracy | 0.0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0001 |
| latency_ms_mean | 33.45 |
| latency_ms_p95 | 52.2 |
| tokens_completion_total | 360 |
| tokens_prompt_total | 720 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 6 | 720 | 360 | 1080 | 0.0001 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | predicted_doc_class: contract · expected_doc_class: corpora… | 52.2 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | predicted_doc_class: contract · expected_doc_class: corpora… | 14.7 | — |


## 20260926T223150Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:50+00:00 → 2026-09-26T22:31:51+00:00 |
| duration_s | 1.5 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 2 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T223150Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T223150Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0 |
| latency_ms_mean | 38.95 |
| latency_ms_p95 | 63.1 |
| tokens_completion_total | 120 |
| tokens_prompt_total | 240 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 2 | 240 | 120 | 360 | 0 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 63.1 | — |
| corpus:ground_truth:train:ABILITYINC_06_15_2020-EX-4.25-SER… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14.8 | — |


## 20260926T223151Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:51+00:00 → 2026-09-26T22:31:52+00:00 |
| duration_s | 1.3 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 403 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:corporate_record |
| subset_manifest_jsonl | data/experiments/20260926T223151Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260926T223151Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 34.15 |
| latency_ms_p95 | 51.8 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 51.8 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | overall_score: 0.0 · needs_judge_review: False · n_expected… | 16.5 | — |


## 20260926T223153Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:53+00:00 → 2026-09-26T22:31:53+00:00 |
| duration_s | 1.3 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:allen-p/deleted_items/65., corpus… |
| config | ground_truth |
| filenames | allen-p/deleted_items/65., arnold-j/deleted_items/395. |
| n_selected | 2 |
| n_total | 915 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:correspondence |
| subset_manifest_jsonl | data/experiments/20260926T223153Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260926T223153Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 39.6 |
| latency_ms_p95 | 62.9 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:allen-p/deleted_items/65. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 62.9 | — |
| corpus:ground_truth:train:arnold-j/deleted_items/395. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 16.3 | — |


## 20260926T223154Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:54+00:00 → 2026-09-26T22:31:56+00:00 |
| duration_s | 2.5 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:carrier:887013387879564.txt, corp… |
| config | ground_truth |
| filenames | carrier:887013387879564.txt, carrier:887023387120037.txt |
| n_selected | 2 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260926T223154Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260926T223154Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.697 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 40 |
| latency_ms_p95 | 54.6 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:carrier:887013387879564.txt | overall_score: 0.697 · needs_judge_review: True · n_expecte… | 54.6 | — |
| corpus:ground_truth:train:carrier:887023387120037.txt | overall_score: 0.697 · needs_judge_review: True · n_expecte… | 25.4 | — |


## 20260926T223157Z-eval-intake

| Key | Value |
|---|---|
| family / task | eval / intake |
| invoke / mode | node / mock |
| model / prompt | mock-model / intake_v1 |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:57+00:00 → 2026-09-26T22:31:58+00:00 |
| duration_s | 1.8 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260926T223157Z-eval-intake/subset_manife… |
| subset_manifest_path | data/experiments/20260926T223157Z-eval-intake/subset_manife… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| messy_flag | 0.0 |
| n | 2 |
| no_truncation | 1 |
| scorer_errors | 0 |
| triage_agrees | 0.0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 93.55 |
| latency_ms_p95 | 118.4 |
| tokens_completion_total | 40 |
| tokens_prompt_total | 40 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| intake | 4 | 40 | 40 | 80 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | no_truncation: 1 · messy_flag: 0 · triage_class: unknown · … | 118.4 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | no_truncation: 1 · messy_flag: 0 · triage_class: unknown · … | 68.7 | — |


## 20260926T223158Z-eval-judge_arbiter

| Key | Value |
|---|---|
| family / task | eval / judge_arbiter |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:58+00:00 → 2026-09-26T22:31:58+00:00 |
| duration_s | 0.7 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T223158Z-eval-judge_arbiter/subset… |
| subset_manifest_path | data/experiments/20260926T223158Z-eval-judge_arbiter/subset… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| judge_agrees | 0.5 |
| judge_score | 1 |
| n | 2 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0 |
| latency_ms_mean | 1.3 |
| latency_ms_p95 | 2 |
| tokens_completion_total | 130 |
| tokens_prompt_total | 250 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 2 | 240 | 120 | 360 | 0 | qwen/qwen3.7-flash |
| judge | 1 | 10 | 10 | 20 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | judge_label: complete · judge_score: 1.0 · judge_agrees: 0 | 2 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | judge_label: skipped · judge_score: None · judge_agrees: 1 | 0.6 | — |


## 20260926T223159Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:59+00:00 → 2026-09-26T22:32:00+00:00 |
| duration_s | 1.4 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_0_merger_agreement.txt, … |
| config | ground_truth |
| filenames | contract_0_merger_agreement.txt, contract_100_merger_agreem… |
| n_selected | 2 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260926T223159Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260926T223159Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0001 |
| latency_ms_mean | 49.8 |
| latency_ms_p95 | 75.4 |
| tokens_completion_total | 540 |
| tokens_prompt_total | 1080 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 9 | 1080 | 540 | 1620 | 0.0001 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_0_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 75.4 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 24.2 | — |


## 20260926T223201Z-eval-pipeline_chain

| Key | Value |
|---|---|
| family / task | eval / pipeline_chain |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:32:01+00:00 → 2026-09-26T22:32:03+00:00 |
| duration_s | 3.5 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:Lucius-Morningstar/docclass-pilot:train+test:0001062… |
| config | Lucius-Morningstar/docclass-pilot |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001469709-14-0000… |
| n_selected | 2 |
| n_total | 138 |
| repo | Lucius-Morningstar/docclass-pilot |
| revision | — |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | pilot |
| subset_manifest_jsonl | data/experiments/20260926T223201Z-eval-pipeline_chain/subse… |
| subset_manifest_path | data/experiments/20260926T223201Z-eval-pipeline_chain/subse… |
| subset_spec | kind: corpus · value: pilot |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 441.5 |
| latency_ms_p95 | 662.2 |
| tokens_completion_total | 420 |
| tokens_prompt_total | 780 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 6 | 720 | 360 | 1080 | 0.0001 | qwen/qwen3.7-flash |
| intake | 4 | 40 | 40 | 80 | — | mock-model |
| sorter_reviewer | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:Lucius-Morningstar/docclass-pilot:train+test:0001062… | final_stage: review · overall_score: 0.0 · needs_judge_revi… | 662.2 | — |
| corpus:Lucius-Morningstar/docclass-pilot:train+test:0001469… | final_stage: review · overall_score: 0.0 · needs_judge_revi… | 220.8 | — |


## 20260926T223211Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / real |
| model / prompt | None / None |
| trace backend | braintrust |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:32:11+00:00 → 2026-09-26T22:32:11+00:00 |
| duration_s | 2.1 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 1 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T223211Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T223211Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 0 |


## 20260926T223222Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:32:22+00:00 → 2026-09-26T22:32:43+00:00 |
| duration_s | 22.5 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 1 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T223222Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T223222Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.7 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0005 |
| latency_ms_mean | 12445.4 |
| latency_ms_p95 | 12445.4 |
| tokens_completion_total | 1519 |
| tokens_prompt_total | 10825 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 1 | 10825 | 1519 | 12344 | 0.0005 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… | overall_score: 0.7 · needs_judge_review: False · n_expected… | 12445.4 | — |


## 20260926T224038Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: a32b39a · dirty: True |
| started / finished | 2026-09-26T22:40:38+00:00 → 2026-09-26T22:40:59+00:00 |
| duration_s | 22.5 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 1 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T224038Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T224038Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.7 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0005 |
| latency_ms_mean | 12447.4 |
| latency_ms_p95 | 12447.4 |
| tokens_completion_total | 1591 |
| tokens_prompt_total | 10825 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 1 | 10825 | 1591 | 12416 | 0.0005 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… | overall_score: 0.7 · needs_judge_review: False · n_expected… | 12447.4 | — |


## 20260926T232531Z-eval-arbiter

| Key | Value |
|---|---|
| family / task | eval / arbiter |
| invoke / mode | node / mock |
| model / prompt | mock-model / arbiter_v1 |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:31+00:00 → 2026-09-26T23:25:31+00:00 |
| duration_s | 1.9 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T232531Z-eval-arbiter/subset_manif… |
| subset_manifest_path | data/experiments/20260926T232531Z-eval-arbiter/subset_manif… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| decision_valid | 1 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 99.5 |
| latency_ms_p95 | 184.4 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| arbiter | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: human_review · decision_valid: 1 | 184.4 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: human_review · decision_valid: 1 | 14.6 | — |


## 20260926T232531Z-eval-archivist

| Key | Value |
|---|---|
| family / task | eval / archivist |
| invoke / mode | node / mock |
| model / prompt | None / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:31+00:00 → 2026-09-26T23:25:32+00:00 |
| duration_s | 0.8 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T232531Z-eval-archivist/subset_man… |
| subset_manifest_path | data/experiments/20260926T232531Z-eval-archivist/subset_man… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| archived_ok | 1 |
| audit_ok | 1 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |
| sha256_ok | 1 |
| stage_ok | 1 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 75.5 |
| latency_ms_p95 | 96.7 |
| tokens_completion_total | 0 |
| tokens_prompt_total | 0 |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | archived_ok: 1 · audit_ok: 1 · sha256_ok: 1 · stage_ok: 1 | 96.7 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | archived_ok: 1 · audit_ok: 1 · sha256_ok: 1 · stage_ok: 1 | 54.3 | — |


## 20260926T232533Z-eval-boss

| Key | Value |
|---|---|
| family / task | eval / boss |
| invoke / mode | node / mock |
| model / prompt | mock-model / boss_v1 |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:33+00:00 → 2026-09-26T23:25:35+00:00 |
| duration_s | 3 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T232533Z-eval-boss/subset_manifest… |
| subset_manifest_path | data/experiments/20260926T232533Z-eval-boss/subset_manifest… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| decision_agrees | 0.0 |
| decision_valid | 1 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 607.35 |
| latency_ms_p95 | 1201.5 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| boss | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: approved · decision_valid: 1 · decision_agrees: 0 | 1201.5 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | decision: approved · decision_valid: 1 | 13.2 | — |


## 20260926T232536Z-eval-classification

| Key | Value |
|---|---|
| family / task | eval / classification |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:36+00:00 → 2026-09-26T23:25:37+00:00 |
| duration_s | 1.8 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260926T232536Z-eval-classification/subse… |
| subset_manifest_path | data/experiments/20260926T232536Z-eval-classification/subse… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |
| subclass_accuracy | 0.0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0001 |
| latency_ms_mean | 38.15 |
| latency_ms_p95 | 61.6 |
| tokens_completion_total | 360 |
| tokens_prompt_total | 720 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 6 | 720 | 360 | 1080 | 0.0001 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | predicted_doc_class: contract · expected_doc_class: corpora… | 61.6 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | predicted_doc_class: contract · expected_doc_class: corpora… | 14.7 | — |


## 20260926T232538Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:38+00:00 → 2026-09-26T23:25:38+00:00 |
| duration_s | 1.4 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 2 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T232538Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T232538Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0 |
| latency_ms_mean | 36.65 |
| latency_ms_p95 | 57.4 |
| tokens_completion_total | 120 |
| tokens_prompt_total | 240 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 2 | 240 | 120 | 360 | 0 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 57.4 | — |
| corpus:ground_truth:train:ABILITYINC_06_15_2020-EX-4.25-SER… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15.9 | — |


## 20260926T232539Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:39+00:00 → 2026-09-26T23:25:40+00:00 |
| duration_s | 1.4 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 403 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:corporate_record |
| subset_manifest_jsonl | data/experiments/20260926T232539Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260926T232539Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 41.55 |
| latency_ms_p95 | 66.6 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 66.6 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | overall_score: 0.0 · needs_judge_review: False · n_expected… | 16.5 | — |


## 20260926T232540Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:40+00:00 → 2026-09-26T23:25:41+00:00 |
| duration_s | 1.4 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:allen-p/deleted_items/65., corpus… |
| config | ground_truth |
| filenames | allen-p/deleted_items/65., arnold-j/deleted_items/395. |
| n_selected | 2 |
| n_total | 915 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:correspondence |
| subset_manifest_jsonl | data/experiments/20260926T232540Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260926T232540Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 48.95 |
| latency_ms_p95 | 79.7 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:allen-p/deleted_items/65. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 79.7 | — |
| corpus:ground_truth:train:arnold-j/deleted_items/395. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18.2 | — |


## 20260926T232542Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | node / mock |
| model / prompt | mock-model / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:42+00:00 → 2026-09-26T23:25:43+00:00 |
| duration_s | 2 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:carrier:887013387879564.txt, corp… |
| config | ground_truth |
| filenames | carrier:887013387879564.txt, carrier:887023387120037.txt |
| n_selected | 2 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260926T232542Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260926T232542Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.697 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 50.2 |
| latency_ms_p95 | 77.9 |
| tokens_completion_total | 20 |
| tokens_prompt_total | 20 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:carrier:887013387879564.txt | overall_score: 0.697 · needs_judge_review: True · n_expecte… | 77.9 | — |
| corpus:ground_truth:train:carrier:887023387120037.txt | overall_score: 0.697 · needs_judge_review: True · n_expecte… | 22.5 | — |


## 20260926T232544Z-eval-intake

| Key | Value |
|---|---|
| family / task | eval / intake |
| invoke / mode | node / mock |
| model / prompt | mock-model / intake_v1 |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:44+00:00 → 2026-09-26T23:25:45+00:00 |
| duration_s | 1.7 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… |
| config | ground_truth |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001078782-12-0013… |
| n_selected | 2 |
| n_total | 2979 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | full |
| subset_manifest_jsonl | data/experiments/20260926T232544Z-eval-intake/subset_manife… |
| subset_manifest_path | data/experiments/20260926T232544Z-eval-intake/subset_manife… |
| subset_spec | kind: full · value: None |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| messy_flag | 0.0 |
| n | 2 |
| no_truncation | 1 |
| scorer_errors | 0 |
| triage_agrees | 0.0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 89.75 |
| latency_ms_p95 | 114.1 |
| tokens_completion_total | 40 |
| tokens_prompt_total | 40 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| intake | 4 | 40 | 40 | 80 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3… | no_truncation: 1 · messy_flag: 0 · triage_class: unknown · … | 114.1 | — |
| corpus:ground_truth:train:0001078782-12-001347_s1_ex3z2.htm | no_truncation: 1 · messy_flag: 0 · triage_class: unknown · … | 65.4 | — |


## 20260926T232545Z-eval-judge_arbiter

| Key | Value |
|---|---|
| family / task | eval / judge_arbiter |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:45+00:00 → 2026-09-26T23:25:45+00:00 |
| duration_s | 0.6 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T232545Z-eval-judge_arbiter/subset… |
| subset_manifest_path | data/experiments/20260926T232545Z-eval-judge_arbiter/subset… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| judge_agrees | 0.5 |
| judge_score | 1 |
| n | 2 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0 |
| latency_ms_mean | 0.95 |
| latency_ms_p95 | 1.4 |
| tokens_completion_total | 130 |
| tokens_prompt_total | 250 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 2 | 240 | 120 | 360 | 0 | qwen/qwen3.7-flash |
| judge | 1 | 10 | 10 | 20 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | judge_label: complete · judge_score: 1.0 · judge_agrees: 0 | 1.4 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | judge_label: skipped · judge_score: None · judge_agrees: 1 | 0.5 | — |


## 20260926T232546Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:46+00:00 → 2026-09-26T23:25:47+00:00 |
| duration_s | 1.4 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_0_merger_agreement.txt, … |
| config | ground_truth |
| filenames | contract_0_merger_agreement.txt, contract_100_merger_agreem… |
| n_selected | 2 |
| n_total | 135 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:merger_agreement |
| subset_manifest_jsonl | data/experiments/20260926T232546Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260926T232546Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0001 |
| latency_ms_mean | 53.8 |
| latency_ms_p95 | 89.2 |
| tokens_completion_total | 540 |
| tokens_prompt_total | 1080 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 9 | 1080 | 540 | 1620 | 0.0001 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_0_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 89.2 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18.4 | — |


## 20260926T232547Z-eval-pipeline_chain

| Key | Value |
|---|---|
| family / task | eval / pipeline_chain |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:47+00:00 → 2026-09-26T23:25:49+00:00 |
| duration_s | 1.7 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:Lucius-Morningstar/docclass-pilot:train+test:0001062… |
| config | Lucius-Morningstar/docclass-pilot |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001469709-14-0000… |
| n_selected | 2 |
| n_total | 138 |
| repo | Lucius-Morningstar/docclass-pilot |
| revision | — |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | pilot |
| subset_manifest_jsonl | data/experiments/20260926T232547Z-eval-pipeline_chain/subse… |
| subset_manifest_path | data/experiments/20260926T232547Z-eval-pipeline_chain/subse… |
| subset_spec | kind: corpus · value: pilot |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 193.55 |
| latency_ms_p95 | 225.3 |
| tokens_completion_total | 420 |
| tokens_prompt_total | 780 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 6 | 720 | 360 | 1080 | 0.0001 | qwen/qwen3.7-flash |
| intake | 4 | 40 | 40 | 80 | — | mock-model |
| sorter_reviewer | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:Lucius-Morningstar/docclass-pilot:train+test:0001062… | final_stage: review · overall_score: 0.0 · needs_judge_revi… | 225.3 | — |
| corpus:Lucius-Morningstar/docclass-pilot:train+test:0001469… | final_stage: review · overall_score: 0.0 · needs_judge_revi… | 161.8 | — |


## 20260926T232556Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / real |
| model / prompt | None / None |
| trace backend | braintrust |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:56+00:00 → 2026-09-26T23:25:56+00:00 |
| duration_s | 2.1 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 1 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T232556Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T232556Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 0 |


## 20260926T232610Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:26:10+00:00 → 2026-09-26T23:26:32+00:00 |
| duration_s | 24 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… |
| config | ground_truth |
| filenames | 2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co… |
| n_selected | 1 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T232610Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T232610Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.7167 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0005 |
| latency_ms_mean | 13026.6 |
| latency_ms_p95 | 13026.6 |
| tokens_completion_total | 1405 |
| tokens_prompt_total | 10825 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 1 | 10825 | 1405 | 12230 | 0.0005 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:2ThemartComInc_19990826_10-12G_EX… | overall_score: 0.7167 · needs_judge_review: False · n_expec… | 13026.6 | — |


## 20260926T234358Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fe120a8 · dirty: True |
| started / finished | 2026-09-26T23:43:58+00:00 → 2026-09-26T23:46:00+00:00 |
| duration_s | 123.4 |
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
| subset_manifest_jsonl | data/experiments/20260926T234358Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260926T234358Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.3179 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0077 |
| latency_ms_mean | 3861.845 |
| latency_ms_p95 | 5505.8 |
| tokens_completion_total | 3197 |
| tokens_prompt_total | 53521 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 20 | 53521 | 3197 | 56718 | 0.0077 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.4058 · needs_judge_review: True · n_expect… | 3953.3 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.3857 · needs_judge_review: False · n_expec… | 3065.9 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.3269 · needs_judge_review: False · n_expec… | 5018 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.2789 · needs_judge_review: False · n_expec… | 3020.5 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4409 · needs_judge_review: False · n_expec… | 4114.6 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.2607 · needs_judge_review: False · n_expec… | 4915.6 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.3244 · needs_judge_review: False · n_expec… | 4357.5 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.5552 · needs_judge_review: True · n_expect… | 3938.2 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.1109 · needs_judge_review: False · n_expec… | 2214.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.1947 · needs_judge_review: False · n_expec… | 3407.5 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.1872 · needs_judge_review: False · n_expec… | 3819.6 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.3143 · needs_judge_review: False · n_expec… | 2544.6 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.3558 · needs_judge_review: True · n_expect… | 3638.3 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.5783 · needs_judge_review: True · n_expect… | 4548.2 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.3464 · needs_judge_review: True · n_expect… | 5505.8 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.3909 · needs_judge_review: False · n_expec… | 3360.8 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.1109 · needs_judge_review: False · n_expec… | 2531 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.1683 · needs_judge_review: False · n_expec… | 6838.4 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.4465 · needs_judge_review: False · n_expec… | 3502.1 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.1752 · needs_judge_review: False · n_expec… | 2942.5 | — |


## 20260926T234603Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fe120a8 · dirty: True |
| started / finished | 2026-09-26T23:46:03+00:00 → 2026-09-26T23:49:16+00:00 |
| duration_s | 195 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:pde:233384494245864.txt, corpus:g… |
| config | ground_truth |
| filenames | pde:233384494245864.txt, insurbias-624.txt, carrier:8874733… |
| n_selected | 20 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260926T234603Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260926T234603Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.8056 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0095 |
| latency_ms_mean | 8608.955 |
| latency_ms_p95 | 11533 |
| tokens_completion_total | 7641 |
| tokens_prompt_total | 51248 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 51248 | 7641 | 58889 | 0.0095 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.728 · needs_judge_review: True · n_expecte… | 7084.4 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8537 · needs_judge_review: False · n_expec… | 6526.5 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7548 · needs_judge_review: True · n_expect… | 7953.5 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.7482 · needs_judge_review: True · n_expect… | 7621.3 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7994 · needs_judge_review: True · n_expect… | 8042.5 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.7327 · needs_judge_review: True · n_expect… | 7325.3 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8822 · needs_judge_review: True · n_expect… | 10141.2 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.8882 · needs_judge_review: True · n_expect… | 7510.6 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9804 · needs_judge_review: True · n_expect… | 6857.3 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.7288 · needs_judge_review: True · n_expect… | 11016.1 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7272 · needs_judge_review: True · n_expect… | 7443.6 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.864 · needs_judge_review: True · n_expecte… | 6167.4 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8742 · needs_judge_review: True · n_expect… | 10884.9 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.8887 · needs_judge_review: True · n_expect… | 7756.3 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.7058 · needs_judge_review: True · n_expect… | 6114.1 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.7491 · needs_judge_review: True · n_expect… | 7683.6 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.8238 · needs_judge_review: True · n_expect… | 21420.3 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.8889 · needs_judge_review: True · n_expect… | 6561.2 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.7277 · needs_judge_review: True · n_expect… | 6536 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.767 · needs_judge_review: True · n_expecte… | 11533 | — |


## 20260926T235347Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | node / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: d386cde · dirty: True |
| started / finished | 2026-09-26T23:53:47+00:00 → 2026-09-27T00:15:10+00:00 |
| duration_s | 1284.9 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… |
| config | ground_truth |
| filenames | MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PD… |
| n_selected | 20 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260926T235347Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260926T235347Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.6199 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0584 |
| latency_ms_mean | 56685.48 |
| latency_ms_p95 | 111956.8 |
| tokens_completion_total | 40872 |
| tokens_prompt_total | 339923 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 24 | 339923 | 40872 | 380795 | 0.0584 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.9445 · needs_judge_review: False · n_expec… | 58268.7 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.5972 · needs_judge_review: False · n_expec… | 52927.8 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.6297 · needs_judge_review: False · n_expec… | 40587.9 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.6429 · needs_judge_review: False · n_expec… | 34239.6 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.6267 · needs_judge_review: False · n_expec… | 80179.3 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.7272 · needs_judge_review: False · n_expec… | 35454.8 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.6444 · needs_judge_review: False · n_expec… | 55641.8 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.6016 · needs_judge_review: False · n_expec… | 111956.8 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 21345.7 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 25516.9 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.7424 · needs_judge_review: False · n_expec… | 76579.2 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.6094 · needs_judge_review: False · n_expec… | 51027 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.4051 · needs_judge_review: False · n_expec… | 59613.1 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.6739 · needs_judge_review: False · n_expec… | 36424.4 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.3514 · needs_judge_review: False · n_expec… | 9061.2 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.5893 · needs_judge_review: False · n_expec… | 119638.3 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.2236 · needs_judge_review: False · n_expec… | 31118.5 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.6666 · needs_judge_review: False · n_expec… | 70910.3 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.6912 · needs_judge_review: False · n_expec… | 95045.6 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.6785 · needs_judge_review: False · n_expec… | 68172.7 | — |


## 20260927T004231Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: 5bdab8d · dirty: True |
| started / finished | 2026-09-27T00:42:31+00:00 → 2026-09-27T00:52:00+00:00 |
| duration_s | 420 |
| error | Interrupted after 1/20: completion budget 8192 truncated me… |

### Dataset

| Key | Value |
|---|---|
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| subset | class:merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0132 |
| latency_ms_mean | 268266.4 |
| latency_ms_p95 | 268266.4 |
| tokens_completion_total | 8195 |
| tokens_prompt_total | 81257 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 1 | 81257 | 8195 | 89452 | 0.0132 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 268266.4 | — |


## 20260927T005233Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / merger_agreement_specialist_v1 |
| trace backend | braintrust |
| git | commit: 533b371 · dirty: True |
| started / finished | 2026-09-27T00:52:33+00:00 → 2026-09-27T01:09:03+00:00 |
| duration_s | 900 |
| error | Interrupted 3/20: unchunked ~350k-char merger text truncate… |

### Dataset

| Key | Value |
|---|---|
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| subset | class:merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 1 |
| n | 3 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0392 |
| latency_ms_mean | 247912.7333 |
| latency_ms_p95 | 289547.9 |
| tokens_completion_total | 24585 |
| tokens_prompt_total | 239586 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 3 | 239586 | 24585 | 264171 | 0.0392 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 234100.5 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt |  | 220089.8 | ValueError: Exceeds the limit (4300 digits) for integer str… |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 289547.9 | — |


## 20260927T011209Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / merger_agreement_specialist_v1 |
| trace backend | braintrust |
| git | commit: f75ccd9 · dirty: True |
| started / finished | 2026-09-27T01:12:09+00:00 → 2026-09-27T01:25:51+00:00 |
| duration_s | 780 |
| error | Interrupted 1/20: 8 chunks still returned unparseable JSON … |

### Dataset

| Key | Value |
|---|---|
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| subset | class:merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 1 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0221 |
| latency_ms_mean | 669067.9 |
| latency_ms_p95 | 669067.9 |
| tokens_completion_total | 22641 |
| tokens_prompt_total | 100682 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 8 | 100682 | 22641 | 123323 | 0.0221 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 669067.9 | — |


## 20260927T014814Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: 4b25a4e · dirty: True |
| started / finished | 2026-09-27T01:48:14+00:00 → 2026-09-27T01:56:35+00:00 |
| duration_s | 503 |
| error | — |

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
| subset_manifest_jsonl | data/experiments/20260927T014814Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T014814Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0259 |
| latency_ms_mean | 249440.15 |
| latency_ms_p95 | 253967.8 |
| tokens_completion_total | 16390 |
| tokens_prompt_total | 157754 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 2 | 157754 | 16390 | 174144 | 0.0259 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 253967.8 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 244912.5 | — |


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
| error | — |

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


## 20260927T022750Z-eval-merger_agreement

| Key | Value |
|---|---|
| family / task | eval / merger_agreement |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:27:50+00:00 → 2026-09-27T02:30:10+00:00 |
| duration_s | 142 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:contract_128_merger_agreement.txt… |
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
| subset_manifest_jsonl | data/experiments/20260927T022750Z-eval-merger_agreement/sub… |
| subset_manifest_path | data/experiments/20260927T022750Z-eval-merger_agreement/sub… |
| subset_spec | kind: class · value: merger_agreement |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.3748 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0575 |
| latency_ms_mean | 45286.88 |
| latency_ms_p95 | 52445.4 |
| tokens_completion_total | 114281 |
| tokens_prompt_total | 1422210 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| merger_agreement_specialist | 18 | 1422210 | 114281 | 1536491 | 0.0575 | qwen/qwen3.7-flash |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:contract_128_merger_agreement.txt | overall_score: 0.2633 · needs_judge_review: False · n_expec… | 47418.8 | — |
| corpus:ground_truth:train:contract_31_merger_agreement.txt | overall_score: 0.2986 · needs_judge_review: False · n_expec… | 37790.1 | — |
| corpus:ground_truth:train:contract_99_merger_agreement.txt | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 40572.7 | — |
| corpus:ground_truth:train:contract_114_merger_agreement.txt | overall_score: 0.1751 · needs_judge_review: False · n_expec… | 37713.3 | — |
| corpus:ground_truth:train:contract_94_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 46588.4 | — |
| corpus:ground_truth:train:contract_120_merger_agreement.txt | overall_score: 0.2927 · needs_judge_review: False · n_expec… | 47017.2 | — |
| corpus:ground_truth:train:contract_41_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 46987.2 | — |
| corpus:ground_truth:train:contract_62_merger_agreement.txt | overall_score: 0.6945 · needs_judge_review: False · n_expec… | 51732.2 | — |
| corpus:ground_truth:train:contract_51_merger_agreement.txt | overall_score: 0.2201 · needs_judge_review: False · n_expec… | 46723.5 | — |
| corpus:ground_truth:train:contract_70_merger_agreement.txt | overall_score: 0.1441 · needs_judge_review: False · n_expec… | 48939.5 | — |
| corpus:ground_truth:train:contract_100_merger_agreement.txt | overall_score: 0.5584 · needs_judge_review: True · n_expect… | 52445.4 | — |
| corpus:ground_truth:train:contract_97_merger_agreement.txt | overall_score: 0.5 · needs_judge_review: True · n_expected_… | 46754.6 | — |
| corpus:ground_truth:train:contract_71_merger_agreement.txt | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 40362.2 | — |
| corpus:ground_truth:train:contract_66_merger_agreement.txt | overall_score: 0.6177 · needs_judge_review: False · n_expec… | 54764.6 | — |
| corpus:ground_truth:train:contract_34_merger_agreement.txt | overall_score: 0.1873 · needs_judge_review: False · n_expec… | 41083 | — |
| corpus:ground_truth:train:contract_5_merger_agreement.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 43248.3 | — |
| corpus:ground_truth:train:contract_76_merger_agreement.txt | overall_score: 0.2755 · needs_judge_review: False · n_expec… | 45097.6 | — |
| corpus:ground_truth:train:contract_136_merger_agreement.txt | overall_score: 0.5938 · needs_judge_review: False · n_expec… | 39142.3 | — |
| corpus:ground_truth:train:contract_122_merger_agreement.txt | overall_score: 0.2377 · needs_judge_review: False · n_expec… | 46538 | — |
| corpus:ground_truth:train:contract_19_merger_agreement.txt | overall_score: 0.575 · needs_judge_review: False · n_expect… | 44818.7 | — |


## 20260927T022738Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:27:38+00:00 → 2026-09-27T02:30:47+00:00 |
| duration_s | 191 |
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
| subset_manifest_jsonl | data/experiments/20260927T022738Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T022738Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0287 |
| latency_ms_mean | 56321.215 |
| latency_ms_p95 | 133521.6 |
| tokens_completion_total | 50672 |
| tokens_prompt_total | 48452 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 20 | 48452 | 50672 | 99124 | 0.0287 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15188 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 13655.3 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15726.7 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 98922.4 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 19837.6 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 16800 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18517.7 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 92858.7 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14052.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 123945.1 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 25086.7 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 11648.6 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 99540.6 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 147604.4 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 50105.2 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 118640.7 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 12548.1 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 133521.6 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15670 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.0 · needs_judge_review: False · n_expected… | 82554.4 | — |


## 20260927T023050Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:30:50+00:00 → 2026-09-27T02:33:44+00:00 |
| duration_s | 175.6 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:pde:233384494245864.txt, corpus:g… |
| config | ground_truth |
| filenames | pde:233384494245864.txt, insurbias-624.txt, carrier:8874733… |
| n_selected | 20 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260927T023050Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260927T023050Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.202 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0192 |
| latency_ms_mean | 34087.465 |
| latency_ms_p95 | 155975.6 |
| tokens_completion_total | 31824 |
| tokens_prompt_total | 40696 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 20 | 40696 | 31824 | 72520 | 0.0192 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14192.7 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8428 · needs_judge_review: False · n_expec… | 27512 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 11072 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15367.8 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 155975.6 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.7034 · needs_judge_review: True · n_expect… | 21359.7 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 15778.7 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 14478.1 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 9325.9 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 158081.2 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 8805.9 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8424 · needs_judge_review: False · n_expec… | 15052.8 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8182 · needs_judge_review: False · n_expec… | 17154.5 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 8780.8 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15097.6 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 11298.6 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18761 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 6566.8 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 126405.9 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 10681.7 | — |


## 20260927T022810Z-eval-corporate_records

| Key | Value |
|---|---|
| family / task | eval / corporate_records |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:28:10+00:00 → 2026-09-27T02:33:59+00:00 |
| duration_s | 352 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… |
| config | ground_truth |
| filenames | 0001047469-12-006895_a2210011zex-4_10.htm, 0001047469-03-03… |
| n_selected | 20 |
| n_total | 403 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:corporate_record |
| subset_manifest_jsonl | data/experiments/20260927T022810Z-eval-corporate_records/su… |
| subset_manifest_path | data/experiments/20260927T022810Z-eval-corporate_records/su… |
| subset_spec | kind: class · value: corporate_record |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.1824 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0403 |
| latency_ms_mean | 50674.82 |
| latency_ms_p95 | 240418.7 |
| tokens_completion_total | 39458 |
| tokens_prompt_total | 190774 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| corporate_records_specialist | 22 | 190774 | 39458 | 230232 | 0.0403 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:0001047469-12-006895_a2210011zex-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 26683.4 | — |
| corpus:ground_truth:train:0001047469-03-032251_a2118977zex-… | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 36336.5 | — |
| corpus:ground_truth:train:0000950123-11-055070_h75396a4exv2… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 7802.2 | — |
| corpus:ground_truth:train:0000898430-01-503595_dex32.txt | overall_score: 0.0 · needs_judge_review: False · n_expected… | 22570.7 | — |
| corpus:ground_truth:train:0001193125-11-240442_dex43.htm | overall_score: 0.5976 · needs_judge_review: False · n_expec… | 22109.4 | — |
| corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 13485.2 | — |
| corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3… | overall_score: 0.5857 · needs_judge_review: False · n_expec… | 17694.5 | — |
| corpus:ground_truth:train:0001193125-13-256819_d428632dex21… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18603.9 | — |
| corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_… | overall_score: 0.2295 · needs_judge_review: False · n_expec… | 20045.8 | — |
| corpus:ground_truth:train:0001193125-08-109289_dex241.htm | overall_score: 0.0 · needs_judge_review: False · n_expected… | 49367 | — |
| corpus:ground_truth:train:0001079974-08-000839_artdimension… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 17474.1 | — |
| corpus:ground_truth:train:0001193125-05-179145_dex32.htm | overall_score: 0.2521 · needs_judge_review: False · n_expec… | 21677.5 | — |
| corpus:ground_truth:train:0001021432-06-000035_certamendriv… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 240418.7 | — |
| corpus:ground_truth:train:0001021432-06-000037_certamendcal… | overall_score: 0.223 · needs_judge_review: False · n_expect… | 42686.9 | — |
| corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4… | overall_score: 0.4576 · needs_judge_review: False · n_expec… | 318812.7 | — |
| corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex… | overall_score: 0.2295 · needs_judge_review: False · n_expec… | 36144.8 | — |
| corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 47011.4 | — |
| corpus:ground_truth:train:0001193125-10-221497_dex32.htm | overall_score: 0.2606 · needs_judge_review: False · n_expec… | 10322.4 | — |
| corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm | overall_score: 0.2615 · needs_judge_review: False · n_expec… | 25769.6 | — |
| corpus:ground_truth:train:0001683168-23-005255_cardiff_ex03… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18479.7 | — |


## 20260927T023347Z-eval-contracts

| Key | Value |
|---|---|
| family / task | eval / contracts |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: fd6a220 · dirty: True |
| started / finished | 2026-09-27T02:33:47+00:00 → 2026-09-27T02:40:49+00:00 |
| duration_s | 424.4 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… |
| config | ground_truth |
| filenames | MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PD… |
| n_selected | 20 |
| n_total | 540 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:contract |
| subset_manifest_jsonl | data/experiments/20260927T023347Z-eval-contracts/subset_man… |
| subset_manifest_path | data/experiments/20260927T023347Z-eval-contracts/subset_man… |
| subset_spec | kind: class · value: contract |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.0762 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0498 |
| latency_ms_mean | 108632.14 |
| latency_ms_p95 | 365572.6 |
| tokens_completion_total | 48066 |
| tokens_prompt_total | 238475 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| contracts_specialist | 21 | 238475 | 48066 | 286541 | 0.0498 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.2… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 41025.8 | — |
| corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 38844.1 | — |
| corpus:ground_truth:train:MorganStanleyDirectLendingFund_20… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 365572.6 | — |
| corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 25336.3 | — |
| corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 72349.4 | — |
| corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 21737.4 | — |
| corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-D… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 266975 | — |
| corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 260779.7 | — |
| corpus:ground_truth:train:0001047469-05-021628_a2161868zex-… | overall_score: 1.0 · needs_judge_review: False · n_expected… | 30970.1 | — |
| corpus:ground_truth:train:0000721748-15-000083_ncmf02121510… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 395455.6 | — |
| corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 61586.8 | — |
| corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 89018.8 | — |
| corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 17135.9 | — |
| corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_0… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 26165.1 | — |
| corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm | overall_score: 0.0 · needs_judge_review: False · n_expected… | 18878.5 | — |
| corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10… | overall_score: 0.5238 · needs_judge_review: False · n_expec… | 73212.6 | — |
| corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 15677.4 | — |
| corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 8563.3 | — |
| corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 195448.8 | — |
| corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-… | overall_score: 0.0 · needs_judge_review: False · n_expected… | 147909.6 | — |


## 20260927T033031Z-eval-correspondence

| Key | Value |
|---|---|
| family / task | eval / correspondence |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: 4b973b7 · dirty: True |
| started / finished | 2026-09-27T03:30:31+00:00 → 2026-09-27T03:50:59+00:00 |
| duration_s | 1230.1 |
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
| subset_manifest_jsonl | data/experiments/20260927T033031Z-eval-correspondence/subse… |
| subset_manifest_path | data/experiments/20260927T033031Z-eval-correspondence/subse… |
| subset_spec | kind: class · value: correspondence |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.513 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.0604 |
| latency_ms_mean | 128861.32 |
| latency_ms_p95 | 150933.7 |
| tokens_completion_total | 110287 |
| tokens_prompt_total | 87002 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| correspondence_specialist | 39 | 87002 | 110287 | 197289 | 0.0604 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:blair-l/meetings/608. | overall_score: 0.4013 · needs_judge_review: False · n_expec… | 99043.5 | — |
| corpus:ground_truth:train:lokey-t/inbox/250. | overall_score: 0.55 · needs_judge_review: False · n_expecte… | 128665.8 | — |
| corpus:ground_truth:train:kean-s/all_documents/849. | overall_score: 0.5577 · needs_judge_review: False · n_expec… | 39379.1 | — |
| corpus:ground_truth:train:may-l/all_documents/41. | overall_score: 0.419 · needs_judge_review: False · n_expect… | 106303.8 | — |
| corpus:ground_truth:train:skilling-j/inbox/1555. | overall_score: 0.4354 · needs_judge_review: False · n_expec… | 150933.7 | — |
| corpus:ground_truth:train:sanders-r/sent_items/261. | overall_score: 0.6111 · needs_judge_review: False · n_expec… | 134271 | — |
| corpus:ground_truth:train:mcconnell-m/all_documents/227. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 55458.9 | — |
| corpus:ground_truth:train:thomas-p/deleted_items/292. | overall_score: 0.7 · needs_judge_review: True · n_expected_… | 48333.9 | — |
| corpus:ground_truth:train:nemec-g/all_documents/906. | overall_score: 0.25 · needs_judge_review: False · n_expecte… | 23353.5 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/13056. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 32837.6 | — |
| corpus:ground_truth:train:kaminski-v/all_documents/5470. | overall_score: 0.3566 · needs_judge_review: False · n_expec… | 136725.8 | — |
| corpus:ground_truth:train:parks-j/sent_items/425. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 44942.1 | — |
| corpus:ground_truth:train:campbell-l/inbox/81. | overall_score: 0.5833 · needs_judge_review: False · n_expec… | 108990.5 | — |
| corpus:ground_truth:train:donoho-l/inbox/35. | overall_score: 0.6572 · needs_judge_review: False · n_expec… | 49599.1 | — |
| corpus:ground_truth:train:kitchen-l/sent_items/613. | overall_score: 0.4496 · needs_judge_review: False · n_expec… | 69641.2 | — |
| corpus:ground_truth:train:derrick-j/deleted_items/79. | overall_score: 0.6 · needs_judge_review: False · n_expected… | 84155 | — |
| corpus:ground_truth:train:rogers-b/_sent_mail/358. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 28686.4 | — |
| corpus:ground_truth:train:dasovich-j/all_documents/10751. | overall_score: 0.6333 · needs_judge_review: False · n_expec… | 1086942.8 | — |
| corpus:ground_truth:train:motley-m/deleted_items/63. | overall_score: 0.5555 · needs_judge_review: False · n_expec… | 47420.2 | — |
| corpus:ground_truth:train:dorland-c/_sent_mail/78. | overall_score: 0.5 · needs_judge_review: False · n_expected… | 101542.5 | — |


## 20260927T035135Z-eval-insurance_claims

| Key | Value |
|---|---|
| family / task | eval / insurance_claims |
| invoke / mode | agent / real |
| model / prompt | qwen/qwen3-8b / None |
| trace backend | braintrust |
| git | commit: bd43f66 · dirty: True |
| started / finished | 2026-09-27T03:51:35+00:00 → 2026-09-27T03:54:57+00:00 |
| duration_s | 203.3 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:ground_truth:train:pde:233384494245864.txt, corpus:g… |
| config | ground_truth |
| filenames | pde:233384494245864.txt, insurbias-624.txt, carrier:8874733… |
| n_selected | 20 |
| n_total | 986 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | 20 |
| seed | 42 |
| split | train |
| subset | class:insurance_claim |
| subset_manifest_jsonl | data/experiments/20260927T035135Z-eval-insurance_claims/sub… |
| subset_manifest_path | data/experiments/20260927T035135Z-eval-insurance_claims/sub… |
| subset_spec | kind: class · value: insurance_claim |

### Metrics

| Metric | Value |
|---|---|
| errors | 0 |
| n | 20 |
| overall_score | 0.7488 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | 0.032 |
| latency_ms_mean | 50681.595 |
| latency_ms_p95 | 147490.1 |
| tokens_completion_total | 50885 |
| tokens_prompt_total | 75955 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| insurance_claims_specialist | 37 | 75955 | 50885 | 126840 | 0.032 | qwen/qwen3-8b |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:ground_truth:train:pde:233384494245864.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 27438.6 | — |
| corpus:ground_truth:train:insurbias-624.txt | overall_score: 0.8556 · needs_judge_review: False · n_expec… | 39907.7 | — |
| corpus:ground_truth:train:carrier:887473385855273.txt | overall_score: 0.7512 · needs_judge_review: False · n_expec… | 27076.5 | — |
| corpus:ground_truth:train:carrier:887453386193813.txt | overall_score: 0.7209 · needs_judge_review: True · n_expect… | 145889.5 | — |
| corpus:ground_truth:train:outpatient:542872281350908:1.txt | overall_score: 0.7347 · needs_judge_review: True · n_expect… | 23580.6 | — |
| corpus:ground_truth:train:pde:233724491332182.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 25049.2 | — |
| corpus:ground_truth:train:auto:CLM-000145.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 19644.4 | — |
| corpus:ground_truth:train:insurbias-163.txt | overall_score: 0.7583 · needs_judge_review: False · n_expec… | 14831.3 | — |
| corpus:ground_truth:train:insurbias-1111.txt | overall_score: 0.9 · needs_judge_review: False · n_expected… | 33817.7 | — |
| corpus:ground_truth:train:pde:233184493359051.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 147490.1 | — |
| corpus:ground_truth:train:outpatient:542152281286913:1.txt | overall_score: 0.7226 · needs_judge_review: True · n_expect… | 21485 | — |
| corpus:ground_truth:train:insurbias-385.txt | overall_score: 0.8408 · needs_judge_review: False · n_expec… | 14622.3 | — |
| corpus:ground_truth:train:insurbias-310.txt | overall_score: 0.8423 · needs_judge_review: False · n_expec… | 38177.8 | — |
| corpus:ground_truth:train:auto:CLM-000322.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 20600.4 | — |
| corpus:ground_truth:train:pde:233614493105212.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 18637.4 | — |
| corpus:ground_truth:train:carrier:887623388590174.txt | overall_score: 0.63 · needs_judge_review: True · n_expected… | 27120.2 | — |
| corpus:ground_truth:train:inpatient:196411177017295:1.txt | overall_score: 0.7535 · needs_judge_review: False · n_expec… | 144598.8 | — |
| corpus:ground_truth:train:auto:CLM-000611.txt | overall_score: 0.8333 · needs_judge_review: False · n_expec… | 19430.5 | — |
| corpus:ground_truth:train:pde:233364488871784.txt | overall_score: 0.658 · needs_judge_review: False · n_expect… | 150612.8 | — |
| corpus:ground_truth:train:property:266855223.txt | overall_score: 0.6768 · needs_judge_review: False · n_expec… | 53621.1 | — |

