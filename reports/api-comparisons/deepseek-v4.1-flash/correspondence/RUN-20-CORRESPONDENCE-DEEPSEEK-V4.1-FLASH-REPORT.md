# Run report — `20260927T105317Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T105317Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-27T10:53:17+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T105317Z-eval-correspondence/subset_manifest.json` |
| eval git | `7712588` |
| finished | `2026-09-27T10:53:56+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T105317Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T10:53:17+00:00` |
| finished_at | `2026-09-27T10:53:56+00:00` |
| duration_s (wall) | 40.3000 |
| latency_ms_mean | 7393.5 |
| latency_ms_p95 | 14399.5 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4419 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4419** (sd 0.1525, min 0.2179, max 0.7333) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 40.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0121** USD |
| cost estimated (roster token rates) | **0.0121** USD |
| cost per document (actual) | 0.0006 USD |
| cost per document (estimated) | 0.0006 USD |
| latency e2e / p50 / p95 / max | 40.3000 / 7.6745 / 14.3995 / 18.7202 s |
| prompt / completion / total tokens | 48744 / 35712 / 84456 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 147.9 s vs wall = 40.3 s -> wall/serial factor 3.67x at concurrency 8.

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
| `correspondence_specialist` | 20 | 48744 | 35712 | 84456 | 0.0121 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 147.9 s over wall 40.3 s = **3.67×** effective parallelism at c8 (46% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:motley-m/deleted_items/63.` (email) 18.7 s = 46% of wall — p95/p50 = 1.88×.
- **Prompt length vs latency:** Pearson r = 0.38 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 1786 tok/doc, mean prompt 2437 tok/doc.
- **Subclass spread:** best `meeting_request` 0.633 (n=1), worst `notice` 0.353 (n=3).
- **Field-level extraction:** 5/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.4561 |
| press_release | 4 | 0.3911 |
| notice | 3 | 0.3531 |
| letter | 2 | 0.5103 |
| meeting_request | 1 | 0.6333 |
| **total** | **20** | **0.4419** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1333 | 4.8020 | 1608 | 1128 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.2179 | 0.0000 | 8.0845 | 1580 | 1613 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.6731 | 0.2000 | 14.3995 | 5980 | 4398 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2222 | 5.8325 | 1652 | 1169 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 10.0786 | 1971 | 1924 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2502 | 0.0000 | 9.3821 | 1881 | 2869 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 11.8722 | 1773 | 2223 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.7333 | 0.2222 | 5.3756 | 2505 | 1359 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.2500 | 0.2500 | 1.5012 | 1566 | 376 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.3068 | 0.0000 | 9.5548 | 2539 | 3274 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.5625 | 0.2000 | 3.4510 | 1921 | 993 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.3368 | 0.2222 | 0.9441 | 1539 | 283 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 6.4467 | 1939 | 1423 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.4959 | 0.1111 | 8.5912 | 1818 | 2285 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.3066 | 0.0000 | 5.0126 | 1962 | 1025 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5750 | 0.2222 | 7.6745 | 1693 | 1645 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3077 | 1.4594 | 1566 | 290 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.2340 | 0.0000 | 10.5319 | 9602 | 2438 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4798 | 0.1052 | 18.7202 | 2078 | 4335 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1333 | 4.1547 | 1571 | 662 | — |

- scored rows: 20/20; min=0.2179 max=0.7333 mean=0.4419

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260927T105317Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T105317Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T105317Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T105317Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T105317Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/correspondence/runs/20260927T105317Z-eval-correspondence.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
