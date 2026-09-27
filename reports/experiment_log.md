# mailroom-evals — experiment log

One row per run (append-only source of truth: `reports/experiment_log.jsonl`). Each run's full detail (dataset provenance, metrics, per-agent performance, case table) lives in its own file under `reports/experiment_log/<run_id>.md` — this index never grows a per-run section inline, so it stays readable regardless of history size. OpenRouter/Braintrust N-doc waves also get a standalone, Modal-comparable write-ups under `reports/api-comparisons/` (see `INDEX.md`; per-run files under `<model>/<task>/runs/`).

## Real evaluation waves (real mode, n≥10 cases) — 25

| run_id | family | task | mode | model | subset | n | key metric | errors |
|---|---|---|---|---|---|---|---|---|
| [20260927T101544Z-eval-classification](experiment_log/20260927T101544Z-eval-classification.md) | eval | classification | real | deepseek/deepseek-v4.1-flash | full | 100 | class_accuracy=0.95 | 0 |
| [20260927T101020Z-eval-classification](experiment_log/20260927T101020Z-eval-classification.md) | eval | classification | real | qwen/qwen3.7-flash | full | 100 | class_accuracy=0.91 | 0 |
| [20260927T100340Z-eval-classification](experiment_log/20260927T100340Z-eval-classification.md) | eval | classification | real | ibm-granite/granite-4.2-8b | full | 100 | class_accuracy=0.94 | 0 |
| [20260927T082404Z-eval-merger_agreement](experiment_log/20260927T082404Z-eval-merger_agreement.md) | eval | merger_agreement | real | ibm-granite/granite-4.2-8b | class:merger_agreement | 20 | — | 0 |
| [20260927T070900Z-eval-classification](experiment_log/20260927T070900Z-eval-classification.md) | eval | classification | real | ibm-granite/granite-4.2-8b | full | 20 | class_accuracy=0.9 | 0 |
| [20260927T065622Z-eval-corporate_records](experiment_log/20260927T065622Z-eval-corporate_records.md) | eval | corporate_records | real | ibm-granite/granite-4.2-8b | class:corporate_record | 20 | — | 0 |
| [20260927T060322Z-eval-merger_agreement](experiment_log/20260927T060322Z-eval-merger_agreement.md) | eval | merger_agreement | real | ibm-granite/granite-4.2-8b | class:merger_agreement | 20 | — | 0 |
| [20260927T054738Z-eval-contracts](experiment_log/20260927T054738Z-eval-contracts.md) | eval | contracts | real | ibm-granite/granite-4.2-8b | class:contract | 20 | — | 0 |
| [20260927T054211Z-eval-insurance_claims](experiment_log/20260927T054211Z-eval-insurance_claims.md) | eval | insurance_claims | real | ibm-granite/granite-4.2-8b | class:insurance_claim | 20 | — | 0 |
| [20260927T053647Z-eval-correspondence](experiment_log/20260927T053647Z-eval-correspondence.md) | eval | correspondence | real | ibm-granite/granite-4.2-8b | class:correspondence | 20 | — | 0 |
| [20260927T052637Z-eval-correspondence](experiment_log/20260927T052637Z-eval-correspondence.md) | eval | correspondence | real | ibm-granite/granite-4.2-8b | class:correspondence | 20 | — | 0 |
| [20260927T044805Z-eval-correspondence](experiment_log/20260927T044805Z-eval-correspondence.md) | eval | correspondence | real | ibm-granite/granite-4.2-8b | class:correspondence | 20 | — | 0 |
| [20260927T043145Z-eval-classification](experiment_log/20260927T043145Z-eval-classification.md) | eval | classification | real | qwen/qwen3-8b | full | 20 | class_accuracy=0.7 | 0 |
| [20260927T042239Z-eval-corporate_records](experiment_log/20260927T042239Z-eval-corporate_records.md) | eval | corporate_records | real | qwen/qwen3-8b | class:corporate_record | 20 | — | 0 |
| [20260927T035621Z-eval-contracts](experiment_log/20260927T035621Z-eval-contracts.md) | eval | contracts | real | qwen/qwen3-8b | class:contract | 20 | — | 0 |
| [20260927T035135Z-eval-insurance_claims](experiment_log/20260927T035135Z-eval-insurance_claims.md) | eval | insurance_claims | real | qwen/qwen3-8b | class:insurance_claim | 20 | — | 0 |
| [20260927T033031Z-eval-correspondence](experiment_log/20260927T033031Z-eval-correspondence.md) | eval | correspondence | real | qwen/qwen3-8b | class:correspondence | 20 | — | 0 |
| [20260927T023347Z-eval-contracts](experiment_log/20260927T023347Z-eval-contracts.md) | eval | contracts | real | qwen/qwen3-8b | class:contract | 20 | — | 0 |
| [20260927T023050Z-eval-insurance_claims](experiment_log/20260927T023050Z-eval-insurance_claims.md) | eval | insurance_claims | real | qwen/qwen3-8b | class:insurance_claim | 20 | — | 0 |
| [20260927T022810Z-eval-corporate_records](experiment_log/20260927T022810Z-eval-corporate_records.md) | eval | corporate_records | real | qwen/qwen3-8b | class:corporate_record | 20 | — | 0 |
| [20260927T022750Z-eval-merger_agreement](experiment_log/20260927T022750Z-eval-merger_agreement.md) | eval | merger_agreement | real | qwen/qwen3.7-flash | class:merger_agreement | 20 | — | 0 |
| [20260927T022738Z-eval-correspondence](experiment_log/20260927T022738Z-eval-correspondence.md) | eval | correspondence | real | qwen/qwen3-8b | class:correspondence | 20 | — | 0 |
| [20260926T235347Z-eval-contracts](experiment_log/20260926T235347Z-eval-contracts.md) | eval | contracts | real | qwen/qwen3-8b | class:contract | 20 | — | 0 |
| [20260926T234603Z-eval-insurance_claims](experiment_log/20260926T234603Z-eval-insurance_claims.md) | eval | insurance_claims | real | qwen/qwen3-8b | class:insurance_claim | 20 | — | 0 |
| [20260926T234358Z-eval-correspondence](experiment_log/20260926T234358Z-eval-correspondence.md) | eval | correspondence | real | qwen/qwen3-8b | class:correspondence | 20 | — | 0 |

