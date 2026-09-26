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
- One root span per case: name = the task's node observation name
  (e.g. `classify-document`), `input` = curated case summary (ids + class +
  chars, never raw doc text), `output` = prediction + scores, `metadata` =
  run_id, dataset config/split/revision, subset, invoke mode, model,
  prompt_version. Scorer results: span `metrics` use `ESSENTIAL_SCORES`;
  Experiment `scores` use `sink_score_metrics` (≤2 headline metrics per case).
  Dataset rows upsert on `doc_text_sha256` with HF repo/revision metadata.
- `evals.tracing.flush()` after each case; `flush_health()` counters surface
  dropped events (never fail a run on tracing errors).

## Reading results

```bash
# Spans land in project mailroom-evals → Logs/Traces, filter metadata.run_id
```

Cross-reference: every experiment-log record carries the same `run_id` and
trace ids, so log rows ↔ traces are joinable.

## Boundaries

Pytest forces tracing off (`EVALS_TRACE_BACKEND=none`). Braintrust is never
used for prompt management here — prompt versions ride `metadata.prompt_version`.
