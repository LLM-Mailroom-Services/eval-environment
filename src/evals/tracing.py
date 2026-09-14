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

            ok = bool(bt_configure())
            if ok:
                _install_langchain_llm_spans()
            return ok
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


_LC_BT_REGISTERED = False
_LC_BT_VAR: Any = None  # ContextVar holding the active handler instance


try:
    from langchain_core.callbacks import BaseCallbackHandler as _LCBaseHandler
except Exception:  # pragma: no cover - langchain-core is a pipeline dependency
    _LCBaseHandler = object  # type: ignore[assignment,misc]


class _LangchainLLMHandler(_LCBaseHandler):
    """Braintrust span writer for LangChain-agent LLM calls (see installer)."""

    def __init__(self) -> None:
        self._spans: dict[Any, Any] = {}

    def _braintrust(self) -> Any:
        import braintrust

        return braintrust

    def _curate(self, message: Any) -> str | None:
        try:
            return str(message)[:4000]
        except Exception:
            return None

    def _flatten(self, payload: Any) -> list[str | None]:
        out: list[str | None] = []
        for group in payload or []:
            if hasattr(group, "content"):
                out.append(self._curate(group))
            else:
                for message in group:
                    out.append(self._curate(message))
        return out

    def on_chat_model_start(self, serialized: Any, messages: Any, *, run_id: Any = None, **kwargs: Any) -> None:
        try:
            bt = self._braintrust()
            self._spans[run_id] = bt.start_span(
                name="Chat Completion", type="llm", input=self._flatten(messages)
            )
        except Exception:
            logger.warning("evals_langchain_span_start_failed", exc_info=True)

    on_llm_start = on_chat_model_start  # plain-LLM callback shape (list[str])

    def _finish(self, run_id: Any, output: Any = None, metrics: dict[str, float] | None = None) -> None:
        span = self._spans.pop(run_id, None)
        if span is None:
            return
        try:
            span.log(output=output, metrics=metrics or None)
            span.end()
        except Exception:
            logger.warning("evals_langchain_span_end_failed", exc_info=True)

    def on_llm_end(self, response: Any, *, run_id: Any = None, **kwargs: Any) -> None:
        usage = (getattr(response, "llm_output", None) or {}).get("token_usage") or {}
        metrics = {
            key: value
            for key, value in (
                ("prompt_tokens", usage.get("prompt_tokens")),
                ("completion_tokens", usage.get("completion_tokens")),
                ("tokens_total", usage.get("total_tokens")),
            )
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        }
        self._finish(run_id, output="ok", metrics=metrics or None)

    def on_llm_error(self, error: Any, *, run_id: Any = None, **kwargs: Any) -> None:
        self._finish(run_id, output=f"error: {error}"[:500])


def _install_langchain_llm_spans() -> None:
    """Route LangChain-agent LLM calls into Braintrust as nested llm spans.

    ``braintrust.wrap_openai`` only instruments raw OpenAI clients — the
    LangChain agents (sorter, specialists, judge, …) build ChatOpenAI
    directly and bypass that chokepoint, leaving their calls invisible in
    the sink. A global callback handler (langchain-core ≥1.x
    ``register_configure_hook`` mechanism) restores the "every LLM call
    auto-traces" contract; spans nest under the active case span. Failures
    warn and never break a run.
    """
    global _LC_BT_REGISTERED, _LC_BT_VAR
    if _LC_BT_REGISTERED and _LC_BT_VAR is not None:
        _LC_BT_VAR.set(_LangchainLLMHandler())  # fresh handler for this run's context
        return
    try:
        from contextvars import ContextVar

        from langchain_core.tracers.context import register_configure_hook
    except Exception:
        logger.warning("evals_langchain_tracing_unavailable")
        return

    try:
        _LC_BT_VAR = ContextVar("evals_langchain_braintrust", default=None)
        register_configure_hook(_LC_BT_VAR, inheritable=True, handle_class=_LangchainLLMHandler)
        _LC_BT_VAR.set(_LangchainLLMHandler())
        _LC_BT_REGISTERED = True
        logger.info("evals_langchain_llm_tracing_enabled")
    except Exception:
        logger.warning("evals_langchain_callback_register_failed", exc_info=True)


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

    def update_metadata(self, metadata: dict[str, Any]) -> Any:
        return self

    @property
    def trace_ref(self) -> dict[str, Any] | None:
        return None

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
        # Captured at open time: the per-case trace cross-reference written
        # into the case rows (the schema documents `trace`; this is its writer).
        try:
            self._span_id = span.id
        except Exception:
            self._span_id = None
        try:
            self._root_span_id = getattr(span, "root_span_id", None)
        except Exception:
            self._root_span_id = None

    @property
    def trace_ref(self) -> dict[str, Any] | None:
        if not self._span_id:
            return None
        return {
            "backend": "braintrust",
            "span_id": str(self._span_id),
            **({"root_span_id": str(self._root_span_id)} if self._root_span_id else {}),
        }

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

    def update_metadata(self, metadata: dict[str, Any]) -> Any:
        try:
            self._span.log(metadata={k: v for k, v in (metadata or {}).items() if v is not None})
        except Exception:
            pass
        return self


class _PhoenixHandle:
    def __init__(self, span: Any) -> None:
        self._span = span

    @property
    def trace_ref(self) -> dict[str, Any] | None:
        try:
            from opentelemetry import trace

            ctx = self._span.get_span_context()
            return {
                "backend": "phoenix",
                "span_id": trace.format_span_id(ctx.span_id),
                "trace_id": trace.format_trace_id(ctx.trace_id),
            }
        except Exception:
            return None

    def update_metadata(self, metadata: dict[str, Any]) -> Any:
        try:
            for key, value in (metadata or {}).items():
                if value is not None:
                    self._span.set_attribute(f"evals.meta.{key}", str(value))
        except Exception:
            pass
        return self

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


@contextmanager
def run_span(
    backend: str,
    *,
    run_meta: dict[str, Any],
) -> Iterator[Any]:
    """One run-level rollup span per eval run (the sink's dashboard entry).

    Carries the run summary's essential aggregates (metrics, latency mean,
    ECE for calibration) — never per-case noise. No-op when backend is none.
    """
    if backend == "none":
        yield _noop
        return
    try:
        if backend == "braintrust":
            import braintrust

            with braintrust.start_span(
                name="evals-run",
                type="task",
                input={"run_id": run_meta.get("run_id"), "task": run_meta.get("task")},
                metadata=run_meta or None,
                tags=list(run_meta.get("tags") or []) or None,
            ) as span:
                yield _BraintrustHandle(span)
            return
        if backend == "phoenix":
            from opentelemetry import trace

            tracer = trace.get_tracer("mailroom-evals")
            with tracer.start_as_current_span("evals-run") as span:
                _otel_attrs(span, "chain", {"run_id": run_meta.get("run_id")}, run_meta)
                yield _PhoenixHandle(span)
            return
    except Exception:
        logger.warning("evals_run_span_failed", backend=backend, exc_info=True)
    yield _noop
