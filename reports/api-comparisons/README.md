# API-leg comparison reports (Modal-comparable)

Per-run reports for the OpenRouter API leg (SAND-027 Leg B), metric-for-metric
against the Modal/vLLM leg reports kept in the sandbox repo
(`local-mailroom-sandbox/reports/RUN-20-CORRESPONDENCE-AWQ-REPORT.md` etc.).

## Naming schema

    <this dir>/<model_short>/RUN-<wave>-<CLASS>-<MODEL_SHORT>-REPORT.md

| slot | meaning | example |
|---|---|---|
| `model_short/` | decode-profile key, else slugified model id | `qwen3-8b`, `granite-4.2-8b` |
| `wave` | draw size: `--sample` when set, else `--n` | `20`, `50` |
| `CLASS` | subset class uppercased | `CORRESPONDENCE`, `INSURANCE_CLAIM`, `CONTRACT`, `MERGER_AGREEMENT`, `CORPORATE_RECORD`; `ALL` for whole-corpus runs |
| stem | `RUN-<wave>-<CLASS>` | pairs with the Modal report of the same stem |

Pairing rule: **same `RUN-<wave>-<CLASS>` stem = same wave and class**; the
model variant is always the final token. E.g.

    Modal leg: RUN-20-CORRESPONDENCE-AWQ-REPORT.md        (sandbox repo)
    API leg:   RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md   (this repo)

## Comparable metric surface

Each Modal metric has an explicit analog (or an explicit N/A row, so the two
tables share a vocabulary): wall duration, concurrency, cost (roster-priced)
+ cost per document, latency e2e/p50/p95/max, prompt/completion/total tokens,
cost-cap status, docs-ok/total + score metrics, per-agent usage,
per-document score table, decode posture (budgets/sampling/timeout),
dataset provenance + subset-manifest paths. Engine-only metrics (cold boot,
gpu_seconds) are recorded as `N/A (serverless API)`.

## Generation

Reports are emitted automatically by `run_task` whenever `--decode-profile`
is active, before the experiment-log record lands
(`summary.comparison_report` holds the path). Regenerate a smoke artifact
with:

    EVALS_TRACE_BACKEND=none uv run python scripts/run_evals.py \
        --task eval:correspondence --mock --n 2 --decode-profile qwen3-8b

## Canonical draws (issue #20)

Before comparing legs, verify both runs drew the same cases:
`uv run python scripts/draw_subsets.py --check` re-verifies the canonical
manifests under `data/manifests/subset-draws/` (5 classes × {20, 50}, seed
42); diff each run's `subset_manifest.json` (filenames + `doc_text_sha256`)
against the canonical copy.
