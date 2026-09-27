# Run report — `20260927T044805Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T044805Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 20 docs, seed 42 |
| timestamp | `2026-09-27T04:48:05+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T044805Z-eval-correspondence/subset_manifest.json` |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.0999 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 185.8000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost (token-priced, roster rates) | **0.0358** USD est |
| cost per document | 0.0018 USD est |
| latency e2e / p50 / p95 / max | 185.8000 / 86.3441 / 88.6388 / 89.7562 s |
| prompt / completion / total tokens | 93101 / 120989 / 214090 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1288.4 s vs wall = 185.8 s -> wall/serial factor 6.93x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | False |
| per-agent completion budgets | `{"contracts_specialist": 8192, "corporate_records_specialist": 8192, "correspondence_specialist": 4096, "insurance_claims_specialist": 6144, "merger_agreement_specialist": 16384}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `correspondence_specialist` | 34 | 93101 | 120989 | 214090 | 0.0358 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.0000 | 0.0000 | 87.1756 | 3434 | 8192 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2222 | 86.0545 | 3372 | 7997 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.0000 | 0.0000 | 87.3152 | 12958 | 8192 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.0000 | 0.0000 | 1.8957 | 1742 | 102 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.0000 | 0.0000 | 78.5188 | 4154 | 8192 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.3057 | 0.0000 | 3.1771 | 2004 | 237 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.0000 | 0.0000 | 87.2073 | 3744 | 8192 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.0000 | 0.0000 | 87.3313 | 5334 | 8192 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.2500 | 0.2500 | 30.5517 | 1648 | 2800 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.0000 | 0.0000 | 86.3441 | 5456 | 8192 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.0000 | 0.0000 | 85.6809 | 4140 | 8192 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.3368 | 0.1818 | 35.3091 | 1640 | 3213 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.0000 | 0.0000 | 89.7562 | 4114 | 8192 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.0000 | 0.0000 | 88.5462 | 3880 | 8192 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.0000 | 0.0000 | 88.6388 | 4096 | 8192 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.0000 | 0.0000 | 88.6285 | 3592 | 8192 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.0000 | 0.0000 | 0.2278 | 1647 | 2 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.0000 | 0.0000 | 88.5914 | 20620 | 8192 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5555 | 0.2666 | 1.3898 | 2216 | 142 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.0000 | 0.0000 | 86.0203 | 3310 | 8192 | — |

- scored rows: 20/20; min=0.0000 max=0.5555 mean=0.0999

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
