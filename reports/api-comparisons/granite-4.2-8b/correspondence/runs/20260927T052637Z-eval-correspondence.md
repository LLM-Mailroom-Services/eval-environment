# Run report — `20260927T052637Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T052637Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-27T05:26:37+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T052637Z-eval-correspondence/subset_manifest.json` |
| eval git | `2a70e8c` |
| finished | `2026-09-27T05:31:27+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T052637Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T05:26:37+00:00` |
| finished_at | `2026-09-27T05:31:27+00:00` |
| duration_s (wall) | 292.0000 |
| latency_ms_mean | 79968.0 |
| latency_ms_p95 | 197714.1 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.3793 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 292.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **0.8000** USD |
| cost actual (derived from case rows) | **0.0336** USD |
| cost estimated (roster token rates) | **0.0336** USD |
| cost per document (actual) | 0.0017 USD |
| cost per document (estimated) | 0.0017 USD |
| latency e2e / p50 / p95 / max | 292.0000 / 76.7583 / 197.7141 / 206.6773 s |
| prompt / completion / total tokens | 62422 / 119301 / 181723 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1599.4 s vs wall = 292.0 s -> wall/serial factor 5.48x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | True |
| per-agent completion budgets | `{"contracts_specialist": 16384, "corporate_records_specialist": 16384, "correspondence_specialist": 8192, "insurance_claims_specialist": 12288, "merger_agreement_specialist": 32768}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `correspondence_specialist` | 23 | 62422 | 119301 | 181723 | 0.0336 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1539 | 94.1862 | 1713 | 6667 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2222 | 68.7473 | 1682 | 4846 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.5769 | 0.2000 | 206.6773 | 12958 | 14864 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.4190 | 0.1333 | 72.4446 | 1742 | 5103 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.0000 | 0.0000 | 0.9920 | 2073 | 2 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.0000 | 0.0000 | 2.2304 | 2004 | 102 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 75.7724 | 1868 | 5317 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.7000 | 0.2222 | 113.9268 | 2663 | 8118 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.5000 | 0.4444 | 35.5227 | 1648 | 2622 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5000 | 0.2105 | 91.4781 | 2724 | 6493 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.5625 | 0.2105 | 76.7583 | 2066 | 5399 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.3409 | 0.1818 | 52.1240 | 1640 | 3788 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 86.5244 | 2053 | 6336 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.0000 | 0.0000 | 197.7141 | 3880 | 16384 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.0000 | 0.0000 | 192.6988 | 4096 | 16384 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5750 | 0.2105 | 82.8085 | 1792 | 6080 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.0000 | 0.0000 | 0.2303 | 1647 | 2 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.5833 | 0.2105 | 90.8292 | 10306 | 6580 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4520 | 0.1539 | 1.9986 | 2216 | 137 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1429 | 55.6958 | 1651 | 4077 | — |

- scored rows: 20/20; min=0.0000 max=0.7000 mean=0.3793

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- **Call count:** `23` specialist LLM calls for `20` documents — this is **not** source chunking when `needed_chunks=1` (here max `1`). Extra calls are JSON parse / network **retries** (`llm_call_budget=2`). Do not apply merger 48K chunk settings to correspondence or insurance.
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
