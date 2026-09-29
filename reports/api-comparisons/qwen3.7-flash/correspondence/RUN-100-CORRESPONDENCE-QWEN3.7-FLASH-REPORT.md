# Run report — `20260928T073402Z-eval-correspondence` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260928T073402Z-eval-correspondence` |
| task / agent | `correspondence` |
| prompt | `correspondence_specialist_v2` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `class:correspondence` — 100 docs, seed 42 |
| timestamp | `2026-09-28T07:34:02+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260928T073402Z-eval-correspondence/subset_manifest.json` |
| eval git | `—` |
| finished | `2026-09-28T07:42:34+00:00` |

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
| prompt source / lineage | frozen / mutation |
| trace backend | none |
| resumed_from | — |
| dry_run | False |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-28T07:34:02+00:00` |
| finished_at | `2026-09-28T07:42:34+00:00` |
| duration_s (wall) | 513.5000 |
| latency_ms_mean | 37104.3 |
| latency_ms_p95 | 48655.6 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **100 / 100** (`errors=0`) |
| errors | 0 |
| overall_score | 0.4996 |
| scorer_errors | 0 |
| thinking_recovered (stripped + re-scored) | 0 |
| overall (per-doc) | **0.4996** (sd 0.1382, min 0.1662, max 0.8750) |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 513.5000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0445** USD |
| cost estimated (roster token rates) | **0.0445** USD |
| cost per document (actual) | 0.0004 USD |
| cost per document (estimated) | 0.0004 USD |
| latency e2e / p50 / p95 / max | 513.5000 / 37.1695 / 48.6556 / 56.8776 s |
| prompt / completion / total tokens | 212494 / 293565 / 506059 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 3710.4 s vs wall = 513.5 s -> wall/serial factor 7.23x at concurrency 8.

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
| `correspondence_specialist` | 100 | 212494 | 293565 | 506059 | 0.0445 | qwen/qwen3.7-flash |

## Analyst insights & findings

- **Concurrency efficiency:** Σ latency 3710.4 s over wall 513.5 s = **7.23×** effective parallelism at c8 (90% of the ideal 8×).
- **Tail:** slowest doc `corpus:ground_truth:train:farmer-d/all_documents/2959.` (email) 56.9 s = 11% of wall — p95/p50 = 1.31×.
- **Prompt length vs latency:** Pearson r = 0.20 across 100 docs (not prefill-dominated).
- **Decode budget:** mean completion 2936 tok/doc, mean prompt 2125 tok/doc.
- **Subclass spread:** best `meeting_request` 0.683 (n=4), worst `notice` 0.467 (n=13).
- **Field-level extraction:** 4/100 docs have extraction F1 = 0 — when non-zero overall scores still appear, entity/structure components may carry the headline.

## Figures

Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the **table views**: **Strata (subclass)** and **Per-document scores** below.

## Strata (subclass)

| subclass | n | mean overall |
| --- | ---: | ---: |
| email | 60 | 0.4716 |
| notice | 13 | 0.4673 |
| letter | 8 | 0.4707 |
| press_release | 7 | 0.5714 |
| memo | 6 | 0.6381 |
| meeting_request | 4 | 0.6825 |
| attorney_demand | 1 | 0.6378 |
| demand | 1 | 0.6280 |
| **total** | **100** | **0.4996** |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:blair-l/meetings/608.` | email | 0.4013 | 0.1176 | 27.4901 | 1642 | 2063 | — |
| 2 | `corpus:ground_truth:train:lokey-t/inbox/250.` | press_release | 0.5500 | 0.2857 | 35.8342 | 1604 | 2820 | — |
| 3 | `corpus:ground_truth:train:kean-s/all_documents/849.` | email | 0.4118 | 0.1111 | 43.0884 | 6101 | 3383 | — |
| 4 | `corpus:ground_truth:train:may-l/all_documents/41.` | email | 0.5833 | 0.2666 | 38.3920 | 1667 | 2845 | — |
| 5 | `corpus:ground_truth:train:skilling-j/inbox/1555.` | letter | 0.4582 | 0.1000 | 30.7612 | 2031 | 2455 | — |
| 6 | `corpus:ground_truth:train:sanders-r/sent_items/261.` | notice | 0.2780 | 0.0000 | 43.2694 | 1929 | 3352 | — |
| 7 | `corpus:ground_truth:train:mcconnell-m/all_documents/227.` | email | 0.5000 | 0.1904 | 45.6280 | 1782 | 3906 | — |
| 8 | `corpus:ground_truth:train:thomas-p/deleted_items/292.` | press_release | 0.6833 | 0.2222 | 32.5456 | 2601 | 2592 | — |
| 9 | `corpus:ground_truth:train:nemec-g/all_documents/906.` | email | 0.3322 | 0.2500 | 33.9180 | 1569 | 2126 | — |
| 10 | `corpus:ground_truth:train:dasovich-j/all_documents/13056.` | press_release | 0.5555 | 0.2105 | 31.8566 | 2579 | 2350 | — |
| 11 | `corpus:ground_truth:train:kaminski-v/all_documents/5470.` | letter | 0.6125 | 0.2105 | 44.7594 | 1955 | 3075 | — |
| 12 | `corpus:ground_truth:train:parks-j/sent_items/425.` | email | 0.5000 | 0.4000 | 26.7162 | 1564 | 1724 | — |
| 13 | `corpus:ground_truth:train:campbell-l/inbox/81.` | meeting_request | 0.6333 | 0.2105 | 41.0407 | 1978 | 3101 | — |
| 14 | `corpus:ground_truth:train:donoho-l/inbox/35.` | email | 0.6572 | 0.1904 | 48.3760 | 1874 | 3696 | — |
| 15 | `corpus:ground_truth:train:kitchen-l/sent_items/613.` | press_release | 0.6654 | 0.2105 | 54.8082 | 1969 | 4477 | — |
| 16 | `corpus:ground_truth:train:derrick-j/deleted_items/79.` | notice | 0.5500 | 0.2105 | 27.5721 | 1710 | 2194 | — |
| 17 | `corpus:ground_truth:train:rogers-b/_sent_mail/358.` | email | 0.5000 | 0.2857 | 24.0465 | 1570 | 1749 | — |
| 18 | `corpus:ground_truth:train:dasovich-j/all_documents/10751.` | notice | 0.6333 | 0.2222 | 42.6012 | 10072 | 3095 | — |
| 19 | `corpus:ground_truth:train:motley-m/deleted_items/63.` | email | 0.5020 | 0.1250 | 40.7308 | 2141 | 3092 | — |
| 20 | `corpus:ground_truth:train:dorland-c/_sent_mail/78.` | email | 0.3409 | 0.1539 | 37.5985 | 1575 | 2680 | — |
| 21 | `corpus:ground_truth:train:campbell-l/inbox/488.` | notice | 0.5500 | 0.2222 | 36.7438 | 2022 | 2616 | — |
| 22 | `corpus:ground_truth:train:lay-k/deleted_items/67.` | email | 0.5041 | 0.1052 | 43.8886 | 1861 | 3388 | — |
| 23 | `corpus:ground_truth:train:shackleton-s/all_documents/4886.` | meeting_request | 0.8750 | 0.2353 | 41.9045 | 1749 | 3556 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/2959.` | email | 0.5227 | 0.1904 | 56.8776 | 2191 | 4561 | — |
| 25 | `corpus:ground_truth:train:jones-t/inbox/61.` | email | 0.2500 | 0.2500 | 27.6907 | 1560 | 1706 | — |
| 26 | `corpus:ground_truth:train:holst-k/inbox/99.` | notice | 0.5500 | 0.2222 | 37.1695 | 1822 | 3064 | — |
| 27 | `corpus:ground_truth:train:skilling-j/inbox/31.` | email | 0.4071 | 0.1052 | 39.0312 | 1848 | 3205 | — |
| 28 | `corpus:ground_truth:train:kaminski-v/_sent_mail/1015.` | email | 0.5000 | 0.1904 | 48.2649 | 2814 | 3629 | — |
| 29 | `corpus:ground_truth:train:hendrickson-s/deleted_items/120.` | email | 0.6136 | 0.2105 | 30.8071 | 5134 | 2482 | — |
| 30 | `corpus:ground_truth:train:hain-m/all_documents/675.` | memo | 0.8670 | 0.2666 | 35.0297 | 1850 | 2867 | — |
| 31 | `corpus:ground_truth:train:jones-t/all_documents/10848.` | email | 0.5417 | 0.2000 | 35.9907 | 1845 | 2918 | — |
| 32 | `corpus:ground_truth:train:cash-m/all_documents/552.` | email | 0.4285 | 0.1176 | 33.2548 | 1728 | 2531 | — |
| 33 | `corpus:ground_truth:train:lewis-a/deleted_items/747.` | letter | 0.1662 | 0.0000 | 47.0378 | 1880 | 3942 | — |
| 34 | `corpus:ground_truth:train:haedicke-m/all_documents/4969.` | memo | 0.5714 | 0.2353 | 44.0643 | 1976 | 3542 | — |
| 35 | `corpus:ground_truth:train:kaminski-v/deleted_items/184.` | email | 0.4118 | 0.1176 | 35.2767 | 2126 | 2844 | — |
| 36 | `corpus:ground_truth:train:schoolcraft-d/deleted_items/689.` | email | 0.3826 | 0.1250 | 42.5675 | 2051 | 3650 | — |
| 37 | `corpus:ground_truth:train:taylor-m/inbox/219.` | memo | 0.5000 | 0.2000 | 36.2579 | 1791 | 3187 | — |
| 38 | `corpus:ground_truth:train:kaminski-v/all_documents/2276.` | letter | 0.5500 | 0.2500 | 26.2286 | 1717 | 2037 | — |
| 39 | `corpus:ground_truth:train:kaminski-v/deleted_items/1330.` | email | 0.5938 | 0.1904 | 41.2244 | 2057 | 3615 | — |
| 40 | `corpus:ground_truth:train:buy-r/inbox/411.` | email | 0.4763 | 0.1176 | 40.2911 | 1680 | 3432 | — |
| 41 | `corpus:ground_truth:train:shankman-j/all_documents/94.` | email | 0.5000 | 0.1904 | 31.6556 | 1788 | 2742 | — |
| 42 | `corpus:ground_truth:train:baughman-d/deleted_items/292.` | notice | 0.4066 | 0.1818 | 27.8373 | 1604 | 1826 | — |
| 43 | `corpus:ground_truth:train:mann-k/_sent_mail/3284.` | memo | 0.5000 | 0.2222 | 40.5571 | 1790 | 2982 | — |
| 44 | `corpus:ground_truth:train:dasovich-j/all_documents/28332.` | email | 0.5278 | 0.3636 | 24.5511 | 1562 | 1853 | — |
| 45 | `corpus:ground_truth:train:rapp-b/inbox/251.` | notice | 0.3672 | 0.1176 | 48.2605 | 1888 | 4005 | — |
| 46 | `corpus:ground_truth:train:smith-m/_sent_mail/70.` | email | 0.5000 | 0.2353 | 32.7039 | 1729 | 2756 | — |
| 47 | `corpus:ground_truth:train:hain-m/all_documents/641.` | email | 0.4127 | 0.1052 | 44.9740 | 2164 | 3362 | — |
| 48 | `corpus:ground_truth:train:skilling-j/inbox/1231.` | letter | 0.3230 | 0.1052 | 42.4639 | 1851 | 3409 | — |
| 49 | `corpus:ground_truth:train:dasovich-j/all_documents/11714.` | letter | 0.7675 | 0.3077 | 31.9235 | 2236 | 2381 | — |
| 50 | `corpus:ground_truth:train:bailey-s/deleted_items/59.` | email | 0.5938 | 0.2000 | 30.7523 | 2014 | 2295 | — |
| 51 | `corpus:ground_truth:train:fischer-m/all_documents/427.` | meeting_request | 0.6033 | 0.1667 | 42.7944 | 2308 | 3341 | — |
| 52 | `corpus:ground_truth:train:hendrickson-s/all_documents/64.` | email | 0.3909 | 0.1667 | 31.9692 | 1707 | 2425 | — |
| 53 | `corpus:ground_truth:train:nemec-g/all_documents/4395.` | email | 0.4857 | 0.1176 | 39.8974 | 1739 | 3225 | — |
| 54 | `corpus:ground_truth:train:ward-k/deleted_items/173.` | email | 0.3617 | 0.1111 | 40.4925 | 6344 | 2816 | — |
| 55 | `corpus:ground_truth:train:shapiro-r/ferc/1.` | email | 0.6500 | 0.2500 | 26.6735 | 1749 | 2203 | — |
| 56 | `corpus:ground_truth:train:haedicke-m/all_documents/2470.` | email | 0.3982 | 0.1333 | 29.6316 | 1656 | 2388 | — |
| 57 | `corpus:ground_truth:train:perlingiere-d/deleted_items/191.` | notice | 0.1946 | 0.0000 | 41.0475 | 2481 | 3156 | — |
| 58 | `corpus:ground_truth:train:kaminski-v/deleted_items/717.` | notice | 0.3643 | 0.1111 | 44.1079 | 1731 | 3307 | — |
| 59 | `corpus:ground_truth:train:arnold-j/sent_items/498.` | email | 0.3409 | 0.1052 | 32.9450 | 2170 | 2504 | — |
| 60 | `corpus:ground_truth:train:mckay-j/sent_items/190.` | email | 0.5500 | 0.2222 | 26.7693 | 1631 | 2099 | — |
| 61 | `corpus:ground_truth:train:tholt-j/janie/104.` | email | 0.4123 | 0.1250 | 32.5443 | 1686 | 2739 | — |
| 62 | `corpus:ground_truth:train:kitchen-l/_americas/netco_hr/18.` | email | 0.3669 | 0.1111 | 42.1020 | 1956 | 3263 | — |
| 63 | `corpus:ground_truth:train:kaminski-v/all_documents/842.` | email | 0.6000 | 0.2105 | 29.1227 | 1679 | 2360 | — |
| 64 | `corpus:ground_truth:train:haedicke-m/all_documents/2298.` | email | 0.4605 | 0.1052 | 56.4350 | 2117 | 5065 | — |
| 65 | `corpus:ground_truth:train:presto-k/sent_items/153.` | email | 0.4346 | 0.1333 | 36.8368 | 1627 | 2737 | — |
| 66 | `corpus:ground_truth:train:tholt-j/deleted_items/205.` | press_release | 0.5500 | 0.2353 | 47.3993 | 1938 | 3862 | — |
| 67 | `corpus:ground_truth:train:quenet-j/inbox/15.` | email | 0.4482 | 0.1176 | 38.0618 | 1853 | 3256 | — |
| 68 | `corpus:ground_truth:train:skilling-j/all_documents/141.` | email | 0.3409 | 0.1429 | 27.7023 | 1580 | 1995 | — |
| 69 | `corpus:ground_truth:train:keiser-k/deleted_items/247.` | email | 0.4607 | 0.1000 | 48.6556 | 2264 | 3624 | — |
| 70 | `corpus:ground_truth:train:kaminski-v/all_documents/2111.` | email | 0.4221 | 0.0953 | 41.5233 | 1897 | 3713 | — |
| 71 | `corpus:ground_truth:train:germany-c/inbox/167.` | notice | 0.5500 | 0.2222 | 31.5011 | 1991 | 2255 | — |
| 72 | `corpus:ground_truth:train:kaminski-v/all_documents/6051.` | email | 0.3349 | 0.1000 | 38.8772 | 1784 | 3081 | — |
| 73 | `corpus:ground_truth:train:skilling-j/all_documents/507.` | email | 0.4118 | 0.1176 | 30.3688 | 2282 | 2470 | — |
| 74 | `corpus:ground_truth:train:sanders-r/px/17.` | attorney_demand | 0.6378 | 0.1429 | 48.7185 | 1945 | 3795 | — |
| 75 | `corpus:ground_truth:train:benson-r/sent_items/14.` | meeting_request | 0.6185 | 0.1818 | 32.9685 | 1743 | 2748 | — |
| 76 | `corpus:ground_truth:train:neal-s/_sent_mail/356.` | email | 0.7000 | 0.2353 | 41.7766 | 1908 | 3205 | — |
| 77 | `corpus:ground_truth:train:shackleton-s/all_documents/11016.` | memo | 0.7405 | 0.2666 | 34.6592 | 1797 | 2686 | — |
| 78 | `corpus:ground_truth:train:kaminski-v/deleted_items/806.` | email | 0.5417 | 0.1904 | 37.1629 | 2292 | 3114 | — |
| 79 | `corpus:ground_truth:train:nemec-g/all_documents/4346.` | email | 0.5417 | 0.2666 | 27.1852 | 1592 | 2344 | — |
| 80 | `corpus:ground_truth:train:mcconnell-m/_sent_mail/217.` | email | 0.5000 | 0.1904 | 30.2699 | 1760 | 2482 | — |
| 81 | `corpus:ground_truth:train:rodrique-r/_sent_mail/166.` | email | 0.5000 | 0.3636 | 21.4871 | 1569 | 1608 | — |
| 82 | `corpus:ground_truth:train:kitchen-l/_americas/rac/10.` | email | 0.2500 | 0.2500 | 16.5693 | 1575 | 1281 | — |
| 83 | `corpus:ground_truth:train:campbell-l/all_documents/1428.` | notice | 0.7247 | 0.1667 | 34.5501 | 1677 | 2770 | — |
| 84 | `corpus:ground_truth:train:shapiro-r/federal_legis_/66.` | email | 0.4828 | 0.1052 | 48.3412 | 2314 | 3604 | — |
| 85 | `corpus:ground_truth:train:mcconnell-m/_sent_mail/151.` | email | 0.5938 | 0.2000 | 47.5264 | 2354 | 3699 | — |
| 86 | `corpus:ground_truth:train:horton-s/all_documents/85.` | letter | 0.4994 | 0.1111 | 27.7186 | 1686 | 2136 | — |
| 87 | `corpus:ground_truth:train:campbell-l/sent_items/19.` | email | 0.3982 | 0.1052 | 37.2159 | 1738 | 2693 | — |
| 88 | `corpus:ground_truth:train:germany-c/inbox/237.` | notice | 0.6611 | 0.2222 | 42.8650 | 1693 | 3434 | — |
| 89 | `corpus:ground_truth:train:presto-k/deleted_items/1350.` | notice | 0.2446 | 0.0000 | 40.4228 | 1640 | 3350 | — |
| 90 | `corpus:ground_truth:train:dasovich-j/all_documents/10430.` | email | 0.5000 | 0.1904 | 51.1911 | 3931 | 4128 | — |
| 91 | `corpus:ground_truth:train:shankman-j/deleted_items/671.` | email | 0.4170 | 0.1052 | 38.5325 | 2289 | 3209 | — |
| 92 | `corpus:ground_truth:train:schwieger-j/sent_items/159.` | email | 0.5682 | 0.1904 | 31.5932 | 1766 | 2852 | — |
| 93 | `corpus:ground_truth:train:fossum-d/_sent_mail/1317.` | email | 0.8616 | 0.2666 | 34.8728 | 2788 | 3211 | — |
| 94 | `corpus:ground_truth:train:kean-s/all_documents/2264.` | press_release | 0.6333 | 0.2353 | 39.8160 | 1846 | 3816 | — |
| 95 | `corpus:ground_truth:train:mann-k/_sent_mail/3628.` | email | 0.3357 | 0.1429 | 26.3252 | 1584 | 2257 | — |
| 96 | `corpus:ground_truth:train:mann-k/all_documents/5748.` | email | 0.3409 | 0.1429 | 23.0141 | 1672 | 1841 | — |
| 97 | `corpus:ground_truth:train:ring-r/eesirenewableenergy/13.` | demand | 0.6280 | 0.1250 | 39.8391 | 1794 | 3291 | — |
| 98 | `corpus:ground_truth:train:lay-k/inbox/286.` | press_release | 0.3625 | 0.1818 | 35.4553 | 1602 | 2962 | — |
| 99 | `corpus:ground_truth:train:jones-t/all_documents/4429.` | memo | 0.6500 | 0.1904 | 31.5105 | 3617 | 2452 | — |
| 100 | `corpus:ground_truth:train:ruscitti-k/deleted_items/88.` | letter | 0.3886 | 0.1111 | 45.0739 | 1911 | 3555 | — |

- scored rows: 100/100; min=0.1662 max=0.8750 mean=0.4996

## Reproduce

```bash
uv run python scripts/run_evals.py --task eval:correspondence --real --sample 100 --seed 42 --concurrency 8 --subset "class:correspondence"
uv run python scripts/score_run.py --run-id 20260928T073402Z-eval-correspondence --recompute
uv run python scripts/render_comparison_reports.py --run-id 20260928T073402Z-eval-correspondence
```

## Artifacts

| path | role |
| --- | --- |
| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |
| `data/experiments/20260928T073402Z-eval-correspondence/cases.jsonl` | per-case rows (scores, tokens, latency) |
| `data/experiments/20260928T073402Z-eval-correspondence/subset_manifest.json` | canonical draw fingerprint (filenames + content hashes) |
| `reports/experiment_log/20260928T073402Z-eval-correspondence.md` | experiment-log markdown mirror |
| `reports/api-comparisons/qwen3.7-flash/correspondence/RUN-100-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md` | Modal-comparable API-leg write-up |

## Caveats / notes

- mode: **real**; trace backend: `none`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
