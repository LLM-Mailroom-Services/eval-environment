# Run report — `20260927T004231Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T004231Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-27T00:42:31+00:00` |
| pipeline git | `—` |
| subset manifest | `—` |
| eval git | `5bdab8d` |
| finished | `2026-09-27T00:52:00+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | — |
| seed | 42 |
| sample / n | 20 / None |
| scorer | — |
| decode profile | qwen3-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | — |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T00:42:31+00:00` |
| finished_at | `2026-09-27T00:52:00+00:00` |
| duration_s (wall) | 420 |
| latency_ms_mean | 268266.4 |
| latency_ms_p95 | 268266.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **1 / 1** (`errors=0`) |
| errors | 0 |
| overall_score | 0.0 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 420 s |
| concurrency | — |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0132** USD |
| cost estimated (roster token rates) | **0.0132** USD |
| cost per document (actual) | 0.0132 USD |
| cost per document (estimated) | 0.0132 USD |
| latency e2e / p50 / p95 / max | 420 / 268.2664 / 268.2664 / 268.2664 s |
| prompt / completion / total tokens | 81257 / 8195 / 89452 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 268.3 s vs wall = 420.0 s -> wall/serial factor 0.64x at concurrency 1.

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
| `merger_agreement_specialist` | 1 | 81257 | 8195 | 89452 | 0.0132 | qwen/qwen3-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.0000 | 0.0000 | 268.2664 | 81257 | 8195 | — |

- scored rows: 1/1; min=0.0000 max=0.0000 mean=0.0000

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
