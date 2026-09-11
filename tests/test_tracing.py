"""Tracing resolution + backend-selection tests (no network)."""

from __future__ import annotations

import pytest

from evals import tracing


def test_explicit_backend(monkeypatch):
    assert tracing.resolve_backend("braintrust") == "braintrust"
    assert tracing.resolve_backend("phoenix") == "phoenix"
    assert tracing.resolve_backend("none") == "none"


def test_auto_prefers_braintrust(monkeypatch):
    monkeypatch.delenv("EVALS_TRACE_BACKEND", raising=False)
    monkeypatch.setenv("BRAINTRUST_API_KEY", "k")
    monkeypatch.setenv("PHOENIX_TRACING", "enabled")
    assert tracing.resolve_backend(None) == "braintrust"


def test_auto_falls_back_to_phoenix(monkeypatch):
    monkeypatch.delenv("EVALS_TRACE_BACKEND", raising=False)
    monkeypatch.delenv("BRAINTRUST_API_KEY", raising=False)
    monkeypatch.setenv("PHOENIX_TRACING", "enabled")
    assert tracing.resolve_backend(None) == "phoenix"


def test_auto_none_when_disabled(monkeypatch):
    monkeypatch.delenv("EVALS_TRACE_BACKEND", raising=False)
    monkeypatch.delenv("BRAINTRUST_API_KEY", raising=False)
    monkeypatch.setenv("PHOENIX_TRACING", "disabled")
    assert tracing.resolve_backend(None) == "none"


def test_unknown_backend_raises():
    with pytest.raises(ValueError):
        tracing.resolve_backend("langfuse")


def test_apply_provider_env(monkeypatch):
    tracing.apply_provider_env("braintrust")
    import os

    assert os.environ["OBSERVABILITY_PROVIDER"] == "braintrust"
    tracing.apply_provider_env("none")
    assert os.environ["OBSERVABILITY_PROVIDER"] == "none"


def test_noop_span_when_disabled():
    with tracing.case_span("none", node_name="classify-document", case={}, run_meta={}) as span:
        span.set_output({"ok": True}).set_metrics({"a": 1.0})


def test_node_observation_names():
    assert tracing.NODE_OBSERVATION_TYPES["classify-document"] == "agent"
    assert tracing.NODE_OBSERVATION_TYPES["judge-verify"] == "evaluator"
