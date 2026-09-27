# Granite 4.2 8B — SAND-027 Leg B N=20 suite

OpenRouter API results for `ibm-granite/granite-4.2-8b` (decode profile `granite-4.2-8b`), traced to Braintrust project `Mailroom-Evals`. Same canonical seed-42 draws as the Qwen suite.

Regenerated from the experiment log by `scripts/render_comparison_reports.py`.

## Final runs (canonical wave stems)

| task | final run | result | parse / scorer errors | LLM calls | cost est | report |
|---|---|---:|---:|---:|---:|---|
| correspondence | `20260927T053647Z-eval-correspondence` | overall 0.4065 | 0 / 0 | 20 | $0.029194 | [report](correspondence/RUN-20-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md) |
| insurance claims | `20260927T054211Z-eval-insurance_claims` | overall 0.7135 | 0 / 0 | 20 | $0.024711 | [report](insurance_claims/RUN-20-INSURANCE_CLAIM-GRANITE-4.2-8B-REPORT.md) |
| contracts | `20260927T054738Z-eval-contracts` | overall 0.4769 | 0 / 0 | 24 | $0.073964 | [report](contracts/RUN-20-CONTRACT-GRANITE-4.2-8B-REPORT.md) |
| merger agreements | `20260927T082404Z-eval-merger_agreement` | overall 0.4548 | 0 / 0 | 38 | $0.177431 | [report](merger_agreement/RUN-20-MERGER_AGREEMENT-GRANITE-4.2-8B-REPORT.md) |
| corporate records | `20260927T065622Z-eval-corporate_records` | overall 0.4156 | 0 / 0 | 22 | $0.043637 | [report](corporate_records/RUN-20-CORPORATE_RECORD-GRANITE-4.2-8B-REPORT.md) |
| sorter / classification | `20260927T070900Z-eval-classification` | class 0.9000; subclass 0.6000 | 0 / 0 | 118 | $0.064366 | [report](classification/RUN-20-FULL-GRANITE-4.2-8B-REPORT.md) |
| sorter / classification | `20260927T100340Z-eval-classification` | class 0.9400; subclass 0.4900 | 0 / 0 | 291 | $0.150648 | [report](classification/RUN-100-FULL-GRANITE-4.2-8B-REPORT.md) |

Suite total: **220 evaluated case rows**, **533 recorded LLM calls**, and **$0.563951 estimated API cost** (aggregate per-agent pricing).

## Granite-specific posture

- IBM sampling on every call: temperature 1.0, top-p 0.95, seed 42.
- Thinking-ON specialist budgets: correspondence 16384, insurance 12288,
  contracts 16384, merger 32768, corporate records 16384.
- Merger uses **280K source spans** (not qwen3-8b 48K chunking).

Superseded diagnostics remain in the append-only experiment log only —
use the final run ids in the table above for comparisons.
