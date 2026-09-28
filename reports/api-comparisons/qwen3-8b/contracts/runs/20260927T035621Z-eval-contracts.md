# Run report — `20260927T035621Z-eval-contracts` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T035621Z-eval-contracts` |
| task / agent | `contracts` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3-8b` (OpenRouter API) |
| profile / provider | `qwen3-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:contract` — 20 docs, seed 42 |
| timestamp | `2026-09-27T03:56:21+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T035621Z-eval-contracts/subset_manifest.json` |
| eval git | `a3506e2` |
| finished | `2026-09-27T04:20:36+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T035621Z-eval-contracts', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T03:56:21+00:00` |
| finished_at | `2026-09-27T04:20:36+00:00` |
| duration_s (wall) | 1457.5 |
| latency_ms_mean | 177560.9 |
| latency_ms_p95 | 285038.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.6169 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.6169** (sd 0.1469, min 0.3514, max 1.0000) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 1457.5 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.1200** USD |
| cost actual (derived from case rows) | **0.1141** USD |
| cost estimated (roster token rates) | **0.1141** USD |
| cost per document (actual) | 0.0057 USD |
| cost per document (estimated) | 0.0057 USD |
| latency e2e / p50 / p95 / max | 1457.5 / 110.9361 / 285.0389 / 1244.6 s |
| prompt / completion / total tokens | 546225 / 110286 / 656511 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 3551.2 s vs wall = 1457.5 s -> wall/serial factor 2.44x at concurrency 8.

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
| `contracts_specialist` | 44 | 546225 | 110286 | 656511 | 0.1141 | qwen/qwen3-8b |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 3551.2 s over wall 1457.5 s = **2.44×** effective parallelism at c8 (30% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` (Marketing) 1244.6 s = 85% of wall — p95/p50 = 2.57×.
- **Prompt length vs latency:** Pearson r = 0.02 across 20 docs (not prefill-dominated).
- **Decode budget:** mean completion 5514 tok/doc, mean prompt 27311 tok/doc.
- **Subclass spread:** best `Consulting Agreements` 1.000 (n=1), worst `Promotion` 0.523 (n=1).
- **Field-level extraction:** 1/20 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Scoring method — CUAD contracts

Headline **overall_score** uses the pipeline contracts extraction rubric. Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| Strategic Alliance | 4 | 0.6201 |
| Distributor | 3 | 0.5559 |
| IP | 2 | 0.6757 |
| Collaboration | 1 | 0.5400 |
| Consulting Agreements | 1 | 1.0000 |
| Development | 1 | 0.5757 |
| Endorsement | 1 | 0.6111 |
| Franchise | 1 | 0.6012 |
| Joint Venture _ Filing | 1 | 0.5535 |
| License_Agreements | 1 | 0.6482 |
| Maintenance | 1 | 0.5689 |
| Marketing | 1 | 0.5806 |
| Promotion | 1 | 0.5234 |
| Sponsorship | 1 | 0.6363 |
| **total** | **20** | **0.6169** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:MOVADOGROUPINC_04_30_2003-EX-10.28-ENDORSEMENT AGREEMENT.PDF` | Endorsement | 0.6111 | 0.2500 | 139.2829 | 11813 | 4903 | — |
| 2 | `corpus:ground_truth:train:GOLDRESOURCECORP_12_11_2008-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5139 | 0.1818 | 85.4253 | 28325 | 3460 | — |
| 3 | `corpus:ground_truth:train:MorganStanleyDirectLendingFund_20191119_10-12GA_EX-10.5_11898508_EX-10.5_Trademark License Agreement.pdf` | License_Agreements | 0.6482 | 0.2857 | 53.3083 | 12153 | 2232 | — |
| 4 | `corpus:ground_truth:train:SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.6429 | 0.2500 | 110.9361 | 31469 | 3337 | — |
| 5 | `corpus:ground_truth:train:FOUNDATIONMEDICINE,INC_02_02_2015-EX-10.2-Collaboration Agreement.PDF` | Collaboration | 0.5400 | 0.1250 | 200.4090 | 89624 | 5882 | — |
| 6 | `corpus:ground_truth:train:EcoScienceSolutionsInc_20180406_8-K_EX-10.1_11135398_EX-10.1_Sponsorship Agreement.pdf` | Sponsorship | 0.6363 | 0.1818 | 76.4063 | 8251 | 2231 | — |
| 7 | `corpus:ground_truth:train:NETGEAR,INC_04_21_2003-EX-10.16-DISTRIBUTOR AGREEMENT.pdf` | Distributor | 0.5555 | 0.2223 | 138.9529 | 10744 | 1079 | — |
| 8 | `corpus:ground_truth:train:KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.PDF` | Promotion | 0.5234 | 0.1111 | 201.4560 | 84414 | 5817 | — |
| 9 | `corpus:ground_truth:train:0001047469-05-021628_a2161868zex-10_9.htm` | IP | 1.0000 | 0.2501 | 51.3260 | 3511 | 1384 | — |
| 10 | `corpus:ground_truth:train:0000721748-15-000083_ncmf02121510_20.htm` | Consulting Agreements | 1.0000 | 0.2858 | 53.5752 | 7013 | 2935 | — |
| 11 | `corpus:ground_truth:train:ConformisInc_20191101_10-Q_EX-10.6_11861402_EX-10.6_Development Agreement.pdf` | Development | 0.5757 | 0.1818 | 175.8125 | 33113 | 6121 | — |
| 12 | `corpus:ground_truth:train:NEONSYSTEMSINC_03_01_1999-EX-10.5-DISTRIBUTOR AGREEMENT_Amendment.pdf` | Distributor | 0.5469 | 0.1818 | 139.2848 | 13563 | 5235 | — |
| 13 | `corpus:ground_truth:train:VERTEXENERGYINC_08_14_2014-EX-10.24-OPERATION AND MAINTENANCE AGREEMENT.PDF` | Maintenance | 0.5689 | 0.2500 | 82.9210 | 28085 | 2462 | — |
| 14 | `corpus:ground_truth:train:LEGACYTECHNOLOGYHOLDINGS,INC_12_09_2005-EX-10.2-DISTRIBUTOR AGREEMENT.PDF` | Distributor | 0.5652 | 0.2000 | 74.1882 | 11487 | 3311 | — |
| 15 | `corpus:ground_truth:train:0001582718-14-000092_ex-10_1.htm` | IP | 0.3514 | 0.0000 | 72.7786 | 5165 | 3288 | — |
| 16 | `corpus:ground_truth:train:PfHospitalityGroupInc_20150923_10-12G_EX-10.1_9266710_EX-10.1_Franchise Agreement1.pdf` | Franchise | 0.6012 | 0.0834 | 211.7237 | 77874 | 7615 | — |
| 17 | `corpus:ground_truth:train:TodosMedicalLtd_20190328_20-F_EX-4.10_11587157_EX-4.10_Marketing Agreement_ Reseller Agreement.pdf` | Marketing | 0.5806 | 0.2223 | 1244.6 | 9275 | 39587 | — |
| 18 | `corpus:ground_truth:train:TURNKEYCAPITAL,INC_07_20_2017-EX-1.1-Strategic Alliance Agreement.PDF` | Strategic Alliance | 0.7500 | 0.1818 | 48.1014 | 10061 | 2188 | — |
| 19 | `corpus:ground_truth:train:ROCKYMOUNTAINCHOCOLATEFACTORY,INC_12_23_2019-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.PDF` | Strategic Alliance | 0.5736 | 0.2223 | 285.0389 | 35636 | 4439 | — |
| 20 | `corpus:ground_truth:train:IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.PDF` | Joint Venture _ Filing | 0.5535 | 0.1250 | 105.6713 | 34649 | 2780 | — |

- scored rows: 20/20; min=0.3514 max=1.0000 mean=0.6169

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:contracts --real --sample 20 --seed 42 --concurrency 8 --decode-profile qwen3-8b --subset "class:contract"
uv run python scripts/score_run.py --run-id 20260927T035621Z-eval-contracts --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260927T035621Z-eval-contracts
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260927T035621Z-eval-contracts/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260927T035621Z-eval-contracts/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260927T035621Z-eval-contracts.md` | experiment-log markdown mirror |
| `/workspace/reports/api-comparisons/qwen3-8b/RUN-20-CONTRACT-QWEN3-8B-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `qwen3-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
