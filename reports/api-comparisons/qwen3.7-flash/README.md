# Qwen3.7 Flash — SAND-027 Leg B N=20 suite

OpenRouter API results for `qwen/qwen3.7-flash`, the production model for every llm-mailroom 0.7.1 agent. N=20, 50 and 100 waves (seed 42, concurrency 8); these legs ran the mutated prompt lineage.

Regenerated from the experiment log by `scripts/render_comparison_reports.py`.

## Final runs (canonical wave stems)

| task | final run | result | parse / scorer errors | LLM calls | cost est | report |
|---|---|---:|---:|---:|---:|---|
| correspondence | `20260928T050325Z-eval-correspondence` | overall 0.5104 | 0 / 0 | 20 | $0.008948 | [report](correspondence/RUN-20-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md) |
| correspondence | `20260928T090253Z-eval-correspondence` | overall 0.4931 | 0 / 0 | 50 | $0.022467 | [report](correspondence/RUN-50-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md) |
| correspondence | `20260928T073402Z-eval-correspondence` | overall 0.4996 | 0 / 0 | 100 | $0.044542 | [report](correspondence/RUN-100-CORRESPONDENCE-QWEN3.7-FLASH-REPORT.md) |
| insurance claims | `20260928T051905Z-eval-insurance_claims` | overall 0.7855 | 0 / 0 | 20 | $0.009384 | [report](insurance_claims/RUN-20-INSURANCE_CLAIM-QWEN3.7-FLASH-REPORT.md) |
| insurance claims | `20260928T070248Z-eval-insurance_claims` | overall 0.7733 | 0 / 0 | 50 | $0.025306 | [report](insurance_claims/RUN-50-INSURANCE_CLAIM-QWEN3.7-FLASH-REPORT.md) |
| contracts | `20260928T063713Z-eval-contracts` | overall 0.5462 | 0 / 0 | 61 | $0.073917 | [report](contracts/RUN-50-CONTRACT-QWEN3.7-FLASH-REPORT.md) |
| contracts | `20260928T075959Z-eval-contracts` | overall 0.5167 | 0 / 0 | 25 | $0.029452 | [report](contracts/RUN-20-CONTRACT-QWEN3.7-FLASH-REPORT.md) |
| merger agreements | `20260928T070803Z-eval-merger_agreement` | overall 0.5213 | 0 / 0 | 53 | $0.161147 | [report](merger_agreement/RUN-50-MERGER_AGREEMENT-QWEN3.7-FLASH-REPORT.md) |
| merger agreements | `20260928T080826Z-eval-merger_agreement` | overall 0.3964 | 0 / 0 | 20 | $0.064965 | [report](merger_agreement/RUN-20-MERGER_AGREEMENT-QWEN3.7-FLASH-REPORT.md) |
| corporate records | `20260928T083627Z-eval-corporate_records` | overall 0.4178 | 0 / 0 | 59 | $0.039275 | [report](corporate_records/RUN-50-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md) |
| corporate records | `20260928T075116Z-eval-corporate_records` | overall 0.4202 | 0 / 0 | 22 | $0.014823 | [report](corporate_records/RUN-20-CORPORATE_RECORD-QWEN3.7-FLASH-REPORT.md) |
| sorter / classification | `20260927T101020Z-eval-classification` | class 0.9100; subclass 0.5600 | 0 / 0 | 329 | $0.085093 | [report](classification/RUN-100-FULL-QWEN3.7-FLASH-REPORT.md) |

Suite total: **550 evaluated case rows**, **809 recorded LLM calls**, and **$0.579319 estimated API cost** (aggregate per-agent pricing).
