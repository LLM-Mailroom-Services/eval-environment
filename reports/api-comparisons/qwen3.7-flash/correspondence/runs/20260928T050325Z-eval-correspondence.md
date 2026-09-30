# Run report — `20260928T050325Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T050325Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-28T05:03:25+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T050325Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:05:30+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | — |
| prompt source / lineage | frozen / mutation |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T050325Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:03:25+00:00` |
| finished_at | `2026-09-28T05:05:30+00:00` |
| duration_s (wall) | 125.1000 |
| latency_ms_mean | 35887.9 |
| latency_ms_p95 | 55219.8 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5104 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5103** (sd 0.1177, min 0.2780, max 0.6833) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 125.1000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0089** USD |
| cost estimated (roster token rates) | **0.0089** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 125.1000 / 34.3262 / 55.2198 / 87.7869 s |
| prompt / completion / total tokens | 49919 / 57329 / 107248 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 717.8 s vs wall = 125.1 s -> wall/serial factor 5.74x at concurrency 8.

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
| `correspondence_specialist` | 20 | 49919 | 57329 | 107248 | 0.0089 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 717.8 s over wall 125.1 s = **5.74×** effective parallelism at c8 (72% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:dasovich-j/all_documents/13056.` (press_release) 87.8 s = 70% of wall — p95/p50 = 1.61×.
- **Prompt length vs latency:** Pearson r = 0.13 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 2866 tok/doc, mean prompt 2496 tok/doc.
- **Subclass spread:** best `meeting_request` 0.633 (n=1), worst `email` 0.462 (n=10).
- **Field-level extraction:** 1/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.4623 |
| press_release | 4 | 0.6136 |
| notice | 3 | 0.4788 |
| letter | 2 | 0.5300 |
| meeting_request | 1 | 0.6333 |
| **total** | **20** | **0.5103** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1429 | 34.3262 | 1642 | 2694 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 37.5603 | 1604 | 3241 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 35.5176 | 6101 | 2859 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2666 | 26.7733 | 1667 | 2241 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4475 | 0.1000 | 32.8875 | 2031 | 2833 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 35.4390 | 1929 | 3047 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 31.4997 | 1782 | 2959 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 32.1096 | 2601 | 2994 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.3322 | 0.2500 | 19.9485 | 1569 | 1599 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5555 | 0.2105 | 87.7869 | 2585 | 4387 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.6125 | 0.2105 | 36.4812 | 1955 | 2991 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 21.0178 | 1564 | 1534 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 40.3433 | 1978 | 3367 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 37.2359 | 1874 | 3183 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.6654 | 0.2105 | 55.2198 | 1969 | 4606 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5750 | 0.2105 | 29.7926 | 1710 | 2428 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.2857 | 25.6882 | 1570 | 2164 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.5833 | 0.2105 | 38.3940 | 10072 | 3543 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4465 | 0.1250 | 32.9424 | 2141 | 2577 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1333 | 26.7936 | 1575 | 2082 | — |

- scored rows: 20/20; min=0.2780 max=0.6833 mean=0.5104

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T050325Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T050325Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T050325Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T050325Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T050325Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-20-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
