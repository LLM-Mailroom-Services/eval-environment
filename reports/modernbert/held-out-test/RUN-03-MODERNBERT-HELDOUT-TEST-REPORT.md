# Held-out test report — ModernBERT run-3 (canonical Modal eval)

**Canonical export (2026-09-27):**
[`eval_full_test_20260927.json`](./eval_full_test_20260927.json)

| | |
| --- | --- |
| compute | **Modal** `mailroom-ml-eval` (L4), profile `hermes-agent-jjb` |
| command | `modal run deploy/eval_app.py --module latest --sample 0 --seed 42 --selective-risk --as-json` |
| checkpoint | `/checkpoints/latest` on volume `modernbert-checkpoints` |
| artifact sha | `56a4e8919cc3ae11d6bcfc13ec012677409afff99daf167cdd4fb70a6e1754f9` |
| n_docs | 323 |
| seed | 42 |
| sample | 0 (full test split) |
| model_kind | pytorch |
| windows evaluated | 541 (8,192-token context, 512 overlap) |

**Live run-3 SSH training (2026-09-27):** metrics below describe the **Sep 21
completed** weights on the Modal `latest` pointer. Re-run the same Modal command
after live training publishes a new checkpoint (without competing on the SSH host).

## Headline metrics

| metric | Modal full test (2026-09-27) | run-2 trainer test | Sep 21 GPU harness (`eval_run3_20260921.json`) |
| --- | --- | --- | --- |
| doc_type accuracy | **0.9257** | 0.9319 | 0.8947 |
| subclass accuracy (conditional) | **0.5117** | 0.5449 | 0.526 |
| window ECE (calibrated) | **0.0155** | — | 0.0203 |
| window band ECE | **0.0678** | — | 0.0528 |
| fast_path_rate | **0.4211** | — | — |

The Sep 21 harness used checkpoint `runs/20260921-132753` and reported lower
doc_type accuracy than this Modal re-run on `latest` (same artifact sha). Treat
**`eval_full_test_20260927.json`** as the current regression record for run-3
weights; keep [`eval_run3_20260921.json`](./eval_run3_20260921.json) as the
archived GPU-host export for diffing.

## Program gates (recorded, report-only)

| gate | threshold | actual | met |
| --- | --- | --- | --- |
| P0 doc_type | 0.95 | 0.9257 | no |
| P0 subclass | 0.75 | 0.5117 | no |

## Per doc_type accuracy (from `per_stratum_confusion`)

| doc_type | correct | total | accuracy |
| --- | --- | --- | --- |
| insurance_claim | 114 | 114 | **1.000** |
| merger_agreement | 17 | 17 | **1.000** |
| correspondence | 81 | 85 | **0.953** |
| contract | 50 | 60 | **0.833** |
| corporate_record | 37 | 47 | **0.787** |

Errors still concentrate in **corporate_record** (10 confused with correspondence)
and **contract** (9 with corporate_record). Insurance and merger doc_types remain
solved at doc_type level on this split.

## Window cohorts (#104)

| cohort | n_docs | doc_type accuracy | mean window agreement |
| --- | --- | --- | --- |
| single-window | 274 | **0.9197** | 1.0 |
| multi-window | 49 | **0.9592** | 0.9426 |

Multi-window cohort accuracy improved vs the Sep 21 harness export; long filings
still need agreement-aware routing and LLM fallback when windows disagree.

## Selective risk (#104)

| field | value |
| --- | --- |
| status | **refused** |
| reason | no per-head ECE sidecar in the artifact (pre-#107 publish) |

The Sep 21 harness JSON includes a full selective-risk sweep (threshold **0.93**,
coverage ≈43%). Re-publish weights with the #107 ECE sidecar before trusting a
new deployment threshold from this checkpoint bundle.

## Per-head test macro-F1 (#112)

See `per_head` in the JSON. Insurance_claim head is strongest (macro-F1 **0.787**);
contract and corporate_record subclass heads remain weak (macro-F1 **0.026** /
**0.043**), consistent with low conditional subclass accuracy.

## Comparison to LLM sorter (API cost only)

Measured API rates and the quality caveat (n=20 vs 323) live in
[../comparisons/SORTER-VS-MODERNBERT-323.md](../comparisons/SORTER-VS-MODERNBERT-323.md).
Use **0.9257** doc_type accuracy from this report for the ModernBERT leg.

## After live SSH training completes

1. Upload or train to `modernbert-checkpoints/latest` (Modal volume) — do not
   run full eval on the SSH host unless needed for parity checks.
2. Re-run Modal eval (same command as above) and replace
   `eval_full_test_20260927.json` or add a dated sibling.
3. `compare_runs.py --a eval_full_test_20260927.json --b <new>.json` for paired
   bootstrap CIs on doc_type accuracy and window ECE.
