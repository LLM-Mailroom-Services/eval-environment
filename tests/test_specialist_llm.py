"""Direct OpenRouter specialist extraction — no LangChain nodes."""

from __future__ import annotations

from unittest.mock import MagicMock

from evals.prompts import frozen_v1
from evals.prompts.registry import activate, deactivate
from evals.specialist_llm import (
    CLASS_PROMPT_STEM,
    CLASS_SPECIALIST,
    extract_entities,
    prompt_key_for,
    set_mock_client,
    specialist_system_prompt,
    user_extract_message,
)


def test_merger_system_prompt_is_frozen_maud_not_cuad():
    keys = activate("frozen")
    try:
        text = specialist_system_prompt("merger_agreement_specialist")
        assert text == frozen_v1.VERSIONS["merger_agreement_specialist_v1"]
        assert "Agreement and Plan of Merger" in text
        assert "You are the contracts specialist" not in text
        cuad = specialist_system_prompt("contracts_specialist")
        assert cuad == frozen_v1.VERSIONS["contracts_specialist_v1"]
        assert cuad != text
        assert keys["merger_agreement_specialist"] == "merger_agreement_specialist_v1"
    finally:
        deactivate()


def test_user_message_asks_to_extract_included_document():
    msg = user_extract_message(
        doc_class="merger_agreement",
        text="AGREEMENT AND PLAN OF MERGER of Parent and Target.",
        subclass="all_cash",
    )
    assert "Extract the registered entities from this document" in msg
    assert "AGREEMENT AND PLAN OF MERGER of Parent and Target." in msg
    assert "merger_agreement" in msg
    assert "maud_clauses" in msg
    assert "cuad_family" not in msg


def test_each_class_uses_its_designated_frozen_prompt():
    activate("frozen")
    try:
        stems = {}
        for doc_class, role in CLASS_SPECIALIST.items():
            text = specialist_system_prompt(role)
            key = prompt_key_for(role)
            assert key == f"{role}_v1"
            assert text == frozen_v1.VERSIONS[key]
            assert text.startswith(CLASS_PROMPT_STEM[doc_class])
            stems[doc_class] = text
        assert len(set(stems.values())) == 5
        assert stems["merger_agreement"].startswith("You are the merger-agreement specialist.")
        assert not stems["merger_agreement"].startswith("You are the contracts specialist.")
        assert "Agreement and Plan of Merger" in stems["merger_agreement"]
    finally:
        deactivate()


def test_wrong_specialist_for_class_is_rejected():
    activate("frozen")
    try:
        set_mock_client(MagicMock())
        try:
            extract_entities(
                "contracts_specialist",
                {"text": "PLAN OF MERGER", "expected_doc_class": "merger_agreement"},
            )
            raise AssertionError("contracts specialist must not extract merger_agreement")
        except RuntimeError as exc:
            assert "designated specialist is 'merger_agreement_specialist'" in str(exc)
    finally:
        set_mock_client(None)
        deactivate()


def test_extract_entities_openrouter_shape_not_langchain():
    activate("frozen")
    try:
        captured: dict = {}

        def _create(**kwargs):
            captured["messages"] = kwargs["messages"]
            captured["model"] = kwargs["model"]
            mock = MagicMock()
            mock.choices[0].message.content = '{"document_name": "Plan of Merger", "confidence": 0.4}'
            mock.usage.prompt_tokens = 11
            mock.usage.completion_tokens = 5
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        out = extract_entities(
            "merger_agreement_specialist",
            {
                "text": "AGREEMENT AND PLAN OF MERGER",
                "expected_doc_class": "merger_agreement",
                "expected_subclass": "all_cash",
            },
        )
        assert out["specialist"] == "merger_agreement_specialist"
        assert out["prompt_key"] == "merger_agreement_specialist_v1"
        assert out["extracted_data"]["document_name"] == "Plan of Merger"
        system = captured["messages"][0]["content"]
        user = captured["messages"][1]["content"]
        assert system.startswith("You are the merger-agreement specialist")
        assert "Extract the registered entities" in user
        assert "AGREEMENT AND PLAN OF MERGER" in user
        assert captured["model"] == "mock-model"
    finally:
        set_mock_client(None)
        deactivate()
