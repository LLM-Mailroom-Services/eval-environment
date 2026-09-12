---
name: experiment-log
description: The centralized append-only experiment log for mailroom-evals — schema v1 record shape, storage layout, loaders, and the markdown renderer. Use when writing run results, reading past runs, validating records, or extending the schema.
---

# Experiment log

One canonical, versioned record schema for ALL task families (`eval`,
`pilot`, `calibration`). Append-only; never overwrite. Current schema:
**v2** (`schemas/experiment_record.v2.json`) — v1 records remain valid.

## Storage layout

```
reports/experiment_log.jsonl      # THE index — one line per RUN (summary + pointers)
reports/experiment_log.md         # human-readable tables, rebuildable from the JSONL
data/experiments/<run_id>/cases.jsonl   # one line per CASE (full fidelity)
data/experiments/<run_id>/summary.json  # same run-summary record, self-contained
data/experiments/<run_id>/prompts_snapshot.json  # exact rendered prompts used
data/experiments/<run_id>/judgments.jsonl        # post-hoc judge verdicts (v2)
data/experiments/<run_id>/rescored.jsonl         # --recompute output (v2)
schemas/experiment_record.v2.json # JSON Schema for validation (v1 records valid)
```

Paths overridable: `EXPERIMENT_LOG_PATH`, `EXPERIMENT_LOG_MD_PATH`,
`EVALS_EXPERIMENTS_DIR`. Tests redirect all three to tmp dirs.

## Run-summary record (schema v2)

`schema_version`, `record_kind="run_summary"`, `run_id`
(`<UTC stamp>-<family>-<task>`), `family`, `task`, `invoke` (node|agent),
`mode` (mock|real), `model`, `prompt_version`, `prompt_lineage`
(frozen|mutation|live-docclass|production), `prompt_source`,
`prompt_versions` (per-agent key/lineage/sha256), `pipeline_git`,
`prompts_snapshot_path`, `trace_backend`,
`trace_ids` (project/session), `dataset` (repo/config/split/revision/subset/
n_selected/n_total/seed), `git` (commit/dirty), `started_at`/`finished_at`/
`duration_s`, `params`, `metrics` (task-specific), `performance`
(latency_ms mean/p95, token totals, cost_usd_est), `calibration` (family=
calibration only: cells, ece, recommended_thresholds), `judging` (v2:
post-hoc local judge block — dimensions, judge_model, mock, metrics,
judgments_ref), `cases_ref`,
`cases_embedded` (rows inlined when n ≤ 50, else empty).

## Case row

`run_id`, `case_id`, `filename`, `expected*` fields, `doc_text_sha256`
(v2: the post-hoc text re-load integrity key), `prediction`, `scores`,
`latency_ms`, `tokens`, `cost_usd`, `trace` (trace/span ids), `error`.

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
