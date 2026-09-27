# Run report — `20260927T020724Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T020724Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 2 docs, seed 42 |
| timestamp | `2026-09-27T02:07:24+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T020724Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `53ffee5` |
| finished | `2026-09-27T02:09:08+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 1 |
| seed | 42 |
| sample / n | 2 / None |
| scorer | extraction |
| decode profile | qwen3-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T020724Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T02:07:24+00:00` |
| finished_at | `2026-09-27T02:09:08+00:00` |
| duration_s (wall) | 106.5000 |
| latency_ms_mean | 46870.0 |
| latency_ms_p95 | 47783.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **2 / 2** (`errors=0`) |
| errors | 0 |
| overall_score | 0.346 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 106.5000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.0120** USD |
| cost actual (derived from case rows) | **0.0064** USD |
| cost estimated (roster token rates) | **0.0064** USD |
| cost per document (actual) | 0.0032 USD |
| cost per document (estimated) | 0.0032 USD |
| latency e2e / p50 / p95 / max | 106.5000 / 47.7839 / 47.7839 / 47.7839 s |
| prompt / completion / total tokens | 157083 / 13016 / 170099 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 93.7 s vs wall = 106.5 s -> wall/serial factor 0.88x at concurrency 1.

## Decode posture

| control | value |
|---|---|
| sampling override | `none (pipeline posture)` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 8192, "corporate_records_specialist": 8192, "correspondence_specialist": 4096, "insurance_claims_specialist": 6144, "merger_agreement_specialist": 16384}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `merger_agreement_specialist` | 2 | 157083 | 13016 | 170099 | 0.0064 | qwen/qwen3.7-flash |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.3221 | 0.0000 | 45.9561 | 81128 | 6297 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.3700 | 0.0000 | 47.7839 | 75955 | 6719 | — |

- scored rows: 2/2; min=0.3221 max=0.3700 mean=0.3460

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
