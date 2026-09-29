# Run report — `20260928T072519Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T072519Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 100 docs, seed 42 |
| timestamp | `2026-09-28T07:25:19+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T072519Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T07:33:55+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / agent |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 100 / None |
| scorer | extraction |
| decode profile | — |
| prompt source / lineage | frozen / frozen |
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T07:25:19+00:00` |
| finished_at | `2026-09-28T07:33:55+00:00` |
| duration_s (wall) | 517.5000 |
| latency_ms_mean | 37895.7 |
| latency_ms_p95 | 51209.7 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **100 / 100** (`errors=0`) |
| errors | 0 |
| overall_score | 0.5081 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.5081** (sd 0.1341, min 0.1662, max 0.9250) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 517.5000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0434** USD |
| cost estimated (roster token rates) | **0.0433** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 517.5000 / 37.3321 / 51.2097 / 86.9111 s |
| prompt / completion / total tokens | 209458 / 285111 / 494569 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 3789.6 s vs wall = 517.5 s -> wall/serial factor 7.32x at concurrency 8.

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
| `correspondence_specialist` | 100 | 209458 | 285111 | 494569 | 0.0433 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 3789.6 s over wall 517.5 s = **7.32×** effective parallelism at c8 (92% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:dasovich-j/all_documents/10430.` (email) 86.9 s = 17% of wall — p95/p50 = 1.37×.
- **Prompt length vs latency:** Pearson r = 0.27 across 100 docs (not prefill-dominated).
- **Decode budget:** mean completion 2851 tok/doc, mean prompt 2095 tok/doc.
- **Subclass spread:** best `attorney_demand` 0.844 (n=1), worst `notice` 0.461 (n=13).
- **Field-level extraction:** 4/100 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 60 | 0.4833 |
| notice | 13 | 0.4613 |
| letter | 8 | 0.4774 |
| press_release | 7 | 0.5651 |
| memo | 6 | 0.6344 |
| meeting_request | 4 | 0.6901 |
| attorney_demand | 1 | 0.8438 |
| demand | 1 | 0.6280 |
| **total** | **100** | **0.5081** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1250 | 32.8630 | 1612 | 2940 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 34.9219 | 1574 | 2494 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1052 | 39.5669 | 6071 | 3358 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2222 | 29.1492 | 1637 | 2424 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 41.6420 | 2001 | 3073 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 43.5405 | 1899 | 3881 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 40.0769 | 1752 | 2789 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 52.1273 | 2571 | 4317 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.3322 | 0.2500 | 25.0044 | 1539 | 2079 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5278 | 0.2105 | 21.4115 | 2549 | 1877 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.6125 | 0.2105 | 38.7515 | 1925 | 3018 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 22.8762 | 1534 | 1790 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 30.2420 | 1948 | 2294 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 45.6897 | 1844 | 3443 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.6654 | 0.2105 | 48.6423 | 1939 | 3838 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2222 | 29.0101 | 1680 | 2520 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.3077 | 18.2953 | 1540 | 1476 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.5833 | 0.2222 | 50.9546 | 10042 | 3814 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.4520 | 0.1333 | 33.1312 | 2111 | 2870 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1539 | 26.2452 | 1545 | 2175 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5500 | 0.2222 | 35.8159 | 1992 | 3029 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5542 | 0.1176 | 33.6764 | 1831 | 2615 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.9250 | 0.3529 | 28.0820 | 1719 | 2502 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5227 | 0.1904 | 45.8846 | 2161 | 3471 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.3864 | 0.2500 | 20.0582 | 1530 | 1609 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2222 | 27.5024 | 1792 | 2287 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1052 | 47.7042 | 1818 | 4000 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 37.2121 | 2784 | 2870 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.5454 | 0.1904 | 25.5977 | 5104 | 2119 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.6924 | 0.2857 | 37.5209 | 1820 | 2963 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.5417 | 0.2222 | 35.9229 | 1815 | 2935 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.4702 | 0.1176 | 30.5192 | 1698 | 2275 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1662 | 0.0000 | 38.9442 | 1850 | 3025 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.6214 | 0.2000 | 48.9333 | 1946 | 3789 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.4118 | 0.1176 | 33.4776 | 2096 | 2564 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.3826 | 0.1333 | 42.6409 | 2021 | 3410 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 29.7135 | 1761 | 2521 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.5000 | 0.2353 | 30.4531 | 1687 | 2266 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 37.3321 | 2027 | 3152 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1250 | 49.2638 | 1650 | 3630 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 38.0484 | 1758 | 3142 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.4066 | 0.1667 | 40.7686 | 1574 | 2852 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.5000 | 0.2000 | 36.9814 | 1760 | 2957 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.3636 | 27.9002 | 1532 | 1947 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.3672 | 0.1111 | 44.1158 | 1858 | 2975 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.5000 | 0.2222 | 32.9889 | 1699 | 2558 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1111 | 48.5019 | 2134 | 3497 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3230 | 0.1052 | 45.9028 | 1821 | 3665 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7675 | 0.3077 | 36.5184 | 2206 | 2695 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.1904 | 31.4446 | 1978 | 2395 | — |
| 51 | `corpus:ground_truth:train:fischer-m/all_documents/427.` | meeting_request | 0.6345 | 0.1818 | 41.6551 | 2278 | 2867 | — |
| 52 | `corpus:ground_truth:train:hendrickson-s/all_documents/64.` | email | 0.3909 | 0.1333 | 37.4222 | 1677 | 2742 | — |
| 53 | `corpus:ground_truth:train:nemec-g/all_documents/4395.` | email | 0.4857 | 0.1176 | 35.0316 | 1709 | 2680 | — |
| 54 | `corpus:ground_truth:train:ward-k/deleted_items/173.` | email | 0.3617 | 0.1111 | 40.7594 | 6314 | 3034 | — |
| 55 | `corpus:ground_truth:train:shapiro-r/ferc/1.` | email | 0.6500 | 0.2500 | 35.1527 | 1719 | 2524 | — |
| 56 | `corpus:ground_truth:train:haedicke-m/all_documents/2470.` | email | 0.3982 | 0.1333 | 31.2189 | 1626 | 2280 | — |
| 57 | `corpus:ground_truth:train:perlingiere-d/deleted_items/191.` | notice | 0.1946 | 0.0000 | 41.5045 | 2451 | 3326 | — |
| 58 | `corpus:ground_truth:train:kaminski-v/deleted_items/717.` | notice | 0.3643 | 0.1052 | 33.7951 | 1701 | 2571 | — |
| 59 | `corpus:ground_truth:train:arnold-j/sent_items/498.` | email | 0.3409 | 0.1250 | 35.2478 | 2140 | 2501 | — |
| 60 | `corpus:ground_truth:train:mckay-j/sent_items/190.` | email | 0.5500 | 0.2222 | 30.7822 | 1601 | 2260 | — |
| 61 | `corpus:ground_truth:train:tholt-j/janie/104.` | email | 0.4123 | 0.1333 | 32.3712 | 1656 | 2376 | — |
| 62 | `corpus:ground_truth:train:kitchen-l/_americas/netco_hr/18.` | email | 0.3982 | 0.1111 | 35.4970 | 1926 | 2240 | — |
| 63 | `corpus:ground_truth:train:kaminski-v/all_documents/842.` | email | 0.6000 | 0.2105 | 30.5335 | 1649 | 2065 | — |
| 64 | `corpus:ground_truth:train:haedicke-m/all_documents/2298.` | email | 0.4605 | 0.1052 | 49.5289 | 2087 | 3612 | — |
| 65 | `corpus:ground_truth:train:presto-k/sent_items/153.` | email | 0.4346 | 0.1429 | 37.1073 | 1597 | 2748 | — |
| 66 | `corpus:ground_truth:train:tholt-j/deleted_items/205.` | press_release | 0.5500 | 0.2353 | 43.1480 | 1908 | 3115 | — |
| 67 | `corpus:ground_truth:train:quenet-j/inbox/15.` | email | 0.4794 | 0.1176 | 42.0609 | 1823 | 2754 | — |
| 68 | `corpus:ground_truth:train:skilling-j/all_documents/141.` | email | 0.3409 | 0.1429 | 30.7433 | 1550 | 1838 | — |
| 69 | `corpus:ground_truth:train:keiser-k/deleted_items/247.` | email | 0.4607 | 0.1000 | 50.5618 | 2234 | 3381 | — |
| 70 | `corpus:ground_truth:train:kaminski-v/all_documents/2111.` | email | 0.4721 | 0.1052 | 42.3115 | 1867 | 3127 | — |
| 71 | `corpus:ground_truth:train:germany-c/inbox/167.` | notice | 0.5500 | 0.2222 | 37.7587 | 1961 | 2664 | — |
| 72 | `corpus:ground_truth:train:kaminski-v/all_documents/6051.` | email | 0.3349 | 0.1000 | 36.9901 | 1754 | 2632 | — |
| 73 | `corpus:ground_truth:train:skilling-j/all_documents/507.` | email | 0.4118 | 0.1333 | 42.8898 | 2246 | 2923 | — |
| 74 | `corpus:ground_truth:train:sanders-r/px/17.` | attorney_demand | 0.8438 | 0.3077 | 43.9304 | 1915 | 3184 | — |
| 75 | `corpus:ground_truth:train:benson-r/sent_items/14.` | meeting_request | 0.5676 | 0.1818 | 42.0786 | 1713 | 2695 | — |
| 76 | `corpus:ground_truth:train:neal-s/_sent_mail/356.` | email | 0.7000 | 0.2353 | 52.1519 | 1872 | 3560 | — |
| 77 | `corpus:ground_truth:train:shackleton-s/all_documents/11016.` | memo | 0.8428 | 0.2353 | 32.8736 | 1761 | 2391 | — |
| 78 | `corpus:ground_truth:train:kaminski-v/deleted_items/806.` | email | 0.5417 | 0.1904 | 32.8551 | 2262 | 2371 | — |
| 79 | `corpus:ground_truth:train:nemec-g/all_documents/4346.` | email | 0.5417 | 0.2666 | 31.1340 | 1562 | 2191 | — |
| 80 | `corpus:ground_truth:train:mcconnell-m/_sent_mail/217.` | email | 0.5000 | 0.1904 | 34.1785 | 1730 | 2532 | — |
| 81 | `corpus:ground_truth:train:rodrique-r/_sent_mail/166.` | email | 0.5000 | 0.3333 | 27.8987 | 1533 | 1854 | — |
| 82 | `corpus:ground_truth:train:kitchen-l/_americas/rac/10.` | email | 0.5000 | 0.4444 | 21.4581 | 1545 | 1364 | — |
| 83 | `corpus:ground_truth:train:campbell-l/all_documents/1428.` | notice | 0.7247 | 0.1667 | 28.9340 | 1647 | 2043 | — |
| 84 | `corpus:ground_truth:train:shapiro-r/federal_legis_/66.` | email | 0.4828 | 0.1052 | 49.9399 | 2284 | 3535 | — |
| 85 | `corpus:ground_truth:train:mcconnell-m/_sent_mail/151.` | email | 0.5938 | 0.1904 | 42.6972 | 2324 | 3069 | — |
| 86 | `corpus:ground_truth:train:horton-s/all_documents/85.` | letter | 0.4637 | 0.1052 | 31.1085 | 1656 | 2288 | — |
| 87 | `corpus:ground_truth:train:campbell-l/sent_items/19.` | email | 0.4294 | 0.1000 | 44.0186 | 1708 | 3153 | — |
| 88 | `corpus:ground_truth:train:germany-c/inbox/237.` | notice | 0.6333 | 0.2222 | 33.4020 | 1663 | 2440 | — |
| 89 | `corpus:ground_truth:train:presto-k/deleted_items/1350.` | notice | 0.2446 | 0.0000 | 52.7370 | 1610 | 3735 | — |
| 90 | `corpus:ground_truth:train:dasovich-j/all_documents/10430.` | email | 0.5000 | 0.2000 | 86.9111 | 3901 | 7711 | — |
| 91 | `corpus:ground_truth:train:shankman-j/deleted_items/671.` | email | 0.4527 | 0.1052 | 52.9641 | 2259 | 3635 | — |
| 92 | `corpus:ground_truth:train:schwieger-j/sent_items/159.` | email | 0.5682 | 0.1904 | 42.1243 | 1736 | 2946 | — |
| 93 | `corpus:ground_truth:train:fossum-d/_sent_mail/1317.` | email | 0.8571 | 0.4000 | 51.2097 | 2758 | 3728 | — |
| 94 | `corpus:ground_truth:train:kean-s/all_documents/2264.` | press_release | 0.6167 | 0.2353 | 38.2117 | 1816 | 2849 | — |
| 95 | `corpus:ground_truth:train:mann-k/_sent_mail/3628.` | email | 0.5000 | 0.2857 | 26.7416 | 1554 | 1899 | — |
| 96 | `corpus:ground_truth:train:mann-k/all_documents/5748.` | email | 0.3409 | 0.1176 | 38.1772 | 1642 | 2560 | — |
| 97 | `corpus:ground_truth:train:ring-r/eesirenewableenergy/13.` | demand | 0.6280 | 0.1333 | 48.2656 | 1764 | 3829 | — |
| 98 | `corpus:ground_truth:train:lay-k/inbox/286.` | press_release | 0.3625 | 0.1818 | 40.3889 | 1572 | 3052 | — |
| 99 | `corpus:ground_truth:train:jones-t/all_documents/4429.` | memo | 0.6500 | 0.1904 | 40.1571 | 3581 | 3010 | — |
| 100 | `corpus:ground_truth:train:ruscitti-k/deleted_items/88.` | letter | 0.5278 | 0.2000 | 45.3877 | 1881 | 3042 | — |

- scored rows: 100/100; min=0.1662 max=0.9250 mean=0.5081

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 100 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T072519Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T072519Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T072519Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T072519Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T072519Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-100-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
