# Experiment log — schema v1 reference

The centralized, append-only experiment log. One record schema
(`schemas/experiment_record.v1.json`, `schema_version: 1`) for every task
family (`eval`, `pilot`, `calibration`).

## Storage layout

| path | contents | env override |
|---|---|---|
| `reports/experiment_log.jsonl` | THE index — one line per RUN (summary + pointers) | `EXPERIMENT_LOG_PATH` |
| `reports/experiment_log.md` | rendered human-readable tables, rebuildable | `EXPERIMENT_LOG_MD_PATH` |
| `data/experiments/<run_id>/cases.jsonl` | one line per CASE (full fidelity) | `EVALS_EXPERIMENTS_DIR` |
| `data/experiments/<run_id>/summary.json` | the same run-summary record, self-contained | `EVALS_EXPERIMENTS_DIR` |

## Run-summary record

| key | type | notes |
|---|---|---|
| `schema_version` | `1` | bump on schema change (same commit updates `schemas/` + skill) |
| `record_kind` | `"run_summary"` | |
| `run_id` | string | `<UTC stamp>-<family>-<task>` |
| `family` | `eval \| pilot \| calibration` | |
| `task` | string | registry task name |
| `invoke` | `node \| agent` | |
| `mode` | `mock \| real` | |
| `model` | string\|null | recorded override or pipeline default |
| `prompt_version` | string\|null | the A/B dimension |
| `trace_backend` | `braintrust \| phoenix \| none` | |
| `trace_ids` | object\|null | backend, project/endpoint — log rows ↔ traces join here |
| `dataset` | object | `repo, config, split, revision, subset, n_selected, n_total, seed` |
| `git` | object | `commit, dirty` at run time |
| `started_at` / `finished_at` / `duration_s` | | ISO-8601 UTC / seconds |
| `params` | object | concurrency, sample, seed, n, dry_run, scorer, `resumed_from`, `skipped_already_run` |
| `metrics` | object | task-specific means + `n` + `errors` |
| `performance` | object | `latency_ms_mean, latency_ms_p95, tokens_prompt_total, tokens_completion_total, cost_usd_est_total` |
| `calibration` | object\|null | family=calibration only: `reliability_table, ece, cell_confusion, threshold_curve, recommended_thresholds, caveats, report_paths` |
| `cases_ref` | string | path to the run's `cases.jsonl` |
| `cases_embedded` | array | case rows inlined when n ≤ 50, else `[]` |
| `error` | string\|null | run-level failure (case-level errors live in case rows) |

## Case row

| key | notes |
|---|---|
| `run_id`, `case_id`, `filename` | identity |
| `expected_doc_class`, `expected_subclass` | ground truth echo |
| `review_expected`, `retry_expected`, `fixture_kind`, `fixture_cell`, `fixture_outcome`, `failure_stage` | fixture/calibration provenance |
| `prediction` | the node/agent output (curated) |
| `scores` | deterministic scorer output |
| `latency_ms`, `tokens`, `cost_usd` | performance |
| `trace` | reserved for per-case trace ids |
| `error` | case-level failure |

## Guarantees

- **Append-only.** Never edit old records; add a follow-up record. A torn
  tail (crashed append) is tolerated on load, never rewritten silently.
- **Every run logs** — including failures and mock runs (`error` field set).
- **Machine**: `pandas.json_normalize(jsonl, sep=".")` works directly;
  `evals.experiment_log.load_runs()` / `load_cases(run_id)` /
  `export_run(run_id, "csv"|"parquet")`.
- **Human**: markdown is tables only; rebuild with
  `uv run python scripts/render_experiment_log.py`; validate with `--validate`.

## CLI

```bash
uv run python scripts/render_experiment_log.py --validate   # schema-check every line
uv run python scripts/render_experiment_log.py              # rebuild markdown
uv run python scripts/run_evals.py --task eval:classify --export csv    # export case rows
```
