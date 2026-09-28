# Run report — `20260928T053010Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T053010Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 50 docs, seed 42 |
| timestamp | `2026-09-28T05:30:10+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T053010Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:34:14+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 50 / None |
| scorer | extraction |
| decode profile | — |
| prompt source / lineage | frozen / mutation |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T053010Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:30:10+00:00` |
| finished_at | `2026-09-28T05:34:14+00:00` |
| duration_s (wall) | 245.3000 |
| latency_ms_mean | 34499.3 |
| latency_ms_p95 | 49235.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5136 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5136** (sd 0.1256, min 0.1966, max 0.8611) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 245.3000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0218** USD |
| cost estimated (roster token rates) | **0.0218** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 245.3000 / 34.9569 / 49.2354 / 55.8451 s |
| prompt / completion / total tokens | 110235 / 142342 / 252577 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1725.0 s vs wall = 245.3 s -> wall/serial factor 7.03x at concurrency 8.

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
| `correspondence_specialist` | 50 | 110235 | 142342 | 252577 | 0.0218 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1725.0 s over wall 245.3 s = **7.03×** effective parallelism at c8 (88% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:donoho-l/inbox/35.` (email) 55.8 s = 23% of wall — p95/p50 = 1.41×.
- **Prompt length vs latency:** Pearson r = 0.29 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 2847 tok/doc, mean prompt 2205 tok/doc.
- **Subclass spread:** best `meeting_request` 0.717 (n=2), worst `letter` 0.468 (n=6).
- **Field-level extraction:** 2/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 27 | 0.4874 |
| notice | 7 | 0.4883 |
| letter | 6 | 0.4680 |
| memo | 4 | 0.6117 |
| press_release | 4 | 0.6039 |
| meeting_request | 2 | 0.7167 |
| **total** | **50** | **0.5136** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1176 | 32.0715 | 1642 | 2631 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 34.9569 | 1604 | 2969 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 35.9065 | 6101 | 2886 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2222 | 30.8370 | 1667 | 2407 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 41.6800 | 2031 | 3032 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 40.8290 | 1929 | 3909 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 36.9112 | 1782 | 3056 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 27.1991 | 2601 | 2388 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.2500 | 0.2500 | 24.3892 | 1569 | 1747 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5555 | 0.2105 | 37.0869 | 2579 | 3034 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.5625 | 0.2000 | 37.6709 | 1955 | 2946 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 23.3619 | 1564 | 1909 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 30.8529 | 1978 | 2536 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 55.8451 | 1874 | 5024 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.6269 | 0.2105 | 50.4147 | 1969 | 4396 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2105 | 30.7120 | 1710 | 2455 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3077 | 20.8048 | 1570 | 1657 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.5833 | 0.2105 | 49.2354 | 10072 | 3874 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5020 | 0.1429 | 33.8207 | 2141 | 2744 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1539 | 23.7775 | 1575 | 1944 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5500 | 0.2222 | 35.4528 | 2022 | 2922 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5542 | 0.1111 | 25.9629 | 1861 | 2358 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.8000 | 0.2353 | 39.0785 | 1749 | 3414 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5227 | 0.2000 | 35.7436 | 2191 | 3171 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.3864 | 0.2222 | 23.1004 | 1560 | 1692 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2353 | 40.1717 | 1822 | 3245 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1052 | 38.5526 | 1848 | 3099 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 38.6815 | 2814 | 3234 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.6136 | 0.2105 | 32.7599 | 5134 | 2663 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.8611 | 0.4000 | 30.6010 | 1850 | 2548 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.5417 | 0.2000 | 38.6020 | 1845 | 3361 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.4285 | 0.1176 | 28.7586 | 1728 | 2350 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1966 | 0.0000 | 32.2756 | 1880 | 2768 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.5857 | 0.2000 | 33.4610 | 1976 | 2856 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.4618 | 0.1250 | 34.9508 | 2126 | 2708 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.5417 | 0.2500 | 29.3744 | 2051 | 2361 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 29.3088 | 1791 | 2418 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.5000 | 0.2353 | 33.9360 | 1717 | 2681 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 40.3912 | 2057 | 3560 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1176 | 37.9158 | 1680 | 2794 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 30.5983 | 1788 | 2683 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.4066 | 0.1667 | 39.0516 | 1604 | 2953 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.5000 | 0.2222 | 37.8024 | 1790 | 3166 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.4000 | 19.7924 | 1562 | 1434 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.5000 | 0.2222 | 43.0154 | 1888 | 3486 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.5000 | 0.2222 | 35.6305 | 1729 | 3036 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1111 | 39.1485 | 2164 | 3245 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3230 | 0.1052 | 43.4432 | 1851 | 3494 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7675 | 0.3077 | 28.6448 | 2236 | 2407 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.1904 | 30.3966 | 2008 | 2691 | — |

- scored rows: 50/50; min=0.1966 max=0.8611 mean=0.5136

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 50 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T053010Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T053010Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T053010Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T053010Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T053010Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-50-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
