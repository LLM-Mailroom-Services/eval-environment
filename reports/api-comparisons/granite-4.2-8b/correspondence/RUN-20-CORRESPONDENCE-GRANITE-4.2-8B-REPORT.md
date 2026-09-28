# Run report — `20260927T053647Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T053647Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-27T05:36:47+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T053647Z-eval-correspondence/subset_manifest.json` |
| eval git | `1d9f8d2` |
| finished | `2026-09-27T05:41:17+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | granite-4.2-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T053647Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T05:36:47+00:00` |
| finished_at | `2026-09-27T05:41:17+00:00` |
| duration_s (wall) | 272.3000 |
| latency_ms_mean | 76726.2 |
| latency_ms_p95 | 146506.5 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4065 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4065** (sd 0.2084, min 0.0000, max 0.7000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 272.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.8000** USD |
| cost actual (derived from case rows) | **0.0292** USD |
| cost estimated (roster token rates) | **0.0292** USD |
| cost per document (actual) | 0.0015 USD |
| cost per document (estimated) | 0.0015 USD |
| latency e2e / p50 / p95 / max | 272.3000 / 87.6437 / 146.5065 / 165.9316 s |
| prompt / completion / total tokens | 51943 / 104315 / 156258 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1534.5 s vs wall = 272.3 s -> wall/serial factor 5.64x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | True |
| per-agent completion budgets | `{"contracts_specialist": 16384, "corporate_records_specialist": 16384, "correspondence_specialist": 16384, "insurance_claims_specialist": 12288, "merger_agreement_specialist": 32768}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `correspondence_specialist` | 20 | 51943 | 104315 | 156258 | 0.0292 | ibm-granite/granite-4.2-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1534.5 s over wall 272.3 s = **5.64×** effective parallelism at c8 (70% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:dasovich-j/all_documents/10751.` (notice) 165.9 s = 61% of wall — p95/p50 = 1.67×.
- **Prompt length vs latency:** Pearson r = 0.36 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 5216 tok/doc, mean prompt 2597 tok/doc.
- **Subclass spread:** best `meeting_request` 0.633 (n=1), worst `letter` 0.281 (n=2).
- **Field-level extraction:** 4/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 10 | 0.3620 |
| press_release | 4 | 0.5203 |
| notice | 3 | 0.4111 |
| letter | 2 | 0.2812 |
| meeting_request | 1 | 0.6333 |
| **total** | **20** | **0.4065** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1539 | 60.2766 | 1713 | 4328 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5000 | 0.2666 | 104.1093 | 1682 | 7158 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.5769 | 0.2000 | 59.3835 | 6475 | 4252 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.4190 | 0.1176 | 87.6437 | 1742 | 6063 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.0000 | 0.0000 | 0.8407 | 2073 | 2 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.0000 | 0.0000 | 2.5482 | 2004 | 102 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 98.0349 | 1868 | 6735 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.7000 | 0.2222 | 89.9464 | 2663 | 6203 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.2500 | 0.2500 | 38.9353 | 1648 | 2841 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5555 | 0.2105 | 135.2252 | 2724 | 9163 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.5625 | 0.2105 | 98.0638 | 2066 | 6430 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.3409 | 0.1818 | 36.8955 | 1640 | 2316 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 79.8995 | 2053 | 5077 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.3887 | 0.1052 | 124.6584 | 1936 | 8195 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.3259 | 0.0000 | 146.5065 | 2044 | 10208 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2105 | 115.5624 | 1792 | 7588 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.0000 | 0.0000 | 0.5773 | 1647 | 2 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.6833 | 0.2222 | 165.9316 | 10306 | 11967 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4520 | 0.1539 | 2.0131 | 2216 | 137 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1429 | 87.4728 | 1651 | 5548 | — |

- scored rows: 20/20; min=0.0000 max=0.7000 mean=0.4065

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 20 --seed 42 --concurrency 8 --decode-profile granite-4.2-8b --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260927T053647Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T053647Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T053647Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T053647Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T053647Z-eval-correspondence.md` | experiment-log markdown mirror |
| `/workspace/reports/api-comparisons/granite-4.2-8b/correspondence/RUN-20-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
