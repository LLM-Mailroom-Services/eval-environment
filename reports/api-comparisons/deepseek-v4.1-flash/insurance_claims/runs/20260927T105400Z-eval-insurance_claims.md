# Run report — `20260927T105400Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T105400Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `—` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 20 docs, seed 42 |
| timestamp | `2026-09-27T10:54:00+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T105400Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `3c2c95c` |
| finished | `2026-09-27T10:55:45+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T105400Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T10:54:00+00:00` |
| finished_at | `2026-09-27T10:55:45+00:00` |
| duration_s (wall) | 107.3000 |
| latency_ms_mean | 15101.9 |
| latency_ms_p95 | 79745.0 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7974 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7974** (sd 0.1022, min 0.6515, max 0.9666) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 107.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0135** USD |
| cost estimated (roster token rates) | **0.0135** USD |
| cost per document (actual) | 0.0007 USD |
| cost per document (estimated) | 0.0007 USD |
| latency e2e / p50 / p95 / max | 107.3000 / 7.9940 / 79.7450 / 92.0834 s |
| prompt / completion / total tokens | 40636 / 41615 / 82251 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 302.0 s vs wall = 107.3 s -> wall/serial factor 2.81x at concurrency 8.

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
| `insurance_claims_specialist` | 20 | 40636 | 41615 | 82251 | 0.0135 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 302.0 s over wall 107.3 s = **2.81×** effective parallelism at c8 (35% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:carrier:887623388590174.txt` (carrier) 92.1 s = 86% of wall — p95/p50 = 9.98×.
- **Prompt length vs latency:** Pearson r = 0.65 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 2081 tok/doc, mean prompt 2032 tok/doc.
- **Subclass spread:** best `auto` 0.912 (n=8), worst `property` 0.651 (n=1).
- **Field-level extraction:** 0/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 8 | 0.9117 |
| pde | 5 | 0.7058 |
| carrier | 3 | 0.7310 |
| outpatient | 2 | 0.7287 |
| inpatient | 1 | 0.8227 |
| property | 1 | 0.6515 |
| **total** | **20** | **0.7974** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.6883 | 0.5385 | 5.5174 | 1878 | 1887 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8651 | 0.7500 | 7.2372 | 1828 | 2384 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7512 | 0.6957 | 7.4352 | 1945 | 1633 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.7209 | 0.6364 | 6.8740 | 1957 | 2387 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7347 | 0.6364 | 8.2268 | 1987 | 1842 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.7489 | 0.6957 | 9.6512 | 1898 | 1972 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.9167 | 0.8148 | 10.1406 | 1872 | 2493 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.8794 | 0.7500 | 2.6077 | 1831 | 734 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9666 | 0.7826 | 14.6548 | 1857 | 3492 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6943 | 0.5600 | 9.9107 | 1888 | 2535 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7226 | 0.6364 | 5.0136 | 1998 | 1380 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8754 | 0.7500 | 7.9940 | 1858 | 1852 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8670 | 0.7500 | 11.0637 | 1857 | 2941 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.9607 | 0.8148 | 2.5602 | 1848 | 1079 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.6943 | 0.5600 | 3.3382 | 1899 | 661 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7209 | 0.5834 | 92.0834 | 2013 | 1678 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.8227 | 0.6957 | 3.4838 | 2046 | 1730 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.9631 | 0.8148 | 10.7708 | 1872 | 2795 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.7034 | 0.5834 | 3.7299 | 1920 | 667 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.6515 | 0.4800 | 79.7450 | 4384 | 5473 | — |

- scored rows: 20/20; min=0.6515 max=0.9666 mean=0.7974

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 20 --seed 42 --concurrency 8 --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260927T105400Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T105400Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T105400Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T105400Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T105400Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/insurance_claims/RUN-20-INSURANCE_CLAIM-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
