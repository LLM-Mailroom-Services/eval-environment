# Deepseek V4.1 Flash — SAND-027 Leg B N=20 suite

OpenRouter API results for `deepseek/deepseek-v4.1-flash`, SAND-027 Leg B N=20 specialist waves (seed 42, frozen v1 prompts, concurrency 8). One coverage call per document (`needed_chunks=1`, max two LLM calls per doc for retry).

Regenerated from the experiment log by `scripts/render_comparison_reports.py`.

## Final runs (canonical wave stems)

| task | final run | result | parse / scorer errors | LLM calls | cost est | report |
|---|---|---:|---:|---:|---:|---|
| correspondence | `20260927T105317Z-eval-correspondence` | overall 0.4419 | 0 / 0 | 20 | $0.012063 | [report](correspondence/RUN-20-CORRESPONDENCE-DEEPSEEK-V4.1-FLASH-REPORT.md) |
| insurance claims | `20260927T105400Z-eval-insurance_claims` | overall 0.7974 | 0 / 0 | 20 | $0.013491 | [report](insurance_claims/RUN-20-INSURANCE_CLAIM-DEEPSEEK-V4.1-FLASH-REPORT.md) |
| contracts | `20260927T105549Z-eval-contracts` | overall 0.5137 | 0 / 0 | 23 | $0.050233 | [report](contracts/RUN-20-CONTRACT-DEEPSEEK-V4.1-FLASH-REPORT.md) |
| merger agreements | `20260927T110153Z-eval-merger_agreement` | overall 0.2423 | 0 / 0 | 15 | $0.075246 | [report](merger_agreement/RUN-20-MERGER_AGREEMENT-DEEPSEEK-V4.1-FLASH-REPORT.md) |
| corporate records | `20260927T110828Z-eval-corporate_records` | overall 0.4415 | 0 / 0 | 21 | $0.019675 | [report](corporate_records/RUN-20-CORPORATE_RECORD-DEEPSEEK-V4.1-FLASH-REPORT.md) |
| sorter / classification | `20260927T101544Z-eval-classification` | class 1.0000; subclass 0.0000 | 0 / 0 | 329 | $0.100112 | [report](classification/RUN-100-FULL-DEEPSEEK-V4.1-FLASH-REPORT.md) |

Suite total: **101 evaluated case rows**, **428 recorded LLM calls**, and **$0.270820 estimated API cost** (aggregate per-agent pricing).
