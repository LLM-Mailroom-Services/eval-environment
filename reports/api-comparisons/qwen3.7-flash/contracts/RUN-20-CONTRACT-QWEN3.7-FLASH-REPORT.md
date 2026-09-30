# Run report — `20260928T075959Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T075959Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `contracts_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 20 docs, seed 42 |
| timestamp | `2026-09-28T07:59:59+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T075959Z-eval-contracts/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:05:34+00:00` |

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
| started_at | `2026-09-28T07:59:59+00:00` |
| finished_at | `2026-09-28T08:05:34+00:00` |
| duration_s (wall) | 335.9000 |
| latency_ms_mean | 90585.5 |
| latency_ms_p95 | 175406.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5167 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5167** (sd 0.2357, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 335.9000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0295** USD |
| cost estimated (roster token rates) | **0.0295** USD |
| cost per document (actual) | 0.0015 USD |
| cost per document (estimated) | 0.0015 USD |
| latency e2e / p50 / p95 / max | 335.9000 / 67.3419 / 175.4069 / 204.9583 s |
| prompt / completion / total tokens | 317710 / 153236 / 470946 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1811.7 s vs wall = 335.9 s -> wall/serial factor 5.39x at concurrency 8.

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
| `contracts_specialist` | 25 | 317710 | 153236 | 470946 | 0.0295 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1811.7 s over wall 335.9 s = **5.39×** effective parallelism at c8 (67% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` (Franchise) 205.0 s = 61% of wall — p95/p50 = 2.60×.
- **Prompt length vs latency:** Pearson r = 0.83 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 7662 tok/doc, mean prompt 15886 tok/doc.
- **Subclass spread:** best `Consulting Agreements` 1.000 (n=1), worst `Maintenance` 0.000 (n=1).
- **Field-level extraction:** 6/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Strategic Alliance | 4 | 0.6357 |
| Distributor | 3 | 0.3916 |
| IP | 2 | 0.3514 |
| Collaboration | 1 | 0.5534 |
| Consulting Agreements | 1 | 1.0000 |
| Development | 1 | 0.5151 |
| Endorsement | 1 | 0.3067 |
| Franchise | 1 | 0.5774 |
| Joint Venture _ Filing | 1 | 0.6965 |
| License_Agreements | 1 | 0.5926 |
| Maintenance | 1 | 0.0000 |
| Marketing | 1 | 0.3043 |
| Promotion | 1 | 0.5938 |
| Sponsorship | 1 | 0.7728 |
| **total** | **20** | **0.5167** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.3067 | 0.0000 | 63.8357 | 5992 | 5191 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5972 | 0.2857 | 48.5567 | 14340 | 4766 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.5926 | 0.2857 | 78.7705 | 6128 | 7954 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6785 | 0.2857 | 100.4088 | 15728 | 4729 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.5534 | 0.3333 | 155.7586 | 44767 | 14877 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.7728 | 0.2223 | 66.6890 | 4194 | 6503 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.5444 | 0.2223 | 51.6265 | 10879 | 5198 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5938 | 0.2223 | 146.2145 | 42753 | 14306 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3514 | 0.0000 | 44.4033 | 3579 | 3846 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2858 | 40.0357 | 3579 | 3451 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.5151 | 0.2500 | 79.3455 | 16467 | 8190 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.0000 | 0.0000 | 138.7495 | 6886 | 6585 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.0000 | 0.0000 | 50.6431 | 14216 | 4670 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.6304 | 0.2000 | 67.3419 | 5829 | 6774 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3514 | 0.0000 | 49.3122 | 2641 | 4183 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.5774 | 0.1667 | 204.9583 | 39032 | 13170 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.3043 | 0.0000 | 58.7101 | 9333 | 5695 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.7084 | 0.2223 | 51.2174 | 5102 | 5271 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5588 | 0.2857 | 175.4069 | 31131 | 13743 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.6965 | 0.2500 | 139.7250 | 35134 | 14134 | — |

- scored rows: 20/20; min=0.0000 max=1.0000 mean=0.5167

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 20 --seed 42 --concurrency 8 --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260928T075959Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T075959Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T075959Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T075959Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T075959Z-eval-contracts.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/contracts/RUN-20-CONTRACT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
