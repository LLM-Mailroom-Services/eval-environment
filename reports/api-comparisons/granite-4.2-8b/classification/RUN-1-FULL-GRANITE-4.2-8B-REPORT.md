# Run report — `20260927T051729Z-eval-classification` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T051729Z-eval-classification` |
| task / agent | `classification` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `full` — 1 docs, seed 42 |
| timestamp | `2026-09-27T05:17:29+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T051729Z-eval-classification/subset_manifest.json` |
| eval git | `5b9d25b` |
| finished | `2026-09-27T05:17:29+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / node |
| mode | mock |
| concurrency | 1 |
| seed | 42 |
| sample / n | None / 1 |
| scorer | classification |
| decode profile | granite-4.2-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T05:17:29+00:00` |
| finished_at | `2026-09-27T05:17:29+00:00` |
| duration_s (wall) | 2.8000 |
| latency_ms_mean | 171.7000 |
| latency_ms_p95 | 171.7000 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **1 / 1** (`errors=0`) |
| class_accuracy | 0.0 |
| errors | 0 |
| scorer_errors | 0 |
| subclass_accuracy | 0.0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 2.8000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.0400** USD |
| cost actual (derived from case rows) | **0.0001** USD |
| cost estimated (roster token rates) | **0.0001** USD |
| cost per document (actual) | 0.0001 USD |
| cost per document (estimated) | 0.0001 USD |
| latency e2e / p50 / p95 / max | 2.8000 / 0.1717 / 0.1717 / 0.1717 s |
| prompt / completion / total tokens | 360 / 180 / 540 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 0.2 s vs wall = 2.8 s -> wall/serial factor 0.06x at concurrency 1.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 16384, "corporate_records_specialist": 16384, "correspondence_specialist": 8192, "insurance_claims_specialist": 12288, "merger_agreement_specialist": 32768}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `sorter` | 3 | 360 | 180 | 540 | 0.0001 | ibm-granite/granite-4.2-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 0.2 s over wall 2.8 s = **0.06×** effective parallelism at c1 (6% of the ideal 1×).
- **Tail:** slowest doc `corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3z2.htm` (powers_of_attorney) 0.2 s = 6% of wall — p95/p50 = 1.00×.
- **Decode budget:** mean completion 180 tok/doc, mean prompt 360 tok/doc.
- **Field-level extraction:** 0/1 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001062993-15-000198_s1011515_ex3z2.htm` | powers_of_attorney | — | — | 0.1717 | 360 | 180 | — |

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:classification --mock --n 1 --seed 42 --concurrency 1 --decode-profile granite-4.2-8b --subset "full"
uv run python scripts/score_run.py --run-id 20260927T051729Z-eval-classification --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T051729Z-eval-classification
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T051729Z-eval-classification/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T051729Z-eval-classification/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T051729Z-eval-classification.md` | experiment-log markdown mirror |
| `reports/api-comparisons/granite-4.2-8b/classification/RUN-1-FULL-GRANITE-4.2-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **mock**; trace backend: `none`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
