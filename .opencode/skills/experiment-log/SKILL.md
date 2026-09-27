---
name: experiment-log
description: The centralized append-only experiment log for mailroom-evals — schema v1 record shape, storage layout, loaders, and the markdown renderer. Use when writing run results, reading past runs, validating records, or extending the schema.
---

# Experiment log

One canonical, versioned record schema for ALL task families (`eval`,
`pilot`, `calibration`). Append-only; never overwrite. Current schema:
**v3** (`schemas/experiment_record.v3.json`) — v1/v2 records remain valid.

## Storage layout

```text
reports/experiment_log.jsonl      # THE index — one line per RUN (summary + pointers)
reports/experiment_log.md         # human-readable tables, rebuildable from the JSONL
data/experiments/<run_id>/cases.jsonl   # one line per CASE (full fidelity)
data/experiments/<run_id>/summary.json  # same run-summary record, self-contained
data/experiments/<run_id>/prompts_snapshot.json  # exact rendered prompts used
data/experiments/<run_id>/subset_manifest.json{l,}  # locked case set (v3)
data/experiments/<run_id>/scoring_suite.json        # full deterministic rollup (v3)
data/experiments/<run_id>/judgments.jsonl        # post-hoc judge verdicts (v2)
data/experiments/<run_id>/rescored.jsonl         # --recompute output (v2)
schemas/experiment_record.v3.json # JSON Schema for validation (v1/v2 records valid)
```

Paths overridable: `EXPERIMENT_LOG_PATH`, `EXPERIMENT_LOG_MD_PATH`,
`EVALS_EXPERIMENTS_DIR`. Tests redirect all three to tmp dirs.

## Run-summary record (schema v3)

`schema_version`, `record_kind="run_summary"`, `run_id`
(`<UTC stamp>-<family>-<task>`), `family`, `task`, `invoke` (node|agent),
`mode` (mock|real), `model`, `prompt_version`, `prompt_lineage`
(frozen|mutation|live-docclass|production), `prompt_source`,
`prompt_versions` (per-agent key/lineage/sha256), `pipeline_git`,
`prompts_snapshot_path`, `trace_backend`,
`trace_ids` (project/session), `dataset` (repo/config/split/revision/subset/
n_selected/n_total/seed; **v3:** `case_ids`, `filenames`,
`subset_manifest_path`, `subset_manifest_jsonl` — the locked case set),
`git` (commit/dirty), `started_at`/`finished_at`/
`duration_s`, `params`, `metrics` (task-specific), `performance`
(latency_ms mean/p95, token totals, cost_usd_est, `by_agent` per-agent
calls/tokens/models/cost), `calibration` (family=
calibration only: cells, ece, recommended_thresholds), `judging` (v2:
post-hoc local judge block — dimensions, judge_model, mock, metrics,
judgments_ref), **v3:** `preflight` (the preflight report: ok/checks/
issues/resolved — written even for blocked runs), `task_framing` (the
eval-task contract framing), `scoring_suite` (pointer to the full
deterministic rollup artifact), `flush` (affirmative sink-flush counters),
`cases_ref`,
`cases_embedded` (rows inlined when n ≤ 50, else empty).

## Case row

`run_id`, `case_id`, `filename`, `expected*` fields, `doc_text_sha256`
(v2: the post-hoc text re-load integrity key), `prediction`, `scores`,
`latency_ms`, `tokens`, `cost_usd`, `agent_usage` (v3: per-agent
calls/tokens/models attribution — non-negotiable #9), `trace` (trace/span
ids), `error`.

## Guarantees

- **Machine**: strict JSONL; `schema_version` on every record; flat dotted
  keys → `pandas.json_normalize`-ready; `load_runs()` / `load_cases(run_id)`;
  optional `--export parquet|csv`.
- **Human**: markdown is TABLES only (never raw JSON dumps); floats 4dp,
  bools ✓/✗; rebuilt idempotently via `scripts/render_experiment_log.py`.
- **Traced**: every record carries Braintrust/Phoenix trace ids so log rows ↔
  traces cross-reference.

## Discipline

Append ONE summary line per run even when the run fails (record the error).
Never edit history — add a follow-up record. Schema changes bump
`schema_version` and update `schemas/` + this skill in the same commit.

**Viewer snapshot**: `reports/experiment_log.jsonl` is tracked. The Vercel
viewer also reads `web/data/snapshot.json`. Whenever the log changes, re-run
`scripts/export_site_snapshot.py` and commit the log + snapshot together
(`--check` exits 1 if stale).
