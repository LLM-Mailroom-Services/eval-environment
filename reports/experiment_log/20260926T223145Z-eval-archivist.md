## 20260926T223145Z-eval-archivist

| Key | Value |
|---|---|
| family / task | eval / archivist |
| invoke / mode | node / mock |
| model / prompt | None / None |
| trace backend | none |
| git | commit: 00082ce · dirty: True |
| started / finished | 2026-09-26T22:31:45+00:00 → 2026-09-26T22:31:45+00:00 |
| duration_s | 0.9 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:fixtures:train+test:fixture:calibration-contract-wro… |
| config | fixtures |
| filenames | fixture:calibration-contract-wrong_high, fixture:calibratio… |
| n_selected | 2 |
| n_total | 32 |
| repo | Lucius-Morningstar/mailroom-dataset |
| revision | 46a4d3c240a36671cde0182fff4960f6b8b73aca |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | fixtures |
| subset_manifest_jsonl | data/experiments/20260926T223145Z-eval-archivist/subset_man… |
| subset_manifest_path | data/experiments/20260926T223145Z-eval-archivist/subset_man… |
| subset_spec | kind: config · value: fixtures |

### Metrics

| Metric | Value |
|---|---|
| archived_ok | 1 |
| audit_ok | 1 |
| errors | 0 |
| n | 2 |
| scorer_errors | 0 |
| sha256_ok | 1 |
| stage_ok | 1 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 95.6 |
| latency_ms_p95 | 106.3 |
| tokens_completion_total | 0 |
| tokens_prompt_total | 0 |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | archived_ok: 1 · audit_ok: 1 · sha256_ok: 1 · stage_ok: 1 | 106.3 | — |
| corpus:fixtures:train+test:fixture:calibration-contract-wro… | archived_ok: 1 · audit_ok: 1 · sha256_ok: 1 · stage_ok: 1 | 84.9 | — |
