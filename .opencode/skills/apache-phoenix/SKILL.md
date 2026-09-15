---
name: apache-phoenix
description: Local Arize Phoenix tracing for mailroom-evals (cost-free default sink). Use when BRAINTRUST_API_KEY is absent, --trace-backend phoenix is passed, or the user wants local OpenTelemetry spans inspected.
---

# Apache Phoenix (local, cost-free default)

Phoenix is the fallback sink when no `BRAINTRUST_API_KEY` is configured and
the explicit zero-spend choice with `--trace-backend phoenix`.

## Run the server

```bash
phoenix serve   # or: arize-phoenix — serves http://localhost:6006
open http://localhost:6006
```

## How this repo uses it

- `evals.tracing` activates `mailroom.observability.phoenix_setup`:
  OpenTelemetry `TracerProvider` + OTLP HTTP exporter to `PHOENIX_ENDPOINT`
  (default `http://localhost:6006/v1/traces`), resource
  `openinference.project.name=mailroom-evals`.
- The runner sets `OBSERVABILITY_PROVIDER=phoenix` so the OpenInference
  `OpenAIInstrumentor` auto-traces every LLM call (model, tokens, latency).
- One OTel span per case with attributes: `evals.run_id`, `evals.task`,
  `evals.case_id`, `evals.subset`, `evals.invoke`, `evals.model`,
  `evals.prompt_version` — filterable in the Phoenix UI.
- `evals.tracing.flush()` force-flushes the batch processor per case;
  failures log warnings, never break the run.

## Environment

```text
PHOENIX_TRACING=enabled        # default
PHOENIX_ENDPOINT=http://localhost:6006/v1/traces
PHOENIX_SERVICE_NAME=mailroom-evals
PHOENIX_PROJECT=mailroom-evals
```

## Boundaries

Phoenix stores locally (SQLite) — delete the DB when a batch is done.
Pytest forces tracing off (`EVALS_TRACE_BACKEND=none`).
