# SAND-027 API leg — master comparison report

Generated: `2026-09-27T09:08:54Z` from `reports/experiment_log.jsonl` via `scripts/render_comparison_reports.py`.

Use this file for cross-model Leg B summaries; drill into per-run detail via the linked canonical stems or [INDEX.md](INDEX.md) (every report-worthy run).

## Model suite rollups

| model | README | master table |
|---|---|---|
| Qwen 3 8B | [qwen3-8b/README.md](qwen3-8b/README.md) | below |
| Granite 4.2 8B | [granite-4.2-8b/README.md](granite-4.2-8b/README.md) | below |

## qwen3-8b — canonical N=20

| task | run_id | result | calls | cost est | report |
|---|---|---:|---:|---:|---|
| correspondence | `20260927T033031Z-eval-correspondence` | overall 0.5130 | 39 | $0.060362 | [RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md](qwen3-8b/correspondence/RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md) |
| insurance claims | `20260927T035135Z-eval-insurance_claims` | overall 0.7488 | 37 | $0.032040 | [RUN-20-INSURANCE_CLAIM-QWEN3-8B-REPORT.md](qwen3-8b/insurance_claims/RUN-20-INSURANCE_CLAIM-QWEN3-8B-REPORT.md) |
| contracts | `20260927T035621Z-eval-contracts` | overall 0.6169 | 44 | $0.114086 | [RUN-20-CONTRACT-QWEN3-8B-REPORT.md](qwen3-8b/contracts/RUN-20-CONTRACT-QWEN3-8B-REPORT.md) |
| merger agreements | `20260927T022750Z-eval-merger_agreement` | overall 0.3748 | 18 | $0.057522 | [RUN-20-MERGER_AGREEMENT-QWEN3-8B-REPORT.md](qwen3-8b/merger_agreement/RUN-20-MERGER_AGREEMENT-QWEN3-8B-REPORT.md) |
| corporate records | `20260927T042239Z-eval-corporate_records` | overall 0.4004 | 34 | $0.060215 | [RUN-20-CORPORATE_RECORD-QWEN3-8B-REPORT.md](qwen3-8b/corporate_records/RUN-20-CORPORATE_RECORD-QWEN3-8B-REPORT.md) |
| sorter / classification | `20260927T043145Z-eval-classification` | class 0.7000; subclass 0.0500 | 150 | $0.149264 | [RUN-20-FULL-QWEN3-8B-REPORT.md](qwen3-8b/classification/RUN-20-FULL-QWEN3-8B-REPORT.md) |

## granite-4.2-8b — canonical N=20

| task | run_id | result | calls | cost est | report |
|---|---|---:|---:|---:|---|
| correspondence | `20260927T053647Z-eval-correspondence` | overall 0.4065 | 20 | $0.029194 | [RUN-20-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md](granite-4.2-8b/correspondence/RUN-20-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md) |
| insurance claims | `20260927T054211Z-eval-insurance_claims` | overall 0.7135 | 20 | $0.024711 | [RUN-20-INSURANCE_CLAIM-GRANITE-4.2-8B-REPORT.md](granite-4.2-8b/insurance_claims/RUN-20-INSURANCE_CLAIM-GRANITE-4.2-8B-REPORT.md) |
| contracts | `20260927T054738Z-eval-contracts` | overall 0.4769 | 24 | $0.073964 | [RUN-20-CONTRACT-GRANITE-4.2-8B-REPORT.md](granite-4.2-8b/contracts/RUN-20-CONTRACT-GRANITE-4.2-8B-REPORT.md) |
| merger agreements | `20260927T082404Z-eval-merger_agreement` | overall 0.4548 | 38 | $0.177431 | [RUN-20-MERGER_AGREEMENT-GRANITE-4.2-8B-REPORT.md](granite-4.2-8b/merger_agreement/RUN-20-MERGER_AGREEMENT-GRANITE-4.2-8B-REPORT.md) |
| corporate records | `20260927T065622Z-eval-corporate_records` | overall 0.4156 | 22 | $0.043637 | [RUN-20-CORPORATE_RECORD-GRANITE-4.2-8B-REPORT.md](granite-4.2-8b/corporate_records/RUN-20-CORPORATE_RECORD-GRANITE-4.2-8B-REPORT.md) |
| sorter / classification | `20260927T070900Z-eval-classification` | class 0.9000; subclass 0.6000 | 118 | $0.064366 | [RUN-20-FULL-GRANITE-4.2-8B-REPORT.md](granite-4.2-8b/classification/RUN-20-FULL-GRANITE-4.2-8B-REPORT.md) |

## Paired comparison (Granite − Qwen, same seed-42 draws)

| task | Qwen 3 8B | Granite 4.2 8B | delta |
|---|---:|---:|---:|
| correspondence | 0.5130 | 0.4065 | -0.1065 |
| insurance claims | 0.7488 | 0.7135 | -0.0353 |
| contracts | 0.6169 | 0.4769 | -0.1400 |
| merger agreements | 0.3748 | 0.4548 | +0.0800 |
| corporate records | 0.4004 | 0.4156 | +0.0152 |
| sorter / classification (class accuracy) | class 0.7000 | class 0.9000 | +0.2000 |
| sorter / classification (subclass accuracy) | 0.0500 | 0.6000 | +0.5500 |

## Superseded runs (append-only log; do not use for pairing)

- `RUN-1-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md`: **final** `20260927T051851Z-eval-correspondence`; superseded `20260927T051725Z-eval-correspondence`
- `RUN-20-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md`: **final** `20260927T053647Z-eval-correspondence`; superseded `20260927T052637Z-eval-correspondence`, `20260927T044805Z-eval-correspondence`
- `RUN-20-MERGER_AGREEMENT-GRANITE-4.2-8B-REPORT.md`: **final** `20260927T082404Z-eval-merger_agreement`; superseded `20260927T060322Z-eval-merger_agreement`
- `RUN-20-CONTRACT-QWEN3-8B-REPORT.md`: **final** `20260927T035621Z-eval-contracts`; superseded `20260927T023347Z-eval-contracts`, `20260926T235347Z-eval-contracts`
- `RUN-20-CORPORATE_RECORD-QWEN3-8B-REPORT.md`: **final** `20260927T042239Z-eval-corporate_records`; superseded `20260927T022810Z-eval-corporate_records`
- `RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md`: **final** `20260927T033031Z-eval-correspondence`; superseded `20260927T022738Z-eval-correspondence`, `20260926T234358Z-eval-correspondence`
- `RUN-20-INSURANCE_CLAIM-QWEN3-8B-REPORT.md`: **final** `20260927T035135Z-eval-insurance_claims`; superseded `20260927T023050Z-eval-insurance_claims`, `20260926T234603Z-eval-insurance_claims`
- `RUN-2-MERGER_AGREEMENT-QWEN3-8B-REPORT.md`: **final** `20260927T020724Z-eval-merger_agreement`; superseded `20260927T014814Z-eval-merger_agreement`
- `RUN-20-MERGER_AGREEMENT-QWEN3-8B-REPORT.md`: **final** `20260927T022750Z-eval-merger_agreement`; superseded `20260927T011209Z-eval-merger_agreement`, `20260927T005233Z-eval-merger_agreement`, `20260927T004231Z-eval-merger_agreement`

## Runbook

- OpenRouter + Braintrust: [docs/openrouter-braintrust-runbook.md](../../docs/openrouter-braintrust-runbook.md)
- One coverage call vs chunking: runbook §5; comparison reports include call-count sanity caveats.
