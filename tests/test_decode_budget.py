"""Comparison decode profiles: budgets, sampling injection, thinking strip."""

from __future__ import annotations

import json

import pytest

from evals.decode_budget import (
    CLASS_BUDGETS,
    COMPARISON_PROFILES,
    apply_decode_budget,
    get_profile,
    recover_prediction,
    strip_thinking_spans,
)


# ── thinking strip ────────────────────────────────────────────────────────────


def test_strip_thinking_spans_unwraps_granite_envelope():
    raw = '<thinking>Let me analyze.</thinking>\n<response>\n{"confidence": 0.9}\n</response>'
    assert strip_thinking_spans(raw) == '{"confidence": 0.9}'


def test_strip_thinking_spans_is_noop_on_clean_text():
    assert strip_thinking_spans('{"confidence": 0.9}') == '{"confidence": 0.9}'


def test_recover_prediction_repairs_parse_error():
    raw = "<response>{\"extracted_data\": {\"parties\": [\"Acme\"]}, \"confidence\": 0.8}</response>"
    pred, did = recover_prediction({"_raw": raw, "_parse_error": True})
    assert did is True
    assert pred["extracted_data"] == {"parties": ["Acme"]}
    assert pred["_thinking_stripped"] is True
    assert "_parse_error" not in pred and "_raw" not in pred


def test_recover_prediction_ignores_clean_predictions():
    pred, did = recover_prediction({"extracted_data": {}, "confidence": 0.9})
    assert did is False and pred == {"extracted_data": {}, "confidence": 0.9}


# ── profiles ─────────────────────────────────────────────────────────────────


def test_profiles_match_issue_18_budgets():
    assert CLASS_BUDGETS["correspondence_specialist"] == 4096
    assert CLASS_BUDGETS["insurance_claims_specialist"] == 6144
    assert CLASS_BUDGETS["contracts_specialist"] == 8192
    assert COMPARISON_PROFILES["granite-4.2-8b"]["sampling"] == {
        "temperature": 1.0, "top_p": 0.95, "seed": 42,
    }
    # Qwen twin keeps the pipeline decode posture (no mandated sampling).
    assert COMPARISON_PROFILES["qwen3-8b"]["sampling"] is None
    for profile in COMPARISON_PROFILES.values():
        assert profile["call_timeout_s"] == 600


def test_get_profile_none_and_unknown():
    assert get_profile(None) is None
    assert get_profile("nope") is None
    assert get_profile("Granite-4.2-8B")["model"] == "ibm-granite/granite-4.2-8b"


# ── apply_decode_budget mechanics ────────────────────────────────────────────


def test_apply_decode_budget_merges_taxonomy(monkeypatch):
    import pipeline.config as pc

    monkeypatch.setattr(
        pc, "load_config",
        lambda *a, **k: {
            "agents": {
                "correspondence_specialist": {"provider": "openrouter", "max_tokens": 999},
                "sorter": {"provider": "openrouter", "max_tokens": 4096},
            },
            "run_limits": {"llm_call_timeout_seconds": 120},
        },
        raising=False,
    )
    with apply_decode_budget(get_profile("qwen3-8b")) as applied:
        cfg = pc.load_config()
        # Specialist budget overridden; non-specialist untouched.
        assert cfg["agents"]["correspondence_specialist"]["max_tokens"] == 4096
        assert cfg["agents"]["sorter"]["max_tokens"] == 4096
        assert applied["max_tokens_by_agent"]["correspondence_specialist"] == 4096
        # Thinking-ON timeout lift.
        assert cfg["run_limits"]["llm_call_timeout_seconds"] == 600
        # Qwen profile injects no sampling.
        assert applied["sampling_injected"] is False
    # Restored.
    assert pc.load_config()["run_limits"]["llm_call_timeout_seconds"] == 120


def test_apply_decode_budget_injects_sampling(monkeypatch):
    import llm.retry as llm_retry

    calls: list[dict] = []
    monkeypatch.setattr(
        llm_retry, "retry_chat_completion",
        lambda client, **kwargs: calls.append(kwargs) or "ok",
        raising=False,
    )
    with apply_decode_budget(get_profile("granite-4.2-8b")) as applied:
        llm_retry.retry_chat_completion(object(), model="x", temperature=0.1)
        assert applied["sampling_injected"] is True
        # Mandated values override the explicit call-site 0.1.
        assert calls[0]["temperature"] == 1.0
        assert calls[0]["top_p"] == 0.95
        assert calls[0]["seed"] == 42
    # Restored: post-context call no longer sees mandated values.
    llm_retry.retry_chat_completion(object(), model="x", temperature=0.1)
    assert calls[1] == {"model": "x", "temperature": 0.1}


def test_apply_decode_budget_none_is_inert():
    with apply_decode_budget(None) as applied:
        assert applied == {"sampling_injected": False, "max_tokens_by_agent": {}}
