"""Tracing resolution + backend-selection tests (no network)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

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
        span.log_document_row(scores={"overall_score": 1.0})


def test_case_span_names_specialist_parent_not_extract_fields():
    exp = MagicMock()
    span_cm = MagicMock()
    span_cm.__enter__.return_value = MagicMock()
    span_cm.__exit__.return_value = None
    exp.start_span.return_value = span_cm
    case = {"id": "c", "text": "hello"}
    with patch("evals.braintrust_experiment.current_experiment", return_value=exp):
        with patch("evals.braintrust_experiment.dataset_record_id", return_value="rec-1"):
            with tracing.case_span(
                "braintrust",
                node_name="extract-fields",
                case=case,
                run_meta={"run_id": "r1"},
                span_name="contracts_specialist",
                specialist="contracts_specialist",
            ) as handle:
                handle.log_document_row(scores={"overall_score": 0.5})
    kw = exp.start_span.call_args.kwargs
    assert kw["name"] == "contracts_specialist"
    assert kw["name"] != "extract-fields"
    assert kw["type"] == "eval"
    assert kw["id"] == tracing.doc_text_sha256(case)
    assert kw["metadata"]["pipeline_node"] == "extract-fields"
    assert kw["metadata"]["specialist"] == "contracts_specialist"


def test_run_span_is_noop_when_experiment_is_open():
    exp = MagicMock()
    with patch("evals.braintrust_experiment.current_experiment", return_value=exp):
        with patch("braintrust.start_span") as start:
            with tracing.run_span("braintrust", run_meta={"run_id": "r1"}) as span:
                span.set_metrics({"overall_score": 0.5})
            start.assert_not_called()


def test_node_observation_names():
    assert tracing.NODE_OBSERVATION_TYPES["classify-document"] == "agent"
    assert tracing.NODE_OBSERVATION_TYPES["judge-verify"] == "evaluator"


def test_format_langchain_llm_input_roles():
    from langchain_core.messages import HumanMessage, SystemMessage

    batch = [[SystemMessage(content="You are the contracts specialist."), HumanMessage(content="Extract fields.")]]
    formatted = tracing.format_langchain_llm_input(batch)
    assert formatted == [
        {
            "role": "system",
            "content": "You are the contracts specialist.",
            "trace_content_chars": 33,
        },
        {"role": "user", "content": "Extract fields.", "trace_content_chars": 15},
    ]


def test_format_langchain_llm_input_openai_dicts():
    payload = [
        [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "usr"},
        ]
    ]
    assert tracing.format_langchain_llm_input(payload) == [
        {"role": "system", "content": "sys", "trace_content_chars": 3},
        {"role": "user", "content": "usr", "trace_content_chars": 3},
    ]


def test_public_case_ref_strips_filename_and_labels():
    case = {
        "id": "corpus:ground_truth:train:2ThemartComInc_19990826_EX-10.10_Co-Branding Agreement.pdf",
        "text": "CO-BRANDING AND ADVERTISING AGREEMENT",
        "expected_doc_class": "contract",
        "expected_subclass": "Co_Branding",
        "filename": "2ThemartComInc_19990826_EX-10.10_Co-Branding Agreement.pdf",
    }
    ref = tracing.public_case_ref(case)
    assert ref.startswith("corpus:ground_truth:train:doc#")
    assert "Co-Branding" not in ref
    assert "Co_Branding" not in ref
    curated = tracing._curate_case_input(case)
    assert "case_ref" in curated
    assert "case_id" not in curated
    assert "filename" not in curated
    assert "expected_doc_class" not in curated
    assert "expected_subclass" not in curated
    assert curated["doc_text_sha256"] == tracing.doc_text_sha256(case)


def test_format_langchain_llm_input_truncates_long_user_content(monkeypatch):
    monkeypatch.setattr(tracing, "_TRACE_MESSAGE_MAX_CHARS", 50)
    long_doc = "A" * 200
    payload = [[{"role": "user", "content": long_doc}]]
    formatted = tracing.format_langchain_llm_input(payload)
    assert formatted[0]["trace_content_truncated"] is True
    assert formatted[0]["trace_content_chars"] == 200
    assert formatted[0]["content"].startswith("A")
    assert "truncated" in formatted[0]["content"]
