# Run report — `20260927T005233Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T005233Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `merger_agreement_specialist_v1` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-27T00:52:33+00:00` |
| pipeline git | `—` |
| subset manifest | `—` |
| eval git | `533b371` |
| finished | `2026-09-27T01:09:03+00:00` |

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
| started_at | `2026-09-27T00:52:33+00:00` |
| finished_at | `2026-09-27T01:09:03+00:00` |
| duration_s (wall) | 900 |
| latency_ms_mean | 247912.7 |
| latency_ms_p95 | 289547.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **2 / 3** (`errors=1`) |
| errors | 1 |
| overall_score | 0.0 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.0000** (sd 0.0000, min 0.0000, max 0.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 900 s |
| concurrency | — |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0392** USD |
| cost estimated (roster token rates) | **0.0392** USD |
| cost per document (actual) | 0.0131 USD |
| cost per document (estimated) | 0.0131 USD |
| latency e2e / p50 / p95 / max | 900 / 234.1005 / 289.5479 / 289.5479 s |
| prompt / completion / total tokens | 239586 / 24585 / 264171 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 743.7 s vs wall = 900.0 s -> wall/serial factor 0.83x at concurrency 1.

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
| `merger_agreement_specialist` | 3 | 239586 | 24585 | 264171 | 0.0392 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 743.7 s over wall 900.0 s = **0.83×** effective parallelism at c1 (83% of the ideal 1×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_99_merger_agreement.txt` (all_cash) 289.5 s = 32% of wall — p95/p50 = 1.24×.
- **Decode budget:** mean completion 8195 tok/doc, mean prompt 81628 tok/doc.
- **Subclass spread:** best `other` 0.000 (n=1), worst `other` 0.000 (n=1).
- **Field-level extraction:** 2/2 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| all_cash | 1 | 0.0000 |
| other | 1 | 0.0000 |
| **total** | **2** | **0.0000** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.0000 | 0.0000 | 234.1005 | 81257 | 8195 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | — | — | 220.0898 | 76331 | 8195 | ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 8191 digits; use sys.set_int_max_str_digits() to increase the limit |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 289.5479 | 81998 | 8195 | — |

- scored rows: 2/3; min=0.0000 max=0.0000 mean=0.0000

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 20 --seed 42 --decode-profile qwen3-8b --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260927T005233Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T005233Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T005233Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T005233Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T005233Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3-8b/merger_agreement/RUN-20-MERGER_AGREEMENT-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
