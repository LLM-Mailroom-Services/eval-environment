# Run report — `20260927T101544Z-eval-classification` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T101544Z-eval-classification` |
| task / agent | `classification` |
| prompt | `—` (frozen) |
| engine | `deepseek/deepseek-v4.1-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `full` — 100 docs, seed 42 |
| timestamp | `2026-09-27T10:45:45+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T101544Z-eval-classification/subset_manifest.json` |
| eval git | `53a9d88` |
| finished | `2026-09-27T10:45:47+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / node |
| mode | real |
| concurrency | 1 |
| seed | 42 |
| sample / n | 100 / None |
| scorer | classification |
| decode profile | — |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | 20260927T101544Z-eval-classification |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T101544Z-eval-classification', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T10:45:45+00:00` |
| finished_at | `2026-09-27T10:45:47+00:00` |
| duration_s (wall) | 4.8000 |
| latency_ms_mean | 6666.5 |
| latency_ms_p95 | 31993.5 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **100 / 100** (`errors=0`) |
| class_accuracy | 1.0 |
| errors | 0 |
| scorer_errors | 0 |
| subclass_accuracy | 0.0 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 4.8000 s |
| concurrency | 1 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.1001** USD |
| cost estimated (roster token rates) | **0.1001** USD |
| cost per document (actual) | 0.0010 USD |
| cost per document (estimated) | 0.0010 USD |
| latency e2e / p50 / p95 / max | 4.8000 / 1.3314 / 31.9935 / 87.3248 s |
| prompt / completion / total tokens | 2437786 / 51008 / 2488794 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 666.7 s vs wall = 4.8 s -> wall/serial factor 138.89x at concurrency 1.

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
| `sorter` | 329 | 2437786 | 51008 | 2488794 | 0.1001 | deepseek/deepseek-v4.1-flash |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:property:261501663.txt` | property | — | — | 4.1392 | 6909 | 120 | — |
| 2 | `corpus:ground_truth:train:inpatient:196841176990879:1.txt` | inpatient | — | — | 3.3113 | 5862 | 126 | — |
| 3 | `corpus:ground_truth:train:insurbias-425.txt` | auto | — | — | 3.0337 | 5637 | 146 | — |
| 4 | `corpus:ground_truth:train:brawner-s/all_documents/59.` | email | — | — | 3.6946 | 5987 | 95 | — |
| 5 | `corpus:ground_truth:train:0000912057-01-507164_a2041839zex-4_38.txt` | rights_instrument | — | — | 4.1487 | 13310 | 327 | — |
| 6 | `corpus:ground_truth:train:dasovich-j/all_documents/9178.` | press_release | — | — | 3.1708 | 5620 | 101 | — |
| 7 | `corpus:ground_truth:train:0000950130-01-502904_dex211.txt` | subsidiary_list | — | — | 9.4590 | 5638 | 115 | — |
| 8 | `corpus:ground_truth:train:inpatient:196091177001318:1.txt` | inpatient | — | — | 8.1149 | 6252 | 119 | — |
| 9 | `corpus:ground_truth:train:inpatient:196831176969260:1.txt` | inpatient | — | — | 4.7231 | 5848 | 137 | — |
| 10 | `corpus:ground_truth:train:0001193125-14-273392_d715499dex415.htm` | indenture | — | — | 1.8357 | 8036 | 164 | — |
| 11 | `corpus:ground_truth:train:contract_117_merger_agreement.txt` | all_stock | — | — | 55.9654 | 247306 | 4980 | — |
| 12 | `corpus:ground_truth:train:property:262952775.txt` | property | — | — | 1.7549 | 14335 | 278 | — |
| 13 | `corpus:ground_truth:train:0000950123-03-010752_y88696a1exv4w7.txt` | indenture | — | — | 81.1729 | 250076 | 5291 | — |
| 14 | `corpus:ground_truth:train:contract_4_merger_agreement.txt` | all_cash | — | — | 47.2487 | 229705 | 4536 | — |
| 15 | `corpus:ground_truth:train:carrier:887493388020303.txt` | carrier | — | — | 0.5494 | 5799 | 127 | — |
| 16 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | — | — | 87.3248 | 311652 | 6674 | — |
| 17 | `corpus:ground_truth:train:inpatient:196641176967981:1.txt` | inpatient | — | — | 1.0559 | 5870 | 121 | — |
| 18 | `corpus:ground_truth:train:0001047469-06-011763_a2173128zex-3_1.htm` | charter_amendment | — | — | 1.9917 | 13853 | 255 | — |
| 19 | `corpus:ground_truth:train:outpatient:542502281397875:1.txt` | outpatient | — | — | 0.8499 | 5786 | 112 | — |
| 20 | `corpus:ground_truth:train:bailey-s/deleted_items/284.` | demand | — | — | 0.4591 | 5715 | 100 | — |
| 21 | `corpus:ground_truth:train:outpatient:542352281002670:1.txt` | outpatient | — | — | 0.5768 | 5786 | 129 | — |
| 22 | `corpus:ground_truth:train:inpatient:196631176995684:1.txt` | inpatient | — | — | 0.9733 | 5850 | 126 | — |
| 23 | `corpus:ground_truth:train:property:267235146.txt` | property | — | — | 1.0186 | 7689 | 151 | — |
| 24 | `corpus:ground_truth:train:inpatient:196501177007233:1.txt` | inpatient | — | — | 1.0660 | 5819 | 133 | — |
| 25 | `corpus:ground_truth:train:0000950136-04-001210_file009.htm` | subsidiary_list | — | — | 0.5630 | 5652 | 133 | — |
| 26 | `corpus:ground_truth:train:farmer-d/all_documents/781.` | email | — | — | 9.1992 | 5478 | 103 | — |
| 27 | `corpus:ground_truth:train:hyatt-k/deleted_items/358.` | meeting_request | — | — | 0.8584 | 5525 | 114 | — |
| 28 | `corpus:ground_truth:train:GLOBALTECHNOLOGIESLTD_06_08_2020-EX-10.16-CONSULTING AGREEMENT.PDF` | Consulting Agreements | — | — | 1.7474 | 15143 | 297 | — |
| 29 | `corpus:ground_truth:train:lewis-a/deleted_items/442.` | demand | — | — | 0.8861 | 5945 | 127 | — |
| 30 | `corpus:ground_truth:train:property:262612176.txt` | property | — | — | 0.6755 | 7191 | 130 | — |
| 31 | `corpus:ground_truth:train:bailey-s/deleted_items/242.` | demand | — | — | 0.5472 | 5580 | 107 | — |
| 32 | `corpus:ground_truth:train:Loop Industries, Inc. - Marketing Agreement.PDF` | Marketing | — | — | 23.2097 | 24203 | 503 | — |
| 33 | `corpus:ground_truth:train:taylor-m/all_documents/3517.` | demand | — | — | 0.8225 | 6149 | 132 | — |
| 34 | `corpus:ground_truth:train:outpatient:542512281378952:1.txt` | outpatient | — | — | 2.1942 | 5779 | 114 | — |
| 35 | `corpus:ground_truth:train:OLDAPIWIND-DOWNLTD_01_08_2016-EX-1.3-AGENCY AGREEMENT2.pdf` | Agency Agreements | — | — | 1.1094 | 6324 | 183 | — |
| 36 | `corpus:ground_truth:train:inpatient:196581176969555:1.txt` | inpatient | — | — | 0.5790 | 5868 | 135 | — |
| 37 | `corpus:ground_truth:train:carrier:887433385491039.txt` | carrier | — | — | 0.5188 | 5779 | 112 | — |
| 38 | `corpus:ground_truth:train:watson-k/e_mail_bin/452.` | press_release | — | — | 1.1390 | 6375 | 101 | — |
| 39 | `corpus:ground_truth:train:0001547903-13-000006_a44registrationrightsagree.htm` | rights_instrument | — | — | 31.9935 | 54732 | 1155 | — |
| 40 | `corpus:ground_truth:train:bailey-s/deleted_items/303.` | demand | — | — | 0.6193 | 5579 | 111 | — |
| 41 | `corpus:ground_truth:train:0001627469-15-000036_ex-10_1.htm` | IP | — | — | 1.3314 | 5737 | 181 | — |
| 42 | `corpus:ground_truth:train:inpatient:196411176983826:1.txt` | inpatient | — | — | 1.1527 | 5888 | 142 | — |
| 43 | `corpus:ground_truth:train:whalley-l/_sent_mail/184.` | press_release | — | — | 0.7676 | 5889 | 76 | — |
| 44 | `corpus:ground_truth:train:hyatt-k/deleted_items/247.` | email | — | — | 0.7863 | 6045 | 90 | — |
| 45 | `corpus:ground_truth:train:ACCELERATEDTECHNOLOGIESHOLDINGCORP_04_24_2003-EX-10.13-JOINT VENTURE AGREEMENT.PDF` | Joint Venture | — | — | 2.1850 | 13802 | 239 | — |
| 46 | `corpus:ground_truth:train:guzman-m/all_documents/1861.` | email | — | — | 0.6197 | 6025 | 113 | — |
| 47 | `corpus:ground_truth:train:taylor-m/all_documents/7548.` | memo | — | — | 0.6121 | 5528 | 117 | — |
| 48 | `corpus:ground_truth:train:0001047469-19-005499_a2239779zex-3_4.htm` | charter_amendment | — | — | 1.3135 | 6139 | 168 | — |
| 49 | `corpus:ground_truth:train:auto:CLM-000632.txt` | auto | — | — | 0.5349 | 5655 | 129 | — |
| 50 | `corpus:ground_truth:train:kaminski-v/all_documents/6462.` | email | — | — | 0.9336 | 5685 | 117 | — |
| 51 | `corpus:ground_truth:train:pde:233204492360064.txt` | pde | — | — | 1.1853 | 5683 | 147 | — |
| 52 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | — | — | 26.4644 | 183687 | 3767 | — |
| 53 | `corpus:ground_truth:train:holst-k/deleted_items/207.` | press_release | — | — | 0.7861 | 5744 | 99 | — |
| 54 | `corpus:ground_truth:train:insurbias-347.txt` | auto | — | — | 0.5553 | 5632 | 139 | — |
| 55 | `corpus:ground_truth:train:carrier:887133389464365.txt` | carrier | — | — | 0.8733 | 5788 | 129 | — |
| 56 | `corpus:ground_truth:train:QuantumGroupIncFl_20090120_8-K_EX-99.2_3672910_EX-99.2_Hosting Agreement.pdf` | Hosting | — | — | 22.0558 | 83551 | 1771 | — |
| 57 | `corpus:ground_truth:train:shackleton-s/sent_items/311.` | notice | — | — | 1.5452 | 5625 | 180 | — |
| 58 | `corpus:ground_truth:train:TRANSMONTAIGNEPARTNERSLLC_03_13_2020-EX-10.9-SERVICES AGREEMENT.PDF` | Service | — | — | 0.7967 | 6602 | 136 | — |
| 59 | `corpus:ground_truth:train:griffith-j/deleted_items/38.` | email | — | — | 0.7462 | 5473 | 117 | — |
| 60 | `corpus:ground_truth:train:kaminski-v/deleted_items/1240.` | memo | — | — | 0.5755 | 6999 | 134 | — |
| 61 | `corpus:ground_truth:train:TomOnlineInc_20060501_20-F_EX-4.46_749700_EX-4.46_Co-Branding Agreement.pdf` | Co_Branding | — | — | 22.0585 | 79848 | 1940 | — |
| 62 | `corpus:ground_truth:train:kaminski-v/all_documents/2111.` | email | — | — | 0.7418 | 5793 | 112 | — |
| 63 | `corpus:ground_truth:train:TRIZETTOGROUPINC_08_18_1999-EX-10.17-TECHNICAL INFRASTRUCTURE MAINTENANCE AGREEMENT.PDF` | Maintenance | — | — | 3.0492 | 14588 | 344 | — |
| 64 | `corpus:ground_truth:train:williams-w3/sent_items/486.` | email | — | — | 0.5765 | 6064 | 120 | — |
| 65 | `corpus:ground_truth:train:geaccone-t/deleted_items/275.` | email | — | — | 1.8643 | 6028 | 140 | — |
| 66 | `corpus:ground_truth:train:carrier:887323389407778.txt` | carrier | — | — | 0.5376 | 5805 | 124 | — |
| 67 | `corpus:ground_truth:train:inpatient:196721176983585:1.txt` | inpatient | — | — | 7.1654 | 5875 | 132 | — |
| 68 | `corpus:ground_truth:train:dasovich-j/all_documents/11957.` | meeting_request | — | — | 1.6360 | 5607 | 95 | — |
| 69 | `corpus:ground_truth:train:carrier:887553386968780.txt` | carrier | — | — | 11.3614 | 5752 | 139 | — |
| 70 | `corpus:ground_truth:train:pimenov-v/deleted_items/307.` | notice | — | — | 4.3657 | 6679 | 142 | — |
| 71 | `corpus:ground_truth:train:ADMA BioManufacturing, LLC -  Amendment #3 to Manufacturing Agreement .PDF` | Manufacturing | — | — | 1.9997 | 14372 | 334 | — |
| 72 | `corpus:ground_truth:train:corman-s/inbox/archives/383.` | email | — | — | 1.6271 | 5534 | 113 | — |
| 73 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | — | — | 2.1604 | 5851 | 136 | — |
| 74 | `corpus:ground_truth:train:0000950123-10-065253_v55076a6exv4w02.htm` | rights_instrument | — | — | 0.9537 | 6273 | 232 | — |
| 75 | `corpus:ground_truth:train:0001193125-06-148518_dex312.htm` | charter_amendment | — | — | 1.4436 | 6416 | 147 | — |
| 76 | `corpus:ground_truth:train:pde:233504492590456.txt` | pde | — | — | 0.5869 | 5719 | 142 | — |
| 77 | `corpus:ground_truth:train:BIOPURECORP_06_30_1999-EX-10.13-AGENCY AGREEMENT.PDF` | Agency Agreements | — | — | 7.1606 | 29945 | 718 | — |
| 78 | `corpus:ground_truth:train:storey-g/sent_items/76.` | notice | — | — | 0.9757 | 5883 | 135 | — |
| 79 | `corpus:ground_truth:train:carrier:887653388701548.txt` | carrier | — | — | 0.9038 | 5776 | 124 | — |
| 80 | `corpus:ground_truth:train:bailey-s/deleted_items/337.` | demand | — | — | 0.7876 | 5602 | 114 | — |
| 81 | `corpus:ground_truth:train:inpatient:196131176992635:1.txt` | inpatient | — | — | 17.8813 | 5891 | 130 | — |
| 82 | `corpus:ground_truth:train:inpatient:196271176979963:1.txt` | inpatient | — | — | 8.9089 | 5845 | 140 | — |
| 83 | `corpus:ground_truth:train:hain-m/_sent_mail/156.` | notice | — | — | 0.6301 | 6054 | 140 | — |
| 84 | `corpus:ground_truth:train:carrier:887043385219196.txt` | carrier | — | — | 1.0725 | 5755 | 144 | — |
| 85 | `corpus:ground_truth:train:lenhart-m/all_documents/915.` | email | — | — | 0.9062 | 5911 | 89 | — |
| 86 | `corpus:ground_truth:train:semperger-c/sent_items/58.` | email | — | — | 1.6572 | 5534 | 106 | — |
| 87 | `corpus:ground_truth:train:0001193125-10-076663_dex104a.htm` | License_Agreements | — | — | 8.1748 | 62477 | 1155 | — |
| 88 | `corpus:ground_truth:train:contract_129_merger_agreement.txt` | all_stock | — | — | 42.5748 | 206756 | 4211 | — |
| 89 | `corpus:ground_truth:train:taylor-m/all_documents/1557.` | email | — | — | 0.5337 | 5498 | 97 | — |
| 90 | `corpus:ground_truth:train:taylor-m/all_documents/3775.` | notice | — | — | 0.6922 | 7578 | 140 | — |
| 91 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0306.htm` | officer_certificate | — | — | 3.9045 | 29183 | 558 | — |
| 92 | `corpus:ground_truth:train:insurbias-719.txt` | auto | — | — | 0.9835 | 5637 | 137 | — |
| 93 | `corpus:ground_truth:train:inpatient:196431176989595:1.txt` | inpatient | — | — | 1.9038 | 5856 | 126 | — |
| 94 | `corpus:ground_truth:train:ward-k/deleted_items/173.` | email | — | — | 1.3918 | 15892 | 190 | — |
| 95 | `corpus:ground_truth:train:thomas-p/deleted_items/42.` | press_release | — | — | 3.0929 | 5618 | 126 | — |
| 96 | `corpus:ground_truth:train:0001193125-11-352115_d200203dex44.htm` | rights_instrument | — | — | 1.8886 | 7090 | 150 | — |
| 97 | `corpus:ground_truth:train:GOCALLINC_03_30_2000-EX-10.7-Promotion Agreement.PDF` | Promotion | — | — | 5.5280 | 15164 | 381 | — |
| 98 | `corpus:ground_truth:train:WHITESMOKE,INC_11_08_2011-EX-10.26-PROMOTION AND DISTRIBUTION AGREEMENT.PDF` | Promotion | — | — | 20.7363 | 54291 | 1244 | — |
| 99 | `corpus:ground_truth:train:taylor-m/deleted_items/66.` | email | — | — | 0.8821 | 5669 | 129 | — |
| 100 | `corpus:ground_truth:train:dasovich-j/all_documents/9309.` | press_release | — | — | 1.2323 | 5858 | 121 | — |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- resumed run: `20260927T101544Z-eval-classification` (subset manifest preserved)
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
