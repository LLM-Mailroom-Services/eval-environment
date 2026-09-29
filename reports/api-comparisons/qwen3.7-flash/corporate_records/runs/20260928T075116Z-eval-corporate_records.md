# Run report — `20260928T075116Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T075116Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `corporate_records_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 20 docs, seed 42 |
| timestamp | `2026-09-28T07:51:16+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T075116Z-eval-corporate_records/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T07:53:38+00:00` |

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
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T07:51:16+00:00` |
| finished_at | `2026-09-28T07:53:38+00:00` |
| duration_s (wall) | 143.4000 |
| latency_ms_mean | 39839.1 |
| latency_ms_p95 | 54172.5 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4202 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4202** (sd 0.1668, min 0.2028, max 0.7854) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 143.4000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0148** USD |
| cost estimated (roster token rates) | **0.0148** USD |
| cost per document (actual) | 0.0007 USD |
| cost per document (estimated) | 0.0007 USD |
| latency e2e / p50 / p95 / max | 143.4000 / 35.3785 / 54.1725 / 98.2951 s |
| prompt / completion / total tokens | 193604 / 69342 / 262946 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 796.8 s vs wall = 143.4 s -> wall/serial factor 5.56x at concurrency 8.

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
| `corporate_records_specialist` | 22 | 193604 | 69342 | 262946 | 0.0148 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 796.8 s over wall 143.4 s = **5.56×** effective parallelism at c8 (69% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` (indenture) 98.3 s = 69% of wall — p95/p50 = 1.53×.
- **Prompt length vs latency:** Pearson r = 0.83 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 3467 tok/doc, mean prompt 9680 tok/doc.
- **Subclass spread:** best `articles_of_incorporation` 0.686 (n=2), worst `officer_certificate` 0.280 (n=3).
- **Field-level extraction:** 11/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| charter_amendment | 4 | 0.2931 |
| indenture | 3 | 0.2911 |
| officer_certificate | 3 | 0.2800 |
| articles_of_incorporation | 2 | 0.6855 |
| board_resolution | 2 | 0.3415 |
| rights_instrument | 2 | 0.6196 |
| subsidiary_list | 2 | 0.4901 |
| bylaws | 1 | 0.6250 |
| powers_of_attorney | 1 | 0.6208 |
| **total** | **20** | **0.4202** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2028 | 0.0000 | 45.3522 | 20052 | 4030 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.6250 | 0.2666 | 26.7149 | 21113 | 2051 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.4666 | 0.1538 | 37.1736 | 1964 | 3315 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.3262 | 0.0000 | 35.3354 | 1886 | 3036 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6714 | 0.2500 | 35.3785 | 2709 | 2862 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.5678 | 0.2352 | 33.6692 | 14630 | 2864 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.5857 | 0.2352 | 25.6634 | 8003 | 2079 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.5136 | 0.1667 | 32.1642 | 1590 | 2565 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.2437 | 0.0000 | 39.8865 | 10254 | 3681 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.6208 | 0.2666 | 39.2720 | 3685 | 3346 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.7854 | 0.5000 | 35.4881 | 3608 | 3257 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.2714 | 0.0000 | 33.0683 | 2250 | 2732 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.2731 | 0.0000 | 33.5716 | 1791 | 2886 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.4098 | 0.1250 | 29.4909 | 1783 | 2766 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 98.2951 | 75054 | 8138 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2437 | 0.0000 | 51.0940 | 5861 | 4224 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.2829 | 0.0000 | 40.9830 | 6921 | 3630 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.2918 | 0.0000 | 35.3218 | 2265 | 3238 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 54.1725 | 3427 | 5410 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3526 | 0.0000 | 34.6859 | 4758 | 3232 | — |

- scored rows: 20/20; min=0.2028 max=0.7854 mean=0.4202

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:corporate_records --real --sample 20 --seed 42 --concurrency 8 --subset "class:corporate_record"
uv run python scripts/score_run.py --run-id 20260928T075116Z-eval-corporate_records --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T075116Z-eval-corporate_records
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T075116Z-eval-corporate_records/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T075116Z-eval-corporate_records/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T075116Z-eval-corporate_records.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/corporate_records/RUN-20-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
