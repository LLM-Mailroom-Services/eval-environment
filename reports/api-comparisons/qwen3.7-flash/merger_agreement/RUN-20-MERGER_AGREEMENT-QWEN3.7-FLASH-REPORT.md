# Run report — `20260928T080826Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T080826Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `merger_agreement_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-28T08:08:26+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T080826Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:11:11+00:00` |

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
| started_at | `2026-09-28T08:08:26+00:00` |
| finished_at | `2026-09-28T08:11:11+00:00` |
| duration_s (wall) | 166.1000 |
| latency_ms_mean | 49937.6 |
| latency_ms_p95 | 61809.5 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.3964 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.3964** (sd 0.2141, min 0.0000, max 0.6471) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 166.1000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0650** USD |
| cost estimated (roster token rates) | **0.0650** USD |
| cost per document (actual) | 0.0032 USD |
| cost per document (estimated) | 0.0032 USD |
| latency e2e / p50 / p95 / max | 166.1000 / 45.5972 / 61.8095 / 101.9436 s |
| prompt / completion / total tokens | 1611013 / 127971 / 1738984 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 998.8 s vs wall = 166.1 s -> wall/serial factor 6.01x at concurrency 8.

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
| `merger_agreement_specialist` | 20 | 1611013 | 127971 | 1738984 | 0.0650 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 998.8 s over wall 166.1 s = **6.01×** effective parallelism at c8 (75% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:contract_31_merger_agreement.txt` (other) 101.9 s = 61% of wall — p95/p50 = 1.36×.
- **Prompt length vs latency:** Pearson r = 0.01 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 6399 tok/doc, mean prompt 80551 tok/doc.
- **Subclass spread:** best `mixed_cash_stock_election` 0.647 (n=1), worst `other` 0.169 (n=9).
- **Field-level extraction:** 11/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — merger extraction

Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled merger agreements; field F1 may be 0 when GT is label-native only.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| other | 9 | 0.1695 |
| all_cash | 5 | 0.5769 |
| mixed_cash_stock | 3 | 0.5639 |
| all_stock | 2 | 0.5899 |
| mixed_cash_stock_election | 1 | 0.6471 |
| **total** | **20** | **0.3964** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.2339 | 0.0000 | 55.0076 | 81147 | 7888 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.0000 | 0.0000 | 101.9436 | 75980 | 8192 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.6000 | 0.1818 | 50.1074 | 81697 | 7341 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.2045 | 0.0000 | 47.2884 | 73297 | 6565 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.6471 | 0.1818 | 45.5972 | 95573 | 5986 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.2339 | 0.0000 | 45.5038 | 79550 | 6800 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.5588 | 0.1428 | 58.9790 | 84637 | 7248 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.6111 | 0.1667 | 42.4784 | 67958 | 6376 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.1867 | 0.0000 | 43.8990 | 92602 | 4838 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.1718 | 0.0000 | 56.1381 | 84796 | 7295 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.5917 | 0.0000 | 41.4771 | 86824 | 5245 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.4445 | 0.0000 | 45.4012 | 56512 | 6779 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.5834 | 0.1538 | 44.4820 | 72696 | 6924 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.5882 | 0.1818 | 46.1113 | 94186 | 6360 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.1578 | 0.0000 | 40.2228 | 82219 | 5737 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.6471 | 0.1333 | 45.2954 | 92882 | 4715 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.1285 | 0.0000 | 46.3017 | 97664 | 4553 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.5312 | 0.1428 | 39.5152 | 57111 | 6428 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.2083 | 0.0000 | 41.1925 | 72647 | 5649 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.6000 | 0.2000 | 61.8095 | 81035 | 7052 | — |

- scored rows: 20/20; min=0.0000 max=0.6471 mean=0.3964

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:merger_agreement --real --sample 20 --seed 42 --concurrency 8 --subset "class:merger_agreement"
uv run python scripts/score_run.py --run-id 20260928T080826Z-eval-merger_agreement --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T080826Z-eval-merger_agreement
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T080826Z-eval-merger_agreement/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T080826Z-eval-merger_agreement/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T080826Z-eval-merger_agreement.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/merger_agreement/RUN-20-MERGER_AGREEMENT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
