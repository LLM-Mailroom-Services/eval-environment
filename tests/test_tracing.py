"""Tracing resolution + backend-selection tests (no network)."""

from __future__ import annotations

import hashlib
import sys
from copy import deepcopy
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, Mock

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


_EMPTY_TEXT_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
_ABC_TEXT_SHA256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


@pytest.mark.parametrize(
    ("case", "expected"),
    [
        pytest.param({}, _EMPTY_TEXT_SHA256, id="missing"),
        pytest.param({"text": None}, _EMPTY_TEXT_SHA256, id="null"),
        pytest.param({"text": ""}, _EMPTY_TEXT_SHA256, id="empty"),
        pytest.param({"text": 0}, _EMPTY_TEXT_SHA256, id="zero"),
        pytest.param({"text": False}, _EMPTY_TEXT_SHA256, id="false"),
        pytest.param({"text": "abc"}, _ABC_TEXT_SHA256, id="known-sha256-vector"),
    ],
)
def test_doc_text_sha256_known_vectors_and_empty_values(case, expected):
    assert tracing.doc_text_sha256(case) == expected


@pytest.mark.parametrize("text", ["Résumé 合同 📨", " abc ", "abc\n", "abc\r\n", 123])
def test_doc_text_sha256_preserves_exact_utf8_text(text):
    expected = hashlib.sha256(str(text).encode("utf-8")).hexdigest()
    assert tracing.doc_text_sha256({"text": text}) == expected


@pytest.mark.parametrize(
    ("case_id", "prefix"),
    [
        ("corpus:ground_truth:train:contract.pdf", "corpus:ground_truth:train"),
        ("corpus:fixtures:test:wrong_high.txt", "corpus:fixtures:test"),
        ("corpus:default:validation:private:contract:label.pdf", "corpus:default:validation"),
        ("corpus:ground_truth:train:", "corpus:ground_truth:train"),
    ],
)
def test_public_case_ref_preserves_only_corpus_position(case_id, prefix):
    case = {"id": case_id, "text": "abc", "config": "other-config", "split": "other-split"}
    assert tracing.public_case_ref(case) == f"{prefix}:doc#ba7816bf8f01"


@pytest.mark.parametrize(
    "case",
    [
        pytest.param({}, id="missing-id"),
        pytest.param({"id": None}, id="null-id"),
        pytest.param({"id": ""}, id="empty-id"),
        pytest.param({"id": "private-contract.pdf"}, id="filename-id"),
        pytest.param({"id": "manual:insurance:claim.pdf"}, id="non-corpus-colons"),
        pytest.param({"id": "corpus:"}, id="missing-config-and-split"),
        pytest.param({"id": "corpus:ground_truth"}, id="missing-split"),
        pytest.param({"id": "corpus:ground_truth:train"}, id="missing-filename-separator"),
        pytest.param({"id": 123}, id="numeric-id"),
    ],
)
def test_public_case_ref_falls_back_to_hashed_id(case):
    raw_id = str(case.get("id") or "")
    expected_digest = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:12]
    assert tracing.public_case_ref({**case, "text": "abc"}) == f"eval-case:doc#{expected_digest}"


def test_corpus_case_ref_depends_on_text_not_filename_or_labels(sample_case):
    case = {**sample_case, "text": "abc"}
    original_ref = tracing.public_case_ref(case)
    assert original_ref == "corpus:ground_truth:train:doc#ba7816bf8f01"

    renamed = {
        **case,
        "id": "corpus:ground_truth:train:renamed-insurance-claim.pdf",
        "filename": "renamed-insurance-claim.pdf",
        "expected_doc_class": "insurance_claim",
        "expected_subclass": "private-subclass",
    }
    assert tracing.public_case_ref(renamed) == original_ref
    assert tracing.doc_text_sha256(renamed) == _ABC_TEXT_SHA256
    assert tracing.public_case_ref({**renamed, "text": "changed document"}) != original_ref


def test_noncorpus_case_ref_is_stable_when_document_text_changes():
    case = {"id": "manual:contract.pdf", "text": "abc"}
    original_ref = tracing.public_case_ref(case)
    changed = {**case, "text": "changed document"}
    assert tracing.public_case_ref(changed) == original_ref
    assert tracing.doc_text_sha256(changed) != tracing.doc_text_sha256(case)
    assert tracing.public_case_ref({**case, "id": "manual:other.pdf"}) != original_ref


@pytest.mark.parametrize("text_fields", [{}, {"text": None}, {"text": ""}])
def test_corpus_case_ref_without_text_uses_empty_document_digest(text_fields):
    case = {"id": "corpus:fixtures:train:private-label.pdf", **text_fields}
    assert tracing.public_case_ref(case) == "corpus:fixtures:train:doc#e3b0c44298fc"


def test_curated_case_input_is_an_allowlist_and_does_not_mutate_case(sample_case):
    case = {
        **sample_case,
        "text": "Résumé 合同 📨",
        "case_ref": "unsafe-preexisting-reference",
        "doc_text_sha256": "stale-digest",
        "extra_private_field": "private-value",
    }
    original = deepcopy(case)
    digest = hashlib.sha256(case["text"].encode("utf-8")).hexdigest()
    assert tracing._curate_case_input(case) == {
        "case_ref": f"corpus:ground_truth:train:doc#{digest[:12]}",
        "doc_text_sha256": digest,
        "chars": 11,
        "config": "ground_truth",
        "split": "train",
    }
    assert case == original


