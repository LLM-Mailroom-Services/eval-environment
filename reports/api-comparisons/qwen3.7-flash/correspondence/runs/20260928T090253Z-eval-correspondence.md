# Run report — `20260928T090253Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T090253Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v6` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 50 docs, seed 42 |
| timestamp | `2026-09-28T09:02:53+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T090253Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T09:08:14+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T090253Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T09:02:53+00:00` |
| finished_at | `2026-09-28T09:08:14+00:00` |
| duration_s (wall) | 322.4000 |
| latency_ms_mean | 34139.0 |
| latency_ms_p95 | 44692.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4931 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4931** (sd 0.1520, min 0.0000, max 0.8750) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 322.4000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0225** USD |
| cost estimated (roster token rates) | **0.0225** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 322.4000 / 34.1597 / 44.6924 / 59.6538 s |
| prompt / completion / total tokens | 112385 / 146894 / 259279 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1707.0 s vs wall = 322.4 s -> wall/serial factor 5.29x at concurrency 8.

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
| `correspondence_specialist` | 50 | 112385 | 146894 | 259279 | 0.0225 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1707.0 s over wall 322.4 s = **5.29×** effective parallelism at c8 (66% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:taylor-m/inbox/219.` (memo) 59.7 s = 19% of wall — p95/p50 = 1.31×.
- **Prompt length vs latency:** Pearson r = 0.22 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 2938 tok/doc, mean prompt 2248 tok/doc.
- **Subclass spread:** best `meeting_request` 0.754 (n=2), worst `notice` 0.452 (n=7).
- **Field-level extraction:** 5/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 27 | 0.4722 |
| notice | 7 | 0.4518 |
| letter | 6 | 0.4694 |
| memo | 4 | 0.5924 |
| press_release | 4 | 0.5121 |
| meeting_request | 2 | 0.7541 |
| **total** | **50** | **0.4931** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.3513 | 0.1250 | 33.8551 | 1685 | 3021 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 32.0403 | 1647 | 2734 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 34.9703 | 6144 | 3006 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2222 | 32.5830 | 1710 | 2741 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4475 | 0.1000 | 40.9063 | 2074 | 3364 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 34.4793 | 1972 | 2832 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 31.2477 | 1825 | 2758 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 32.0276 | 2644 | 2714 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.0000 | 0.0000 | 17.0401 | 1612 | 1336 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5278 | 0.2105 | 31.3738 | 2622 | 2356 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.6125 | 0.2105 | 32.3365 | 1998 | 2771 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.3636 | 26.0234 | 1607 | 2158 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 27.9131 | 2021 | 2567 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 40.8448 | 1917 | 3367 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.2874 | 0.0000 | 41.7391 | 2012 | 3551 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2105 | 30.9340 | 1753 | 2751 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3077 | 20.5493 | 1613 | 1685 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.6333 | 0.2353 | 42.0093 | 10115 | 3380 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5020 | 0.1176 | 36.0548 | 2184 | 3114 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1539 | 22.8343 | 1618 | 1869 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5500 | 0.2105 | 34.2647 | 2065 | 2934 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5542 | 0.1111 | 31.1503 | 1904 | 2590 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.8750 | 0.2353 | 43.0178 | 1792 | 3981 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5227 | 0.1904 | 44.6924 | 2234 | 3803 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.3864 | 0.2222 | 24.2389 | 1603 | 1851 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2353 | 32.6646 | 1865 | 2954 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1052 | 40.1955 | 1891 | 3501 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 34.1597 | 2857 | 2619 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.6136 | 0.2000 | 38.2631 | 5177 | 3329 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.7838 | 0.2857 | 31.0282 | 1893 | 2836 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.5417 | 0.2000 | 36.7445 | 1888 | 3449 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.4285 | 0.1176 | 27.6785 | 1771 | 2299 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1662 | 0.0000 | 35.8795 | 1923 | 3229 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.5857 | 0.2000 | 48.1013 | 2019 | 4126 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.4618 | 0.1250 | 39.6322 | 2169 | 3389 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.3826 | 0.1250 | 37.7532 | 2094 | 3753 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 59.6538 | 1834 | 5361 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.5000 | 0.2353 | 27.1557 | 1760 | 2283 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 37.7251 | 2100 | 3108 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1176 | 37.5642 | 1723 | 3154 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 28.9720 | 1831 | 2669 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.4066 | 0.1667 | 35.1785 | 1647 | 2758 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.5000 | 0.2222 | 28.8793 | 1833 | 2605 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.4000 | 22.1005 | 1605 | 1665 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.1946 | 0.0000 | 41.5801 | 1931 | 3515 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.5000 | 0.2222 | 27.8653 | 1772 | 2484 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1052 | 40.8855 | 2207 | 3652 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3230 | 0.1052 | 36.4923 | 1894 | 3273 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7675 | 0.3077 | 27.7137 | 2279 | 2430 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.1904 | 33.9584 | 2051 | 3219 | — |

- scored rows: 50/50; min=0.0000 max=0.8750 mean=0.4931

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 50 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T090253Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T090253Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T090253Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T090253Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T090253Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-50-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
