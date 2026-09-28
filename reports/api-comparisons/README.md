# API-leg comparison reports (Modal-comparable)

Per-run reports for the OpenRouter API leg (SAND-027 Leg B), metric-for-metric
against the Modal/vLLM leg reports kept in the sandbox repo
(`local-mailroom-sandbox/reports/RUN-20-CORRESPONDENCE-AWQ-REPORT.md` etc.).

## Naming schema

    <this dir>/<model_short>/<task>/runs/<run_id>.md
    <this dir>/<model_short>/<task>/RUN-<wave>-<CLASS>-<MODEL_SHORT>-REPORT.md
    <this dir>/INDEX.md
    <this dir>/API-LEG-MASTER-REPORT.md

| slot | meaning | example |
|---|---|---|
| `model_short/` | decode-profile key, else slugified model id | `qwen3-8b`, `granite-4.2-8b` |
| `task/` | the eval task id — reports are always separated by specialist/task, never flat across a model dir | `contracts`, `insurance_claims`, `correspondence`, `corporate_records`, `merger_agreement`, `classification` |
| `runs/` | immutable per-run write-up (one markdown file per experiment-log run id) | `20260927T033031Z-eval-correspondence.md` |
| `INDEX.md` | catalog of every run write-up + link to its canonical wave stem when present | — |
| `API-LEG-MASTER-REPORT.md` | cross-model master rollup (Qwen vs Granite, superseded runs) | regenerated with the script below |
| `<model>/README.md` | per-model N=20 suite summary (`qwen3-8b`, `granite-4.2-8b`) | — |
| `wave` | draw size: `--sample` when set, else `--n` | `20`, `50` |
| `CLASS` | subset class uppercased | `CORRESPONDENCE`, `INSURANCE_CLAIM`, `CONTRACT`, `MERGER_AGREEMENT`, `CORPORATE_RECORD`; `ALL` for whole-corpus runs |
| stem | `RUN-<wave>-<CLASS>` | pairs with the Modal report of the same stem |

E.g. `qwen3-8b/insurance_claims/RUN-20-INSURANCE_CLAIM-QWEN3-8B-REPORT.md`.

Pairing rule: **same `RUN-<wave>-<CLASS>` stem = same wave and class**; the
model variant is always the final token. E.g.

    Modal leg: RUN-20-CORRESPONDENCE-AWQ-REPORT.md                              (sandbox repo)
    API leg:   qwen3-8b/correspondence/RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md (this repo)

## Comparable metric surface

Each Modal metric has an explicit analog (or an explicit N/A row, so the two
tables share a vocabulary): wall duration, concurrency, **expected cost**
(wave planning from the decode profile), **actual cost** (sum of per-case
`cost_usd` from the run), **estimated cost** (roster token rates on aggregate
usage), cost per document (actual + estimated), latency e2e/p50/p95/max,
prompt/completion/total tokens, cost-cap status, docs-ok/total + score
metrics, per-agent usage, per-document score table, **run configuration**
(concurrency/seed/scorer/trace), **runtime performance** (duration + latency
rollups), decode posture (budgets/sampling/timeout), dataset provenance +
subset-manifest paths. Engine-only metrics (cold boot, gpu_seconds) are
recorded as `N/A (serverless API)`.

Sandbox-parity narrative blocks (same vocabulary as
`mailroom-sandbox/scripts/sand032/report.py`):

- **Analyst insights & findings** — concurrency efficiency, tail latency,
  prompt-length correlation, subclass spread, field-F1 zeros
- **Scoring method** — CUAD / MAUD context for contracts and merger tasks
- **Strata (subclass)** — mean overall by expected subclass
- **Reproduce** / **Artifacts** — CLI replay and on-disk paths

SVG figures stay in the Modal sandbox repo; API-leg reports use strata +
per-document tables as the figure table views.

## Generation

Reports are emitted automatically by `run_task` whenever `--decode-profile`
is active **or** the run is a substantive real eval wave (n≥20), before the
experiment-log record lands (`summary.comparison_report` holds the path).
Backfill or refresh **all** report-worthy runs, `INDEX.md`, model suite READMEs,
and the master rollup with:

    uv run python scripts/render_comparison_reports.py

Regenerate a smoke artifact with:

    EVALS_TRACE_BACKEND=none uv run python scripts/run_evals.py \
        --task eval:correspondence --mock --n 2 --decode-profile qwen3-8b

## Canonical draws (issue #20)

Before comparing legs, verify both runs drew the same cases:
`uv run python scripts/draw_subsets.py --check` re-verifies the canonical
manifests under `data/manifests/subset-draws/` (5 classes × {20, 50}, seed
42); diff each run's `subset_manifest.json` (filenames + `doc_text_sha256`)
against the canonical copy.
