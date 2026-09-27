# Run report — `20260927T065622Z-eval-corporate_records` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T065622Z-eval-corporate_records` |
| task / agent | `corporate_records` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:corporate_record` — 20 docs, seed 42 |
| timestamp | `2026-09-27T06:56:22+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T065622Z-eval-corporate_records/subset_manifest.json` |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4156 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 508.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost (token-priced, roster rates) | **0.0436** USD est |
| cost per document | 0.0022 USD est |
| latency e2e / p50 / p95 / max | 508.6000 / 86.2307 / 205.0196 / 412.9075 s |
| prompt / completion / total tokens | 196299 / 127441 / 323740 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1902.9 s vs wall = 508.6 s -> wall/serial factor 3.74x at concurrency 8.

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
| `corporate_records_specialist` | 22 | 196299 | 127441 | 323740 | 0.0436 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:0001047469-12-006895_a2210011zex-4_10.htm` | indenture | 0.2545 | 0.0000 | 86.2307 | 20192 | 5815 | — |
| 2 | `corpus:ground_truth:train:0001047469-03-032251_a2118977zex-3_2.htm` | bylaws | 0.5500 | 0.2105 | 3.6028 | 20574 | 159 | — |
| 3 | `corpus:ground_truth:train:0000950123-11-055070_h75396a4exv21w1.htm` | subsidiary_list | 0.0000 | 0.0000 | 10.0501 | 2135 | 569 | — |
| 4 | `corpus:ground_truth:train:0000898430-01-503595_dex32.txt` | charter_amendment | 0.2762 | 0.0000 | 117.1225 | 2017 | 7662 | — |
| 5 | `corpus:ground_truth:train:0001193125-11-240442_dex43.htm` | rights_instrument | 0.6691 | 0.2352 | 49.0597 | 2854 | 3330 | — |
| 6 | `corpus:ground_truth:train:0000950123-10-001751_c54716a1exv4w2.htm` | rights_instrument | 0.6214 | 0.2352 | 205.0196 | 15176 | 13623 | — |
| 7 | `corpus:ground_truth:train:0001571049-14-000599_t1400242_ex3-1.htm` | articles_of_incorporation | 0.6750 | 0.2223 | 3.8954 | 8206 | 170 | — |
| 8 | `corpus:ground_truth:train:0001193125-13-256819_d428632dex211.htm` | subsidiary_list | 0.4636 | 0.2000 | 113.2662 | 1725 | 7433 | — |
| 9 | `corpus:ground_truth:train:0001104659-22-110926_tm2225873d4_ex3-5.htm` | officer_certificate | 0.3372 | 0.0000 | 2.4331 | 10529 | 169 | — |
| 10 | `corpus:ground_truth:train:0001193125-08-109289_dex241.htm` | powers_of_attorney | 0.5708 | 0.2666 | 197.2134 | 4008 | 13191 | — |
| 11 | `corpus:ground_truth:train:0001079974-08-000839_artdimensionss1x31_9252008.htm` | articles_of_incorporation | 0.7063 | 0.4000 | 75.9105 | 3724 | 5191 | — |
| 12 | `corpus:ground_truth:train:0001193125-05-179145_dex32.htm` | charter_amendment | 0.3098 | 0.0000 | 89.8757 | 2391 | 5973 | — |
| 13 | `corpus:ground_truth:train:0001021432-06-000035_certamendriv090106.txt` | board_resolution | 0.4234 | 0.1333 | 64.8671 | 1911 | 4041 | — |
| 14 | `corpus:ground_truth:train:0001021432-06-000037_certamendcal092706.txt` | board_resolution | 0.4098 | 0.1250 | 76.2684 | 1904 | 4898 | — |
| 15 | `corpus:ground_truth:train:0000950137-05-002026_c91812a1exv4w1.txt` | indenture | 0.3589 | 0.0000 | 412.9075 | 75165 | 28170 | — |
| 16 | `corpus:ground_truth:train:0001104659-18-050217_a18-2297_8ex3d3.htm` | officer_certificate | 0.2294 | 0.0000 | 99.5942 | 5942 | 6647 | — |
| 17 | `corpus:ground_truth:train:0001144204-16-109616_v442647_ex3-1.htm` | charter_amendment | 0.2521 | 0.0000 | 163.8421 | 6951 | 11293 | — |
| 18 | `corpus:ground_truth:train:0001193125-10-221497_dex32.htm` | charter_amendment | 0.5910 | 0.1538 | 2.4111 | 2396 | 168 | — |
| 19 | `corpus:ground_truth:train:0001493152-23-024269_ex4-5.htm` | indenture | 0.3115 | 0.0000 | 126.8707 | 3619 | 8773 | — |
| 20 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0302.htm` | officer_certificate | 0.3025 | 0.0000 | 2.5044 | 4880 | 166 | — |

- scored rows: 20/20; min=0.0000 max=0.7063 mean=0.4156

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
