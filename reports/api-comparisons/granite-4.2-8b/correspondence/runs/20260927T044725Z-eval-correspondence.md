# Run report — `20260927T044725Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T044725Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 2 docs, seed 42 |
| timestamp | `2026-09-27T04:47:25+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T044725Z-eval-correspondence/subset_manifest.json` |
| eval git | `74390d1` |
| finished | `2026-09-27T04:47:25+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | mock |
| concurrency | 1 |
| seed | 42 |
| sample / n | None / 2 |
| scorer | extraction |
| decode profile | granite-4.2-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T04:47:25+00:00` |
| finished_at | `2026-09-27T04:47:25+00:00` |
| duration_s (wall) | 2.5000 |
| latency_ms_mean | 0.7000 |
| latency_ms_p95 | 0.8000 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **2 / 2** (`errors=0`) |
| errors | 0 |
| overall_score | 0.0 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 2.5000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.0800** USD |
| cost actual (derived from case rows) | **0.0000** USD |
| cost estimated (roster token rates) | **0.0000** USD |
| cost per document (actual) | 0.0000 USD |
| cost per document (estimated) | 0.0000 USD |
| latency e2e / p50 / p95 / max | 2.5000 / 0.0008 / 0.0008 / 0.0008 s |
| prompt / completion / total tokens | 20 / 20 / 40 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 0.0 s vs wall = 2.5 s -> wall/serial factor 0.00x at concurrency 1.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 8192, "corporate_records_specialist": 8192, "correspondence_specialist": 4096, "insurance_claims_specialist": 6144, "merger_agreement_specialist": 16384}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `correspondence_specialist` | 2 | 20 | 20 | 40 | — | mock-model |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:allen-p/deleted_items/65.` | email | 0.0000 | 0.0000 | 0.0008 | 10 | 10 | — |
| 2 | `corpus:ground_truth:train:arnold-j/deleted_items/395.` | memo | 0.0000 | 0.0000 | 0.0006 | 10 | 10 | — |

- scored rows: 2/2; min=0.0000 max=0.0000 mean=0.0000

## Caveats / notes

- mode: **mock**; trace backend: `none`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
