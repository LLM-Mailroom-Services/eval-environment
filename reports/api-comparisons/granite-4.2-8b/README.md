# Granite 4.2 8B — SAND-027 Leg B N=20 suite

Final corrected OpenRouter API results for
`ibm-granite/granite-4.2-8b`, traced to Braintrust project
`Mailroom-Evals`. Every row uses the same canonical seed-42 document draw as
the corresponding Qwen run, frozen prompts, concurrency 8, and the same
deterministic scorer. Follow each report link for per-document scores,
provenance, decode posture, calls, tokens, and cost.

## Final runs

| task | final run | result | parse / scorer errors | LLM calls | cost est | report |
|---|---|---:|---:|---:|---:|---|
| correspondence | `20260927T053647Z-eval-correspondence` | overall 0.4065 | 0 / 0 | 20 | $0.029195 | [report](correspondence/RUN-20-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md) |
| insurance claims | `20260927T054211Z-eval-insurance_claims` | overall 0.7135 | 0 / 0 | 20 | $0.024710 | [report](insurance_claims/RUN-20-INSURANCE_CLAIM-GRANITE-4.2-8B-REPORT.md) |
| contracts | `20260927T054738Z-eval-contracts` | overall 0.4769 | 0 / 0 | 24 | $0.073963 | [report](contracts/RUN-20-CONTRACT-GRANITE-4.2-8B-REPORT.md) |
| merger agreements | `20260927T082404Z-eval-merger_agreement` | overall 0.4548 | 0 / 0 | 38 | $0.177433 | [report](merger_agreement/RUN-20-MERGER_AGREEMENT-GRANITE-4.2-8B-REPORT.md) |
| corporate records | `20260927T065622Z-eval-corporate_records` | overall 0.4156 | 0 / 0 | 22 | $0.043638 | [report](corporate_records/RUN-20-CORPORATE_RECORD-GRANITE-4.2-8B-REPORT.md) |
| sorter / classification | `20260927T070900Z-eval-classification` | class 0.9000; subclass 0.6000 | 0 / 0 | 118 | $0.064367 | [report](classification/RUN-20-FULL-GRANITE-4.2-8B-REPORT.md) |

Suite total: **120 evaluated case rows**, **242 recorded LLM calls**, and
**$0.413306 estimated API cost**. Each run is below its $1.50 cap. Costs use
the live-verified OpenRouter roster rates ($0.06/M input, $0.25/M output)
and are computed from aggregate per-agent tokens before rounding.

## Paired Qwen view

| task | Granite | Qwen 3 8B | delta |
|---|---:|---:|---:|
| correspondence overall | 0.4065 | 0.5130 | -0.1065 |
| insurance claims overall | 0.7135 | 0.7488 | -0.0353 |
| contracts overall | 0.4769 | 0.6169 | -0.1400 |
| corporate records overall | 0.4156 | 0.4004 | +0.0152 |
| sorter class accuracy | 0.9000 | 0.7000 | +0.2000 |
| sorter subclass accuracy | 0.6000 | 0.0500 | +0.5500 |

There is no final `qwen/qwen3-8b` merger run in this session: that spend was
explicitly reserved for another agent. The existing Qwen 3.7 Flash stand-in
scored 0.3748 but is **not** treated as a paired model comparison here.

## Granite-specific, apples-to-apples posture

- model: `ibm-granite/granite-4.2-8b` through OpenRouter;
- IBM sampling on every call family: temperature 1.0, top-p 0.95, seed 42;
- 600-second per-call timeout;
- thinking-ON specialist budgets:
  correspondence 16384, insurance 12288, contracts 16384,
  merger agreement 32768, corporate records 16384;
- identical documents, prompts, extraction schemas, scorer code, and
  concurrency to the Qwen suite;
- merger uses **280K source spans** for Granite (one LLM call when the doc
  fits; at most two coverage chunks for the 465K-char outlier). The qwen3-8b
  **48K multi-chunk** path remains for models with a ~8K completion cap only.

Superseded diagnostics retained in the append-only experiment log:

- correspondence `20260927T044805Z` / `20260927T052637Z` (sampling and budget);
- merger `20260927T060322Z`: incorrectly inherited qwen3-8b 48K chunking
  (170 calls, ~$0.44) instead of Granite context-sized spans.

Only the final run ids in the table above should be used for comparison.
