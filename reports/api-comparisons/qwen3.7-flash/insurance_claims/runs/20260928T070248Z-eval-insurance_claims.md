# Run report — `20260928T070248Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T070248Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `insurance_claims_specialist_v3` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 50 docs, seed 42 |
| timestamp | `2026-09-28T07:02:48+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T070248Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T07:07:55+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T070248Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T07:02:48+00:00` |
| finished_at | `2026-09-28T07:07:55+00:00` |
| duration_s (wall) | 307.9000 |
| latency_ms_mean | 42344.0 |
| latency_ms_p95 | 63022.3 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7733 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7733** (sd 0.0885, min 0.6317, max 0.9573) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 307.9000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0253** USD |
| cost estimated (roster token rates) | **0.0253** USD |
| cost per document (actual) | 0.0005 USD |
| cost per document (estimated) | 0.0005 USD |
| latency e2e / p50 / p95 / max | 307.9000 / 40.8077 / 63.0223 / 64.6885 s |
| prompt / completion / total tokens | 115773 / 167942 / 283715 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2117.2 s vs wall = 307.9 s -> wall/serial factor 6.88x at concurrency 8.

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
| `insurance_claims_specialist` | 50 | 115773 | 167942 | 283715 | 0.0253 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2117.2 s over wall 307.9 s = **6.88×** effective parallelism at c8 (86% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:property:262548994.txt` (property) 64.7 s = 21% of wall — p95/p50 = 1.54×.
- **Prompt length vs latency:** Pearson r = 0.60 across 50 docs (prefill-bound).
- **Decode budget:** mean completion 3359 tok/doc, mean prompt 2315 tok/doc.
- **Subclass spread:** best `auto` 0.886 (n=16), worst `pde` 0.678 (n=9).
- **Field-level extraction:** 0/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 16 | 0.8864 |
| pde | 9 | 0.6782 |
| property | 8 | 0.7385 |
| outpatient | 7 | 0.7330 |
| carrier | 5 | 0.7044 |
| inpatient | 5 | 0.7639 |
| **total** | **50** | **0.7733** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.7489 | 0.6957 | 38.2670 | 1956 | 2724 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8585 | 0.7826 | 41.0661 | 1887 | 3054 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7226 | 0.6667 | 38.2922 | 2039 | 3402 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.6317 | 0.6000 | 44.0370 | 2045 | 3458 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7347 | 0.6364 | 36.3121 | 2066 | 3453 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.6580 | 0.6364 | 36.4417 | 1956 | 2942 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.9221 | 0.8000 | 42.0984 | 1918 | 2921 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.8788 | 0.7826 | 41.0378 | 1890 | 2909 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9573 | 0.8182 | 40.0706 | 1893 | 3022 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6580 | 0.6364 | 29.7934 | 1967 | 2768 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7226 | 0.6364 | 40.3191 | 2077 | 3009 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8588 | 0.7826 | 32.7103 | 1894 | 2881 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8469 | 0.7826 | 39.3515 | 1894 | 2805 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.9268 | 0.8000 | 42.8316 | 1917 | 3268 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.6580 | 0.6364 | 37.9284 | 1954 | 3425 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7226 | 0.6667 | 46.0283 | 2122 | 3601 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.7978 | 0.6957 | 34.4568 | 2163 | 3305 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.9216 | 0.8000 | 40.6447 | 1918 | 3108 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.6580 | 0.6364 | 37.1708 | 1980 | 3436 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.7273 | 0.6154 | 63.0223 | 4596 | 5161 | — |
| 21 | `corpus:ground_truth:train:auto:CLM-000355.txt` | auto | 0.9223 | 0.8000 | 28.1408 | 1917 | 2526 | — |
| 22 | `corpus:ground_truth:train:insurbias-535.txt` | auto | 0.8555 | 0.7826 | 37.4383 | 1893 | 2697 | — |
| 23 | `corpus:ground_truth:train:pde:233734492807320.txt` | pde | 0.6580 | 0.6364 | 41.6699 | 1975 | 3267 | — |
| 24 | `corpus:ground_truth:train:property:268405870.txt` | property | 0.6932 | 0.5715 | 42.3522 | 4249 | 4065 | — |
| 25 | `corpus:ground_truth:train:outpatient:542762281171383:1.txt` | outpatient | 0.7347 | 0.6364 | 31.9884 | 2068 | 2868 | — |
| 26 | `corpus:ground_truth:train:property:261716804.txt` | property | 0.7336 | 0.5185 | 63.3033 | 4036 | 5000 | — |
| 27 | `corpus:ground_truth:train:carrier:887263386589340.txt` | carrier | 0.7226 | 0.6667 | 45.5065 | 2033 | 3263 | — |
| 28 | `corpus:ground_truth:train:outpatient:542062281218793:1.txt` | outpatient | 0.7347 | 0.6364 | 33.6218 | 2061 | 3005 | — |
| 29 | `corpus:ground_truth:train:insurbias-1222.txt` | auto | 0.8576 | 0.7826 | 47.1845 | 1889 | 3785 | — |
| 30 | `corpus:ground_truth:train:inpatient:196401177008033:1.txt` | inpatient | 0.7353 | 0.6364 | 49.5673 | 2221 | 3445 | — |
| 31 | `corpus:ground_truth:train:property:269879669.txt` | property | 0.8485 | 0.6923 | 57.2366 | 3574 | 4198 | — |
| 32 | `corpus:ground_truth:train:pde:233024489630762.txt` | pde | 0.7489 | 0.7273 | 42.3039 | 1977 | 3156 | — |
| 33 | `corpus:ground_truth:train:insurbias-976.txt` | auto | 0.8738 | 0.7826 | 33.3011 | 1888 | 2375 | — |
| 34 | `corpus:ground_truth:train:insurbias-914.txt` | auto | 0.8855 | 0.7826 | 54.3539 | 1902 | 3992 | — |
| 35 | `corpus:ground_truth:train:pde:233654491978707.txt` | pde | 0.6580 | 0.6667 | 30.9819 | 1973 | 2594 | — |
| 36 | `corpus:ground_truth:train:property:267944087.txt` | property | 0.7434 | 0.5600 | 47.2709 | 3469 | 4468 | — |
| 37 | `corpus:ground_truth:train:inpatient:196451176994433:1.txt` | inpatient | 0.7535 | 0.6957 | 49.0374 | 2174 | 3249 | — |
| 38 | `corpus:ground_truth:train:pde:233634491375303.txt` | pde | 0.6580 | 0.6667 | 46.3429 | 1975 | 3144 | — |
| 39 | `corpus:ground_truth:train:outpatient:542712281056440:1.txt` | outpatient | 0.7347 | 0.6364 | 33.8603 | 2098 | 2945 | — |
| 40 | `corpus:ground_truth:train:auto:CLM-000809.txt` | auto | 0.8766 | 0.8148 | 38.7876 | 1958 | 3258 | — |
| 41 | `corpus:ground_truth:train:inpatient:196991176968589:1.txt` | inpatient | 0.7535 | 0.6957 | 40.8077 | 2191 | 2958 | — |
| 42 | `corpus:ground_truth:train:outpatient:542922281376960:1.txt` | outpatient | 0.7347 | 0.6364 | 37.0934 | 2065 | 3212 | — |
| 43 | `corpus:ground_truth:train:outpatient:542472281487558:1.txt` | outpatient | 0.7347 | 0.6364 | 50.0365 | 2105 | 3695 | — |
| 44 | `corpus:ground_truth:train:carrier:887393389256013.txt` | carrier | 0.7226 | 0.6364 | 37.6058 | 2090 | 3287 | — |
| 45 | `corpus:ground_truth:train:property:262548994.txt` | property | 0.6545 | 0.5000 | 64.6885 | 3869 | 4976 | — |
| 46 | `corpus:ground_truth:train:property:261515174.txt` | property | 0.7546 | 0.5600 | 54.0026 | 3904 | 3888 | — |
| 47 | `corpus:ground_truth:train:insurbias-969.txt` | auto | 0.8540 | 0.7826 | 33.0253 | 1891 | 2913 | — |
| 48 | `corpus:ground_truth:train:auto:CLM-000249.txt` | auto | 0.8860 | 0.8148 | 54.5799 | 1957 | 4263 | — |
| 49 | `corpus:ground_truth:train:property:263266666.txt` | property | 0.7532 | 0.6400 | 39.5931 | 4040 | 3386 | — |
| 50 | `corpus:ground_truth:train:inpatient:196781176972873:1.txt` | inpatient | 0.7794 | 0.6364 | 49.6360 | 2199 | 3412 | — |

- scored rows: 50/50; min=0.6317 max=0.9573 mean=0.7733

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 50 --seed 42 --concurrency 8 --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260928T070248Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T070248Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T070248Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T070248Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T070248Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/insurance_claims/RUN-50-INSURANCE_CLAIM-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
