# Run report — `20260926T234358Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260926T234358Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-26T23:43:58+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260926T234358Z-eval-correspondence/subset_manifest.json` |
| eval git | `fe120a8` |
| finished | `2026-09-26T23:46:00+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / node |
| mode | real |
| concurrency | 1 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | qwen3-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260926T234358Z-eval-correspondence', 'dataset': 'mailroom-hf-46a4d3c2', 'dataset_records': 20}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-26T23:43:58+00:00` |
| finished_at | `2026-09-26T23:46:00+00:00` |
| duration_s (wall) | 123.4000 |
| latency_ms_mean | 3861.8 |
| latency_ms_p95 | 5505.8 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.3179 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.3179** (sd 0.1306, min 0.1109, max 0.5783) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 123.4000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0077** USD |
| cost estimated (roster token rates) | **0.0077** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 123.4000 / 3.8196 / 5.5058 / 6.8384 s |
| prompt / completion / total tokens | 53521 / 3197 / 56718 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 77.2 s vs wall = 123.4 s -> wall/serial factor 0.63x at concurrency 1.

## Decode posture

| control | value |
|---|---|
| sampling override | `none (pipeline posture)` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 8192, "corporate_records_specialist": 8192, "correspondence_specialist": 4096, "insurance_claims_specialist": 6144, "merger_agreement_specialist": 8192}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `correspondence_specialist` | 20 | 53521 | 3197 | 56718 | 0.0077 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 77.2 s over wall 123.4 s = **0.63×** effective parallelism at c1 (63% of the ideal 1×).
- **Tail:** slowest doc `corpus:ground_truth:train:dasovich-j/all_documents/10751.` (notice) 6.8 s = 6% of wall — p95/p50 = 1.44×.
- **Prompt length vs latency:** Pearson r = 0.72 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 160 tok/doc, mean prompt 2676 tok/doc.
- **Subclass spread:** best `press_release` 0.370 (n=4), worst `notice` 0.273 (n=3).
- **Field-level extraction:** 11/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.3072 |
| press_release | 4 | 0.3705 |
| notice | 3 | 0.2733 |
| letter | 2 | 0.3140 |
| meeting_request | 1 | 0.3558 |
| **total** | **20** | **0.3179** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4058 | 0.0000 | 3.9533 | 1829 | 159 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.3857 | 0.1333 | 3.0659 | 1791 | 134 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.3269 | 0.1052 | 5.0180 | 6244 | 148 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.2789 | 0.0000 | 3.0205 | 1857 | 138 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4409 | 0.1000 | 4.1146 | 2212 | 187 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2607 | 0.0000 | 4.9156 | 2107 | 251 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.3244 | 0.1000 | 4.3575 | 1971 | 192 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.5552 | 0.1111 | 3.9382 | 2765 | 178 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.1109 | 0.0000 | 2.2145 | 1759 | 76 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.1947 | 0.0000 | 3.4075 | 2737 | 147 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.1872 | 0.0000 | 3.8196 | 2141 | 174 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.3143 | 0.1818 | 2.5446 | 1754 | 101 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.3558 | 0.0000 | 3.6383 | 2154 | 160 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.5783 | 0.1052 | 4.5482 | 2059 | 201 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.3464 | 0.0000 | 5.5058 | 2159 | 276 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.3909 | 0.1052 | 3.3608 | 1894 | 162 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.1109 | 0.0000 | 2.5310 | 1759 | 89 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.1683 | 0.0000 | 6.8384 | 10251 | 169 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4465 | 0.1176 | 3.5021 | 2313 | 146 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.1752 | 0.0000 | 2.9425 | 1765 | 109 | — |

- scored rows: 20/20; min=0.1109 max=0.5783 mean=0.3179

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 1 --decode-profile qwen3-8b --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260926T234358Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260926T234358Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260926T234358Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260926T234358Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260926T234358Z-eval-correspondence.md` | experiment-log markdown mirror |
| `/workspace/reports/api-comparisons/qwen3-8b/RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
