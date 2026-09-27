# Run report — `20260927T051851Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T051851Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 1 docs, seed 42 |
| timestamp | `2026-09-27T05:18:51+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T051851Z-eval-correspondence/subset_manifest.json` |
| eval git | `5b9d25b` |
| finished | `2026-09-27T05:20:31+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 1 |
| seed | 42 |
| sample / n | 1 / None |
| scorer | extraction |
| decode profile | granite-4.2-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T051851Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T05:18:51+00:00` |
| finished_at | `2026-09-27T05:20:31+00:00` |
| duration_s (wall) | 101.3000 |
| latency_ms_mean | 94734.6 |
| latency_ms_p95 | 94734.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **1 / 1** (`errors=0`) |
| errors | 0 |
| overall_score | 0.3513 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 101.3000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.0400** USD |
| cost actual (derived from case rows) | **0.0017** USD |
| cost estimated (roster token rates) | **0.0017** USD |
| cost per document (actual) | 0.0017 USD |
| cost per document (estimated) | 0.0017 USD |
| latency e2e / p50 / p95 / max | 101.3000 / 94.7346 / 94.7346 / 94.7346 s |
| prompt / completion / total tokens | 1713 / 6568 / 8281 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 94.7 s vs wall = 101.3 s -> wall/serial factor 0.94x at concurrency 1.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | True |
| per-agent completion budgets | `{"contracts_specialist": 16384, "corporate_records_specialist": 16384, "correspondence_specialist": 8192, "insurance_claims_specialist": 12288, "merger_agreement_specialist": 32768}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `correspondence_specialist` | 1 | 1713 | 6568 | 8281 | 0.0017 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1250 | 94.7346 | 1713 | 6568 | — |

- scored rows: 1/1; min=0.3513 max=0.3513 mean=0.3513

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
