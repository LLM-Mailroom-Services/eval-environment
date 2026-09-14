# AGENTS.md

mailroom-evals: evaluation tasks, pilot scenarios, and calibration suites for
the llm-mailroom LangGraph pipeline, traced to Braintrust or Arize Phoenix,
logged to one centralized append-only experiment log. Python 3.11+, uv.

## Skills (all agents)

Read **`.opencode/skills/eval-tool-router/SKILL.md` first**, then exactly one
specialty skill:

- **mailroom-corpus** — schema v9 configs (`mailroom-dataset`, successor of the frozen v8 `mailroom-corpus`), subset grammar, GT columns (incl. the nested `gt_fields` payload), pinned revision
- **braintrust** / **apache-phoenix** — the two trace sinks (never Langfuse here)
- **experiment-log** — the record schema, storage layout, render/validate discipline
- **calibration** — the fixtures grid + per-node calibration methodology
- **pipeline-internals** — node fns, `DocumentState` construction, isolation rules
- **eval-engineering** — how to design and register a NEW task
- **prompt-lineage** — the frozen v1 snapshot, injection choke points, GEPA gates

## Non-negotiables

1. **Every run logs.** One run-summary line to `reports/experiment_log.jsonl`
   per run — including failures and mock runs. No exceptions.
2. **Pin the corpus.** Repo `Lucius-Morningstar/mailroom-dataset` (schema v9),
   revision `46a4d3c240a36671cde0182fff4960f6b8b73aca` (the GT-closure
   republish of 2026-09-13; the v8 parent
   `mailroom-corpus` @ `eafe1ab4c0d330d8f9c7a5fb254155e75d290828` stays frozen
   for lineage reference). Join `ground_truth` ⇆ `default` on `filename`; never
   zip positionally; expand the nested `gt_fields` JSON payload before scoring.
3. **Mock before real.** `--mock` must never touch the network. `--real`
   requires a configured LLM provider: `OPENROUTER_API_KEY` (primary), or
   the repo `.env` routing through the Vercel AI Gateway as an alternative
   (`DEFAULT_PROVIDER=generic` + `GENERIC_BASE_URL` + `GENERIC_API_KEY` —
   loaded by `evals/__init__`, real environment always wins).
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
8. **Sinks score essentials only.** `ESSENTIAL_SCORES` (scoring.py) is the
   complete span-metric surface; the full suite is post-hoc
   (`scripts/score_run.py`, `scripts/compare_runs.py`) — never re-add
   full-score forwarding to spans.
9. **Per-agent performance is cataloged.** Every case row carries
   `agent_usage` (per-agent calls/tokens/models) and every run summary
   `performance.by_agent` with estimated cost — sourced from the pipeline
   usage accumulator (`pipeline.limits.record_usage(..., agent=...)`).
   `AGENT_CATALOG` (registry.py) maps every evaluated node to its agents.
9. **Frozen lineage is immutable.** Never edit `src/evals/prompts/frozen_v1.py`
   or `prompts/*.md` by hand; mutations append via
   `evals.prompts.mutations.apply_mutation` (four gates, one rule per A/B).
   Drift-check with `scripts/freeze_prompts.py --check`.
10. **Refresh the viewer snapshot.** When the experiment log changes,
    re-run `scripts/export_site_snapshot.py` and commit
    `web/data/snapshot.json` — the Vercel viewer reads only that file.

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
uv run python scripts/score_run.py --run-id <run_id> --recompute     # post-hoc deterministic re-score
uv run python scripts/score_run.py --run-id <run_id> --judge verdict,quality --mock  # local judges
uv run python scripts/score_run.py --run-id <run_id> --export-failures data/manifests/x.jsonl  # GEPA OBSERVE
uv run python scripts/compare_runs.py --a <run_a> --b <run_b> --md reports/comparisons/  # A/B + CIs
uv run python scripts/freeze_prompts.py --check      # prompt lineage drift check
uv run python scripts/export_site_snapshot.py        # refresh the Vercel viewer snapshot
uv run python scripts/export_site_snapshot.py --check  # exit 1 if snapshot is stale
node scripts/viewer_smoke.js                         # headless viewer regression check (needs node)
uv run pytest tests/ -q                              # hermetic test suite (124 tests)
uv run python scripts/render_experiment_log.py --validate
uv run python scripts/render_experiment_log.py       # rebuild markdown
```

## Environment

| variable | note |
|---|---|
| `OPENROUTER_API_KEY` | real runs (primary provider) |
| `DEFAULT_PROVIDER` / `GENERIC_BASE_URL` / `GENERIC_API_KEY` | optional alternative via the repo `.env`: Vercel AI Gateway (OpenAI-compatible; model IDs pass through, e.g. `openai/gpt-4o`) |
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
- **prompt-engineer** — GEPA iteration loop over the frozen lineage (see also PROMPT_ENGINEER_GEPA_PROVENANCE.md)

## Adding a task

Follow `.opencode/skills/eval-engineering/SKILL.md`: register a `TaskSpec` in
`src/evals/registry.py`, implement invocation in `src/evals/invoke.py` (both
modes unless procedural), scoring in `src/evals/scoring.py`, then mock smoke
(`--mock --n 3`) before any real run. One-off scripts outside the registry
are not acceptable.