## Exploratory / debug real runs (real mode, n<10 cases) — 14

| run_id | family | task | mode | model | subset | n | key metric | errors |
|---|---|---|---|---|---|---|---|---|
| [20260927T101544Z-eval-classification](experiment_log/20260927T101544Z-eval-classification.md) | eval | classification | real | deepseek/deepseek-v4.1-flash | full | 1 | class_accuracy=1.0 | 0 |
| [20260927T101526Z-eval-classification](experiment_log/20260927T101526Z-eval-classification.md) | eval | classification | real | — | full | 0 | — | 0 |
| [20260927T093106Z-eval-classification](experiment_log/20260927T093106Z-eval-classification.md) | eval | classification | real | — | full | 0 | — | 0 |
| [20260927T051851Z-eval-correspondence](experiment_log/20260927T051851Z-eval-correspondence.md) | eval | correspondence | real | ibm-granite/granite-4.2-8b | class:correspondence | 1 | — | 0 |
| [20260927T020724Z-eval-merger_agreement](experiment_log/20260927T020724Z-eval-merger_agreement.md) | eval | merger_agreement | real | qwen/qwen3.7-flash | class:merger_agreement | 2 | — | 0 |
| [20260927T014814Z-eval-merger_agreement](experiment_log/20260927T014814Z-eval-merger_agreement.md) | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 2 | — | 0 |
| [20260927T011209Z-eval-merger_agreement](experiment_log/20260927T011209Z-eval-merger_agreement.md) | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 1 | — | 0 |
| [20260927T005233Z-eval-merger_agreement](experiment_log/20260927T005233Z-eval-merger_agreement.md) | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 3 | — | 1 |
| [20260927T004231Z-eval-merger_agreement](experiment_log/20260927T004231Z-eval-merger_agreement.md) | eval | merger_agreement | real | qwen/qwen3-8b | class:merger_agreement | 1 | — | 0 |
| [20260926T232610Z-eval-contracts](experiment_log/20260926T232610Z-eval-contracts.md) | eval | contracts | real | qwen/qwen3.7-flash | class:contract | 1 | — | 0 |
| [20260926T232556Z-eval-contracts](experiment_log/20260926T232556Z-eval-contracts.md) | eval | contracts | real | — | class:contract | 0 | — | 0 |
| [20260926T224038Z-eval-contracts](experiment_log/20260926T224038Z-eval-contracts.md) | eval | contracts | real | qwen/qwen3.7-flash | class:contract | 1 | — | 0 |
| [20260926T223222Z-eval-contracts](experiment_log/20260926T223222Z-eval-contracts.md) | eval | contracts | real | qwen/qwen3.7-flash | class:contract | 1 | — | 0 |
| [20260926T223211Z-eval-contracts](experiment_log/20260926T223211Z-eval-contracts.md) | eval | contracts | real | — | class:contract | 0 | — | 0 |

## Mock / CI-smoke runs — 27

