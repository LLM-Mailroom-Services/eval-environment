# Run report — `20260927T100340Z-eval-classification` (API leg)

Comparison report for the OpenRouter API leg, metric-for-metric against
the Modal/vLLM leg reports (same wave+class stem = paired report).

| | |
|---|---|
| run_id | `20260927T100340Z-eval-classification` |
| task / agent | `classification` |
| prompt | `—` (frozen) |
| engine | `ibm-granite/granite-4.2-8b` (OpenRouter API) |
| profile / provider | `granite-4.2-8b` / `openrouter` |
| dataset | Lucius-Morningstar/mailroom-dataset rev `46a4d3c240a36671cde0182fff4960f6b8b73aca` |
| subset / draw | `full` — 100 docs, seed 42 |
| timestamp | `2026-09-27T10:03:40+00:00` |
| pipeline git | `28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636` |
| subset manifest | `data/experiments/20260927T100340Z-eval-classification/subset_manifest.json` |
| eval git | `53a9d88` |
| finished | `2026-09-27T10:08:33+00:00` |

## Run configuration

| control | value |
|---|---|
| family / invoke | eval / node |
| mode | real |
| concurrency | 8 |
| seed | 42 |
| sample / n | 100 / None |
| scorer | classification |
| decode profile | granite-4.2-8b |
| prompt source / lineage | frozen / frozen |
| trace backend | braintrust |
| resumed_from | — |
| dry_run | False |
| trace ids | `{'backend': 'braintrust', 'project': 'Mailroom-Evals', 'experiment': '20260927T100340Z-eval-classification', 'dataset': None, 'dataset_records': 0}` |

## Runtime performance

| metric | value |
|---|---|
| started_at | `2026-09-27T10:03:40+00:00` |
| finished_at | `2026-09-27T10:08:33+00:00` |
| duration_s (wall) | 294.8000 |
| latency_ms_mean | 14845.8 |
| latency_ms_p95 | 75382.4 |

## Headline results

| metric | value |
|---|---|
| docs ok / total | **100 / 100** (`errors=0`) |
| class_accuracy | 0.94 |
| errors | 0 |
| scorer_errors | 0 |
| subclass_accuracy | 0.49 |
| thinking_recovered (stripped + re-scored) | 0 |

## Serving / cost metrics (API leg)

| metric | value |
|---|---|
| wall (run duration) | 294.8000 s |
| concurrency | 8 |
| cold boot | N/A (serverless API — no cold boot) |
| gpu_seconds | N/A (no local GPU) |
| cost expected (wave planning) | **4.0000** USD |
| cost actual (derived from case rows) | **0.1506** USD |
| cost estimated (roster token rates) | **0.1506** USD |
| cost per document (actual) | 0.0015 USD |
| cost per document (estimated) | 0.0015 USD |
| latency e2e / p50 / p95 / max | 294.8000 / 3.3616 / 75.3824 / 183.1452 s |
| prompt / completion / total tokens | 2201847 / 74141 / 2275988 |
| cost cap | 1.5000 USD (profile) -> **under_cap** |

**Serial-vs-batched proof:** sum(per-doc latency) = 1484.6 s vs wall = 294.8 s -> wall/serial factor 5.04x at concurrency 8.

## Decode posture

| control | value |
|---|---|
| sampling override | `{"temperature": 1.0, "top_p": 0.95, "seed": 42}` |
| sampling injected on wire | True |
| per-agent completion budgets | `{"contracts_specialist": 16384, "corporate_records_specialist": 16384, "correspondence_specialist": 16384, "insurance_claims_specialist": 12288, "merger_agreement_specialist": 32768}` |
| per-call timeout | 600 s |

## Per-agent usage

| agent | calls | prompt tok | completion tok | total tok | cost est | models |
|---|---|---|---|---|---|---|
| `sorter` | 291 | 2201847 | 74141 | 2275988 | 0.1506 | ibm-granite/granite-4.2-8b |

## Per-document scores

