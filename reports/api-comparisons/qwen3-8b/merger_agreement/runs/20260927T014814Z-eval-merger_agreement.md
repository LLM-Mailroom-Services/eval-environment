# Run report — `20260927T014814Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T014814Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 2 docs, seed 42 |
| timestamp | `2026-09-27T01:48:14+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T014814Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `4b25a4e` |
| finished | `2026-09-27T01:56:35+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T014814Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T01:48:14+00:00` |
| finished_at | `2026-09-27T01:56:35+00:00` |
| duration_s (wall) | 503.0000 |
| latency_ms_mean | 249440.1 |
| latency_ms_p95 | 253967.8 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **2 / 2** (`errors=0`) |
| errors | 0 |
| overall_score | 0.0 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.0000** (sd 0.0000, min 0.0000, max 0.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 503.0000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.0120** USD |
| cost actual (derived from case rows) | **0.0259** USD |
| cost estimated (roster token rates) | **0.0259** USD |
| cost per document (actual) | 0.0130 USD |
| cost per document (estimated) | 0.0130 USD |
| latency e2e / p50 / p95 / max | 503.0000 / 253.9678 / 253.9678 / 253.9678 s |
| prompt / completion / total tokens | 157754 / 16390 / 174144 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 498.9 s vs wall = 503.0 s -> wall/serial factor 0.99x at concurrency 1.

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
| `merger_agreement_specialist` | 2 | 157754 | 16390 | 174144 | 0.0259 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 498.9 s over wall 503.0 s = **0.99×** effective parallelism at c1 (99% of the ideal 1×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_128_merger_agreement.txt` (other) 254.0 s = 50% of wall — p95/p50 = 1.00×.
- **Decode budget:** mean completion 8195 tok/doc, mean prompt 78877 tok/doc.
- **Field-level extraction:** 2/2 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 2 | 0.0000 |
| **total** | **2** | **0.0000** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.0000 | 0.0000 | 253.9678 | 81340 | 8195 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.0000 | 0.0000 | 244.9125 | 76414 | 8195 | — |

- scored rows: 2/2; min=0.0000 max=0.0000 mean=0.0000

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 2 --seed 42 --concurrency 1 --decode-profile qwen3-8b --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260927T014814Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T014814Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T014814Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T014814Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T014814Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3-8b/merger_agreement/RUN-2-MERGER_AGREEMENT-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
