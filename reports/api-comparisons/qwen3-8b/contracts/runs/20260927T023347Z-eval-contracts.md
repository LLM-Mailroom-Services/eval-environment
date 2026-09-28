# Run report — `20260927T023347Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T023347Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 20 docs, seed 42 |
| timestamp | `2026-09-27T02:33:47+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T023347Z-eval-contracts/subset_manifest.json` |
| eval git | `fd6a220` |
| finished | `2026-09-27T02:40:49+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T023347Z-eval-contracts', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T02:33:47+00:00` |
| finished_at | `2026-09-27T02:40:49+00:00` |
| duration_s (wall) | 424.4000 |
| latency_ms_mean | 108632.1 |
| latency_ms_p95 | 365572.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.0762 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.0762** (sd 0.2407, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 424.4000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0498** USD |
| cost estimated (roster token rates) | **0.0498** USD |
| cost per document (actual) | 0.0025 USD |
| cost per document (estimated) | 0.0025 USD |
| latency e2e / p50 / p95 / max | 424.4000 / 61.5868 / 365.5726 / 395.4556 s |
| prompt / completion / total tokens | 238475 / 48066 / 286541 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 2172.6 s vs wall = 424.4 s -> wall/serial factor 5.12x at concurrency 8.

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
| `contracts_specialist` | 21 | 238475 | 48066 | 286541 | 0.0498 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 2172.6 s over wall 424.4 s = **5.12×** effective parallelism at c8 (64% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` (Consulting Agreements) 395.5 s = 93% of wall — p95/p50 = 5.94×.
- **Prompt length vs latency:** Pearson r = -0.07 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 2403 tok/doc, mean prompt 11924 tok/doc.
- **Subclass spread:** best `Franchise` 0.524 (n=1), worst `Endorsement` 0.000 (n=1).
- **Field-level extraction:** 18/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Strategic Alliance | 4 | 0.0000 |
| Distributor | 3 | 0.0000 |
| IP | 2 | 0.5000 |
| Collaboration | 1 | 0.0000 |
| Consulting Agreements | 1 | 0.0000 |
| Development | 1 | 0.0000 |
| Endorsement | 1 | 0.0000 |
| Franchise | 1 | 0.5238 |
| Joint Venture _ Filing | 1 | 0.0000 |
| License_Agreements | 1 | 0.0000 |
| Maintenance | 1 | 0.0000 |
| Marketing | 1 | 0.0000 |
| Promotion | 1 | 0.0000 |
| Sponsorship | 1 | 0.0000 |
| **total** | **20** | **0.0762** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.0000 | 0.0000 | 41.0258 | 5904 | 1855 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.0000 | 0.0000 | 38.8441 | 14160 | 1116 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.0000 | 0.0000 | 365.5726 | 6074 | 8795 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.0000 | 0.0000 | 25.3363 | 15732 | 541 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.0000 | 0.0000 | 72.3494 | 44807 | 2021 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.0000 | 0.0000 | 21.7374 | 4123 | 864 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.0000 | 0.0000 | 266.9750 | 10739 | 8607 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.0000 | 0.0000 | 260.7797 | 26450 | 1237 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 1.0000 | 0.2501 | 30.9701 | 3511 | 1449 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 0.0000 | 0.0000 | 395.4556 | 3504 | 8929 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.0000 | 0.0000 | 61.5868 | 16554 | 1634 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.0000 | 0.0000 | 89.0188 | 6779 | 2931 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.0000 | 0.0000 | 17.1359 | 14040 | 592 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.0000 | 0.0000 | 26.1651 | 5741 | 852 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.0000 | 0.0000 | 18.8785 | 2580 | 1145 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.5238 | 0.1538 | 73.2126 | 38932 | 2165 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.0000 | 0.0000 | 15.6774 | 9275 | 553 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.0000 | 0.0000 | 8.5633 | 5028 | 391 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.0000 | 0.0000 | 195.4488 | 4542 | 2389 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.0000 | 0.0000 | 147.9096 | 0 | 0 | — |

- scored rows: 20/20; min=0.0000 max=1.0000 mean=0.0762

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 20 --seed 42 --concurrency 8 --decode-profile qwen3-8b --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260927T023347Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T023347Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T023347Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T023347Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T023347Z-eval-contracts.md` | experiment-log markdown mirror |
| `/workspace/reports/api-comparisons/qwen3-8b/RUN-20-CONTRACT-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