| # | doc id | subclass | overall | f1 | latency s | tok in | tok out | error |
|---|---|---|---|---|---|---|---|---|
| 1 | `corpus:ground_truth:train:dasovich-j/all_documents/9309.` | press_release | — | — | 3.3204 | 6114 | 142 | — |
| 2 | `corpus:ground_truth:train:brawner-s/all_documents/59.` | email | — | — | 3.3466 | 6195 | 151 | — |
| 3 | `corpus:ground_truth:train:insurbias-425.txt` | auto | — | — | 3.3565 | 5839 | 151 | — |
| 4 | `corpus:ground_truth:train:dasovich-j/all_documents/9178.` | press_release | — | — | 3.3616 | 5832 | 113 | — |
| 5 | `corpus:ground_truth:train:0000950130-01-502904_dex211.txt` | subsidiary_list | — | — | 3.7346 | 5844 | 132 | — |
| 6 | `corpus:ground_truth:train:inpatient:196841176990879:1.txt` | inpatient | — | — | 3.8595 | 6087 | 178 | — |
| 7 | `corpus:ground_truth:train:property:261501663.txt` | property | — | — | 4.4020 | 7206 | 171 | — |
| 8 | `corpus:ground_truth:train:inpatient:196091177001318:1.txt` | inpatient | — | — | 3.0935 | 6094 | 162 | — |
| 9 | `corpus:ground_truth:train:inpatient:196831176969260:1.txt` | inpatient | — | — | 3.3394 | 6070 | 174 | — |
| 10 | `corpus:ground_truth:train:0001193125-14-273392_d715499dex415.htm` | indenture | — | — | 4.1041 | 8466 | 221 | — |
| 11 | `corpus:ground_truth:train:0000912057-01-507164_a2041839zex-4_38.txt` | rights_instrument | — | — | 9.1433 | 13636 | 408 | — |
| 12 | `corpus:ground_truth:train:carrier:887493388020303.txt` | carrier | — | — | 2.9645 | 6013 | 142 | — |
| 13 | `corpus:ground_truth:train:inpatient:196641176967981:1.txt` | inpatient | — | — | 2.6236 | 6094 | 162 | — |
| 14 | `corpus:ground_truth:train:property:262952775.txt` | property | — | — | 6.6975 | 14874 | 345 | — |
| 15 | `corpus:ground_truth:train:outpatient:542502281397875:1.txt` | outpatient | — | — | 3.2746 | 6003 | 190 | — |
| 16 | `corpus:ground_truth:train:bailey-s/deleted_items/284.` | demand | — | — | 2.5589 | 5925 | 144 | — |
| 17 | `corpus:ground_truth:train:outpatient:542352281002670:1.txt` | outpatient | — | — | 3.0684 | 6001 | 172 | — |
| 18 | `corpus:ground_truth:train:0001047469-06-011763_a2173128zex-3_1.htm` | charter_amendment | — | — | 6.1854 | 14430 | 303 | — |
| 19 | `corpus:ground_truth:train:inpatient:196631176995684:1.txt` | inpatient | — | — | 3.7722 | 6078 | 222 | — |
| 20 | `corpus:ground_truth:train:property:267235146.txt` | property | — | — | 3.5025 | 7980 | 203 | — |
| 21 | `corpus:ground_truth:train:inpatient:196501177007233:1.txt` | inpatient | — | — | 3.0559 | 6040 | 186 | — |
| 22 | `corpus:ground_truth:train:0000950136-04-001210_file009.htm` | subsidiary_list | — | — | 2.5442 | 5850 | 140 | — |
| 23 | `corpus:ground_truth:train:hyatt-k/deleted_items/358.` | meeting_request | — | — | 2.3905 | 5726 | 143 | — |
| 24 | `corpus:ground_truth:train:farmer-d/all_documents/781.` | email | — | — | 3.6521 | 5681 | 224 | — |
| 25 | `corpus:ground_truth:train:lewis-a/deleted_items/442.` | demand | — | — | 3.7689 | 6125 | 185 | — |
| 26 | `corpus:ground_truth:train:property:262612176.txt` | property | — | — | 3.2959 | 7484 | 188 | — |
| 27 | `corpus:ground_truth:train:bailey-s/deleted_items/242.` | demand | — | — | 2.6387 | 5782 | 159 | — |
| 28 | `corpus:ground_truth:train:GLOBALTECHNOLOGIESLTD_06_08_2020-EX-10.16-CONSULTING AGREEMENT.PDF` | Consulting Agreements | — | — | 6.5723 | 15607 | 385 | — |
| 29 | `corpus:ground_truth:train:taylor-m/all_documents/3517.` | demand | — | — | 2.7760 | 6380 | 157 | — |
| 30 | `corpus:ground_truth:train:outpatient:542512281378952:1.txt` | outpatient | — | — | 3.1851 | 5994 | 181 | — |
| 31 | `corpus:ground_truth:train:OLDAPIWIND-DOWNLTD_01_08_2016-EX-1.3-AGENCY AGREEMENT2.pdf` | Agency Agreements | — | — | 4.4365 | 6544 | 225 | — |
| 32 | `corpus:ground_truth:train:carrier:887433385491039.txt` | carrier | — | — | 2.3884 | 5992 | 115 | — |
| 33 | `corpus:ground_truth:train:inpatient:196581176969555:1.txt` | inpatient | — | — | 3.7719 | 6094 | 184 | — |
| 34 | `corpus:ground_truth:train:watson-k/e_mail_bin/452.` | press_release | — | — | 2.8653 | 6598 | 144 | — |
| 35 | `corpus:ground_truth:train:bailey-s/deleted_items/303.` | demand | — | — | 2.3224 | 5785 | 134 | — |
| 36 | `corpus:ground_truth:train:inpatient:196411176983826:1.txt` | inpatient | — | — | 3.6333 | 6112 | 170 | — |
| 37 | `corpus:ground_truth:train:0001627469-15-000036_ex-10_1.htm` | IP | — | — | 5.6955 | 5954 | 276 | — |
| 38 | `corpus:ground_truth:train:Loop Industries, Inc. - Marketing Agreement.PDF` | Marketing | — | — | 15.7695 | 24378 | 963 | — |
| 39 | `corpus:ground_truth:train:whalley-l/_sent_mail/184.` | press_release | — | — | 2.3245 | 5686 | 131 | — |
| 40 | `corpus:ground_truth:train:hyatt-k/deleted_items/247.` | email | — | — | 3.0748 | 6342 | 165 | — |
| 41 | `corpus:ground_truth:train:guzman-m/all_documents/1861.` | email | — | — | 3.2019 | 6259 | 174 | — |
| 42 | `corpus:ground_truth:train:taylor-m/all_documents/7548.` | memo | — | — | 2.3275 | 5731 | 135 | — |
| 43 | `corpus:ground_truth:train:ACCELERATEDTECHNOLOGIESHOLDINGCORP_04_24_2003-EX-10.13-JOINT VENTURE AGREEMENT.PDF` | Joint Venture | — | — | 7.2718 | 14290 | 421 | — |
| 44 | `corpus:ground_truth:train:auto:CLM-000632.txt` | auto | — | — | 2.2949 | 5864 | 108 | — |
| 45 | `corpus:ground_truth:train:0001047469-19-005499_a2239779zex-3_4.htm` | charter_amendment | — | — | 3.9786 | 6386 | 187 | — |
| 46 | `corpus:ground_truth:train:kaminski-v/all_documents/6462.` | email | — | — | 2.6328 | 5903 | 135 | — |
| 47 | `corpus:ground_truth:train:pde:233204492360064.txt` | pde | — | — | 3.1863 | 5894 | 181 | — |
| 48 | `corpus:ground_truth:train:holst-k/deleted_items/207.` | press_release | — | — | 3.2186 | 5970 | 184 | — |
| 49 | `corpus:ground_truth:train:insurbias-347.txt` | auto | — | — | 3.3379 | 5834 | 189 | — |
| 50 | `corpus:ground_truth:train:carrier:887133389464365.txt` | carrier | — | — | 3.6424 | 5998 | 182 | — |
| 51 | `corpus:ground_truth:train:shackleton-s/sent_items/311.` | notice | — | — | 3.7617 | 5830 | 179 | — |
| 52 | `corpus:ground_truth:train:TRANSMONTAIGNEPARTNERSLLC_03_13_2020-EX-10.9-SERVICES AGREEMENT.PDF` | Service | — | — | 3.0809 | 6870 | 175 | — |
| 53 | `corpus:ground_truth:train:0001547903-13-000006_a44registrationrightsagree.htm` | rights_instrument | — | — | 33.1974 | 56347 | 1900 | — |
| 54 | `corpus:ground_truth:train:kaminski-v/deleted_items/1240.` | memo | — | — | 2.3894 | 7302 | 128 | — |
| 55 | `corpus:ground_truth:train:griffith-j/deleted_items/38.` | email | — | — | 2.7562 | 5673 | 149 | — |
| 56 | `corpus:ground_truth:train:kaminski-v/all_documents/2111.` | email | — | — | 2.4238 | 6017 | 135 | — |
| 57 | `corpus:ground_truth:train:TRIZETTOGROUPINC_08_18_1999-EX-10.17-TECHNICAL INFRASTRUCTURE MAINTENANCE AGREEMENT.PDF` | Maintenance | — | — | 10.3631 | 14966 | 459 | — |
| 58 | `corpus:ground_truth:train:contract_4_merger_agreement.txt` | all_cash | — | — | 75.3824 | 41572 | 2206 | — |
| 59 | `corpus:ground_truth:train:williams-w3/sent_items/486.` | email | — | — | 2.8077 | 6281 | 132 | — |
| 60 | `corpus:ground_truth:train:geaccone-t/deleted_items/275.` | email | — | — | 3.0058 | 6240 | 156 | — |
| 61 | `corpus:ground_truth:train:carrier:887323389407778.txt` | carrier | — | — | 3.0403 | 6023 | 155 | — |
| 62 | `corpus:ground_truth:train:inpatient:196721176983585:1.txt` | inpatient | — | — | 2.9763 | 6098 | 148 | — |
| 63 | `corpus:ground_truth:train:carrier:887553386968780.txt` | carrier | — | — | 3.4517 | 5963 | 131 | — |
| 64 | `corpus:ground_truth:train:dasovich-j/all_documents/11957.` | meeting_request | — | — | 6.1457 | 5824 | 295 | — |
| 65 | `corpus:ground_truth:train:pimenov-v/deleted_items/307.` | notice | — | — | 2.6733 | 6959 | 136 | — |
| 66 | `corpus:ground_truth:train:corman-s/inbox/archives/383.` | email | — | — | 2.8139 | 5739 | 142 | — |
| 67 | `corpus:ground_truth:train:inpatient:196411177017295:1.txt` | inpatient | — | — | 3.0846 | 6074 | 168 | — |
| 68 | `corpus:ground_truth:train:QuantumGroupIncFl_20090120_8-K_EX-99.2_3672910_EX-99.2_Hosting Agreement.pdf` | Hosting | — | — | 47.2465 | 85800 | 2408 | — |
| 69 | `corpus:ground_truth:train:ADMA BioManufacturing, LLC -  Amendment #3 to Manufacturing Agreement .PDF` | Manufacturing | — | — | 10.0964 | 14804 | 512 | — |
| 70 | `corpus:ground_truth:train:0000950123-10-065253_v55076a6exv4w02.htm` | rights_instrument | — | — | 4.4572 | 6536 | 212 | — |
| 71 | `corpus:ground_truth:train:0001193125-06-148518_dex312.htm` | charter_amendment | — | — | 4.7672 | 6658 | 231 | — |
| 72 | `corpus:ground_truth:train:pde:233504492590456.txt` | pde | — | — | 2.4791 | 5933 | 123 | — |
| 73 | `corpus:ground_truth:train:storey-g/sent_items/76.` | notice | — | — | 2.8727 | 6108 | 156 | — |
| 74 | `corpus:ground_truth:train:carrier:887653388701548.txt` | carrier | — | — | 2.9978 | 5991 | 163 | — |
| 75 | `corpus:ground_truth:train:inpatient:196131176992635:1.txt` | inpatient | — | — | 2.9031 | 6121 | 173 | — |
| 76 | `corpus:ground_truth:train:bailey-s/deleted_items/337.` | demand | — | — | 4.0077 | 5810 | 180 | — |
| 77 | `corpus:ground_truth:train:inpatient:196271176979963:1.txt` | inpatient | — | — | 3.3708 | 6068 | 169 | — |
| 78 | `corpus:ground_truth:train:hain-m/_sent_mail/156.` | notice | — | — | 3.2362 | 6284 | 166 | — |
| 79 | `corpus:ground_truth:train:carrier:887043385219196.txt` | carrier | — | — | 3.4369 | 5967 | 177 | — |
| 80 | `corpus:ground_truth:train:lenhart-m/all_documents/915.` | email | — | — | 3.2192 | 5714 | 156 | — |
| 81 | `corpus:ground_truth:train:TomOnlineInc_20060501_20-F_EX-4.46_749700_EX-4.46_Co-Branding Agreement.pdf` | Co_Branding | — | — | 54.5095 | 82459 | 2826 | — |
| 82 | `corpus:ground_truth:train:semperger-c/sent_items/58.` | email | — | — | 3.1078 | 5739 | 131 | — |
| 83 | `corpus:ground_truth:train:BIOPURECORP_06_30_1999-EX-10.13-AGENCY AGREEMENT.PDF` | Agency Agreements | — | — | 20.7557 | 30993 | 1003 | — |
| 84 | `corpus:ground_truth:train:taylor-m/all_documents/1557.` | email | — | — | 2.2825 | 5704 | 129 | — |
| 85 | `corpus:ground_truth:train:taylor-m/all_documents/3775.` | notice | — | — | 4.5209 | 7942 | 204 | — |
| 86 | `corpus:ground_truth:train:insurbias-719.txt` | auto | — | — | 2.6750 | 5839 | 151 | — |
| 87 | `corpus:ground_truth:train:0000950123-03-010752_y88696a1exv4w7.txt` | indenture | — | — | 130.8457 | 260636 | 6827 | — |
| 88 | `corpus:ground_truth:train:inpatient:196431176989595:1.txt` | inpatient | — | — | 4.2668 | 6077 | 177 | — |
| 89 | `corpus:ground_truth:train:thomas-p/deleted_items/42.` | press_release | — | — | 2.8104 | 5836 | 130 | — |
| 90 | `corpus:ground_truth:train:0001683168-23-005255_cardiff_ex0306.htm` | officer_certificate | — | — | 14.8477 | 30216 | 762 | — |
| 91 | `corpus:ground_truth:train:0001193125-11-352115_d200203dex44.htm` | rights_instrument | — | — | 4.5360 | 7369 | 218 | — |
| 92 | `corpus:ground_truth:train:ward-k/deleted_items/173.` | email | — | — | 10.0242 | 16591 | 498 | — |
| 93 | `corpus:ground_truth:train:taylor-m/deleted_items/66.` | email | — | — | 3.9140 | 5890 | 166 | — |
| 94 | `corpus:ground_truth:train:GOCALLINC_03_30_2000-EX-10.7-Promotion Agreement.PDF` | Promotion | — | — | 11.9667 | 15634 | 605 | — |
| 95 | `corpus:ground_truth:train:0001193125-10-076663_dex104a.htm` | License_Agreements | — | — | 40.1404 | 64988 | 1845 | — |
| 96 | `corpus:ground_truth:train:WHITESMOKE,INC_11_08_2011-EX-10.26-PROMOTION AND DISTRIBUTION AGREEMENT.PDF` | Promotion | — | — | 31.7062 | 55953 | 1656 | — |
| 97 | `corpus:ground_truth:train:contract_117_merger_agreement.txt` | all_stock | — | — | 173.1147 | 253107 | 9552 | — |
| 98 | `corpus:ground_truth:train:contract_94_merger_agreement.txt` | mixed_cash_stock_election | — | — | 183.1452 | 204468 | 7769 | — |
| 99 | `corpus:ground_truth:train:contract_136_merger_agreement.txt` | all_cash | — | — | 161.9622 | 187630 | 8659 | — |
| 100 | `corpus:ground_truth:train:contract_129_merger_agreement.txt` | all_stock | — | — | 170.0434 | 212140 | 8976 | — |

## Caveats / notes

- mode: **real**; trace backend: `braintrust`
- decode profile: `granite-4.2-8b`; budgets/timeout per issue #18 §3
- Pair with the Modal leg: same `RUN-<wave>-<CLASS>` stem in `local-mailroom-sandbox/reports/` (e.g. `RUN-20-CORRESPONDENCE-AWQ-REPORT.md`).
