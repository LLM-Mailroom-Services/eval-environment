# Run report — `20260928T085028Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T085028Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `insurance_claims_specialist_v2` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 20 docs, seed 42 |
| timestamp | `2026-09-28T08:50:28+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T085028Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:51:39+00:00` |

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
| prompt source / lineage | frozen / mutation |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T085028Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:50:28+00:00` |
| finished_at | `2026-09-28T08:51:39+00:00` |
| duration_s (wall) | 72.0000 |
| latency_ms_mean | 10424.8 |
| latency_ms_p95 | 19177.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7912 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7912** (sd 0.1026, min 0.6463, max 0.9714) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 72.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0135** USD |
| cost estimated (roster token rates) | **0.0135** USD |
| cost per document (actual) | 0.0007 USD |
| cost per document (estimated) | 0.0007 USD |
| latency e2e / p50 / p95 / max | 72.0000 / 10.4751 / 19.1777 / 19.7160 s |
| prompt / completion / total tokens | 41068 / 41616 / 82684 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 208.5 s vs wall = 72.0 s -> wall/serial factor 2.90x at concurrency 8.

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
| `insurance_claims_specialist` | 20 | 41068 | 41616 | 82684 | 0.0135 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 208.5 s over wall 72.0 s = **2.90×** effective parallelism at c8 (36% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:carrier:887623388590174.txt` (carrier) 19.7 s = 27% of wall — p95/p50 = 1.83×.
- **Prompt length vs latency:** Pearson r = 0.25 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 2081 tok/doc, mean prompt 2053 tok/doc.
- **Subclass spread:** best `auto` 0.908 (n=8), worst `property` 0.646 (n=1).
- **Field-level extraction:** 0/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 8 | 0.9080 |
| pde | 5 | 0.6959 |
| carrier | 3 | 0.7410 |
| outpatient | 2 | 0.7287 |
| inpatient | 1 | 0.7535 |
| property | 1 | 0.6463 |
| **total** | **20** | **0.7912** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.6839 | 0.5185 | 17.0650 | 1926 | 2859 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8625 | 0.7500 | 13.0788 | 1876 | 2071 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7511 | 0.6957 | 3.3127 | 1971 | 959 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.7511 | 0.6957 | 9.8564 | 1983 | 3367 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7347 | 0.6364 | 4.2305 | 1991 | 1319 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.7034 | 0.5834 | 8.6679 | 1902 | 1913 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.8838 | 0.7692 | 5.2487 | 1876 | 1553 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.8685 | 0.7500 | 11.1644 | 1879 | 1825 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9670 | 0.7826 | 10.4751 | 1861 | 709 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6943 | 0.5600 | 18.4203 | 1936 | 2896 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7226 | 0.6364 | 4.5653 | 2002 | 1635 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8754 | 0.7500 | 6.4034 | 1862 | 656 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8703 | 0.7500 | 13.8082 | 1883 | 1946 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.9647 | 0.8148 | 3.1922 | 1874 | 1307 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.7034 | 0.5834 | 10.8148 | 1903 | 2029 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7208 | 0.5834 | 19.7160 | 2039 | 1598 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.7535 | 0.6957 | 4.5814 | 2072 | 1802 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.9714 | 0.8148 | 19.1777 | 1898 | 3459 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.6943 | 0.5600 | 8.1324 | 1924 | 2514 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.6463 | 0.4800 | 16.5844 | 4410 | 5199 | — |

- scored rows: 20/20; min=0.6463 max=0.9714 mean=0.7912

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 20 --seed 42 --concurrency 8 --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260928T085028Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T085028Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T085028Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T085028Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T085028Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/insurance_claims/RUN-20-INSURANCE_CLAIM-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
