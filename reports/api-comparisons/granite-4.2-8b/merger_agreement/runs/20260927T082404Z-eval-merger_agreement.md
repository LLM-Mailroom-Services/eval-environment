# Run report — `20260927T082404Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T082404Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-27T08:24:04+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T082404Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `b66e30f` |
| finished | `2026-09-27T08:44:30+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 20 / None |
| scorer | extraction |
| decode profile | granite-4.2-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T082404Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T08:24:04+00:00` |
| finished_at | `2026-09-27T08:44:30+00:00` |
| duration_s (wall) | 1228.0 |
| latency_ms_mean | 383811.6 |
| latency_ms_p95 | 580299.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4548 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 1228.0 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.8000** USD |
| cost actual (derived from case rows) | **0.1774** USD |
| cost estimated (roster token rates) | **0.1774** USD |
| cost per document (actual) | 0.0089 USD |
| cost per document (estimated) | 0.0089 USD |
| latency e2e / p50 / p95 / max | 1228.0 / 423.3011 / 580.2994 / 655.5391 s |
| prompt / completion / total tokens | 1678904 / 306796 / 1985700 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 7676.2 s vs wall = 1228.0 s -> wall/serial factor 6.25x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | True |
| per-agent completion budgets | `{"contracts_specialist": 16384, "corporate_records_specialist": 16384, "correspondence_specialist": 16384, "insurance_claims_specialist": 12288, "merger_agreement_specialist": 32768}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `merger_agreement_specialist` | 38 | 1678904 | 306796 | 1985700 | 0.1774 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.5000 | 0.2000 | 423.3011 | 84602 | 15472 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.5000 | 0.2000 | 440.9204 | 79473 | 15426 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.6666 | 0.1818 | 655.5391 | 86208 | 22864 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.5000 | 0.2000 | 292.2944 | 77359 | 12347 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.5588 | 0.1818 | 573.6464 | 99604 | 20314 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.0990 | 0.0000 | 526.4088 | 82985 | 18713 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.5000 | 0.1818 | 508.2245 | 87542 | 18044 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.5278 | 0.1818 | 419.1535 | 71717 | 14447 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.5000 | 0.2223 | 219.8686 | 95965 | 8494 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.5000 | 0.2000 | 142.9306 | 88448 | 7533 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.5000 | 0.2000 | 580.2994 | 89028 | 38991 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5000 | 0.1818 | 143.9970 | 56862 | 5142 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.5278 | 0.1818 | 457.4594 | 76233 | 16934 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.3315 | 0.0000 | 313.7211 | 99384 | 10954 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.0990 | 0.0000 | 212.1525 | 86404 | 7377 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.5000 | 0.2000 | 293.5110 | 96449 | 10648 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.0990 | 0.0000 | 517.8981 | 102162 | 21817 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.5625 | 0.1818 | 223.6103 | 57658 | 7736 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.5000 | 0.2000 | 248.7591 | 76663 | 9668 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.6250 | 0.1538 | 482.5362 | 84158 | 23875 | — |

- scored rows: 20/20; min=0.0990 max=0.6666 mean=0.4548

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
