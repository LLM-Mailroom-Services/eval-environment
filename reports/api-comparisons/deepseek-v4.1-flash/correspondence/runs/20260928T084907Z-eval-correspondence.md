# Run report — `20260928T084907Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T084907Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v2` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-28T08:49:07+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T084907Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:50:18+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T084907Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:49:07+00:00` |
| finished_at | `2026-09-28T08:50:18+00:00` |
| duration_s (wall) | 72.5000 |
| latency_ms_mean | 9544.9 |
| latency_ms_p95 | 22374.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4248 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4248** (sd 0.1700, min 0.0000, max 0.6833) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 72.5000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0108** USD |
| cost estimated (roster token rates) | **0.0108** USD |
| cost per document (actual) | 0.0005 USD |
| cost per document (estimated) | 0.0005 USD |
| latency e2e / p50 / p95 / max | 72.5000 / 5.8633 / 22.3744 / 30.3222 s |
| prompt / completion / total tokens | 49190 / 31395 / 80585 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 190.9 s vs wall = 72.5 s -> wall/serial factor 2.63x at concurrency 8.

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
| `correspondence_specialist` | 20 | 49190 | 31395 | 80585 | 0.0108 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 190.9 s over wall 72.5 s = **2.63×** effective parallelism at c8 (33% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:donoho-l/inbox/35.` (email) 30.3 s = 42% of wall — p95/p50 = 3.82×.
- **Prompt length vs latency:** Pearson r = 0.32 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 1570 tok/doc, mean prompt 2460 tok/doc.
- **Subclass spread:** best `meeting_request` 0.633 (n=1), worst `notice` 0.336 (n=3).
- **Field-level extraction:** 6/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.4245 |
| press_release | 4 | 0.3912 |
| notice | 3 | 0.3364 |
| letter | 2 | 0.5217 |
| meeting_request | 1 | 0.6333 |
| **total** | **20** | **0.4248** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1429 | 2.3632 | 1638 | 516 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.2679 | 0.0000 | 5.0934 | 1610 | 1272 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.6346 | 0.2000 | 14.5429 | 6010 | 2562 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2353 | 4.4391 | 1660 | 719 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4809 | 0.1000 | 2.9714 | 1979 | 629 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2502 | 0.0000 | 19.7462 | 1933 | 2881 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 11.6531 | 1781 | 1638 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2105 | 4.0440 | 2535 | 946 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.0000 | 0.0000 | 2.9718 | 1596 | 586 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.3068 | 0.0000 | 13.2941 | 2569 | 2877 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.5625 | 0.2105 | 2.4485 | 1951 | 592 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.3368 | 0.2000 | 2.9242 | 1569 | 350 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 8.7381 | 1969 | 1319 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.4959 | 0.1111 | 30.3222 | 1848 | 4191 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.3067 | 0.0000 | 22.3744 | 1970 | 4052 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5750 | 0.2222 | 5.8633 | 1701 | 1032 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3333 | 2.0817 | 1596 | 242 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.1840 | 0.0000 | 17.6384 | 9610 | 3273 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4520 | 0.1052 | 15.8155 | 2086 | 1313 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1429 | 1.5724 | 1579 | 405 | — |

- scored rows: 20/20; min=0.0000 max=0.6833 mean=0.4248

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T084907Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T084907Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T084907Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T084907Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T084907Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/correspondence/RUN-20-CORRESPONDENCE-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
