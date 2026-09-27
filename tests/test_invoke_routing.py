"""Specialist dispatch wiring — no pipeline import required."""

from __future__ import annotations

from unittest.mock import MagicMock

from evals.invoke import TASK_SPECIALIST, _SPECIALIST_CLASSES, _specialist_for_class, invoke
from evals.prompts.registry import activate, deactivate
from evals.specialist_llm import set_mock_client


def test_merger_agreement_uses_dedicated_specialist():
    assert TASK_SPECIALIST["merger_agreement"] == "merger_agreement_specialist"
    assert _specialist_for_class("merger_agreement") == "merger_agreement_specialist"
    assert "merger_agreement_specialist" in _SPECIALIST_CLASSES


def test_invoke_merger_does_not_call_extract_node(monkeypatch):
    activate("frozen")
    try:
        client = MagicMock()
        resp = MagicMock()
        resp.choices[0].message.content = '{"document_name": "Merger", "confidence": 0.2}'
        resp.usage.prompt_tokens = 8
        resp.usage.completion_tokens = 4
        client.chat.completions.create.return_value = resp
        set_mock_client(client)

        def _boom(*_a, **_k):
            raise AssertionError("extract_node must not run for specialist evals")

        monkeypatch.setattr("graph.build_graph.extract_node", _boom)
        case = {
            "id": "c",
            "text": "Agreement and Plan of Merger",
            "expected_doc_class": "merger_agreement",
            "expected_subclass": "all_stock",
            "filename": "ma.txt",
        }
        pred = invoke("merger_agreement", case, mode="node")
        assert pred["specialist"] == "merger_agreement_specialist"
        assert pred["extracted_data"]["document_name"] == "Merger"
        client.chat.completions.create.assert_called_once()
        system = client.chat.completions.create.call_args.kwargs["messages"][0]["content"]
        assert "merger-agreement specialist" in system
        assert "You are the contracts specialist" not in system
    finally:
        set_mock_client(None)
        deactivate()
