# Run report — `20260927T023050Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T023050Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 20 docs, seed 42 |
| timestamp | `2026-09-27T02:30:50+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T023050Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `fd6a220` |
| finished | `2026-09-27T02:33:44+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T023050Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T02:30:50+00:00` |
| finished_at | `2026-09-27T02:33:44+00:00` |
| duration_s (wall) | 175.6000 |
| latency_ms_mean | 34087.5 |
| latency_ms_p95 | 155975.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.202 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 175.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0192** USD |
| cost estimated (roster token rates) | **0.0192** USD |
| cost per document (actual) | 0.0010 USD |
| cost per document (estimated) | 0.0010 USD |
| latency e2e / p50 / p95 / max | 175.6000 / 15.0976 / 155.9756 / 158.0812 s |
| prompt / completion / total tokens | 40696 / 31824 / 72520 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 681.7 s vs wall = 175.6 s -> wall/serial factor 3.88x at concurrency 8.

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
| `insurance_claims_specialist` | 20 | 40696 | 31824 | 72520 | 0.0192 | qwen/qwen3-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.0000 | 0.0000 | 14.1927 | 1884 | 690 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8428 | 0.7500 | 27.5120 | 1815 | 1398 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.0000 | 0.0000 | 11.0720 | 1964 | 497 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.0000 | 0.0000 | 15.3678 | 1970 | 746 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.0000 | 0.0000 | 155.9756 | 1995 | 6531 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.7034 | 0.5834 | 21.3597 | 1884 | 1077 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.8333 | 0.7692 | 15.7787 | 1846 | 753 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.0000 | 0.0000 | 14.4781 | 1818 | 686 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.0000 | 0.0000 | 9.3259 | 1821 | 509 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.0000 | 0.0000 | 158.0812 | 1895 | 6528 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.0000 | 0.0000 | 8.8059 | 2006 | 411 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8424 | 0.7500 | 15.0528 | 1822 | 739 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8182 | 0.7500 | 17.1545 | 1822 | 995 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.0000 | 0.0000 | 8.7808 | 1845 | 450 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.0000 | 0.0000 | 15.0976 | 1882 | 711 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.0000 | 0.0000 | 11.2986 | 2045 | 665 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.0000 | 0.0000 | 18.7610 | 2089 | 993 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.0000 | 0.0000 | 6.5668 | 1846 | 321 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.0000 | 0.0000 | 126.4059 | 1908 | 6601 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.0000 | 0.0000 | 10.6817 | 4539 | 523 | — |

- scored rows: 20/20; min=0.0000 max=0.8428 mean=0.2020

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
