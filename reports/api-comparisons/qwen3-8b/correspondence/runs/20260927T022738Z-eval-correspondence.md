# Run report — `20260927T022738Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T022738Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-27T02:27:38+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T022738Z-eval-correspondence/subset_manifest.json` |
| eval git | `fd6a220` |
| finished | `2026-09-27T02:30:47+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T022738Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T02:27:38+00:00` |
| finished_at | `2026-09-27T02:30:47+00:00` |
| duration_s (wall) | 191.0000 |
| latency_ms_mean | 56321.2 |
| latency_ms_p95 | 133521.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.0 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.0000** (sd 0.0000, min 0.0000, max 0.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 191.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0287** USD |
| cost estimated (roster token rates) | **0.0287** USD |
| cost per document (actual) | 0.0014 USD |
| cost per document (estimated) | 0.0014 USD |
| latency e2e / p50 / p95 / max | 191.0000 / 25.0867 / 133.5216 / 147.6044 s |
| prompt / completion / total tokens | 48452 / 50672 / 99124 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1126.4 s vs wall = 191.0 s -> wall/serial factor 5.90x at concurrency 8.

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
| `correspondence_specialist` | 20 | 48452 | 50672 | 99124 | 0.0287 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1126.4 s over wall 191.0 s = **5.90×** effective parallelism at c8 (74% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:donoho-l/inbox/35.` (email) 147.6 s = 77% of wall — p95/p50 = 5.32×.
- **Prompt length vs latency:** Pearson r = 0.29 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 2534 tok/doc, mean prompt 2423 tok/doc.
- **Subclass spread:** best `email` 0.000 (n=10), worst `email` 0.000 (n=10).
- **Field-level extraction:** 20/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.0000 |
| press_release | 4 | 0.0000 |
| notice | 3 | 0.0000 |
| letter | 2 | 0.0000 |
| meeting_request | 1 | 0.0000 |
| **total** | **20** | **0.0000** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.0000 | 0.0000 | 15.1880 | 1576 | 719 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.0000 | 0.0000 | 13.6553 | 1539 | 499 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.0000 | 0.0000 | 15.7267 | 5990 | 586 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.0000 | 0.0000 | 98.9224 | 1603 | 4791 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.0000 | 0.0000 | 19.8376 | 1958 | 1003 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.0000 | 0.0000 | 16.8000 | 1854 | 840 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.0000 | 0.0000 | 18.5177 | 1717 | 893 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.0000 | 0.0000 | 92.8587 | 2513 | 4767 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.0000 | 0.0000 | 14.0525 | 1505 | 721 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.0000 | 0.0000 | 123.9451 | 2485 | 4997 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.0000 | 0.0000 | 25.0867 | 1887 | 1239 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.0000 | 0.0000 | 11.6486 | 1500 | 549 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.0000 | 0.0000 | 99.5406 | 1901 | 4691 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.0000 | 0.0000 | 147.6044 | 1805 | 5969 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.0000 | 0.0000 | 50.1052 | 1906 | 2344 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.0000 | 0.0000 | 118.6407 | 1640 | 4467 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.0000 | 0.0000 | 12.5481 | 1505 | 745 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.0000 | 0.0000 | 133.5216 | 9997 | 5849 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.0000 | 0.0000 | 15.6700 | 2060 | 663 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.0000 | 0.0000 | 82.5544 | 1511 | 4340 | — |

- scored rows: 20/20; min=0.0000 max=0.0000 mean=0.0000

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 8 --decode-profile qwen3-8b --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260927T022738Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T022738Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T022738Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T022738Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T022738Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3-8b/RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
