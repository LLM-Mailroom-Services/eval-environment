# Run report — `20260928T054349Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T054349Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `insurance_claims_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 50 docs, seed 42 |
| timestamp | `2026-09-28T05:43:49+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T054349Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:48:20+00:00` |

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
| prompt source / lineage | frozen / mutation |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T054349Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:43:49+00:00` |
| finished_at | `2026-09-28T05:48:20+00:00` |
| duration_s (wall) | 272.3000 |
| latency_ms_mean | 39429.3 |
| latency_ms_p95 | 51438.1 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7812 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7812** (sd 0.0859, min 0.6317, max 0.9752) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 272.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0259** USD |
| cost estimated (roster token rates) | **0.0259** USD |
| cost per document (actual) | 0.0005 USD |
| cost per document (estimated) | 0.0005 USD |
| latency e2e / p50 / p95 / max | 272.3000 / 38.5930 / 51.4381 / 51.7765 s |
| prompt / completion / total tokens | 115273 / 172751 / 288024 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1971.5 s vs wall = 272.3 s -> wall/serial factor 7.24x at concurrency 8.

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
| `insurance_claims_specialist` | 50 | 115273 | 172751 | 288024 | 0.0259 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1971.5 s over wall 272.3 s = **7.24×** effective parallelism at c8 (91% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:property:262548994.txt` (property) 51.8 s = 19% of wall — p95/p50 = 1.33×.
- **Prompt length vs latency:** Pearson r = 0.56 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3455 tok/doc, mean prompt 2305 tok/doc.
- **Subclass spread:** best `auto` 0.887 (n=16), worst `carrier` 0.704 (n=5).
- **Field-level extraction:** 0/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 16 | 0.8865 |
| pde | 9 | 0.7085 |
| property | 8 | 0.7459 |
| outpatient | 7 | 0.7330 |
| carrier | 5 | 0.7044 |
| inpatient | 5 | 0.7755 |
| **total** | **50** | **0.7812** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.7489 | 0.6957 | 31.9118 | 1946 | 2711 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8585 | 0.7826 | 39.8168 | 1877 | 3362 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7226 | 0.6667 | 51.4266 | 2029 | 4335 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.6317 | 0.5715 | 47.1119 | 2035 | 4065 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7347 | 0.6364 | 36.6420 | 2056 | 3173 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.7489 | 0.6957 | 31.9052 | 1946 | 2670 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.9221 | 0.8000 | 38.0551 | 1908 | 3000 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.8791 | 0.7826 | 43.5305 | 1880 | 3561 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9752 | 0.8182 | 44.6851 | 1883 | 3532 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6580 | 0.6364 | 46.2808 | 1957 | 4011 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7226 | 0.6364 | 33.7612 | 2067 | 2960 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8588 | 0.7826 | 38.9523 | 1884 | 3274 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8469 | 0.7826 | 36.1521 | 1884 | 3143 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.9268 | 0.8000 | 32.5894 | 1907 | 2729 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.6580 | 0.6364 | 42.7053 | 1944 | 3720 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7226 | 0.6364 | 39.8021 | 2112 | 3484 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.7978 | 0.6957 | 34.7864 | 2153 | 3254 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.9213 | 0.8000 | 43.0578 | 1908 | 3506 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.6580 | 0.6364 | 33.9189 | 1970 | 3158 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.7353 | 0.5600 | 48.2027 | 4586 | 4564 | — |
| 21 | `corpus:ground_truth:train:auto:CLM-000355.txt` | auto | 0.9223 | 0.8000 | 32.9292 | 1907 | 2942 | — |
| 22 | `corpus:ground_truth:train:insurbias-535.txt` | auto | 0.8508 | 0.7826 | 34.8938 | 1883 | 2949 | — |
| 23 | `corpus:ground_truth:train:pde:233734492807320.txt` | pde | 0.7489 | 0.7273 | 35.5283 | 1965 | 3151 | — |
| 24 | `corpus:ground_truth:train:property:268405870.txt` | property | 0.6698 | 0.5000 | 51.6961 | 4239 | 4409 | — |
| 25 | `corpus:ground_truth:train:outpatient:542762281171383:1.txt` | outpatient | 0.7347 | 0.6364 | 32.3316 | 2058 | 3145 | — |
| 26 | `corpus:ground_truth:train:property:261716804.txt` | property | 0.7336 | 0.5185 | 41.1310 | 4026 | 3889 | — |
| 27 | `corpus:ground_truth:train:carrier:887263386589340.txt` | carrier | 0.7226 | 0.6364 | 51.4381 | 2023 | 4575 | — |
| 28 | `corpus:ground_truth:train:outpatient:542062281218793:1.txt` | outpatient | 0.7347 | 0.6364 | 32.5801 | 2051 | 2916 | — |
| 29 | `corpus:ground_truth:train:insurbias-1222.txt` | auto | 0.8576 | 0.7826 | 32.4687 | 1879 | 2744 | — |
| 30 | `corpus:ground_truth:train:inpatient:196401177008033:1.txt` | inpatient | 0.7353 | 0.6364 | 38.6869 | 2211 | 3531 | — |
| 31 | `corpus:ground_truth:train:property:269879669.txt` | property | 0.7576 | 0.6400 | 45.4302 | 3564 | 4006 | — |
| 32 | `corpus:ground_truth:train:pde:233024489630762.txt` | pde | 0.7489 | 0.6957 | 36.8578 | 1967 | 3497 | — |
| 33 | `corpus:ground_truth:train:insurbias-976.txt` | auto | 0.8652 | 0.7826 | 35.7239 | 1878 | 3033 | — |
| 34 | `corpus:ground_truth:train:insurbias-914.txt` | auto | 0.8855 | 0.7826 | 36.2443 | 1892 | 2883 | — |
| 35 | `corpus:ground_truth:train:pde:233654491978707.txt` | pde | 0.7489 | 0.6957 | 31.7443 | 1963 | 2875 | — |
| 36 | `corpus:ground_truth:train:property:267944087.txt` | property | 0.7434 | 0.5385 | 46.1391 | 3459 | 3803 | — |
| 37 | `corpus:ground_truth:train:inpatient:196451176994433:1.txt` | inpatient | 0.8130 | 0.6957 | 36.6612 | 2164 | 3073 | — |
| 38 | `corpus:ground_truth:train:pde:233634491375303.txt` | pde | 0.6580 | 0.6364 | 32.7242 | 1965 | 2973 | — |
| 39 | `corpus:ground_truth:train:outpatient:542712281056440:1.txt` | outpatient | 0.7347 | 0.6364 | 32.0704 | 2088 | 2980 | — |
| 40 | `corpus:ground_truth:train:auto:CLM-000809.txt` | auto | 0.8762 | 0.7857 | 31.3371 | 1948 | 2739 | — |
| 41 | `corpus:ground_truth:train:inpatient:196991176968589:1.txt` | inpatient | 0.7535 | 0.6957 | 42.8141 | 2181 | 3904 | — |
| 42 | `corpus:ground_truth:train:outpatient:542922281376960:1.txt` | outpatient | 0.7347 | 0.6364 | 42.8644 | 2055 | 3608 | — |
| 43 | `corpus:ground_truth:train:outpatient:542472281487558:1.txt` | outpatient | 0.7347 | 0.6364 | 36.7956 | 2095 | 3291 | — |
| 44 | `corpus:ground_truth:train:carrier:887393389256013.txt` | carrier | 0.7226 | 0.6364 | 44.6457 | 2080 | 4068 | — |
| 45 | `corpus:ground_truth:train:property:262548994.txt` | property | 0.6356 | 0.5000 | 51.7765 | 3859 | 4891 | — |
| 46 | `corpus:ground_truth:train:property:261515174.txt` | property | 0.8431 | 0.6154 | 48.5626 | 3894 | 4325 | — |
| 47 | `corpus:ground_truth:train:insurbias-969.txt` | auto | 0.8521 | 0.7826 | 39.5417 | 1881 | 3448 | — |
| 48 | `corpus:ground_truth:train:auto:CLM-000249.txt` | auto | 0.8860 | 0.7857 | 37.8107 | 1947 | 3382 | — |
| 49 | `corpus:ground_truth:train:property:263266666.txt` | property | 0.8488 | 0.6154 | 44.1520 | 4030 | 3919 | — |
| 50 | `corpus:ground_truth:train:inpatient:196781176972873:1.txt` | inpatient | 0.7779 | 0.6364 | 38.5930 | 2189 | 3590 | — |

- scored rows: 50/50; min=0.6317 max=0.9752 mean=0.7812

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 50 --seed 42 --concurrency 8 --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260928T054349Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T054349Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T054349Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T054349Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T054349Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/insurance_claims/RUN-50-INSURANCE_CLAIM-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
