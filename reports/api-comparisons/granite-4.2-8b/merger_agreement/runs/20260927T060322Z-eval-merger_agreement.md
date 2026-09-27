# Run report — `20260927T060322Z-eval-merger_agreement` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T060322Z-eval-merger_agreement` |
| task / agent | `merger_agreement` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:merger_agreement` — 20 docs, seed 42 |
| timestamp | `2026-09-27T06:03:22+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T060322Z-eval-merger_agreement/subset_manifest.json` |
| eval git | `1d9f8d2` |
| finished | `2026-09-27T06:54:02+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T060322Z-eval-merger_agreement', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T06:03:22+00:00` |
| finished_at | `2026-09-27T06:54:02+00:00` |
| duration_s (wall) | 3041.9 |
| latency_ms_mean | 1065584.0 |
| latency_ms_p95 | 1748404.3 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.387 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 3041.9 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.8000** USD |
| cost actual (derived from case rows) | **0.4374** USD |
| cost estimated (roster token rates) | **0.4374** USD |
| cost per document (actual) | 0.0219 USD |
| cost per document (estimated) | 0.0219 USD |
| latency e2e / p50 / p95 / max | 3041.9 / 1017.2 / 1748.4 / 1950.6 s |
| prompt / completion / total tokens | 2044275 / 1259169 / 3303444 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 21311.7 s vs wall = 3041.9 s -> wall/serial factor 7.01x at concurrency 8.

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
| `merger_agreement_specialist` | 170 | 2044275 | 1259169 | 3303444 | 0.4374 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:contract_128_merger_agreement.txt` | other | 0.0990 | 0.0000 | 1247.6 | 104044 | 64446 | — |
| 2 | `corpus:ground_truth:train:contract_31_merger_agreement.txt` | other | 0.0990 | 0.0000 | 1112.4 | 95601 | 65538 | — |
| 3 | `corpus:ground_truth:train:contract_99_merger_agreement.txt` | all_cash | 0.5333 | 0.1818 | 1424.5 | 105932 | 77147 | — |
| 4 | `corpus:ground_truth:train:contract_114_merger_agreement.txt` | other | 0.1163 | 0.0000 | 909.9936 | 95829 | 53930 | — |
| 5 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | 0.5588 | 0.1818 | 1748.4 | 121317 | 87462 | — |
| 6 | `corpus:ground_truth:train:contract_120_merger_agreement.txt` | other | 0.0990 | 0.0000 | 1005.0 | 100024 | 59287 | — |
| 7 | `corpus:ground_truth:train:contract_41_merger_agreement.txt` | all_cash | 0.5588 | 0.1667 | 1234.8 | 105664 | 70005 | — |
| 8 | `corpus:ground_truth:train:contract_62_merger_agreement.txt` | all_cash | 0.7222 | 0.1818 | 953.9027 | 85766 | 56862 | — |
| 9 | `corpus:ground_truth:train:contract_51_merger_agreement.txt` | other | 0.5000 | 0.2000 | 1361.0 | 116943 | 77736 | — |
| 10 | `corpus:ground_truth:train:contract_70_merger_agreement.txt` | other | 0.1441 | 0.0000 | 893.2194 | 107603 | 50852 | — |
| 11 | `corpus:ground_truth:train:contract_100_merger_agreement.txt` | all_stock | 0.5000 | 0.1818 | 1950.6 | 106317 | 135798 | — |
| 12 | `corpus:ground_truth:train:contract_97_merger_agreement.txt` | mixed_cash_stock | 0.5278 | 0.2000 | 556.9023 | 72158 | 31008 | — |
| 13 | `corpus:ground_truth:train:contract_71_merger_agreement.txt` | all_cash | 0.6111 | 0.2000 | 1186.2 | 91793 | 67453 | — |
| 14 | `corpus:ground_truth:train:contract_66_merger_agreement.txt` | all_stock | 0.3905 | 0.0000 | 1256.1 | 121184 | 72636 | — |
| 15 | `corpus:ground_truth:train:contract_34_merger_agreement.txt` | other | 0.0990 | 0.0000 | 1017.2 | 107976 | 58228 | — |
| 16 | `corpus:ground_truth:train:contract_5_merger_agreement.txt` | mixed_cash_stock | 0.5000 | 0.2223 | 796.0787 | 117575 | 46666 | — |
| 17 | `corpus:ground_truth:train:contract_76_merger_agreement.txt` | other | 0.0990 | 0.0000 | 870.4453 | 123664 | 52696 | — |
| 18 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | 0.5312 | 0.1818 | 430.0161 | 71543 | 28171 | — |
| 19 | `corpus:ground_truth:train:contract_122_merger_agreement.txt` | other | 0.5000 | 0.1818 | 606.5959 | 93603 | 46121 | — |
| 20 | `corpus:ground_truth:train:contract_19_merger_agreement.txt` | mixed_cash_stock | 0.5500 | 0.1667 | 750.7011 | 99739 | 57127 | — |

- scored rows: 20/20; min=0.0990 max=0.7222 mean=0.3870

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- **Merger chunking:** up to `10` source chunks per row — confirm the run model inherits merger-specific limits from `LARGE_COMPLETION_MODELS` / `CHUNK_CHARS`, not an accidental qwen3-8b default on Granite.
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
