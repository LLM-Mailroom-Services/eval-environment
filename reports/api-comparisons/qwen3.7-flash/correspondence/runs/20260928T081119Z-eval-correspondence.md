# Run report — `20260928T081119Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T081119Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v4` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 50 docs, seed 42 |
| timestamp | `2026-09-28T08:11:20+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T081119Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:15:27+00:00` |

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
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:11:20+00:00` |
| finished_at | `2026-09-28T08:15:27+00:00` |
| duration_s (wall) | 248.6000 |
| latency_ms_mean | 35461.8 |
| latency_ms_p95 | 47740.1 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5046 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5046** (sd 0.1382, min 0.1662, max 0.9250) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 248.6000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0228** USD |
| cost estimated (roster token rates) | **0.0228** USD |
| cost per document (actual) | 0.0005 USD |
| cost per document (estimated) | 0.0005 USD |
| latency e2e / p50 / p95 / max | 248.6000 / 36.0804 / 47.7401 / 49.0295 s |
| prompt / completion / total tokens | 110235 / 149707 / 259942 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1773.1 s vs wall = 248.6 s -> wall/serial factor 7.13x at concurrency 8.

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
| `correspondence_specialist` | 50 | 110235 | 149707 | 259942 | 0.0228 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1773.1 s over wall 248.6 s = **7.13×** effective parallelism at c8 (89% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:sanders-r/sent_items/261.` (notice) 49.0 s = 20% of wall — p95/p50 = 1.32×.
- **Prompt length vs latency:** Pearson r = 0.29 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 2994 tok/doc, mean prompt 2205 tok/doc.
- **Subclass spread:** best `meeting_request` 0.779 (n=2), worst `letter` 0.445 (n=6).
- **Field-level extraction:** 2/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 27 | 0.4788 |
| notice | 7 | 0.5240 |
| letter | 6 | 0.4449 |
| memo | 4 | 0.5894 |
| press_release | 4 | 0.5121 |
| meeting_request | 2 | 0.7792 |
| **total** | **50** | **0.5046** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1333 | 32.9389 | 1642 | 2817 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 42.4494 | 1604 | 3622 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 39.2094 | 6101 | 3667 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2222 | 33.0928 | 1667 | 2802 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 36.1099 | 2031 | 3000 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.6111 | 0.1904 | 49.0295 | 1929 | 3963 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 31.3045 | 1782 | 2628 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 28.0326 | 2601 | 2434 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.3322 | 0.2500 | 21.3141 | 1569 | 1680 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5278 | 0.2105 | 25.8716 | 2579 | 2127 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.5625 | 0.2000 | 40.0290 | 1955 | 3414 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 29.9657 | 1564 | 2469 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 30.9336 | 1978 | 2749 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 45.3856 | 1874 | 3776 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.2874 | 0.0000 | 46.0935 | 1969 | 3767 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2105 | 25.2560 | 1710 | 2093 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.2857 | 26.2371 | 1570 | 1984 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.6333 | 0.2353 | 48.2217 | 10072 | 3743 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4798 | 0.1250 | 36.0804 | 2141 | 2992 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1333 | 27.7013 | 1575 | 2308 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5500 | 0.2222 | 32.8973 | 2022 | 2571 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5542 | 0.1111 | 38.3982 | 1861 | 3521 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.9250 | 0.3529 | 36.1277 | 1749 | 3475 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5227 | 0.1904 | 38.6680 | 2191 | 3341 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.3864 | 0.2222 | 22.8240 | 1560 | 1673 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2222 | 36.5499 | 1822 | 3342 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1052 | 43.3058 | 1848 | 3767 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 39.6981 | 2814 | 3164 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.6136 | 0.2105 | 37.6016 | 5134 | 2995 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.8750 | 0.4000 | 38.8558 | 1850 | 3314 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.3674 | 0.1052 | 35.1855 | 1845 | 2989 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.4702 | 0.1176 | 31.4099 | 1728 | 2559 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1662 | 0.0000 | 47.7401 | 1880 | 4034 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.4825 | 0.1111 | 40.5955 | 1976 | 3238 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.4618 | 0.1250 | 28.4155 | 2126 | 2329 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.3826 | 0.1333 | 43.8791 | 2051 | 3918 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 33.1000 | 1791 | 2871 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.3609 | 0.1333 | 38.5818 | 1717 | 3445 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 45.8763 | 2057 | 3974 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1176 | 42.8480 | 1680 | 3778 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 30.1299 | 1788 | 2462 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.4066 | 0.1667 | 32.9702 | 1604 | 2859 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.5000 | 0.2222 | 33.6707 | 1790 | 2979 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.4000 | 22.5259 | 1562 | 1895 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.3672 | 0.1176 | 45.4275 | 1888 | 3385 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.5000 | 0.2353 | 30.6164 | 1729 | 2653 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1176 | 32.7115 | 2164 | 2839 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3230 | 0.1052 | 36.1698 | 1851 | 3118 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7987 | 0.3333 | 26.1911 | 2236 | 2162 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.1904 | 34.8612 | 2008 | 3022 | — |

- scored rows: 50/50; min=0.1662 max=0.9250 mean=0.5046

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 50 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T081119Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T081119Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T081119Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T081119Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T081119Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-50-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
