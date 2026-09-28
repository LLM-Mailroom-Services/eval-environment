# Run report — `20260927T035135Z-eval-insurance_claims` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T035135Z-eval-insurance_claims` |
| task / agent | `insurance_claims` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:insurance_claim` — 20 docs, seed 42 |
| timestamp | `2026-09-27T03:51:35+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T035135Z-eval-insurance_claims/subset_manifest.json` |
| eval git | `bd43f66` |
| finished | `2026-09-27T03:54:57+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T035135Z-eval-insurance_claims', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T03:51:35+00:00` |
| finished_at | `2026-09-27T03:54:57+00:00` |
| duration_s (wall) | 203.3000 |
| latency_ms_mean | 50681.6 |
| latency_ms_p95 | 147490.1 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.7488 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.7488** (sd 0.0822, min 0.6300, max 0.9000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 203.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0320** USD |
| cost estimated (roster token rates) | **0.0320** USD |
| cost per document (actual) | 0.0016 USD |
| cost per document (estimated) | 0.0016 USD |
| latency e2e / p50 / p95 / max | 203.3000 / 27.1202 / 147.4901 / 150.6128 s |
| prompt / completion / total tokens | 75955 / 50885 / 126840 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1013.6 s vs wall = 203.3 s -> wall/serial factor 4.99x at concurrency 8.

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
| `insurance_claims_specialist` | 37 | 75955 | 50885 | 126840 | 0.0320 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1013.6 s over wall 203.3 s = **4.99×** effective parallelism at c8 (62% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:pde:233364488871784.txt` (pde) 150.6 s = 74% of wall — p95/p50 = 5.44×.
- **Prompt length vs latency:** Pearson r = 0.19 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 2544 tok/doc, mean prompt 3798 tok/doc.
- **Subclass spread:** best `auto` 0.837 (n=8), worst `pde` 0.658 (n=5).
- **Field-level extraction:** 0/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| auto | 8 | 0.8371 |
| pde | 5 | 0.6580 |
| carrier | 3 | 0.7007 |
| outpatient | 2 | 0.7287 |
| inpatient | 1 | 0.7535 |
| property | 1 | 0.6768 |
| **total** | **20** | **0.7488** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:pde:233384494245864.txt` | pde | 0.6580 | 0.6364 | 27.4386 | 3773 | 1449 | — |
| 2 | `corpus:ground_truth:train:insurbias-624.txt` | auto | 0.8556 | 0.7826 | 39.9077 | 3635 | 2099 | — |
| 3 | `corpus:ground_truth:train:carrier:887473385855273.txt` | carrier | 0.7512 | 0.6957 | 27.0765 | 3933 | 1398 | — |
| 4 | `corpus:ground_truth:train:carrier:887453386193813.txt` | carrier | 0.7209 | 0.6364 | 145.8895 | 3945 | 7376 | — |
| 5 | `corpus:ground_truth:train:outpatient:542872281350908:1.txt` | outpatient | 0.7347 | 0.6364 | 23.5806 | 3995 | 1141 | — |
| 6 | `corpus:ground_truth:train:pde:233724491332182.txt` | pde | 0.6580 | 0.6364 | 25.0492 | 3773 | 1283 | — |
| 7 | `corpus:ground_truth:train:auto:CLM-000145.txt` | auto | 0.8333 | 0.7692 | 19.6444 | 3697 | 1004 | — |
| 8 | `corpus:ground_truth:train:insurbias-163.txt` | auto | 0.7583 | 0.6957 | 14.8313 | 1818 | 749 | — |
| 9 | `corpus:ground_truth:train:insurbias-1111.txt` | auto | 0.9000 | 0.8182 | 33.8177 | 3647 | 1720 | — |
| 10 | `corpus:ground_truth:train:pde:233184493359051.txt` | pde | 0.6580 | 0.6087 | 147.4901 | 3795 | 7130 | — |
| 11 | `corpus:ground_truth:train:outpatient:542152281286913:1.txt` | outpatient | 0.7226 | 0.6364 | 21.4850 | 4017 | 1040 | — |
| 12 | `corpus:ground_truth:train:insurbias-385.txt` | auto | 0.8408 | 0.7500 | 14.6223 | 1822 | 765 | — |
| 13 | `corpus:ground_truth:train:insurbias-310.txt` | auto | 0.8423 | 0.7500 | 38.1778 | 3649 | 1952 | — |
| 14 | `corpus:ground_truth:train:auto:CLM-000322.txt` | auto | 0.8333 | 0.7692 | 20.6004 | 3695 | 1080 | — |
| 15 | `corpus:ground_truth:train:pde:233614493105212.txt` | pde | 0.6580 | 0.6087 | 18.6374 | 1882 | 869 | — |
| 16 | `corpus:ground_truth:train:carrier:887623388590174.txt` | carrier | 0.6300 | 0.5715 | 27.1202 | 4095 | 1515 | — |
| 17 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | 0.7535 | 0.7273 | 144.5988 | 4183 | 7640 | — |
| 18 | `corpus:ground_truth:train:auto:CLM-000611.txt` | auto | 0.8333 | 0.7692 | 19.4305 | 3697 | 1047 | — |
| 19 | `corpus:ground_truth:train:pde:233364488871784.txt` | pde | 0.6580 | 0.6667 | 150.6128 | 3821 | 7239 | — |
| 20 | `corpus:ground_truth:train:property:266855223.txt` | property | 0.6768 | 0.5385 | 53.6211 | 9083 | 2389 | — |

- scored rows: 20/20; min=0.6300 max=0.9000 mean=0.7488

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:insurance_claims --real --sample 20 --seed 42 --concurrency 8 --decode-profile qwen3-8b --subset "class:insurance_claim"
uv run python scripts/score_run.py --run-id 20260927T035135Z-eval-insurance_claims --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T035135Z-eval-insurance_claims
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T035135Z-eval-insurance_claims/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T035135Z-eval-insurance_claims/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T035135Z-eval-insurance_claims.md` | experiment-log markdown mirror |
| `/workspace/reports/api-comparisons/qwen3-8b/RUN-20-INSURANCE_CLAIM-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- **Call count:** `37` specialist LLM calls for `20` documents — this is **not** source chunking when `needed_chunks=1` (here max `1`). Extra calls are JSON parse / network **retries** (`llm_call_budget=2`). Do not apply merger 48K chunk settings to correspondence or insurance.
- **High retry rate:** calls exceed ~1.5× document count — see runbook §4 (concurrency reliability) before accepting the wave as canonical.
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
