"""invoke.py — mock invocation modes, state building, mode validation.

Real-mode paths are covered by the full mock smoke (run_evals --task all
--mock) and live runs; these tests pin the hermetic surface: mock clients
install cleanly, node + agent modes produce predictions, unknown modes fail
loudly, and daemon drains/isolation restore the environment.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from evals import invoke


def test_invoke_unknown_mode_raises(sample_case):
    with pytest.raises(ValueError, match="unknown invoke mode"):
        invoke.invoke("classification", sample_case, mode="teleport")


def test_invoke_node_requires_base_dir(sample_case, monkeypatch):
    monkeypatch.delenv("MAILROOM_BASE_DIR", raising=False)
    with pytest.raises(KeyError):
        invoke.invoke("classification", sample_case, mode="node")


def test_build_state_shape(sample_case):
    state = invoke.build_state(sample_case)
    assert state["stage"] == "inbox"
    assert state["doc_type"] == "contract"
    assert state["doc_text"] == sample_case["text"]
    assert Path(state["file_path"]).exists()
    assert Path(state["file_path"]).read_text() == sample_case["text"]
    assert state["original_filename"] == "test_doc.txt"


def test_build_state_flattens_pathed_filenames(sample_case):
    case = dict(sample_case)
    case["filename"] = "thread_42/attachment_1.eml"
    state = invoke.build_state(case)
    assert "/" not in Path(state["file_path"]).name
    assert Path(state["file_path"]).parent.name == "inbox"


def test_build_state_doc_type_override(sample_case):
    state = invoke.build_state(sample_case, doc_type="correspondence")
    assert state["doc_type"] == "correspondence"


def test_install_mocks_patches_clients():
    import agents.base as base_mod
    import llm.client as client_mod
    from langchain_agents.base_agent import BaseAgent as LangChainBase

    before = (base_mod.BaseAgent.__init__, client_mod.OpenAI, LangChainBase.llm)
    invoke.install_mocks()
    try:
        assert base_mod.BaseAgent.__init__ != before[0]
        assert client_mod.OpenAI != before[1]
        assert LangChainBase.llm != before[2]
        # mocked OpenAI client returns a canonical JSON payload
        client = client_mod.OpenAI()
        import json

        payload = json.loads(
            client.chat.completions.create(model="m", messages=[{"role": "user", "content": "x"}])
            .choices[0]
            .message.content
        )
        assert payload["doc_type"] == "contract"
        assert 0.0 <= payload["confidence"] <= 1.0
    finally:
        base_mod.BaseAgent.__init__, client_mod.OpenAI, LangChainBase.llm = before


def test_drain_daemons_is_safe():
    invoke.drain_daemons(0.05)  # must not raise on an idle loop


def test_canonical_task_aliases():
    assert invoke._canonical_task("classify") == "classification"
    assert invoke._canonical_task("judge") == "judge_arbiter"
    assert invoke._canonical_task("classification") == "classification"  # passthrough


def test_mock_node_invocation_classification(sample_case):
    invoke.install_mocks()
    prediction = invoke.invoke("classification", sample_case, mode="node")
    assert isinstance(prediction, dict)
    assert prediction


def test_mock_agent_involution_classification(sample_case):
    invoke.install_mocks()
    prediction = invoke.invoke("classification", sample_case, mode="agent")
    assert isinstance(prediction, dict)
    assert prediction


def test_isolation_restores_base_dir(sample_case, monkeypatch, tmp_path):
    original = os.environ["MAILROOM_BASE_DIR"]
    with invoke.Isolation():
        assert os.environ["MAILROOM_BASE_DIR"] != original
        assert Path(os.environ["MAILROOM_BASE_DIR"]).exists()
    assert os.environ["MAILROOM_BASE_DIR"] == original
