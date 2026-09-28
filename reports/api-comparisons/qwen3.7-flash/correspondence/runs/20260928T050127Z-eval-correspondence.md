# Run report — `20260928T050127Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T050127Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-28T05:01:27+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T050127Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:03:20+00:00` |

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
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T050127Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:01:27+00:00` |
| finished_at | `2026-09-28T05:03:20+00:00` |
| duration_s (wall) | 115.8000 |
| latency_ms_mean | 34089.2 |
| latency_ms_p95 | 51102.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5129 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5129** (sd 0.0982, min 0.2780, max 0.6833) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 115.8000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0088** USD |
| cost estimated (roster token rates) | **0.0088** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 115.8000 / 33.6434 / 51.1029 / 56.5836 s |
| prompt / completion / total tokens | 49313 / 56452 / 105765 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 681.8 s vs wall = 115.8 s -> wall/serial factor 5.89x at concurrency 8.

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
| `correspondence_specialist` | 20 | 49313 | 56452 | 105765 | 0.0088 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 681.8 s over wall 115.8 s = **5.89×** effective parallelism at c8 (74% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:donoho-l/inbox/35.` (email) 56.6 s = 49% of wall — p95/p50 = 1.52×.
- **Prompt length vs latency:** Pearson r = 0.36 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 2823 tok/doc, mean prompt 2466 tok/doc.
- **Subclass spread:** best `meeting_request` 0.633 (n=1), worst `notice` 0.470 (n=3).
- **Field-level extraction:** 1/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.4728 |
| press_release | 4 | 0.6039 |
| notice | 3 | 0.4704 |
| letter | 2 | 0.5353 |
| meeting_request | 1 | 0.6333 |
| **total** | **20** | **0.5129** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1250 | 34.2575 | 1612 | 2802 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 36.6529 | 1574 | 3070 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 34.4094 | 6071 | 2749 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2222 | 33.2456 | 1637 | 2621 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 33.6434 | 2001 | 2986 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 37.0449 | 1899 | 3172 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 34.1918 | 1752 | 2876 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 26.8632 | 2571 | 2310 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.5000 | 0.4444 | 25.1624 | 1539 | 1970 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5555 | 0.2105 | 38.8433 | 2549 | 3032 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.6125 | 0.2105 | 32.5455 | 1925 | 2662 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 24.7682 | 1534 | 1950 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 28.3118 | 1948 | 2411 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.4885 | 0.1000 | 56.5836 | 1844 | 4962 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.6269 | 0.2105 | 51.1029 | 1939 | 4496 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2105 | 25.8372 | 1680 | 2210 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.2857 | 25.7545 | 1540 | 2035 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.5833 | 0.2105 | 48.0202 | 10042 | 3563 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5020 | 0.1176 | 30.4149 | 2111 | 2772 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1539 | 24.1300 | 1545 | 1803 | — |

- scored rows: 20/20; min=0.2780 max=0.6833 mean=0.5129

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T050127Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T050127Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T050127Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T050127Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T050127Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-20-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
