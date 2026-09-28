# Run report — `20260927T051725Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T051725Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 1 docs, seed 42 |
| timestamp | `2026-09-27T05:17:25+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T051725Z-eval-correspondence/subset_manifest.json` |
| eval git | `5b9d25b` |
| finished | `2026-09-27T05:17:26+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | mock |
| concurrency | 1 |
| seed | 42 |
| sample / n | None / 1 |
| scorer | extraction |
| decode profile | granite-4.2-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T05:17:25+00:00` |
| finished_at | `2026-09-27T05:17:26+00:00` |
| duration_s (wall) | 2.5000 |
| latency_ms_mean | 0.8000 |
| latency_ms_p95 | 0.8000 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **1 / 1** (`errors=0`) |
| errors | 0 |
| overall_score | 0.0 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.0000** (sd 0.0000, min 0.0000, max 0.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 2.5000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.0400** USD |
| cost actual (derived from case rows) | **0.0000** USD |
| cost estimated (roster token rates) | **0.0000** USD |
| cost per document (actual) | 0.0000 USD |
| cost per document (estimated) | 0.0000 USD |
| latency e2e / p50 / p95 / max | 2.5000 / 0.0008 / 0.0008 / 0.0008 s |
| prompt / completion / total tokens | 10 / 10 / 20 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 0.0 s vs wall = 2.5 s -> wall/serial factor 0.00x at concurrency 1.

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
| `correspondence_specialist` | 1 | 10 | 10 | 20 | — | mock-model |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 0.0 s over wall 2.5 s = **0.00×** effective parallelism at c1 (0% of the ideal 1×).
- **Tail:** slowest doc `corpus:ground_truth:train:allen-p/deleted_items/65.` (email) 0.0 s = 0% of wall — p95/p50 = 1.00×.
- **Decode budget:** mean completion 10 tok/doc, mean prompt 10 tok/doc.
- **Field-level extraction:** 1/1 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 1 | 0.0000 |
| **total** | **1** | **0.0000** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:allen-p/deleted_items/65.` | email | 0.0000 | 0.0000 | 0.0008 | 10 | 10 | — |

- scored rows: 1/1; min=0.0000 max=0.0000 mean=0.0000

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --mock --n 1 --seed 42 --concurrency 1 --decode-profile granite-4.2-8b --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260927T051725Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T051725Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T051725Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T051725Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T051725Z-eval-correspondence.md` | experiment-log markdown mirror |
| `/workspace/reports/api-comparisons/granite-4.2-8b/correspondence/RUN-1-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **mock**; trace backend: `none`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
