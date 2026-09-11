"""Trace-sink resolution and per-case spans for eval runs.

Backend order (default ``auto``): **Braintrust** when ``BRAINTRUST_API_KEY``
is set, else **local Arize Phoenix** (cost-free), else ``none``. Explicit
``--trace-backend braintrust|phoenix|none`` (env ``EVALS_TRACE_BACKEND``)
overrides. Langfuse is intentionally NOT a sink here — issue #7 names
Phoenix and/or Braintrust as the preferences.

The runner sets ``OBSERVABILITY_PROVIDER`` to the resolved backend BEFORE the
first agent instantiation so llm-mailroom's ``llm/client.get_llm`` wraps the
OpenAI client with the matching instrumentation — every LLM call inside a
node/agent invocation auto-traces.

One root span per case, named after the node's stable observation name
(`classify-document`, `extract-fields`, …). Input/output are CURATED
(identifiers + scores, never raw document text). Scorer metrics attach to
the span (Braintrust ``log(metrics=...)`` / Phoenix span attributes).
Tracing failures log warnings and never fail a run.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Self

import structlog

logger = structlog.get_logger(__name__)

BACKENDS = ("auto", "braintrust", "phoenix", "none")

# Node observation names mirrored from llm-mailroom's
# observability.tracing.NODE_OBSERVATION_TYPES so spans read identically
# across pipeline runs and eval runs.
NODE_OBSERVATION_TYPES: dict[str, str] = {
    "intake-document": "span",
    "classify-document": "agent",
    "extract-fields": "agent",
    "judge-verify": "evaluator",
    "arbitrate-verdict": "agent",
    "adjudicate-conflict": "agent",
    "archive-document": "span",
    "document-pipeline": "chain",
}


def resolve_backend(explicit: str | None = None) -> str:
    """Resolve the active trace backend: braintrust | phoenix | none."""
    choice = (explicit or os.environ.get("EVALS_TRACE_BACKEND") or "auto").strip().lower()
    if choice not in BACKENDS:
        raise ValueError(f"unknown trace backend {choice!r}; known: {BACKENDS}")
    if choice != "auto":
        return choice
    if os.environ.get("BRAINTRUST_API_KEY"):
        return "braintrust"
    if os.environ.get("PHOENIX_TRACING", "enabled").strip().lower() in (
        "1", "true", "enabled", "yes", "on"
    ):
        return "phoenix"
    return "none"


def apply_provider_env(backend: str) -> None:
    """Point llm-mailroom's tracing facade at the resolved backend.

    Must run BEFORE any agent/client construction so ``get_llm`` wraps the
    OpenAI client with the matching instrumentation.
    """
    if backend in ("braintrust", "phoenix"):
        os.environ["OBSERVABILITY_PROVIDER"] = backend
    elif backend == "none":
        os.environ["OBSERVABILITY_PROVIDER"] = "none"


def configure(backend: str) -> bool:
    """Initialize the backend (Braintrust logger / Phoenix OTel). Idempotent."""
    if backend == "braintrust":
        try:
            from observability.braintrust_setup import configure as bt_configure

            return bool(bt_configure())
        except Exception:
            logger.warning("evals_braintrust_configure_failed", exc_info=True)
            return False
    if backend == "phoenix":
        try:
            from observability.phoenix_setup import instrument_openai_client

            instrument_openai_client(None)  # initializes the OTel provider
            return True
        except Exception:
            logger.warning("evals_phoenix_configure_failed", exc_info=True)
            return False
    return False


def _curate_case_input(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": case.get("id"),
        "filename": case.get("filename"),
        "expected_doc_class": case.get("expected_doc_class"),
        "expected_subclass": case.get("expected_subclass"),
        "chars": len(str(case.get("text") or "")),
        "config": case.get("config"),
        "split": case.get("split"),
    }


class _NoopSpan:
    name = ""

    def set_output(self, output: dict[str, Any]) -> Any:
        return self

    def set_metrics(self, metrics: dict[str, float]) -> Any:
        return self

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        pass


_noop = _NoopSpan()


@contextmanager
def case_span(
    backend: str,
    *,
    node_name: str,
    case: dict[str, Any],
    run_meta: dict[str, Any],
) -> Iterator[Any]:
    """One root span per case with curated input; yields a span handle with
    ``set_output`` / ``set_metrics``. Yields a no-op when backend is none."""
    if backend == "none":
        yield _noop
        return
    as_type = NODE_OBSERVATION_TYPES.get(node_name, "span")
    meta = dict(run_meta or {})
    meta.setdefault("case_id", case.get("id"))
    meta.setdefault("filename", case.get("filename"))
    try:
        if backend == "braintrust":
            import braintrust

            with braintrust.start_span(
                name=node_name,
                type=as_type,
                input=_curate_case_input(case),
                metadata=meta or None,
                tags=list(meta.get("tags") or []) or None,
            ) as span:
                yield _BraintrustHandle(span)
            return
        if backend == "phoenix":
            from opentelemetry import trace

            tracer = trace.get_tracer("mailroom-evals")
            with tracer.start_as_current_span(node_name) as span:
                _otel_attrs(span, as_type, _curate_case_input(case), meta)
                yield _PhoenixHandle(span)
            return
    except Exception:
        logger.warning("evals_case_span_failed", backend=backend, node=node_name, exc_info=True)
    yield _noop


def _otel_attrs(span: Any, as_type: str, inp: dict[str, Any], meta: dict[str, Any]) -> None:
    try:
        span.set_attribute("openinference.span.kind", as_type.upper())
        for key, value in {**inp, **meta}.items():
            if value is None:
                continue
            span.set_attribute(f"evals.{key}" if key in meta else f"evals.input.{key}", str(value))
    except Exception:
        pass


class _BraintrustHandle:
    def __init__(self, span: Any) -> None:
        self._span = span

    def set_output(self, output: dict[str, Any]) -> Any:
        try:
            self._span.log(output=output)
        except Exception:
            pass
        return self

    def set_metrics(self, metrics: dict[str, float]) -> Any:
        try:
            self._span.log(metrics={k: v for k, v in metrics.items() if isinstance(v, (int, float))})
        except Exception:
            pass
        return self


class _PhoenixHandle:
    def __init__(self, span: Any) -> None:
        self._span = span

    def set_output(self, output: dict[str, Any]) -> Any:
        try:
            import json

            self._span.set_attribute("evals.output", json.dumps(output, default=str)[:4000])
        except Exception:
            pass
        return self

    def set_metrics(self, metrics: dict[str, float]) -> Any:
        try:
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    self._span.set_attribute(f"evals.metric.{key}", float(value))
        except Exception:
            pass
        return self


def flush(backend: str) -> None:
    """Force-export buffered spans for the backend. Never raises."""
    try:
        if backend == "braintrust":
            from observability.braintrust_setup import flush_braintrust

            flush_braintrust()
        elif backend == "phoenix":
            from observability.phoenix_setup import flush_phoenix

            flush_phoenix()
    except Exception:
        logger.warning("evals_flush_failed", backend=backend, exc_info=True)
