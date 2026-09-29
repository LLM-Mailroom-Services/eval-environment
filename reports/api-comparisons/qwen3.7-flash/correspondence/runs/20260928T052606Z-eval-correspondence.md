# Run report — `20260928T052606Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T052606Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 50 docs, seed 42 |
| timestamp | `2026-09-28T05:26:06+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T052606Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T05:30:04+00:00` |

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
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T052606Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T05:26:06+00:00` |
| finished_at | `2026-09-28T05:30:04+00:00` |
| duration_s (wall) | 240.0000 |
| latency_ms_mean | 34356.3 |
| latency_ms_p95 | 49371.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5022 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5022** (sd 0.1327, min 0.1966, max 0.9250) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 240.0000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0221** USD |
| cost estimated (roster token rates) | **0.0221** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 240.0000 / 33.8628 / 49.3717 / 52.8043 s |
| prompt / completion / total tokens | 108735 / 144601 / 253336 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1717.8 s vs wall = 240.0 s -> wall/serial factor 7.16x at concurrency 8.

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
| `correspondence_specialist` | 50 | 108735 | 144601 | 253336 | 0.0221 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1717.8 s over wall 240.0 s = **7.16×** effective parallelism at c8 (89% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:buy-r/inbox/411.` (email) 52.8 s = 22% of wall — p95/p50 = 1.46×.
- **Prompt length vs latency:** Pearson r = 0.22 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 2892 tok/doc, mean prompt 2175 tok/doc.
- **Subclass spread:** best `meeting_request` 0.779 (n=2), worst `email` 0.463 (n=27).
- **Field-level extraction:** 2/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 27 | 0.4626 |
| notice | 7 | 0.4811 |
| letter | 6 | 0.4898 |
| memo | 4 | 0.5798 |
| press_release | 4 | 0.6088 |
| meeting_request | 2 | 0.7792 |
| **total** | **50** | **0.5022** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1250 | 34.1726 | 1612 | 2811 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 38.9840 | 1574 | 3316 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 39.8822 | 6071 | 3244 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2222 | 26.4478 | 1637 | 2225 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 33.5710 | 2001 | 2769 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 37.7866 | 1899 | 3149 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 38.3616 | 1752 | 3374 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 31.9972 | 2571 | 2706 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.2500 | 0.2500 | 20.0339 | 1539 | 1577 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5555 | 0.2105 | 39.7025 | 2549 | 3290 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.6125 | 0.2105 | 34.6197 | 1925 | 2857 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 22.2651 | 1534 | 1644 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 27.7744 | 1948 | 2350 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.4959 | 0.1000 | 49.3717 | 1844 | 3955 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.6462 | 0.2105 | 47.7404 | 1939 | 4186 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2222 | 31.3685 | 1680 | 2475 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3077 | 32.6495 | 1540 | 2607 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.5833 | 0.2105 | 43.3535 | 10042 | 3376 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5020 | 0.1429 | 28.7709 | 2111 | 2618 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1539 | 25.0157 | 1545 | 1956 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5000 | 0.2000 | 27.5524 | 1992 | 2442 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5542 | 0.1176 | 25.8965 | 1831 | 2349 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.9250 | 0.3529 | 36.3061 | 1719 | 3218 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5227 | 0.1904 | 29.6359 | 2161 | 2658 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.3864 | 0.2222 | 25.4590 | 1530 | 2047 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2353 | 30.9741 | 1792 | 2615 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1111 | 30.6125 | 1818 | 2703 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 33.8628 | 2784 | 2936 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.6136 | 0.2105 | 35.5364 | 5104 | 3021 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.7480 | 0.2857 | 34.0215 | 1820 | 2864 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.3673 | 0.1000 | 44.4701 | 1815 | 3837 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.4702 | 0.1176 | 28.1601 | 1698 | 2465 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1966 | 0.0000 | 33.3030 | 1850 | 2833 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.5714 | 0.2105 | 47.9246 | 1946 | 4019 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.3618 | 0.1176 | 35.3074 | 2096 | 2740 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.3826 | 0.1333 | 41.7178 | 2021 | 3911 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 34.3228 | 1761 | 3197 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.5500 | 0.2500 | 27.1537 | 1687 | 2458 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 49.9067 | 2027 | 4106 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1176 | 52.8043 | 1650 | 4170 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 30.6241 | 1758 | 2678 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.4066 | 0.1667 | 33.7433 | 1574 | 2640 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.5000 | 0.1904 | 40.4020 | 1760 | 3330 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.3636 | 15.5076 | 1532 | 1119 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.5000 | 0.2222 | 46.7416 | 1858 | 3757 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.3357 | 0.1250 | 33.5107 | 1699 | 2672 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1052 | 34.8592 | 2134 | 3097 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3230 | 0.1052 | 38.7719 | 1821 | 3474 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7987 | 0.3333 | 30.0705 | 2206 | 2491 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.1904 | 24.7859 | 1978 | 2269 | — |

- scored rows: 50/50; min=0.1966 max=0.9250 mean=0.5022

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 50 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T052606Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T052606Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T052606Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T052606Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T052606Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-50-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
