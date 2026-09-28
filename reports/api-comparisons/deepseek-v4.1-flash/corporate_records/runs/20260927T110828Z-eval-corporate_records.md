# Run report — `20260927T110828Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T110828Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `—` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 20 docs, seed 42 |
| timestamp | `2026-09-27T11:08:28+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T110828Z-eval-corporate_records/subset_manifest.json` |
| eval git | `3c2c95c` |
| finished | `2026-09-27T11:09:57+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T110828Z-eval-corporate_records', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T11:08:28+00:00` |
| finished_at | `2026-09-27T11:09:57+00:00` |
| duration_s (wall) | 91.6000 |
| latency_ms_mean | 10693.7 |
| latency_ms_p95 | 16931.3 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4415 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4415** (sd 0.1792, min 0.2137, max 0.7688) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 91.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0197** USD |
| cost estimated (roster token rates) | **0.0197** USD |
| cost per document (actual) | 0.0010 USD |
| cost per document (estimated) | 0.0010 USD |
| latency e2e / p50 / p95 / max | 91.6000 / 6.9364 / 16.9313 / 71.9777 s |
| prompt / completion / total tokens | 186564 / 45325 / 231889 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 213.9 s vs wall = 91.6 s -> wall/serial factor 2.33x at concurrency 8.

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
| `corporate_records_specialist` | 21 | 186564 | 45325 | 231889 | 0.0197 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 213.9 s over wall 91.6 s = **2.33×** effective parallelism at c8 (29% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` (charter_amendment) 72.0 s = 79% of wall — p95/p50 = 2.44×.
- **Prompt length vs latency:** Pearson r = 0.10 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 2266 tok/doc, mean prompt 9328 tok/doc.
- **Subclass spread:** best `articles_of_incorporation` 0.747 (n=2), worst `officer_certificate` 0.252 (n=3).
- **Field-level extraction:** 10/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 4 | 0.2936 |
| indenture | 3 | 0.3183 |
| officer_certificate | 3 | 0.2519 |
| articles_of_incorporation | 2 | 0.7469 |
| board_resolution | 2 | 0.4473 |
| rights_instrument | 2 | 0.6214 |
| subsidiary_list | 2 | 0.4651 |
| bylaws | 1 | 0.6500 |
| powers_of_attorney | 1 | 0.7333 |
| **total** | **20** | **0.4415** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2528 | 0.0000 | 5.1264 | 18736 | 1319 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6500 | 0.2666 | 3.0307 | 19426 | 489 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4666 | 0.1429 | 4.1945 | 1949 | 1105 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3679 | 0.0000 | 5.8229 | 1877 | 1593 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6214 | 0.2352 | 6.9364 | 2690 | 1352 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.6214 | 0.2352 | 11.4096 | 14200 | 2390 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.7250 | 0.2500 | 6.8937 | 7824 | 1708 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.4636 | 0.1429 | 4.7770 | 1591 | 1185 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2437 | 0.0000 | 16.9313 | 9939 | 3892 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.7333 | 0.2857 | 7.3453 | 3578 | 2203 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.7688 | 0.5000 | 5.0101 | 3600 | 673 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3099 | 0.0000 | 6.4265 | 2230 | 1285 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.4597 | 0.1250 | 2.9730 | 1799 | 571 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.4348 | 0.1250 | 8.1711 | 1790 | 1604 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 10.1889 | 66592 | 2518 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2437 | 0.0000 | 14.7291 | 5674 | 3569 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 71.9777 | 12941 | 13240 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2137 | 0.0000 | 9.5643 | 2246 | 1923 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3431 | 0.0000 | 7.7211 | 3223 | 2095 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.2682 | 0.0000 | 4.6437 | 4659 | 611 | — |

- scored rows: 20/20; min=0.2137 max=0.7688 mean=0.4415

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 20 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260927T110828Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T110828Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T110828Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T110828Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T110828Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/corporate_records/runs/20260927T110828Z-eval-corporate_records.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
