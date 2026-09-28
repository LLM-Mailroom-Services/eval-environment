# Run report — `20260928T053903Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T053903Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 50 docs, seed 42 |
| timestamp | `2026-09-28T05:39:03+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T053903Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:43:42+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 50 / None |
| scorer | extraction |
| decode profile | — |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T053903Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:39:03+00:00` |
| finished_at | `2026-09-28T05:43:42+00:00` |
| duration_s (wall) | 281.4000 |
| latency_ms_mean | 40475.3 |
| latency_ms_p95 | 50805.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7846 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7846** (sd 0.0860, min 0.6317, max 0.9779) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 281.4000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0264** USD |
| cost estimated (roster token rates) | **0.0264** USD |
| cost per document (actual) | 0.0005 USD |
| cost per document (estimated) | 0.0005 USD |
| latency e2e / p50 / p95 / max | 281.4000 / 39.5515 / 50.8056 / 59.9949 s |
| prompt / completion / total tokens | 114073 / 176597 / 290670 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2023.8 s vs wall = 281.4 s -> wall/serial factor 7.19x at concurrency 8.

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
| `insurance_claims_specialist` | 50 | 114073 | 176597 | 290670 | 0.0264 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2023.8 s over wall 281.4 s = **7.19×** effective parallelism at c8 (90% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:property:269879669.txt` (property) 60.0 s = 21% of wall — p95/p50 = 1.28×.
- **Prompt length vs latency:** Pearson r = 0.64 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3532 tok/doc, mean prompt 2281 tok/doc.
- **Subclass spread:** best `auto` 0.886 (n=16), worst `carrier` 0.704 (n=5).
- **Field-level extraction:** 0/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 16 | 0.8860 |
| pde | 9 | 0.7085 |
| property | 8 | 0.7643 |
| outpatient | 7 | 0.7330 |
| carrier | 5 | 0.7044 |
| inpatient | 5 | 0.7817 |
| **total** | **50** | **0.7846** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.7489 | 0.6957 | 30.6689 | 1922 | 2794 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8583 | 0.7826 | 36.0266 | 1853 | 3301 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7226 | 0.6364 | 45.6662 | 2005 | 4241 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.6317 | 0.5715 | 38.1132 | 2011 | 3443 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7347 | 0.6364 | 33.3276 | 2032 | 2954 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.6580 | 0.6364 | 31.3084 | 1922 | 2726 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.9221 | 0.8000 | 44.7462 | 1884 | 4038 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.8702 | 0.7826 | 34.0182 | 1856 | 2888 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9779 | 0.8182 | 34.3214 | 1859 | 3340 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6580 | 0.6364 | 30.1983 | 1933 | 2961 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7226 | 0.6364 | 39.1992 | 2043 | 3675 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8464 | 0.7826 | 35.0524 | 1860 | 3336 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8469 | 0.7826 | 26.3515 | 1860 | 2408 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.9268 | 0.8000 | 32.1065 | 1883 | 3192 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.7489 | 0.6957 | 44.5209 | 1920 | 4371 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7226 | 0.6364 | 40.8549 | 2088 | 3717 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.7978 | 0.6957 | 36.8866 | 2129 | 3411 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.9213 | 0.8000 | 36.8656 | 1884 | 3312 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.6580 | 0.6364 | 48.9141 | 1946 | 4191 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.7343 | 0.5600 | 47.2815 | 4562 | 3860 | — |
| 21 | `corpus:ground_truth:train:auto:CLM-000355.txt` | auto | 0.9223 | 0.8000 | 39.4460 | 1883 | 3373 | — |
| 22 | `corpus:ground_truth:train:insurbias-535.txt` | auto | 0.8508 | 0.7826 | 35.0457 | 1859 | 2849 | — |
| 23 | `corpus:ground_truth:train:pde:233734492807320.txt` | pde | 0.7489 | 0.6957 | 48.8687 | 1941 | 4169 | — |
| 24 | `corpus:ground_truth:train:property:268405870.txt` | property | 0.6689 | 0.5000 | 48.3915 | 4215 | 4200 | — |
| 25 | `corpus:ground_truth:train:outpatient:542762281171383:1.txt` | outpatient | 0.7347 | 0.6364 | 36.0120 | 2034 | 3174 | — |
| 26 | `corpus:ground_truth:train:property:261716804.txt` | property | 0.7437 | 0.5834 | 56.8228 | 4002 | 4528 | — |
| 27 | `corpus:ground_truth:train:carrier:887263386589340.txt` | carrier | 0.7226 | 0.6364 | 35.4081 | 1999 | 3271 | — |
| 28 | `corpus:ground_truth:train:outpatient:542062281218793:1.txt` | outpatient | 0.7347 | 0.6364 | 32.1753 | 2027 | 2956 | — |
| 29 | `corpus:ground_truth:train:insurbias-1222.txt` | auto | 0.8576 | 0.7826 | 44.1647 | 1855 | 3647 | — |
| 30 | `corpus:ground_truth:train:inpatient:196401177008033:1.txt` | inpatient | 0.7353 | 0.6364 | 42.8051 | 2187 | 3761 | — |
| 31 | `corpus:ground_truth:train:property:269879669.txt` | property | 0.8485 | 0.6923 | 59.9949 | 3540 | 5051 | — |
| 32 | `corpus:ground_truth:train:pde:233024489630762.txt` | pde | 0.6580 | 0.6364 | 44.8799 | 1943 | 3456 | — |
| 33 | `corpus:ground_truth:train:insurbias-976.txt` | auto | 0.8738 | 0.7826 | 35.1371 | 1854 | 3150 | — |
| 34 | `corpus:ground_truth:train:insurbias-914.txt` | auto | 0.8854 | 0.7826 | 37.1470 | 1868 | 2986 | — |
| 35 | `corpus:ground_truth:train:pde:233654491978707.txt` | pde | 0.7489 | 0.6957 | 35.5569 | 1939 | 3237 | — |
| 36 | `corpus:ground_truth:train:property:267944087.txt` | property | 0.7434 | 0.5600 | 40.2855 | 3435 | 3515 | — |
| 37 | `corpus:ground_truth:train:inpatient:196451176994433:1.txt` | inpatient | 0.8127 | 0.6957 | 39.5515 | 2140 | 3397 | — |
| 38 | `corpus:ground_truth:train:pde:233634491375303.txt` | pde | 0.7489 | 0.6957 | 37.6020 | 1941 | 3533 | — |
| 39 | `corpus:ground_truth:train:outpatient:542712281056440:1.txt` | outpatient | 0.7347 | 0.6364 | 36.8968 | 2064 | 3042 | — |
| 40 | `corpus:ground_truth:train:auto:CLM-000809.txt` | auto | 0.8762 | 0.8148 | 41.0699 | 1924 | 3496 | — |
| 41 | `corpus:ground_truth:train:inpatient:196991176968589:1.txt` | inpatient | 0.7766 | 0.6957 | 42.5904 | 2157 | 3464 | — |
| 42 | `corpus:ground_truth:train:outpatient:542922281376960:1.txt` | outpatient | 0.7347 | 0.6364 | 47.9207 | 2031 | 4199 | — |
| 43 | `corpus:ground_truth:train:outpatient:542472281487558:1.txt` | outpatient | 0.7347 | 0.6364 | 41.8275 | 2071 | 3647 | — |
| 44 | `corpus:ground_truth:train:carrier:887393389256013.txt` | carrier | 0.7226 | 0.6364 | 46.3341 | 2056 | 3818 | — |
| 45 | `corpus:ground_truth:train:property:262548994.txt` | property | 0.6539 | 0.5000 | 50.6460 | 3835 | 4171 | — |
| 46 | `corpus:ground_truth:train:property:261515174.txt` | property | 0.8728 | 0.6957 | 49.4622 | 3870 | 3858 | — |
| 47 | `corpus:ground_truth:train:insurbias-969.txt` | auto | 0.8540 | 0.7826 | 40.7197 | 1857 | 3106 | — |
| 48 | `corpus:ground_truth:train:auto:CLM-000249.txt` | auto | 0.8860 | 0.8148 | 37.7365 | 1923 | 3160 | — |
| 49 | `corpus:ground_truth:train:property:263266666.txt` | property | 0.8488 | 0.6154 | 50.8056 | 4006 | 4462 | — |
| 50 | `corpus:ground_truth:train:inpatient:196781176972873:1.txt` | inpatient | 0.7859 | 0.6364 | 42.0309 | 2165 | 3762 | — |

- scored rows: 50/50; min=0.6317 max=0.9779 mean=0.7846

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 50 --seed 42 --concurrency 8 --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260928T053903Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T053903Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T053903Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T053903Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T053903Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/insurance_claims/RUN-50-INSURANCE_CLAIM-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
