# Run report — `20260926T235347Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260926T235347Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 20 docs, seed 42 |
| timestamp | `2026-09-26T23:53:47+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260926T235347Z-eval-contracts/subset_manifest.json` |
| eval git | `d386cde` |
| finished | `2026-09-27T00:15:10+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / node |
| mode | real |
| concurrency | 1 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | qwen3-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260926T235347Z-eval-contracts', 'dataset': 'mailroom-hf-46a4d3c2', 'dataset_records': 20}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-26T23:53:47+00:00` |
| finished_at | `2026-09-27T00:15:10+00:00` |
| duration_s (wall) | 1284.9 |
| latency_ms_mean | 56685.5 |
| latency_ms_p95 | 111956.8 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.6199 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.6199** (sd 0.1790, min 0.2236, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 1284.9 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.0584** USD |
| cost estimated (roster token rates) | **0.0584** USD |
| cost per document (actual) | 0.0029 USD |
| cost per document (estimated) | 0.0029 USD |
| latency e2e / p50 / p95 / max | 1284.9 / 55.6418 / 111.9568 / 119.6383 s |
| prompt / completion / total tokens | 339923 / 40872 / 380795 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1133.7 s vs wall = 1284.9 s -> wall/serial factor 0.88x at concurrency 1.

## Decode posture

| control | value |
|---|---|
| sampling override | `none (pipeline posture)` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 8192, "corporate_records_specialist": 8192, "correspondence_specialist": 4096, "insurance_claims_specialist": 6144, "merger_agreement_specialist": 8192}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `contracts_specialist` | 24 | 339923 | 40872 | 380795 | 0.0584 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1133.7 s over wall 1284.9 s = **0.88×** effective parallelism at c1 (88% of the ideal 1×).
- **Tail:** slowest doc `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` (Franchise) 119.6 s = 9% of wall — p95/p50 = 2.01×.
- **Prompt length vs latency:** Pearson r = 0.83 across 20 docs (prefill-bound).
- **Decode budget:** mean completion 2044 tok/doc, mean prompt 16996 tok/doc.
- **Subclass spread:** best `Consulting Agreements` 1.000 (n=1), worst `Marketing` 0.224 (n=1).
- **Field-level extraction:** 4/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Strategic Alliance | 4 | 0.6495 |
| Distributor | 3 | 0.6426 |
| IP | 2 | 0.3514 |
| Collaboration | 1 | 0.6267 |
| Consulting Agreements | 1 | 1.0000 |
| Development | 1 | 0.7424 |
| Endorsement | 1 | 0.9445 |
| Franchise | 1 | 0.5893 |
| Joint Venture _ Filing | 1 | 0.6785 |
| License_Agreements | 1 | 0.6297 |
| Maintenance | 1 | 0.4051 |
| Marketing | 1 | 0.2236 |
| Promotion | 1 | 0.6016 |
| Sponsorship | 1 | 0.7272 |
| **total** | **20** | **0.6199** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.9445 | 0.1111 | 58.2687 | 7676 | 2660 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5972 | 0.1818 | 52.9278 | 15932 | 2231 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.6297 | 0.2500 | 40.5879 | 7845 | 1831 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6429 | 0.2500 | 34.2396 | 17504 | 1230 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.6267 | 0.0571 | 80.1793 | 48145 | 2898 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.7272 | 0.1818 | 35.4548 | 5895 | 1788 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.6444 | 0.2000 | 55.6418 | 12512 | 1914 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.6016 | 0.2000 | 111.9568 | 46052 | 2855 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 0.3514 | 0.0000 | 21.3457 | 5285 | 983 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2501 | 25.5169 | 5275 | 1263 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.7424 | 0.1250 | 76.5792 | 18328 | 3188 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.6094 | 0.2223 | 51.0270 | 8552 | 2105 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.4051 | 0.0000 | 59.6131 | 15814 | 2184 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.6739 | 0.1818 | 36.4244 | 7514 | 1501 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3514 | 0.0000 | 9.0612 | 4354 | 428 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.5893 | 0.1428 | 119.6383 | 42060 | 3186 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.2236 | 0.0000 | 31.1185 | 11049 | 1289 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.6666 | 0.2000 | 70.9103 | 6800 | 1462 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6912 | 0.1538 | 95.0456 | 34239 | 3201 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.6785 | 0.1428 | 68.1727 | 19092 | 2675 | — |

- scored rows: 20/20; min=0.2236 max=1.0000 mean=0.6199

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 20 --seed 42 --concurrency 1 --decode-profile qwen3-8b --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260926T235347Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260926T235347Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260926T235347Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260926T235347Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260926T235347Z-eval-contracts.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3-8b/contracts/RUN-20-CONTRACT-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
