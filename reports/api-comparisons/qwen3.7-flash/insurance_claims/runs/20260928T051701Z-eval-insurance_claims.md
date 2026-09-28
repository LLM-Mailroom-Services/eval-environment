# Run report — `20260928T051701Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T051701Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 20 docs, seed 42 |
| timestamp | `2026-09-28T05:17:01+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T051701Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:19:00+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T051701Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:17:01+00:00` |
| finished_at | `2026-09-28T05:19:00+00:00` |
| duration_s (wall) | 121.0000 |
| latency_ms_mean | 37009.2 |
| latency_ms_p95 | 40900.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7894 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7894** (sd 0.0969, min 0.6580, max 0.9785) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 121.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0099** USD |
| cost estimated (roster token rates) | **0.0099** USD |
| cost per document (actual) | 0.0005 USD |
| cost per document (estimated) | 0.0005 USD |
| latency e2e / p50 / p95 / max | 121.0000 / 37.8743 / 40.9007 / 43.6706 s |
| prompt / completion / total tokens | 41452 / 66346 / 107798 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 740.2 s vs wall = 121.0 s -> wall/serial factor 6.12x at concurrency 8.

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
| `insurance_claims_specialist` | 20 | 41452 | 66346 | 107798 | 0.0099 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 740.2 s over wall 121.0 s = **6.12×** effective parallelism at c8 (76% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:property:266855223.txt` (property) 43.7 s = 36% of wall — p95/p50 = 1.08×.
- **Prompt length vs latency:** Pearson r = 0.45 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 3317 tok/doc, mean prompt 2073 tok/doc.
- **Subclass spread:** best `auto` 0.898 (n=8), worst `pde` 0.694 (n=5).
- **Field-level extraction:** 0/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 8 | 0.8980 |
| pde | 5 | 0.6944 |
| carrier | 3 | 0.7226 |
| outpatient | 2 | 0.7287 |
| inpatient | 1 | 0.7535 |
| property | 1 | 0.7532 |
| **total** | **20** | **0.7894** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.7489 | 0.6957 | 40.7301 | 1922 | 3856 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8585 | 0.7826 | 37.5302 | 1853 | 3328 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7226 | 0.6364 | 37.8743 | 2005 | 3431 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.7226 | 0.6364 | 35.8315 | 2011 | 3401 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7347 | 0.6364 | 40.7579 | 2032 | 3450 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.6580 | 0.6364 | 37.2295 | 1922 | 3133 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.9221 | 0.8000 | 40.0744 | 1884 | 3361 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.8714 | 0.7826 | 33.3637 | 1856 | 2819 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9785 | 0.8182 | 34.1688 | 1859 | 3092 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6580 | 0.6364 | 29.2874 | 1933 | 2785 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7226 | 0.6364 | 38.0613 | 2043 | 3394 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8588 | 0.7826 | 33.5004 | 1860 | 3205 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8469 | 0.7826 | 29.9682 | 1860 | 2802 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.9268 | 0.8000 | 39.2688 | 1883 | 3705 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.7489 | 0.6957 | 40.0632 | 1920 | 3789 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7226 | 0.6364 | 38.1809 | 2088 | 3422 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.7535 | 0.6957 | 36.7823 | 2129 | 3192 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.9213 | 0.8000 | 32.9401 | 1884 | 3229 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.6580 | 0.6364 | 40.9007 | 1946 | 3367 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.7532 | 0.6154 | 43.6706 | 4562 | 3585 | — |

- scored rows: 20/20; min=0.6580 max=0.9785 mean=0.7894

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 20 --seed 42 --concurrency 8 --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260928T051701Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T051701Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T051701Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T051701Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T051701Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/insurance_claims/RUN-20-INSURANCE_CLAIM-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
