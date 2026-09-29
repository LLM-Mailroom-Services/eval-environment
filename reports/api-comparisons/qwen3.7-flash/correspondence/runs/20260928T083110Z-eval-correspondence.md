# Run report — `20260928T083110Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T083110Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v5` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 50 docs, seed 42 |
| timestamp | `2026-09-28T08:31:10+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T083110Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T08:36:19+00:00` |

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
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260928T083110Z-eval-correspondence', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T08:31:10+00:00` |
| finished_at | `2026-09-28T08:36:19+00:00` |
| duration_s (wall) | 309.7000 |
| latency_ms_mean | 34288.1 |
| latency_ms_p95 | 45787.8 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **50 / 50** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5094 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5094** (sd 0.1410, min 0.1662, max 0.9250) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 309.7000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0221** USD |
| cost estimated (roster token rates) | **0.0221** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 309.7000 / 34.2475 / 45.7878 / 51.9408 s |
| prompt / completion / total tokens | 111485 / 144509 / 255994 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1714.4 s vs wall = 309.7 s -> wall/serial factor 5.54x at concurrency 8.

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
| `correspondence_specialist` | 50 | 111485 | 144509 | 255994 | 0.0221 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 1714.4 s over wall 309.7 s = **5.54×** effective parallelism at c8 (69% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:kitchen-l/sent_items/613.` (press_release) 51.9 s = 17% of wall — p95/p50 = 1.34×.
- **Prompt length vs latency:** Pearson r = 0.18 across 50 docs (not prefill-dominated).
- **Decode budget:** mean completion 2890 tok/doc, mean prompt 2230 tok/doc.
- **Subclass spread:** best `meeting_request` 0.779 (n=2), worst `letter` 0.473 (n=6).
- **Field-level extraction:** 3/50 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 27 | 0.4882 |
| notice | 7 | 0.4990 |
| letter | 6 | 0.4726 |
| memo | 4 | 0.5805 |
| press_release | 4 | 0.5191 |
| meeting_request | 2 | 0.7792 |
| **total** | **50** | **0.5094** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1250 | 34.6518 | 1667 | 2866 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 36.8060 | 1629 | 3101 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 38.6549 | 6126 | 3213 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2666 | 25.7940 | 1692 | 2241 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4354 | 0.1000 | 33.0168 | 2056 | 2745 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 30.9819 | 1954 | 2656 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 34.2773 | 1807 | 2870 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 27.2260 | 2626 | 2461 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.5000 | 0.4444 | 20.7816 | 1594 | 1623 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5555 | 0.2105 | 37.4251 | 2604 | 3208 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.6125 | 0.2105 | 42.2000 | 1980 | 3235 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 27.5367 | 1589 | 2099 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 26.7104 | 2003 | 2276 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 42.5568 | 1899 | 3367 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.2874 | 0.0000 | 51.9408 | 1994 | 4443 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5750 | 0.2105 | 27.1458 | 1735 | 2201 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3077 | 24.4732 | 1595 | 2057 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.6333 | 0.2222 | 38.9872 | 10097 | 3328 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5298 | 0.1333 | 34.5832 | 2166 | 2845 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1539 | 26.5753 | 1600 | 2091 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5500 | 0.2222 | 28.2016 | 2047 | 2568 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5542 | 0.1111 | 32.5547 | 1886 | 2822 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.9250 | 0.3529 | 35.1664 | 1774 | 3148 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5227 | 0.1904 | 36.7023 | 2216 | 2983 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.2500 | 0.2500 | 21.7175 | 1585 | 1524 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2666 | 29.0901 | 1847 | 2386 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1052 | 48.9389 | 1873 | 4129 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 44.6254 | 2839 | 3955 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.6136 | 0.2105 | 34.2475 | 5159 | 2786 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.8750 | 0.4000 | 29.0655 | 1875 | 2680 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.5417 | 0.2000 | 36.7954 | 1870 | 2989 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.4702 | 0.1176 | 29.0734 | 1753 | 2424 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1662 | 0.0000 | 44.7746 | 1905 | 3499 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.5857 | 0.2000 | 45.5956 | 2001 | 3706 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.4118 | 0.1250 | 30.3892 | 2151 | 2438 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.3826 | 0.1250 | 41.3910 | 2076 | 3606 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 34.1483 | 1816 | 2983 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.5000 | 0.2353 | 33.4506 | 1742 | 2871 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 45.7878 | 2082 | 3874 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1176 | 38.5100 | 1705 | 3184 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 29.2828 | 1813 | 2537 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.4066 | 0.1667 | 35.3451 | 1629 | 2853 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.3611 | 0.1000 | 33.4841 | 1815 | 3045 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.4000 | 22.8139 | 1587 | 1951 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.5000 | 0.2353 | 42.5716 | 1913 | 3671 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.5000 | 0.2222 | 23.4921 | 1754 | 2037 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1176 | 40.3433 | 2189 | 3519 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3230 | 0.1052 | 45.0318 | 1876 | 4284 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7987 | 0.3333 | 25.5996 | 2261 | 2199 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.1904 | 33.8896 | 2033 | 2932 | — |

- scored rows: 50/50; min=0.1662 max=0.9250 mean=0.5094

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 50 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T083110Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T083110Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T083110Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T083110Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T083110Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-50-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
