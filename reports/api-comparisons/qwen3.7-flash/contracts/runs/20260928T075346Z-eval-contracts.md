# Run report — `20260928T075346Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T075346Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 20 docs, seed 42 |
| timestamp | `2026-09-28T07:53:46+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T075346Z-eval-contracts/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T07:59:52+00:00` |

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
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T07:53:46+00:00` |
| finished_at | `2026-09-28T07:59:52+00:00` |
| duration_s (wall) | 368.0000 |
| latency_ms_mean | 86958.2 |
| latency_ms_p95 | 199808.3 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5464 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5464** (sd 0.1938, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 368.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0326** USD |
| cost estimated (roster token rates) | **0.0326** USD |
| cost per document (actual) | 0.0016 USD |
| cost per document (estimated) | 0.0016 USD |
| latency e2e / p50 / p95 / max | 368.0000 / 69.5975 / 199.8083 / 227.4652 s |
| prompt / completion / total tokens | 335174 / 173457 / 508631 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1739.2 s vs wall = 368.0 s -> wall/serial factor 4.73x at concurrency 8.

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
| `contracts_specialist` | 27 | 335174 | 173457 | 508631 | 0.0326 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1739.2 s over wall 368.0 s = **4.73×** effective parallelism at c8 (59% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` (Franchise) 227.5 s = 62% of wall — p95/p50 = 2.87×.
- **Prompt length vs latency:** Pearson r = 0.86 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 8673 tok/doc, mean prompt 16759 tok/doc.
- **Subclass spread:** best `Consulting Agreements` 1.000 (n=1), worst `IP` 0.176 (n=2).
- **Field-level extraction:** 4/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Strategic Alliance | 4 | 0.5945 |
| Distributor | 3 | 0.5682 |
| IP | 2 | 0.1757 |
| Collaboration | 1 | 0.5666 |
| Consulting Agreements | 1 | 1.0000 |
| Development | 1 | 0.5757 |
| Endorsement | 1 | 0.2511 |
| Franchise | 1 | 0.5416 |
| Joint Venture _ Filing | 1 | 0.5715 |
| License_Agreements | 1 | 0.6666 |
| Maintenance | 1 | 0.5689 |
| Marketing | 1 | 0.3849 |
| Promotion | 1 | 0.5938 |
| Sponsorship | 1 | 0.7728 |
| **total** | **20** | **0.5464** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.2511 | 0.0000 | 65.4601 | 5971 | 5812 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5278 | 0.2857 | 65.7093 | 14319 | 6705 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.6666 | 0.2857 | 112.9217 | 6113 | 7109 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6785 | 0.2500 | 54.0269 | 15701 | 5284 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.5666 | 0.3333 | 199.8083 | 59979 | 24902 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.7728 | 0.2223 | 63.3002 | 4173 | 6293 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.5333 | 0.2223 | 50.6328 | 10858 | 4983 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5938 | 0.2223 | 126.0492 | 42711 | 12531 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3514 | 0.0000 | 55.1256 | 3558 | 5140 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2858 | 47.0106 | 3558 | 4334 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.5757 | 0.2223 | 69.5975 | 16446 | 6764 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.5625 | 0.2000 | 76.7795 | 6859 | 7236 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.5689 | 0.2500 | 45.2096 | 14195 | 4690 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.6087 | 0.1818 | 77.3559 | 5808 | 8174 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.0000 | 0.0000 | 42.7405 | 2620 | 3786 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.5416 | 0.3333 | 227.4652 | 49968 | 23079 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.3849 | 0.0000 | 129.5330 | 18630 | 13375 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.5834 | 0.1818 | 49.7069 | 5081 | 5193 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5882 | 0.2223 | 103.1649 | 31083 | 9987 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.5715 | 0.2223 | 77.5673 | 17543 | 8080 | — |

- scored rows: 20/20; min=0.0000 max=1.0000 mean=0.5464

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 20 --seed 42 --concurrency 8 --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260928T075346Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T075346Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T075346Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T075346Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T075346Z-eval-contracts.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/contracts/RUN-20-CONTRACT-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
