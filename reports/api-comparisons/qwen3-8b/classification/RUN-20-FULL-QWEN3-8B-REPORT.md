# Run report — `20260927T043145Z-eval-classification` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T043145Z-eval-classification` |
| task / agent | `classification` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `full` — 20 docs, seed 42 |
| timestamp | `2026-09-27T04:31:45+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T043145Z-eval-classification/subset_manifest.json` |
| eval git | `782ddeb` |
| finished | `2026-09-27T04:34:57+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / node |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | classification |
| decode profile | — |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T043145Z-eval-classification', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T04:31:45+00:00` |
| finished_at | `2026-09-27T04:34:57+00:00` |
| duration_s (wall) | 194.3000 |
| latency_ms_mean | 33056.5 |
| latency_ms_p95 | 133971.5 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| class_accuracy | 0.7 |
| errors | 0 |
| scorer_errors | 0 |
| subclass_accuracy | 0.05 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 194.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.1493** USD |
| cost estimated (roster token rates) | **0.1493** USD |
| cost per document (actual) | 0.0075 USD |
| cost per document (estimated) | 0.0075 USD |
| latency e2e / p50 / p95 / max | 194.3000 / 5.5296 / 133.9715 / 180.8246 s |
| prompt / completion / total tokens | 1213021 / 16132 / 1229153 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 661.1 s vs wall = 194.3 s -> wall/serial factor 3.40x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `none (pipeline posture)` |
| sampling injected on wire | False |
| per-agent completion budgets | `{}` |
| per-call timeout | pipeline default s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `sorter` | 150 | 1213021 | 16132 | 1229153 | 0.1493 | qwen/qwen3-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:property:261501663.txt` | property | — | — | 5.6564 | 7426 | 94 | — |
| 2 | `corpus:ground_truth:train:inpatient:196841176990879:1.txt` | inpatient | — | — | 4.8705 | 6295 | 97 | — |
| 3 | `corpus:ground_truth:train:insurbias-425.txt` | auto | — | — | 4.6740 | 5995 | 81 | — |
| 4 | `corpus:ground_truth:train:brawner-s/all_documents/59.` | email | — | — | 4.9668 | 6321 | 102 | — |
| 5 | `corpus:ground_truth:train:0000912057-01-507164_a2041839zex-4_38.txt` | rights_instrument | — | — | 9.1310 | 13787 | 152 | — |
| 6 | `corpus:ground_truth:train:dasovich-j/all_documents/9309.` | press_release | — | — | 5.0791 | 6211 | 68 | — |
| 7 | `corpus:ground_truth:train:dasovich-j/all_documents/9178.` | press_release | — | — | 5.6205 | 5958 | 90 | — |
| 8 | `corpus:ground_truth:train:0000950130-01-502904_dex211.txt` | subsidiary_list | — | — | 5.3338 | 5972 | 75 | — |
| 9 | `corpus:ground_truth:train:inpatient:196091177001318:1.txt` | inpatient | — | — | 4.5266 | 6295 | 95 | — |
| 10 | `corpus:ground_truth:train:inpatient:196831176969260:1.txt` | inpatient | — | — | 4.0848 | 6272 | 97 | — |
| 11 | `corpus:ground_truth:train:0001193125-14-273392_d715499dex415.htm` | indenture | — | — | 5.5296 | 8504 | 105 | — |
| 12 | `corpus:ground_truth:train:contract_117_merger_agreement.txt` | all_stock | — | — | 131.7061 | 257423 | 3385 | — |
| 13 | `corpus:ground_truth:train:property:262952775.txt` | property | — | — | 9.2177 | 15227 | 213 | — |
| 14 | `corpus:ground_truth:train:0000950123-03-010752_y88696a1exv4w7.txt` | indenture | — | — | 133.9715 | 264780 | 3371 | — |
| 15 | `corpus:ground_truth:train:contract_4_merger_agreement.txt` | all_cash | — | — | 125.8209 | 240112 | 3260 | — |
| 16 | `corpus:ground_truth:train:carrier:887493388020303.txt` | carrier | — | — | 3.2138 | 6203 | 106 | — |
| 17 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | — | — | 180.8246 | 323073 | 4359 | — |
| 18 | `corpus:ground_truth:train:inpatient:196641176967981:1.txt` | inpatient | — | — | 4.6574 | 6313 | 104 | — |
| 19 | `corpus:ground_truth:train:0001047469-06-011763_a2173128zex-3_1.htm` | charter_amendment | — | — | 7.8767 | 14663 | 182 | — |
| 20 | `corpus:ground_truth:train:outpatient:542502281397875:1.txt` | outpatient | — | — | 4.3687 | 6191 | 96 | — |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
