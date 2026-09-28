# Run report — `20260927T033031Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T033031Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-27T03:30:31+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T033031Z-eval-correspondence/subset_manifest.json` |
| eval git | `4b973b7` |
| finished | `2026-09-27T03:50:59+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | qwen3-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T033031Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T03:30:31+00:00` |
| finished_at | `2026-09-27T03:50:59+00:00` |
| duration_s (wall) | 1230.1 |
| latency_ms_mean | 128861.3 |
| latency_ms_p95 | 150933.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.513 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5130** (sd 0.1057, min 0.2500, max 0.7000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 1230.1 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0604** USD |
| cost estimated (roster token rates) | **0.0604** USD |
| cost per document (actual) | 0.0030 USD |
| cost per document (estimated) | 0.0030 USD |
| latency e2e / p50 / p95 / max | 1230.1 / 84.1550 / 150.9337 / 1086.9 s |
| prompt / completion / total tokens | 87002 / 110287 / 197289 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2577.2 s vs wall = 1230.1 s -> wall/serial factor 2.10x at concurrency 8.

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
| `correspondence_specialist` | 39 | 87002 | 110287 | 197289 | 0.0604 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2577.2 s over wall 1230.1 s = **2.10×** effective parallelism at c8 (26% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:dasovich-j/all_documents/10751.` (notice) 1086.9 s = 88% of wall — p95/p50 = 1.79×.
- **Prompt length vs latency:** Pearson r = 0.52 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 5514 tok/doc, mean prompt 4350 tok/doc.
- **Subclass spread:** best `notice` 0.615 (n=3), worst `letter` 0.396 (n=2).
- **Field-level extraction:** 0/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.4841 |
| press_release | 4 | 0.5499 |
| notice | 3 | 0.6148 |
| letter | 2 | 0.3960 |
| meeting_request | 1 | 0.5833 |
| **total** | **20** | **0.5130** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1818 | 99.0435 | 3157 | 5150 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 128.6658 | 3083 | 5123 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.5577 | 0.2000 | 39.3791 | 11985 | 1334 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.4190 | 0.1429 | 106.3038 | 3211 | 5620 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4354 | 0.1000 | 150.9337 | 3921 | 6206 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.6111 | 0.1904 | 134.2710 | 3713 | 5397 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 55.4589 | 3439 | 2985 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.7000 | 0.2500 | 48.3339 | 5031 | 2369 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.2500 | 0.2500 | 23.3535 | 3015 | 915 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5000 | 0.2105 | 32.8376 | 4975 | 1941 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.3566 | 0.1111 | 136.7258 | 3779 | 7188 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.3636 | 44.9421 | 3005 | 1695 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.5833 | 0.2000 | 108.9905 | 3807 | 5852 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 49.5991 | 3615 | 2582 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.4496 | 0.1000 | 69.6412 | 3817 | 3465 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.6000 | 0.2353 | 84.1550 | 3285 | 4774 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3636 | 28.6864 | 3015 | 1396 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.6333 | 0.1333 | 1086.9 | 9997 | 39120 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5555 | 0.2353 | 47.4202 | 4125 | 1567 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.5000 | 0.3077 | 101.5425 | 3027 | 5608 | — |

- scored rows: 20/20; min=0.2500 max=0.7000 mean=0.5130

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 8 --decode-profile qwen3-8b --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260927T033031Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T033031Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T033031Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T033031Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T033031Z-eval-correspondence.md` | experiment-log markdown mirror |
| `/workspace/reports/api-comparisons/qwen3-8b/RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- **Call count:** `39` specialist LLM calls for `20` documents — this is **not** source chunking when `needed_chunks=1` (here max `1`). Extra calls are JSON parse / network **retries** (`llm_call_budget=2`). Do not apply merger 48K chunk settings to correspondence or insurance.
- **High retry rate:** calls exceed ~1.5× document count — see runbook §4 (concurrency reliability) before accepting the wave as canonical.
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
