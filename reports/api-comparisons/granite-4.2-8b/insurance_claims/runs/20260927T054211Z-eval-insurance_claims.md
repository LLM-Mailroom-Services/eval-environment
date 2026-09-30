# Run report — `20260927T054211Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T054211Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 20 docs, seed 42 |
| timestamp | `2026-09-27T05:42:11+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T054211Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `1d9f8d2` |
| finished | `2026-09-27T05:45:37+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T054211Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T05:42:11+00:00` |
| finished_at | `2026-09-27T05:45:37+00:00` |
| duration_s (wall) | 208.1000 |
| latency_ms_mean | 58454.3 |
| latency_ms_p95 | 121582.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7135 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7135** (sd 0.1983, min 0.0000, max 0.9664) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 208.1000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.8000** USD |
| cost actual (derived from case rows) | **0.0247** USD |
| cost estimated (roster token rates) | **0.0247** USD |
| cost per document (actual) | 0.0012 USD |
| cost per document (estimated) | 0.0012 USD |
| latency e2e / p50 / p95 / max | 208.1000 / 75.5769 / 121.5826 / 132.3413 s |
| prompt / completion / total tokens | 43656 / 88363 / 132019 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1169.1 s vs wall = 208.1 s -> wall/serial factor 5.62x at concurrency 8.

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
| `insurance_claims_specialist` | 20 | 43656 | 88363 | 132019 | 0.0247 | ibm-granite/granite-4.2-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1169.1 s over wall 208.1 s = **5.62×** effective parallelism at c8 (70% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:insurbias-310.txt` (auto) 132.3 s = 64% of wall — p95/p50 = 1.61×.
- **Prompt length vs latency:** Pearson r = 0.05 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 4418 tok/doc, mean prompt 2183 tok/doc.
- **Subclass spread:** best `auto` 0.871 (n=8), worst `carrier` 0.444 (n=3).
- **Field-level extraction:** 1/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 8 | 0.8714 |
| pde | 5 | 0.6502 |
| carrier | 3 | 0.4438 |
| outpatient | 2 | 0.6555 |
| inpatient | 1 | 0.6626 |
| property | 1 | 0.7422 |
| **total** | **20** | **0.7135** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.7286 | 0.6364 | 101.5882 | 2038 | 7214 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8537 | 0.7500 | 98.8304 | 1976 | 7013 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.6300 | 0.5715 | 3.9660 | 2103 | 258 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.0000 | 0.0000 | 0.8799 | 2116 | 2 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.6620 | 0.6364 | 3.8966 | 2121 | 253 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.5670 | 0.5715 | 4.4067 | 2035 | 295 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.8833 | 0.7692 | 78.2059 | 2003 | 5540 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.7911 | 0.7273 | 3.9307 | 1979 | 253 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9664 | 0.7826 | 116.3002 | 1982 | 8322 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6902 | 0.6364 | 107.0961 | 2045 | 7599 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.6490 | 0.5715 | 3.5048 | 2136 | 275 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8620 | 0.7500 | 110.5573 | 1983 | 7856 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8480 | 0.7500 | 132.3413 | 1984 | 9810 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.8826 | 0.7692 | 75.5769 | 2002 | 5290 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.5670 | 0.5715 | 3.6231 | 2035 | 265 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.7013 | 0.5715 | 121.5826 | 2177 | 10524 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.6626 | 0.6364 | 4.3909 | 2215 | 332 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.8844 | 0.7692 | 55.7409 | 2004 | 4664 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.6981 | 0.6364 | 62.9546 | 2060 | 5524 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.7422 | 0.5600 | 79.7137 | 4662 | 7074 | — |

- scored rows: 20/20; min=0.0000 max=0.9664 mean=0.7135

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 20 --seed 42 --concurrency 8 --decode-profile granite-4.2-8b --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260927T054211Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T054211Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T054211Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T054211Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T054211Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `reports/api-comparisons/granite-4.2-8b/insurance_claims/RUN-20-INSURANCE_CLAIM-GRANITE-4.2-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
