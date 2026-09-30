# Run report — `20260926T234603Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260926T234603Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 20 docs, seed 42 |
| timestamp | `2026-09-26T23:46:03+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260926T234603Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `fe120a8` |
| finished | `2026-09-26T23:49:16+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260926T234603Z-eval-insurance_claims', 'dataset': 'mailroom-hf-46a4d3c2', 'dataset_records': 20}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-26T23:46:03+00:00` |
| finished_at | `2026-09-26T23:49:16+00:00` |
| duration_s (wall) | 195.0000 |
| latency_ms_mean | 8609.0 |
| latency_ms_p95 | 11533.0 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.8056 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.8056** (sd 0.0768, min 0.7058, max 0.9804) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 195.0000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0095** USD |
| cost estimated (roster token rates) | **0.0095** USD |
| cost per document (actual) | 0.0005 USD |
| cost per document (estimated) | 0.0005 USD |
| latency e2e / p50 / p95 / max | 195.0000 / 7.6213 / 11.5330 / 21.4203 s |
| prompt / completion / total tokens | 51248 / 7641 / 58889 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 172.2 s vs wall = 195.0 s -> wall/serial factor 0.88x at concurrency 1.

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
| `insurance_claims_specialist` | 20 | 51248 | 7641 | 58889 | 0.0095 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 172.2 s over wall 195.0 s = **0.88×** effective parallelism at c1 (88% of the ideal 1×).
- **Tail:** slowest doc `corpus:ground_truth:train:inpatient:196411177017295:1.txt` (inpatient) 21.4 s = 11% of wall — p95/p50 = 1.51×.
- **Prompt length vs latency:** Pearson r = 0.26 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 382 tok/doc, mean prompt 2562 tok/doc.
- **Subclass spread:** best `auto` 0.890 (n=8), worst `pde` 0.725 (n=5).
- **Field-level extraction:** 0/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 8 | 0.8900 |
| pde | 5 | 0.7246 |
| carrier | 3 | 0.7507 |
| outpatient | 2 | 0.7633 |
| inpatient | 1 | 0.8238 |
| property | 1 | 0.7670 |
| **total** | **20** | **0.8056** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.7280 | 0.6364 | 7.0844 | 2411 | 345 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8537 | 0.7500 | 6.5265 | 2343 | 327 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7548 | 0.5385 | 7.9535 | 2492 | 445 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.7482 | 0.5385 | 7.6213 | 2498 | 404 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7994 | 0.6364 | 8.0425 | 2522 | 431 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.7327 | 0.6364 | 7.3253 | 2411 | 372 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.8822 | 0.7692 | 10.1412 | 2374 | 364 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.8882 | 0.7500 | 7.5106 | 2346 | 363 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9804 | 0.7826 | 6.8573 | 2349 | 370 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.7288 | 0.6364 | 11.0161 | 2422 | 356 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7272 | 0.5385 | 7.4436 | 2533 | 397 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8640 | 0.7500 | 6.1674 | 2350 | 339 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8742 | 0.7500 | 10.8849 | 2350 | 337 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.8887 | 0.7692 | 7.7563 | 2373 | 406 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.7058 | 0.6364 | 6.1141 | 2409 | 323 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7491 | 0.5385 | 7.6836 | 2573 | 410 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.8238 | 0.5714 | 21.4203 | 2616 | 464 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.8889 | 0.7692 | 6.5612 | 2374 | 366 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.7277 | 0.6364 | 6.5360 | 2435 | 343 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.7670 | 0.5385 | 11.5330 | 5067 | 479 | — |

- scored rows: 20/20; min=0.7058 max=0.9804 mean=0.8056

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 20 --seed 42 --concurrency 1 --decode-profile qwen3-8b --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260926T234603Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260926T234603Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260926T234603Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260926T234603Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260926T234603Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3-8b/insurance_claims/RUN-20-INSURANCE_CLAIM-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
