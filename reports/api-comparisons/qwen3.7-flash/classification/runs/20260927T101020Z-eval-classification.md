# Run report — `20260927T101020Z-eval-classification` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T101020Z-eval-classification` |
| task / agent | `classification` |
| prompt | `—` (frozen) |
| engine | `qwen/qwen3.7-flash` (OpenRouter API) |
| profile / provider | `—` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `full` — 100 docs, seed 42 |
| timestamp | `2026-09-27T10:10:20+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T101020Z-eval-classification/subset_manifest.json` |
| eval git | `53a9d88` |
| finished | `2026-09-27T10:15:12+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / node |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 100 / None |
| scorer | classification |
| decode profile | — |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T101020Z-eval-classification', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T10:10:20+00:00` |
| finished_at | `2026-09-27T10:15:12+00:00` |
| duration_s (wall) | 293.7000 |
| latency_ms_mean | 15624.5 |
| latency_ms_p95 | 126629.0 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **100 / 100** (`errors=0`) |
| class_accuracy | 0.91 |
| errors | 0 |
| scorer_errors | 0 |
| subclass_accuracy | 0.56 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 293.7000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **—** USD |
| cost actual (derived from case rows) | **0.0851** USD |
| cost estimated (roster token rates) | **0.0851** USD |
| cost per document (actual) | 0.0009 USD |
| cost per document (estimated) | 0.0009 USD |
| latency e2e / p50 / p95 / max | 293.7000 / 3.1470 / 126.6290 / 196.1663 s |
| prompt / completion / total tokens | 2580060 / 59141 / 2639201 |
| cost cap | — USD (profile) -> **—** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1562.5 s vs wall = 293.7 s -> wall/serial factor 5.32x at concurrency 8.

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
| `sorter` | 329 | 2580060 | 59141 | 2639201 | 0.0851 | qwen/qwen3.7-flash |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:dasovich-j/all_documents/9309.` | press_release | — | — | 3.1086 | 6286 | 115 | — |
| 2 | `corpus:ground_truth:train:dasovich-j/all_documents/9178.` | press_release | — | — | 3.1223 | 6034 | 113 | — |
| 3 | `corpus:ground_truth:train:0000950130-01-502904_dex211.txt` | subsidiary_list | — | — | 3.1527 | 6052 | 133 | — |
| 4 | `corpus:ground_truth:train:brawner-s/all_documents/59.` | email | — | — | 3.1667 | 6403 | 114 | — |
| 5 | `corpus:ground_truth:train:property:261501663.txt` | property | — | — | 3.4965 | 7487 | 154 | — |
| 6 | `corpus:ground_truth:train:inpatient:196841176990879:1.txt` | inpatient | — | — | 3.5236 | 6374 | 129 | — |
| 7 | `corpus:ground_truth:train:insurbias-425.txt` | auto | — | — | 4.7460 | 6072 | 214 | — |
| 8 | `corpus:ground_truth:train:inpatient:196831176969260:1.txt` | inpatient | — | — | 2.2839 | 6351 | 117 | — |
| 9 | `corpus:ground_truth:train:inpatient:196091177001318:1.txt` | inpatient | — | — | 2.5097 | 6374 | 137 | — |
| 10 | `corpus:ground_truth:train:0000912057-01-507164_a2041839zex-4_38.txt` | rights_instrument | — | — | 7.4662 | 14056 | 336 | — |
| 11 | `corpus:ground_truth:train:0001193125-14-273392_d715499dex415.htm` | indenture | — | — | 4.6914 | 8603 | 193 | — |
| 12 | `corpus:ground_truth:train:carrier:887493388020303.txt` | carrier | — | — | 2.6156 | 6284 | 126 | — |
| 13 | `corpus:ground_truth:train:property:262952775.txt` | property | — | — | 5.5201 | 15350 | 254 | — |
| 14 | `corpus:ground_truth:train:inpatient:196641176967981:1.txt` | inpatient | — | — | 2.4296 | 6392 | 111 | — |
| 15 | `corpus:ground_truth:train:outpatient:542502281397875:1.txt` | outpatient | — | — | 2.3367 | 6267 | 114 | — |
| 16 | `corpus:ground_truth:train:bailey-s/deleted_items/284.` | demand | — | — | 2.8571 | 6153 | 122 | — |
| 17 | `corpus:ground_truth:train:outpatient:542352281002670:1.txt` | outpatient | — | — | 2.2362 | 6256 | 111 | — |
| 18 | `corpus:ground_truth:train:0001047469-06-011763_a2173128zex-3_1.htm` | charter_amendment | — | — | 5.3769 | 14871 | 249 | — |
| 19 | `corpus:ground_truth:train:inpatient:196631176995684:1.txt` | inpatient | — | — | 2.6063 | 6347 | 148 | — |
| 20 | `corpus:ground_truth:train:inpatient:196501177007233:1.txt` | inpatient | — | — | 2.4820 | 6315 | 120 | — |
| 21 | `corpus:ground_truth:train:property:267235146.txt` | property | — | — | 2.9432 | 8271 | 130 | — |
| 22 | `corpus:ground_truth:train:0000950136-04-001210_file009.htm` | subsidiary_list | — | — | 2.6141 | 6065 | 129 | — |
| 23 | `corpus:ground_truth:train:farmer-d/all_documents/781.` | email | — | — | 2.8795 | 5898 | 123 | — |
| 24 | `corpus:ground_truth:train:hyatt-k/deleted_items/358.` | meeting_request | — | — | 2.5289 | 5942 | 113 | — |
| 25 | `corpus:ground_truth:train:property:262612176.txt` | property | — | — | 2.7364 | 7756 | 125 | — |
| 26 | `corpus:ground_truth:train:lewis-a/deleted_items/442.` | demand | — | — | 3.5513 | 6360 | 185 | — |
| 27 | `corpus:ground_truth:train:GLOBALTECHNOLOGIESLTD_06_08_2020-EX-10.16-CONSULTING AGREEMENT.PDF` | Consulting Agreements | — | — | 5.3297 | 16047 | 229 | — |
| 28 | `corpus:ground_truth:train:bailey-s/deleted_items/242.` | demand | — | — | 4.6060 | 6019 | 130 | — |
| 29 | `corpus:ground_truth:train:taylor-m/all_documents/3517.` | demand | — | — | 2.8878 | 6550 | 138 | — |
| 30 | `corpus:ground_truth:train:outpatient:542512281378952:1.txt` | outpatient | — | — | 3.3264 | 6262 | 169 | — |
| 31 | `corpus:ground_truth:train:OLDAPIWIND-DOWNLTD_01_08_2016-EX-1.3-AGENCY AGREEMENT2.pdf` | Agency Agreements | — | — | 3.5475 | 6751 | 154 | — |
| 32 | `corpus:ground_truth:train:inpatient:196581176969555:1.txt` | inpatient | — | — | 3.1451 | 6387 | 121 | — |
| 33 | `corpus:ground_truth:train:carrier:887433385491039.txt` | carrier | — | — | 3.0235 | 6254 | 120 | — |
| 34 | `corpus:ground_truth:train:watson-k/e_mail_bin/452.` | press_release | — | — | 3.8055 | 6823 | 114 | — |
| 35 | `corpus:ground_truth:train:bailey-s/deleted_items/303.` | demand | — | — | 2.9142 | 6006 | 146 | — |
| 36 | `corpus:ground_truth:train:inpatient:196411176983826:1.txt` | inpatient | — | — | 2.4106 | 6413 | 120 | — |
| 37 | `corpus:ground_truth:train:0001627469-15-000036_ex-10_1.htm` | IP | — | — | 3.3427 | 6164 | 186 | — |
| 38 | `corpus:ground_truth:train:whalley-l/_sent_mail/184.` | press_release | — | — | 2.4637 | 5900 | 108 | — |
| 39 | `corpus:ground_truth:train:hyatt-k/deleted_items/247.` | email | — | — | 2.3326 | 6503 | 102 | — |
| 40 | `corpus:ground_truth:train:Loop Industries, Inc. - Marketing Agreement.PDF` | Marketing | — | — | 18.2573 | 25016 | 520 | — |
| 41 | `corpus:ground_truth:train:guzman-m/all_documents/1861.` | email | — | — | 3.0143 | 6489 | 127 | — |
| 42 | `corpus:ground_truth:train:taylor-m/all_documents/7548.` | memo | — | — | 2.7200 | 5943 | 130 | — |
| 43 | `corpus:ground_truth:train:0001047469-19-005499_a2239779zex-3_4.htm` | charter_amendment | — | — | 2.8889 | 6605 | 132 | — |
| 44 | `corpus:ground_truth:train:ACCELERATEDTECHNOLOGIESHOLDINGCORP_04_24_2003-EX-10.13-JOINT VENTURE AGREEMENT.PDF` | Joint Venture | — | — | 6.5671 | 14706 | 281 | — |
| 45 | `corpus:ground_truth:train:auto:CLM-000632.txt` | auto | — | — | 2.8417 | 6100 | 114 | — |
| 46 | `corpus:ground_truth:train:kaminski-v/all_documents/6462.` | email | — | — | 2.6871 | 6108 | 117 | — |
| 47 | `corpus:ground_truth:train:pde:233204492360064.txt` | pde | — | — | 4.7033 | 6136 | 230 | — |
| 48 | `corpus:ground_truth:train:holst-k/deleted_items/207.` | press_release | — | — | 2.3413 | 6169 | 116 | — |
| 49 | `corpus:ground_truth:train:carrier:887133389464365.txt` | carrier | — | — | 2.3814 | 6260 | 132 | — |
| 50 | `corpus:ground_truth:train:insurbias-347.txt` | auto | — | — | 3.1470 | 6067 | 144 | — |
| 51 | `corpus:ground_truth:train:0001547903-13-000006_a44registrationrightsagree.htm` | rights_instrument | — | — | 24.2553 | 57808 | 1161 | — |
| 52 | `corpus:ground_truth:train:TRANSMONTAIGNEPARTNERSLLC_03_13_2020-EX-10.9-SERVICES AGREEMENT.PDF` | Service | — | — | 2.2665 | 7051 | 112 | — |
| 53 | `corpus:ground_truth:train:shackleton-s/sent_items/311.` | notice | — | — | 3.0030 | 6062 | 137 | — |
| 54 | `corpus:ground_truth:train:griffith-j/deleted_items/38.` | email | — | — | 4.2149 | 5889 | 246 | — |
| 55 | `corpus:ground_truth:train:kaminski-v/deleted_items/1240.` | memo | — | — | 10.4999 | 7523 | 102 | — |
| 56 | `corpus:ground_truth:train:kaminski-v/all_documents/2111.` | email | — | — | 2.5704 | 6219 | 124 | — |
| 57 | `corpus:ground_truth:train:TRIZETTOGROUPINC_08_18_1999-EX-10.17-TECHNICAL INFRASTRUCTURE MAINTENANCE AGREEMENT.PDF` | Maintenance | — | — | 13.5040 | 15386 | 333 | — |
| 58 | `corpus:ground_truth:train:williams-w3/sent_items/486.` | email | — | — | 2.9395 | 6492 | 125 | — |
| 59 | `corpus:ground_truth:train:geaccone-t/deleted_items/275.` | email | — | — | 2.6549 | 6471 | 138 | — |
| 60 | `corpus:ground_truth:train:carrier:887323389407778.txt` | carrier | — | — | 2.3606 | 6290 | 126 | — |
| 61 | `corpus:ground_truth:train:TomOnlineInc_20060501_20-F_EX-4.46_749700_EX-4.46_Co-Branding Agreement.pdf` | Co_Branding | — | — | 39.2160 | 84489 | 1508 | — |
| 62 | `corpus:ground_truth:train:QuantumGroupIncFl_20090120_8-K_EX-99.2_3672910_EX-99.2_Hosting Agreement.pdf` | Hosting | — | — | 47.7972 | 87989 | 1584 | — |
| 63 | `corpus:ground_truth:train:dasovich-j/all_documents/11957.` | meeting_request | — | — | 2.6500 | 6025 | 126 | — |
| 64 | `corpus:ground_truth:train:carrier:887553386968780.txt` | carrier | — | — | 2.5340 | 6217 | 137 | — |
| 65 | `corpus:ground_truth:train:inpatient:196721176983585:1.txt` | inpatient | — | — | 12.7078 | 6389 | 138 | — |
| 66 | `corpus:ground_truth:train:pimenov-v/deleted_items/307.` | notice | — | — | 2.7603 | 7274 | 112 | — |
| 67 | `corpus:ground_truth:train:ADMA BioManufacturing, LLC -  Amendment #3 to Manufacturing Agreement .PDF` | Manufacturing | — | — | 6.5694 | 15300 | 367 | — |
| 68 | `corpus:ground_truth:train:0000950123-10-065253_v55076a6exv4w02.htm` | rights_instrument | — | — | 3.8388 | 6758 | 184 | — |
| 69 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | — | — | 10.4065 | 6344 | 120 | — |
| 70 | `corpus:ground_truth:train:0001193125-06-148518_dex312.htm` | charter_amendment | — | — | 3.1067 | 6874 | 113 | — |
| 71 | `corpus:ground_truth:train:corman-s/inbox/archives/383.` | email | — | — | 13.8417 | 5963 | 124 | — |
| 72 | `corpus:ground_truth:train:pde:233504492590456.txt` | pde | — | — | 4.7670 | 6172 | 232 | — |
| 73 | `corpus:ground_truth:train:storey-g/sent_items/76.` | notice | — | — | 2.8091 | 6325 | 128 | — |
| 74 | `corpus:ground_truth:train:carrier:887653388701548.txt` | carrier | — | — | 2.6749 | 6248 | 126 | — |
| 75 | `corpus:ground_truth:train:bailey-s/deleted_items/337.` | demand | — | — | 3.8077 | 6026 | 150 | — |
| 76 | `corpus:ground_truth:train:inpatient:196131176992635:1.txt` | inpatient | — | — | 2.3264 | 6418 | 124 | — |
| 77 | `corpus:ground_truth:train:inpatient:196271176979963:1.txt` | inpatient | — | — | 2.2078 | 6340 | 123 | — |
| 78 | `corpus:ground_truth:train:hain-m/_sent_mail/156.` | notice | — | — | 2.8930 | 6475 | 142 | — |
| 79 | `corpus:ground_truth:train:carrier:887043385219196.txt` | carrier | — | — | 11.8145 | 6217 | 140 | — |
| 80 | `corpus:ground_truth:train:semperger-c/sent_items/58.` | email | — | — | 2.7716 | 5950 | 132 | — |
| 81 | `corpus:ground_truth:train:contract_4_merger_agreement.txt` | all_cash | — | — | 140.9834 | 241839 | 5985 | — |
| 82 | `corpus:ground_truth:train:BIOPURECORP_06_30_1999-EX-10.13-AGENCY AGREEMENT.PDF` | Agency Agreements | — | — | 31.5401 | 31898 | 594 | — |
| 83 | `corpus:ground_truth:train:taylor-m/all_documents/1557.` | email | — | — | 3.0032 | 5915 | 107 | — |
| 84 | `corpus:ground_truth:train:0000950123-03-010752_y88696a1exv4w7.txt` | indenture | — | — | 147.9017 | 268184 | 6852 | — |
| 85 | `corpus:ground_truth:train:lenhart-m/all_documents/915.` | email | — | — | 23.8864 | 5927 | 929 | — |
| 86 | `corpus:ground_truth:train:contract_117_merger_agreement.txt` | all_stock | — | — | 154.5193 | 259243 | 6679 | — |
| 87 | `corpus:ground_truth:train:inpatient:196431176989595:1.txt` | inpatient | — | — | 3.2761 | 6351 | 116 | — |
| 88 | `corpus:ground_truth:train:taylor-m/all_documents/3775.` | notice | — | — | 13.0528 | 8057 | 151 | — |
| 89 | `corpus:ground_truth:train:thomas-p/deleted_items/42.` | press_release | — | — | 2.3751 | 6044 | 109 | — |
| 90 | `corpus:ground_truth:train:ward-k/deleted_items/173.` | email | — | — | 5.2366 | 17234 | 252 | — |
| 91 | `corpus:ground_truth:train:0001193125-11-352115_d200203dex44.htm` | rights_instrument | — | — | 2.6819 | 7571 | 147 | — |
| 92 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | — | — | 126.6290 | 192115 | 5309 | — |
| 93 | `corpus:ground_truth:train:GOCALLINC_03_30_2000-EX-10.7-Promotion Agreement.PDF` | Promotion | — | — | 6.3986 | 16121 | 280 | — |
| 94 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0306.htm` | officer_certificate | — | — | 22.4771 | 31026 | 583 | — |
| 95 | `corpus:ground_truth:train:taylor-m/deleted_items/66.` | email | — | — | 2.7549 | 6128 | 120 | — |
| 96 | `corpus:ground_truth:train:0001193125-10-076663_dex104a.htm` | License_Agreements | — | — | 32.7628 | 66505 | 1045 | — |
| 97 | `corpus:ground_truth:train:insurbias-719.txt` | auto | — | — | 33.3030 | 6072 | 118 | — |
| 98 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | — | — | 196.1663 | 325337 | 7645 | — |
| 99 | `corpus:ground_truth:train:WHITESMOKE,INC_11_08_2011-EX-10.26-PROMOTION AND DISTRIBUTION AGREEMENT.PDF` | Promotion | — | — | 38.3034 | 57405 | 1000 | — |
| 100 | `corpus:ground_truth:train:contract_129_merger_agreement.txt` | all_stock | — | — | 143.7638 | 217807 | 4911 | — |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `—`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
