# Run report — `20260928T085821Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T085821Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `corporate_records_specialist_v2` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 20 docs, seed 42 |
| timestamp | `2026-09-28T08:58:21+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T085821Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T09:00:03+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T085821Z-eval-corporate_records', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:58:21+00:00` |
| finished_at | `2026-09-28T09:00:03+00:00` |
| duration_s (wall) | 103.3000 |
| latency_ms_mean | 12773.6 |
| latency_ms_p95 | 34387.0 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4624 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4624** (sd 0.1813, min 0.2437, max 0.8688) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 103.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0176** USD |
| cost estimated (roster token rates) | **0.0176** USD |
| cost per document (actual) | 0.0009 USD |
| cost per document (estimated) | 0.0009 USD |
| latency e2e / p50 / p95 / max | 103.3000 / 8.9826 / 34.3870 / 68.7670 s |
| prompt / completion / total tokens | 180067 / 38943 / 219010 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 255.5 s vs wall = 103.3 s -> wall/serial factor 2.47x at concurrency 8.

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
| `corporate_records_specialist` | 20 | 180067 | 38943 | 219010 | 0.0176 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 255.5 s over wall 103.3 s = **2.47×** effective parallelism at c8 (31% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` (charter_amendment) 68.8 s = 67% of wall — p95/p50 = 3.83×.
- **Prompt length vs latency:** Pearson r = -0.08 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 1947 tok/doc, mean prompt 9003 tok/doc.
- **Subclass spread:** best `articles_of_incorporation` 0.797 (n=2), worst `indenture` 0.290 (n=3).
- **Field-level extraction:** 10/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 4 | 0.3500 |
| indenture | 3 | 0.2905 |
| officer_certificate | 3 | 0.2982 |
| articles_of_incorporation | 2 | 0.7969 |
| board_resolution | 2 | 0.4598 |
| rights_instrument | 2 | 0.6452 |
| subsidiary_list | 2 | 0.4472 |
| bylaws | 1 | 0.6500 |
| powers_of_attorney | 1 | 0.7333 |
| **total** | **20** | **0.4624** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2528 | 0.0000 | 11.3462 | 18742 | 2016 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6500 | 0.2500 | 5.0453 | 19432 | 569 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4308 | 0.1429 | 7.3516 | 1955 | 1687 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3887 | 0.0000 | 8.8768 | 1905 | 1434 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6691 | 0.2352 | 9.2749 | 2696 | 1956 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.6214 | 0.2352 | 6.2621 | 14184 | 1113 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.7250 | 0.2666 | 11.6341 | 7830 | 2016 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.4636 | 0.1538 | 7.3549 | 1597 | 1460 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.3014 | 0.0000 | 10.1110 | 9923 | 1784 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.7333 | 0.2857 | 8.9826 | 3584 | 2363 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.8688 | 0.5000 | 3.4152 | 3584 | 546 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3983 | 0.0000 | 13.1742 | 2214 | 1895 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.5098 | 0.1333 | 12.4075 | 1805 | 2078 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.4098 | 0.1250 | 9.4927 | 1796 | 1261 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 7.4449 | 66598 | 1966 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2437 | 0.0000 | 34.3870 | 5658 | 3194 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.3214 | 0.0000 | 68.7670 | 6462 | 7450 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 5.9590 | 2230 | 2257 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.2597 | 0.0000 | 6.8348 | 3229 | 1265 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3494 | 0.0000 | 7.3504 | 4643 | 633 | — |

- scored rows: 20/20; min=0.2437 max=0.8688 mean=0.4624

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 20 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T085821Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T085821Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T085821Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T085821Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T085821Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/corporate_records/RUN-20-CORPORATE_RECORD-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