| run_id | family | task | mode | model | subset | n | key metric | errors |
|---|---|---|---|---|---|---|---|---|
| [20260927T051729Z-eval-classification](experiment_log/20260927T051729Z-eval-classification.md) | eval | classification | mock | ibm-granite/granite-4.2-8b | full | 1 | class_accuracy=0.0 | 0 |
| [20260927T051725Z-eval-correspondence](experiment_log/20260927T051725Z-eval-correspondence.md) | eval | correspondence | mock | ibm-granite/granite-4.2-8b | class:correspondence | 1 | — | 0 |
| [20260927T044725Z-eval-correspondence](experiment_log/20260927T044725Z-eval-correspondence.md) | eval | correspondence | mock | ibm-granite/granite-4.2-8b | class:correspondence | 2 | — | 0 |
| [20260926T232547Z-eval-pipeline_chain](experiment_log/20260926T232547Z-eval-pipeline_chain.md) | eval | pipeline_chain | mock | qwen/qwen3.7-flash | pilot | 2 | class_accuracy=0.0 | 0 |
| [20260926T232546Z-eval-merger_agreement](experiment_log/20260926T232546Z-eval-merger_agreement.md) | eval | merger_agreement | mock | qwen/qwen3.7-flash | class:merger_agreement | 2 | — | 0 |
| [20260926T232545Z-eval-judge_arbiter](experiment_log/20260926T232545Z-eval-judge_arbiter.md) | eval | judge_arbiter | mock | qwen/qwen3.7-flash | fixtures | 2 | — | 0 |
| [20260926T232544Z-eval-intake](experiment_log/20260926T232544Z-eval-intake.md) | eval | intake | mock | mock-model | full | 2 | — | 0 |
| [20260926T232542Z-eval-insurance_claims](experiment_log/20260926T232542Z-eval-insurance_claims.md) | eval | insurance_claims | mock | mock-model | class:insurance_claim | 2 | — | 0 |
| [20260926T232540Z-eval-correspondence](experiment_log/20260926T232540Z-eval-correspondence.md) | eval | correspondence | mock | mock-model | class:correspondence | 2 | — | 0 |
| [20260926T232539Z-eval-corporate_records](experiment_log/20260926T232539Z-eval-corporate_records.md) | eval | corporate_records | mock | mock-model | class:corporate_record | 2 | — | 0 |
| [20260926T232538Z-eval-contracts](experiment_log/20260926T232538Z-eval-contracts.md) | eval | contracts | mock | qwen/qwen3.7-flash | class:contract | 2 | — | 0 |
| [20260926T232536Z-eval-classification](experiment_log/20260926T232536Z-eval-classification.md) | eval | classification | mock | qwen/qwen3.7-flash | full | 2 | class_accuracy=0.0 | 0 |
| [20260926T232533Z-eval-boss](experiment_log/20260926T232533Z-eval-boss.md) | eval | boss | mock | mock-model | fixtures | 2 | — | 0 |
| [20260926T232531Z-eval-archivist](experiment_log/20260926T232531Z-eval-archivist.md) | eval | archivist | mock | — | fixtures | 2 | — | 0 |
| [20260926T232531Z-eval-arbiter](experiment_log/20260926T232531Z-eval-arbiter.md) | eval | arbiter | mock | mock-model | fixtures | 2 | — | 0 |
| [20260926T223201Z-eval-pipeline_chain](experiment_log/20260926T223201Z-eval-pipeline_chain.md) | eval | pipeline_chain | mock | qwen/qwen3.7-flash | pilot | 2 | class_accuracy=0.0 | 0 |
| [20260926T223159Z-eval-merger_agreement](experiment_log/20260926T223159Z-eval-merger_agreement.md) | eval | merger_agreement | mock | qwen/qwen3.7-flash | class:merger_agreement | 2 | — | 0 |
| [20260926T223158Z-eval-judge_arbiter](experiment_log/20260926T223158Z-eval-judge_arbiter.md) | eval | judge_arbiter | mock | qwen/qwen3.7-flash | fixtures | 2 | — | 0 |
| [20260926T223157Z-eval-intake](experiment_log/20260926T223157Z-eval-intake.md) | eval | intake | mock | mock-model | full | 2 | — | 0 |
| [20260926T223154Z-eval-insurance_claims](experiment_log/20260926T223154Z-eval-insurance_claims.md) | eval | insurance_claims | mock | mock-model | class:insurance_claim | 2 | — | 0 |
| [20260926T223153Z-eval-correspondence](experiment_log/20260926T223153Z-eval-correspondence.md) | eval | correspondence | mock | mock-model | class:correspondence | 2 | — | 0 |
| [20260926T223151Z-eval-corporate_records](experiment_log/20260926T223151Z-eval-corporate_records.md) | eval | corporate_records | mock | mock-model | class:corporate_record | 2 | — | 0 |
| [20260926T223150Z-eval-contracts](experiment_log/20260926T223150Z-eval-contracts.md) | eval | contracts | mock | qwen/qwen3.7-flash | class:contract | 2 | — | 0 |
| [20260926T223149Z-eval-classification](experiment_log/20260926T223149Z-eval-classification.md) | eval | classification | mock | qwen/qwen3.7-flash | full | 2 | class_accuracy=0.0 | 0 |
| [20260926T223146Z-eval-boss](experiment_log/20260926T223146Z-eval-boss.md) | eval | boss | mock | mock-model | fixtures | 2 | — | 0 |
| [20260926T223145Z-eval-archivist](experiment_log/20260926T223145Z-eval-archivist.md) | eval | archivist | mock | — | fixtures | 2 | — | 0 |
| [20260926T223144Z-eval-arbiter](experiment_log/20260926T223144Z-eval-arbiter.md) | eval | arbiter | mock | mock-model | fixtures | 2 | — | 0 |
