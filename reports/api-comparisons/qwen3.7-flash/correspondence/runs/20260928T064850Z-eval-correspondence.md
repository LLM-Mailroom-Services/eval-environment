# Run report — `20260928T064850Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T064850Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v3` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 50 docs, seed 42 |
| timestamp | `2026-09-28T06:48:50+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T064850Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T06:53:08+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T064850Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T06:48:50+00:00` |
| finished_at | `2026-09-28T06:53:08+00:00` |
| duration_s (wall) | 259.7000 |
| latency_ms_mean | 35531.8 |
| latency_ms_p95 | 48428.9 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5087 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5087** (sd 0.1353, min 0.1662, max 0.8750) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 259.7000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0220** USD |
| cost estimated (roster token rates) | **0.0220** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 259.7000 / 35.2498 / 48.4289 / 59.6505 s |
| prompt / completion / total tokens | 110785 / 143770 / 254555 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1776.6 s vs wall = 259.7 s -> wall/serial factor 6.84x at concurrency 8.

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
| `correspondence_specialist` | 50 | 110785 | 143770 | 254555 | 0.0220 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1776.6 s over wall 259.7 s = **6.84×** effective parallelism at c8 (86% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:donoho-l/inbox/35.` (email) 59.7 s = 23% of wall — p95/p50 = 1.37×.
- **Prompt length vs latency:** Pearson r = 0.12 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 2875 tok/doc, mean prompt 2216 tok/doc.
- **Subclass spread:** best `meeting_request` 0.729 (n=2), worst `letter` 0.468 (n=6).
- **Field-level extraction:** 2/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 27 | 0.4797 |
| notice | 7 | 0.4811 |
| letter | 6 | 0.4681 |
| memo | 4 | 0.6152 |
| press_release | 4 | 0.5970 |
| meeting_request | 2 | 0.7291 |
| **total** | **50** | **0.5087** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1429 | 38.3597 | 1653 | 3004 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 34.9971 | 1615 | 2643 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 35.5197 | 6112 | 2754 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2666 | 35.9534 | 1678 | 2641 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 36.5828 | 2042 | 2758 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.5833 | 0.1904 | 40.5622 | 1940 | 3123 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 38.9112 | 1793 | 3069 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 32.2517 | 2612 | 2556 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.3322 | 0.2500 | 27.8695 | 1580 | 1972 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5278 | 0.2105 | 38.2110 | 2590 | 3248 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.5625 | 0.2000 | 35.2977 | 1966 | 2989 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 30.2563 | 1575 | 2074 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 30.0527 | 1989 | 2545 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 59.6505 | 1885 | 5117 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.6269 | 0.2105 | 48.4289 | 1980 | 4315 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2105 | 31.7913 | 1721 | 2354 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3077 | 22.8737 | 1581 | 1941 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.5833 | 0.2105 | 43.3504 | 10083 | 3201 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5020 | 0.1250 | 34.9481 | 2152 | 2889 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1429 | 29.6385 | 1586 | 2486 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5500 | 0.2222 | 46.8059 | 2033 | 3840 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5542 | 0.1111 | 37.8940 | 1872 | 2760 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.8250 | 0.2353 | 31.0202 | 1760 | 2713 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5000 | 0.1904 | 43.8794 | 2202 | 3799 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.3864 | 0.2222 | 25.0962 | 1571 | 1678 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2222 | 22.2007 | 1833 | 2030 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1052 | 32.0960 | 1859 | 2741 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 40.1961 | 2825 | 3122 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.6136 | 0.2105 | 27.0814 | 5145 | 2359 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.8750 | 0.4000 | 35.2492 | 1861 | 2911 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.3674 | 0.1052 | 32.6159 | 1856 | 2815 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.3868 | 0.1176 | 26.8606 | 1739 | 2129 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1662 | 0.0000 | 40.6493 | 1891 | 2968 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.5857 | 0.2000 | 37.5433 | 1987 | 3367 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.4118 | 0.1176 | 33.9568 | 2137 | 2493 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.5417 | 0.2500 | 36.3754 | 2062 | 3389 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 28.2504 | 1802 | 2213 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.5000 | 0.2353 | 32.0124 | 1728 | 2804 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 39.1571 | 2068 | 3407 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1176 | 31.5308 | 1691 | 2932 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 39.8216 | 1799 | 3121 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.1840 | 0.0000 | 43.2568 | 1615 | 3025 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.5000 | 0.2105 | 37.1089 | 1801 | 2875 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.3636 | 19.9549 | 1573 | 1650 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.3672 | 0.1176 | 46.5672 | 1899 | 3589 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.5000 | 0.2222 | 35.2498 | 1740 | 2638 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1111 | 33.9516 | 2175 | 2909 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3231 | 0.1052 | 56.2733 | 1862 | 4487 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7987 | 0.3333 | 26.4454 | 2247 | 2335 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.1904 | 31.9826 | 2019 | 2992 | — |

- scored rows: 50/50; min=0.1662 max=0.8750 mean=0.5087

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 50 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T064850Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T064850Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T064850Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T064850Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T064850Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-50-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
