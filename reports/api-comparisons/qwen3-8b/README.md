# Qwen 3 8B — SAND-027 Leg B N=20 suite

OpenRouter API results for `qwen/qwen3-8b` (decode profile `qwen3-8b`), SAND-027 Leg B N=20 waves, seed 42, frozen prompts, concurrency 8.

Regenerated from the experiment log by `scripts/render_comparison_reports.py`.

## Final runs (canonical wave stems)

| task | final run | result | parse / scorer errors | LLM calls | cost est | report |
|---|---|---:|---:|---:|---:|---|
| correspondence | `20260927T033031Z-eval-correspondence` | overall 0.5130 | 0 / 0 | 39 | $0.060362 | [report](correspondence/RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md) |
| insurance claims | `20260927T035135Z-eval-insurance_claims` | overall 0.7488 | 0 / 0 | 37 | $0.032040 | [report](insurance_claims/RUN-20-INSURANCE_CLAIM-QWEN3-8B-REPORT.md) |
| contracts | `20260927T035621Z-eval-contracts` | overall 0.6169 | 0 / 0 | 44 | $0.114086 | [report](contracts/RUN-20-CONTRACT-QWEN3-8B-REPORT.md) |
| merger agreements | `20260927T022750Z-eval-merger_agreement` | overall 0.3748 | 0 / 0 | 18 | $0.057522 | [report](merger_agreement/RUN-20-MERGER_AGREEMENT-QWEN3-8B-REPORT.md) |
| corporate records | `20260927T042239Z-eval-corporate_records` | overall 0.4004 | 0 / 0 | 34 | $0.060215 | [report](corporate_records/RUN-20-CORPORATE_RECORD-QWEN3-8B-REPORT.md) |
| sorter / classification | `20260927T043145Z-eval-classification` | class 0.7000; subclass 0.0500 | 0 / 0 | 150 | $0.149264 | [report](classification/RUN-20-FULL-QWEN3-8B-REPORT.md) |

Suite total: **120 evaluated case rows**, **322 recorded LLM calls**, and **$0.473489 estimated API cost** (aggregate per-agent pricing).

## Qwen 3 8B notes

- Merger N=20 on `qwen/qwen3-8b` may be reserved for a separate agent wave;
  treat any stand-in merger run as non-canonical unless this table lists it.
- Correspondence with **~39 calls / 20 docs** is JSON **retries**, not source
  chunking — see runbook §5 and per-run report caveats.
- Merger uses validated **48K** source spans (multi-chunk) due to the ~8K
  completion-token cap on this model.
