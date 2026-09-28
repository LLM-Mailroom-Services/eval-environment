# Run report — `20260928T085148Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T085148Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `contracts_specialist_v3` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 20 docs, seed 42 |
| timestamp | `2026-09-28T08:51:48+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T085148Z-eval-contracts/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:54:15+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T085148Z-eval-contracts', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:51:48+00:00` |
| finished_at | `2026-09-28T08:54:15+00:00` |
| duration_s (wall) | 148.3000 |
| latency_ms_mean | 29340.0 |
| latency_ms_p95 | 62363.3 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.6219 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.6219** (sd 0.2184, min 0.0000, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 148.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0456** USD |
| cost estimated (roster token rates) | **0.0456** USD |
| cost per document (actual) | 0.0023 USD |
| cost per document (estimated) | 0.0023 USD |
| latency e2e / p50 / p95 / max | 148.3000 / 18.5814 / 62.3633 / 100.2350 s |
| prompt / completion / total tokens | 300981 / 121079 / 422060 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 586.8 s vs wall = 148.3 s -> wall/serial factor 3.96x at concurrency 8.

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
| `contracts_specialist` | 22 | 300981 | 121079 | 422060 | 0.0456 | deepseek/deepseek-v4.1-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 586.8 s over wall 148.3 s = **3.96×** effective parallelism at c8 (49% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` (Development) 100.2 s = 68% of wall — p95/p50 = 3.36×.
- **Prompt length vs latency:** Pearson r = 0.39 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 6054 tok/doc, mean prompt 15049 tok/doc.
- **Subclass spread:** best `Consulting Agreements` 1.000 (n=1), worst `Development` 0.000 (n=1).
- **Field-level extraction:** 4/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Strategic Alliance | 4 | 0.7299 |
| Distributor | 3 | 0.6839 |
| IP | 2 | 0.3515 |
| Collaboration | 1 | 0.6134 |
| Consulting Agreements | 1 | 1.0000 |
| Development | 1 | 0.0000 |
| Endorsement | 1 | 0.8334 |
| Franchise | 1 | 0.5476 |
| Joint Venture _ Filing | 1 | 0.6071 |
| License_Agreements | 1 | 0.6852 |
| Maintenance | 1 | 0.7069 |
| Marketing | 1 | 0.3365 |
| Promotion | 1 | 0.5703 |
| Sponsorship | 1 | 0.8637 |
| **total** | **20** | **0.6219** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.8334 | 0.2500 | 22.5334 | 5856 | 3481 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6805 | 0.2500 | 17.9733 | 13994 | 2915 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.6852 | 0.2857 | 14.8986 | 6123 | 4369 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.7857 | 0.2500 | 27.7624 | 15459 | 4994 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.6134 | 0.1818 | 10.8444 | 38708 | 1401 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.8637 | 0.2223 | 18.3898 | 4126 | 5647 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.7000 | 0.2223 | 23.5568 | 10863 | 7410 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5703 | 0.2000 | 33.9439 | 37850 | 4724 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3515 | 0.0000 | 15.3534 | 3438 | 4785 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2858 | 14.0807 | 3519 | 4374 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.0000 | 0.0000 | 100.2350 | 32565 | 16384 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.6562 | 0.2500 | 62.3633 | 13395 | 14053 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.7069 | 0.2500 | 16.0368 | 13785 | 5248 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.6956 | 0.2000 | 58.3512 | 5793 | 7018 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3515 | 0.0000 | 6.4581 | 2648 | 1929 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.5476 | 0.1818 | 52.8193 | 34367 | 8082 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.3365 | 0.0000 | 18.5814 | 9240 | 6738 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.7916 | 0.2223 | 13.7093 | 5053 | 3963 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6618 | 0.2000 | 15.9405 | 27110 | 5372 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.6071 | 0.2223 | 42.9694 | 17089 | 8192 | — |

- scored rows: 20/20; min=0.0000 max=1.0000 mean=0.6219

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 20 --seed 42 --concurrency 8 --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260928T085148Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T085148Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T085148Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T085148Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T085148Z-eval-contracts.md` | experiment-log markdown mirror |
| `reports/api-comparisons/deepseek-v4.1-flash/contracts/RUN-20-CONTRACT-DEEPSEEK-V4.1-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
