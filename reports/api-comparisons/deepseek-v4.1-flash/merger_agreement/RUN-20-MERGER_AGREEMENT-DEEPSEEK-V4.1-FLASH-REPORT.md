# Run report — `20260927T110153Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T110153Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-27T11:01:53+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T110153Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `3c2c95c` |
| finished | `2026-09-27T11:08:24+00:00` |

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
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T110153Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T11:01:53+00:00` |
| finished_at | `2026-09-27T11:08:24+00:00` |
| duration_s (wall) | 392.7000 |
| latency_ms_mean | 41119.4 |
| latency_ms_p95 | 63886.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.2423 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 392.7000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0752** USD |
| cost estimated (roster token rates) | **0.0752** USD |
| cost per document (actual) | 0.0038 USD |
| cost per document (estimated) | 0.0038 USD |
| latency e2e / p50 / p95 / max | 392.7000 / 29.3745 / 63.8866 / 388.5278 s |
| prompt / completion / total tokens | 1228920 / 111149 / 1340069 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 822.4 s vs wall = 392.7 s -> wall/serial factor 2.09x at concurrency 8.

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
| `merger_agreement_specialist` | 15 | 1228920 | 111149 | 1340069 | 0.0752 | deepseek/deepseek-v4.1-flash |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.6162 | 0.1333 | 23.2105 | 81609 | 6652 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.3700 | 0.0000 | 29.9922 | 77613 | 7336 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.7333 | 0.1428 | 26.5494 | 84384 | 6912 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.3221 | 0.0000 | 56.7746 | 74753 | 6407 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.0000 | 0.0000 | 63.8866 | 194355 | 16384 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.3516 | 0.0000 | 388.5278 | 159841 | 15147 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.7059 | 0.1818 | 30.0938 | 86115 | 8192 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.7500 | 0.1818 | 26.9649 | 69431 | 5825 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.0000 | 0.0000 | 29.9136 | 94667 | 8192 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.3385 | 0.0000 | 29.3745 | 86843 | 6480 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.6583 | 0.0000 | 33.8184 | 87820 | 7238 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.0000 | 0.0000 | 38.2242 | 58090 | 8192 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 35.6446 | 73399 | 8192 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.0000 | 0.0000 | 0.8509 | 0 | 0 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.0000 | 0.0000 | 1.2669 | 0 | 0 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.0000 | 0.0000 | 1.3166 | 0 | 0 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.0000 | 0.0000 | 1.9221 | 0 | 0 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.0000 | 0.0000 | 1.8994 | 0 | 0 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.0000 | 0.0000 | 1.3158 | 0 | 0 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.0000 | 0.0000 | 0.8414 | 0 | 0 | — |

- scored rows: 20/20; min=0.0000 max=0.7500 mean=0.2423

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
