# AGENTS.md

mailroom-evals: evaluation tasks, pilot scenarios, and calibration suites for
the llm-mailroom LangGraph pipeline, traced to Braintrust or Arize Phoenix,
logged to one centralized append-only experiment log. Python 3.11+, uv.

## Skills (all agents)

Read **`.opencode/skills/eval-tool-router/SKILL.md` first**, then exactly one
specialty skill:

- **mailroom-corpus** — schema v8 configs, subset grammar, GT columns, pinned revision
- **braintrust** / **apache-phoenix** — the two trace sinks (never Langfuse here)
- **experiment-log** — the record schema, storage layout, render/validate discipline
- **calibration** — the fixtures grid + per-node calibration methodology
- **pipeline-internals** — node fns, `DocumentState` construction, isolation rules
- **eval-engineering** — how to design and register a NEW task

## Non-negotiables

1. **Every run logs.** One run-summary line to `reports/experiment_log.jsonl`
   per run — including failures and mock runs. No exceptions.
2. **Pin the corpus.** Revision `eafe1ab4c0d330d8f9c7a5fb254155e75d290828`.
   Join `ground_truth` ⇆ `default` on `filename`; never zip positionally.
3. **Mock before real.** `--mock` must never touch the network. `--real`
   requires `OPENROUTER_API_KEY`.
4. **Isolate the base dir.** Every run sets `MAILROOM_BASE_DIR` to a temp dir;
   pipeline_chain drains daemon threads before restoring it. Never eval
   against a live data dir.
5. **Trace, never break.** Tracing failures log warnings; a run never fails
   because its sink is down.
6. **Calibration is report-only.** Threshold recommendations land in
   `reports/calibration/` — never auto-write pipeline configs.
7. **History is append-only.** Never edit old experiment-log records; add a
   follow-up record. Schema changes bump `schema_version` + update
   `schemas/` + the experiment-log skill in the same commit.

## Commands

```bash
uv sync --extra dev                                  # install
uv run python scripts/run_evals.py --list            # task catalog
uv run python scripts/run_evals.py --task all --mock --n 2   # CI smoke
uv run python scripts/run_evals.py --task eval:classification --mock --n 3
uv run python scripts/run_evals.py --task pilot:pipeline_chain --mock
uv run python scripts/run_evals.py --task calibration:classify --real
uv run python scripts/run_evals.py --task eval:insurance_claims --real \
    --subset class:insurance_claim --sample 25 --seed 42
uv run python scripts/run_evals.py --task <id> --resume <run_id>     # continue an interrupted run
uv run pytest tests/ -q                              # hermetic test suite (49 tests)
uv run python scripts/render_experiment_log.py --validate
uv run python scripts/render_experiment_log.py       # rebuild markdown
```

## Environment

| variable | note |
|---|---|
| `OPENROUTER_API_KEY` | real runs |
| `BRAINTRUST_API_KEY` / `BRAINTRUST_PROJECT` | Braintrust sink (auto when set) |
| `PHOENIX_ENDPOINT` / `PHOENIX_PROJECT` | Phoenix sink (local default) |
| `EVALS_TRACE_BACKEND` | `auto` default; `none` in tests |
| `EXPERIMENT_LOG_PATH` / `EXPERIMENT_LOG_MD_PATH` / `EVALS_EXPERIMENTS_DIR` | tests redirect all three |

`OBSERVABILITY_PROVIDER` and `MAILROOM_BASE_DIR` are set BY the runner — do
not export them in shells or `.env`.

## Subagents

`.opencode/agents/` — delegate when the task matches:

- **eval-runner** — executes run_evals.py commands, monitors long runs, triages failures
- **corpus-curator** — subset resolution, GT interpretation, load debugging
- **trace-auditor** — post-run trace verification against the checklist
- **calibration-analyst** — turns calibration reports into threshold recommendations
- **experiment-log-sync** — validates/renders/compares the experiment log

## Adding a task

Follow `.opencode/skills/eval-engineering/SKILL.md`: register a `TaskSpec` in
`src/evals/registry.py`, implement invocation in `src/evals/invoke.py` (both
modes unless procedural), scoring in `src/evals/scoring.py`, then mock smoke
(`--mock --n 3`) before any real run. One-off scripts outside the registry
are not acceptable.
