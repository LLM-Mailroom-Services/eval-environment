# Sorter vs ModernBERT — doc_type on held-out test (323 docs)

Cost/performance comparison for the **intake doc_type gate** ModernBERT is
trained for. No new LLM or GPU jobs were run for this write-up (SSH BERT
training in progress).

## ModernBERT leg (measured)

| | |
| --- | --- |
| weights | run-3 `latest` on Modal volume `modernbert-checkpoints` (artifact sha matches Sep 21 export) |
| eval | **Modal** `mailroom-ml-eval` L4, `--sample 0`, seed 42 |
| artifact | [../held-out-test/eval_full_test_20260927.json](../held-out-test/eval_full_test_20260927.json) |
| n_docs | 323 |
| doc_type accuracy | **0.9257** |
| subclass accuracy (conditional) | **0.5117** |
| window ECE (calibrated) | 0.0155 |
| CPU e2e (warm, short doc) | ~0.075 s/doc (Sep 21 serving validation) |
| $/doc (ONNX-CPU floor) | **$1×10⁻⁶** (plan default; no token meter) |

## LLM sorter legs (API — eval-environment)

Measured **OpenRouter** classification/sorter runs from this repo (real API $,
not Modal GPU proxy).

| run_id | n | class_accuracy | $/doc (actual) | report |
| --- | ---: | ---: | ---: | --- |
| `20260927T043145Z-eval-classification` | 20 | 0.70 | **0.0075** | [RUN-20-FULL-QWEN3-8B-REPORT.md](../../api-comparisons/qwen3-8b/classification/RUN-20-FULL-QWEN3-8B-REPORT.md) |

**Scaled planning view (323 docs, cost only):**

| leg | $/doc | est. total @ 323 docs |
| --- | ---: | ---: |
| ModernBERT (CPU floor) | 1×10⁻⁶ | ~$0.0003 |
| API sorter `qwen/qwen3-8b` (same run’s rate) | 0.0075 | ~$2.42 |

That is roughly **7,500×** lower $/doc on the ModernBERT floor vs the measured
API sorter rate — before any selective-abstention or LLM-only tail routing.

**Latency (order of magnitude):** API run mean ~33 s/doc vs ModernBERT ~0.075 s/doc
warm CPU (~440× faster on wall per doc for the BERT path).

## Quality tradeoff (honest)

| leg | doc_type accuracy | n | comparable? |
| --- | ---: | ---: | --- |
| ModernBERT run-3 | **0.9257** | **323** | yes — full held-out test |
| API `qwen/qwen3-8b` sorter | 0.70 | 20 | **no** — different n, subset `full` draw, pipeline sorter node |

Do **not** treat 0.70 vs 0.9257 as a paired A/B on the same 323 filenames until
`eval:classification` (or equivalent) is run on the exact modernbert test
manifest. For now, use the API row for **$/doc and latency**; use ModernBERT for
**323-doc doc_type accuracy**.

## Interpretation

ModernBERT is the cheap, fast **pre-check**: acceptable when doc_type accuracy
and calibration gates are met; the LLM sorter remains authority for ambiguous
tails, low agreement, and excluded subclass heads. API sorter cost at ~**3/4¢
per document** (measured on the 20-doc wave) dominates batch economics even when
ModernBERT gives up ~8.5 points vs an optimistic 0.98 Modal sorter reference
(sandbox `run-50-modal-hf`, n=50 — not duplicated here).

Machine-readable pairing:
[sorter-vs-modernbert-full-test-323.json](./sorter-vs-modernbert-full-test-323.json).