@pytest.mark.parametrize("case", [{}, {"id": None, "text": None}])
def test_curated_case_input_handles_missing_optional_fields(case):
    assert tracing._curate_case_input(case) == {
        "case_ref": "eval-case:doc#e3b0c44298fc",
        "doc_text_sha256": _EMPTY_TEXT_SHA256,
        "chars": 0,
        "config": None,
        "split": None,
    }


@pytest.fixture(params=["braintrust", "phoenix"])
def case_trace_sink(request, monkeypatch):
    """Capture SDK calls without importing or contacting either trace provider."""
    backend = request.param
    span = MagicMock()
    context = MagicMock()
    context.__enter__.return_value = span
    start_span = Mock(return_value=context)
    if backend == "braintrust":
        sdk = ModuleType("braintrust")
        sdk.start_span = start_span
        monkeypatch.setitem(sys.modules, "braintrust", sdk)
    else:
        sdk = ModuleType("opentelemetry")
        sdk.trace = SimpleNamespace(
            get_tracer=Mock(return_value=SimpleNamespace(start_as_current_span=start_span))
        )
        monkeypatch.setitem(sys.modules, "opentelemetry", sdk)
    return backend, span, start_span


@pytest.mark.parametrize(
    ("case_fields", "expected_ref"),
    [
        ({"id": "corpus:ground_truth:train:private:label.pdf", "text": "abc"},
         "corpus:ground_truth:train:doc#ba7816bf8f01"),
        ({"id": "abc", "text": "abc"}, "eval-case:doc#ba7816bf8f01"),
    ],
    ids=["corpus", "non-corpus"],
)
def test_case_span_sends_only_sanitized_case_data(
    case_trace_sink, sample_case, case_fields, expected_ref
):
    backend, span, start_span = case_trace_sink
    case = {**sample_case, **case_fields}
    run_meta = {"run_id": "privacy-test", "task": "eval:classification"}
    original_case, original_meta = deepcopy(case), deepcopy(run_meta)

    with tracing.case_span(
        backend, node_name="classify-document", case=case, run_meta=run_meta
    ) as handle:
        assert handle._span is span  # A swallowed SDK error must not pass as a no-op.

    start_span.assert_called_once()
    if backend == "braintrust":
        start_span.assert_called_once_with(
            name="classify-document",
            type="agent",
            input={
                "case_ref": expected_ref,
                "doc_text_sha256": _ABC_TEXT_SHA256,
                "chars": 3,
                "config": "ground_truth",
                "split": "train",
            },
            metadata={
                **run_meta,
                "case_ref": expected_ref,
                "doc_text_sha256": _ABC_TEXT_SHA256,
            },
            tags=None,
        )
    else:
        start_span.assert_called_once_with("classify-document")
        attributes = {call.args[0]: call.args[1] for call in span.set_attribute.call_args_list}
        assert attributes == {
            "openinference.span.kind": "AGENT",
            "evals.case_ref": expected_ref,
            "evals.doc_text_sha256": _ABC_TEXT_SHA256,
            "evals.input.chars": "3",
            "evals.input.config": "ground_truth",
            "evals.input.split": "train",
            "evals.run_id": "privacy-test",
            "evals.task": "eval:classification",
        }
    assert case == original_case
    assert run_meta == original_meta


def test_case_span_adds_join_keys_for_empty_case(case_trace_sink):
    backend, span, start_span = case_trace_sink
    with tracing.case_span(backend, node_name="classify-document", case={}, run_meta={}) as handle:
        assert handle._span is span

    if backend == "braintrust":
        payload = start_span.call_args.kwargs
        assert payload["metadata"] == {
            "case_ref": "eval-case:doc#e3b0c44298fc",
            "doc_text_sha256": _EMPTY_TEXT_SHA256,
        }
        assert payload["input"] == {
            **payload["metadata"], "chars": 0, "config": None, "split": None,
        }
    else:
        attributes = {call.args[0]: call.args[1] for call in span.set_attribute.call_args_list}
        assert attributes == {
            "openinference.span.kind": "AGENT",
            "evals.case_ref": "eval-case:doc#e3b0c44298fc",
            "evals.doc_text_sha256": _EMPTY_TEXT_SHA256,
            "evals.input.chars": "0",
        }


def test_case_span_preserves_explicit_join_metadata(case_trace_sink, sample_case):
    backend, span, start_span = case_trace_sink
    run_meta = {
        "case_ref": "external:doc#123456789abc",
        "doc_text_sha256": "f" * 64,
        "run_id": "privacy-test",
    }
    original_meta = run_meta.copy()
    case = {**sample_case, "text": "abc"}
    with tracing.case_span(
        backend, node_name="classify-document", case=case, run_meta=run_meta
    ) as handle:
        assert handle._span is span

    if backend == "braintrust":
        payload = start_span.call_args.kwargs
        assert payload["metadata"] == original_meta
        assert payload["input"]["case_ref"] == "corpus:ground_truth:train:doc#ba7816bf8f01"
        assert payload["input"]["doc_text_sha256"] == _ABC_TEXT_SHA256
    else:
        attributes = {call.args[0]: call.args[1] for call in span.set_attribute.call_args_list}
        for key, value in original_meta.items():
            assert attributes[f"evals.{key}"] == value
    assert run_meta == original_meta


def test_format_langchain_llm_input_truncates_long_user_content(monkeypatch):
    monkeypatch.setattr(tracing, "_TRACE_MESSAGE_MAX_CHARS", 50)
    long_doc = "A" * 200
    payload = [[{"role": "user", "content": long_doc}]]
    formatted = tracing.format_langchain_llm_input(payload)
    assert formatted[0]["trace_content_truncated"] is True
    assert formatted[0]["trace_content_chars"] == 200
    assert formatted[0]["content"].startswith("A")
    assert "truncated" in formatted[0]["content"]
