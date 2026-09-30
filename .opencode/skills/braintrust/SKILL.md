---
name: braintrust
description: Braintrust trace sink and eval logging for mailroom-evals. Use when BRAINTRUST_API_KEY is set, --trace-backend braintrust is passed, or the user wants spans/scores inspected in Braintrust.
---

# Braintrace sink (Braintrust)

mailroom-evals default sink order: **Braintrust (key set) → Phoenix → none**.
`evals.tracing.resolve_backend()` implements it; `--trace-backend` overrides.

## Enable

```bash
BRAINTRUST_API_KEY=...        # required
BRAINTRUST_PROJECT=mailroom-evals   # default project for eval runs
```

## How this repo uses it

- `evals.tracing` initializes via `mailroom.observability.braintrust_setup.configure()`
  (`init_logger` → nested LLM spans). Real eval runs also open a per-run
  **Experiment** via `evals.braintrust_experiment` (`braintrust.init` +
  `init_dataset`) linked to the pinned HF corpus (`BRAINTRUST_EXPERIMENTS=auto`,
  disable with `BRAINTRUST_EXPERIMENTS=off`).
- The runner sets `OBSERVABILITY_PROVIDER=braintrust` so llm-mailroom's
  `llm/client.py:get_llm` wraps the OpenAI client (`braintrust.wrap_openai`)
  and every LLM call auto-logs as a `type=llm` span.
- One **Experiment row per specialist call** (20 docs → 20 specialist
  rows). Documents are not inserted as Dataset rows. The parent span is
  named for the specialist (`merger_agreement_specialist`, …) or the
  node when there is no specialist. Nested LLM spans stay children.
  Scores attach via `span.log` — never a second `Experiment.log`.
  `input` = curated case summary (ids + chars, never raw doc text).
  Pipeline nodes (`extract-fields`, classify, …) must not appear as
  sibling rows on specialist evals.
- `evals.tracing.flush()` after each case; `flush_health()` counters surface
  dropped events (never fail a run on tracing errors).

## Reading results

```bash
# Spans land in project mailroom-evals → Logs/Traces, filter metadata.run_id
```

Cross-reference: every experiment-log record carries the same `run_id` and
trace ids, so log rows ↔ traces are joinable.

GEPA OBSERVE pulls the specialist backlog from Braintrust readonly experiments
(experiment name = `run_id`) via `evals.gepa.braintrust_backlog` /
`scripts/gepa_observe_specialists.py --braintrust-backlog` (eval roots + nested
LLM reasoning excerpts; never raw document text).

## Boundaries

Pytest forces tracing off (`EVALS_TRACE_BACKEND=none`). Braintrust is never
used for prompt management here — prompt versions ride `metadata.prompt_version`.
