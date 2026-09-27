# Run report — `20260927T070900Z-eval-classification` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T070900Z-eval-classification` |
| task / agent | `classification` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `full` — 20 docs, seed 42 |
| timestamp | `2026-09-27T07:09:00+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T070900Z-eval-classification/subset_manifest.json` |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **20 / 20** (`errors=0`) |
| class_accuracy | 0.9 |
| errors | 0 |
| scorer_errors | 0 |
| subclass_accuracy | 0.6 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 184.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost (token-priced, roster rates) | **0.0644** USD est |
| cost per document | 0.0032 USD est |
| latency e2e / p50 / p95 / max | 184.3000 / 3.6696 / 111.1213 / 174.0132 s |
| prompt / completion / total tokens | 933912 / 33329 / 967241 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 537.2 s vs wall = 184.3 s -> wall/serial factor 2.91x at concurrency 8.

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
| `sorter` | 118 | 933912 | 33329 | 967241 | 0.0644 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:property:261501663.txt` | property | — | — | 3.6696 | 7206 | 171 | — |
| 2 | `corpus:ground_truth:train:inpatient:196841176990879:1.txt` | inpatient | — | — | 9.7479 | 6087 | 192 | — |
| 3 | `corpus:ground_truth:train:insurbias-425.txt` | auto | — | — | 2.8564 | 5839 | 151 | — |
| 4 | `corpus:ground_truth:train:brawner-s/all_documents/59.` | email | — | — | 3.8993 | 6195 | 187 | — |
| 5 | `corpus:ground_truth:train:0000912057-01-507164_a2041839zex-4_38.txt` | rights_instrument | — | — | 6.3046 | 13636 | 372 | — |
| 6 | `corpus:ground_truth:train:dasovich-j/all_documents/9309.` | press_release | — | — | 3.2054 | 6114 | 142 | — |
| 7 | `corpus:ground_truth:train:dasovich-j/all_documents/9178.` | press_release | — | — | 2.8426 | 5832 | 149 | — |
| 8 | `corpus:ground_truth:train:0000950130-01-502904_dex211.txt` | subsidiary_list | — | — | 2.7020 | 5844 | 134 | — |
| 9 | `corpus:ground_truth:train:inpatient:196091177001318:1.txt` | inpatient | — | — | 2.7587 | 6094 | 162 | — |
| 10 | `corpus:ground_truth:train:inpatient:196831176969260:1.txt` | inpatient | — | — | 3.1110 | 6070 | 192 | — |
| 11 | `corpus:ground_truth:train:0001193125-14-273392_d715499dex415.htm` | indenture | — | — | 3.1009 | 8466 | 179 | — |
| 12 | `corpus:ground_truth:train:contract_117_merger_agreement.txt` | all_stock | — | — | 111.1213 | 115533 | 5383 | — |
| 13 | `corpus:ground_truth:train:property:262952775.txt` | property | — | — | 5.1676 | 14874 | 319 | — |
| 14 | `corpus:ground_truth:train:0000950123-03-010752_y88696a1exv4w7.txt` | indenture | — | — | 97.5466 | 260636 | 6850 | — |
| 15 | `corpus:ground_truth:train:contract_4_merger_agreement.txt` | all_cash | — | — | 92.1201 | 115241 | 4573 | — |
| 16 | `corpus:ground_truth:train:carrier:887493388020303.txt` | carrier | — | — | 2.4212 | 6013 | 142 | — |
| 17 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | — | — | 174.0132 | 317705 | 13346 | — |
| 18 | `corpus:ground_truth:train:inpatient:196641176967981:1.txt` | inpatient | — | — | 2.6248 | 6094 | 159 | — |
| 19 | `corpus:ground_truth:train:0001047469-06-011763_a2173128zex-3_1.htm` | charter_amendment | — | — | 4.9986 | 14430 | 336 | — |
| 20 | `corpus:ground_truth:train:outpatient:542502281397875:1.txt` | outpatient | — | — | 3.0053 | 6003 | 190 | — |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
