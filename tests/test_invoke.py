"""invoke.py — mock invocation modes, state building, mode validation.

Real-mode paths are covered by the full mock smoke (run_evals --task all
--mock) and live runs; these tests pin the hermetic surface: mock clients
install cleanly, node + agent modes produce predictions, unknown modes fail
loudly, and daemon drains/isolation restore the environment.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock

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


@pytest.fixture
def specialist_agents(monkeypatch):
    """Stub the two pipeline agents at their import boundary, with distinct results."""
    contracts, merger = Mock(name="ContractsSpecialist"), Mock(name="MergerAgreementSpecialist")
    for module_name, class_name, agent in [
        ("agents.contracts_specialist", "ContractsSpecialist", contracts),
        ("agents.merger_agreement_specialist", "MergerAgreementSpecialist", merger),
    ]:
        module = ModuleType(module_name)
        setattr(module, class_name, agent)
        monkeypatch.setitem(sys.modules, module_name, module)
    contracts.return_value.extract.return_value = {"cuad_family": "service", "confidence": 0.8}
    merger.return_value.extract.return_value = {
        "merger_consideration": "all_cash", "confidence": 0.0,
    }
    return contracts, merger


@pytest.mark.parametrize(("doc_class", "specialist"), [
    ("merger_agreement", "merger_agreement_specialist"),
    ("contract", "contracts_specialist"),
    ("unknown", None),
    ("", None),
])
def test_specialist_for_class_keeps_maud_and_cuad_separate(doc_class, specialist):
    assert invoke._specialist_for_class(doc_class) == specialist


@pytest.mark.parametrize(("task", "selected"), [("contracts", 0), ("merger_agreement", 1)])
@pytest.mark.parametrize("text", ["Agreement text", "", None])
def test_specialist_agent_dispatch_uses_task_and_preserves_result(
    specialist_agents, task, selected, text,
):
    # A conflicting class hint must not override the explicitly requested task.
    case = {"text": text, "expected_doc_class": "correspondence"}
    result = invoke.invoke(task, case, mode="agent")

    chosen = specialist_agents[selected]
    chosen.assert_called_once_with()
    chosen.return_value.extract.assert_called_once_with(text or "")
    assert result is chosen.return_value.extract.return_value
    specialist_agents[1 - selected].assert_not_called()


@pytest.mark.parametrize(("doc_class", "selected"), [("contract", 0), ("merger_agreement", 1)])
def test_retry_agent_uses_class_specific_specialist(specialist_agents, doc_class, selected):
    """MAUD retry calibration must use the same dedicated specialist as direct evals."""
    result = invoke.invoke(
        "retry", {"expected_doc_class": doc_class, "text": "Retry text"}, mode="agent",
    )

    chosen = specialist_agents[selected]
    chosen.assert_called_once_with()
    chosen.return_value.extract.assert_called_once_with("Retry text")
    assert result == {
        "extracted_data": chosen.return_value.extract.return_value,
        "extraction_confidence": chosen.return_value.extract.return_value["confidence"],
        "doc_type": doc_class,
    }
    specialist_agents[1 - selected].assert_not_called()


def test_merger_specialist_failure_propagates_without_falling_back_to_contracts(specialist_agents):
    contracts, merger = specialist_agents
    merger.return_value.extract.side_effect = RuntimeError("merger extraction failed")

    with pytest.raises(RuntimeError, match="merger extraction failed"):
        invoke.invoke("merger_agreement", {"text": "Agreement text"}, mode="agent")

    contracts.assert_not_called()


def test_judge_node_receives_merger_specialist_extraction(
    specialist_agents, monkeypatch, sample_case,
):
    judge = Mock(return_value={
        "judge_verdict": "complete", "judge_score": 1.0, "judge_findings": [],
    })
    graph = ModuleType("graph")
    graph.build_graph = SimpleNamespace(judge_verify_node=judge)
    monkeypatch.setitem(sys.modules, "graph", graph)
    config = ModuleType("pipeline.config")
    config.get_confidence_thresholds = Mock(return_value={"low": 0.88})
    monkeypatch.setitem(sys.modules, "pipeline.config", config)
    case = dict(sample_case, expected_doc_class="merger_agreement", review_expected=True)

    result = invoke.invoke("judge_arbiter", case, mode="node")

    contracts, merger = specialist_agents
    merger.assert_called_once_with()
    merger.return_value.extract.assert_called_once_with(case["text"])
    contracts.assert_not_called()
    judge.assert_called_once()
    state = judge.call_args.args[0]
    assert state["doc_type"] == "merger_agreement"
    assert state["extracted_data"] is merger.return_value.extract.return_value
    assert result["judge_input_extracted"] is state["extracted_data"]
    assert result["judge_verdict"] == "complete"
