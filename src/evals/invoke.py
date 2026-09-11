"""Case invocation — run one eval case through a pipeline node OR its agent.

Two modes (``--invoke node|agent``):

- **node** (default): build a faithful ``DocumentState`` from the corpus row
  and call the raw graph node function (``classify_node``, ``extract_node``,
  ``judge_verify_node``, …) — true node-level measurement inside the same
  code path the pipeline runs.
- **agent**: call the underlying agent class directly (``SorterAgent``,
  specialists, ``CompletenessJudge``, …) — the ``agent_eval.py`` style.

Mock mode installs the deterministic fake-LLM shims (FakeLangChainLLM +
mocked OpenAI client) so nothing touches the network. Isolation: every
invocation runs with ``MAILROOM_BASE_DIR`` pointed at a per-run temp dir so
bins/manifests/catalogs/audit chains never touch real data.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Self

import structlog

logger = structlog.get_logger(__name__)

_SPECIALIST_CLASSES: dict[str, tuple[str, str]] = {
    "contracts_specialist": ("agents.contracts_specialist", "ContractsSpecialist"),
    "corporate_records_specialist": (
        "agents.corporate_records_specialist",
        "CorporateRecordsSpecialist",
    ),
    "correspondence_specialist": (
        "agents.correspondence_specialist",
        "CorrespondenceSpecialist",
    ),
    "compliance_specialist": ("agents.compliance_specialist", "ComplianceSpecialist"),
    "insurance_claims_specialist": (
        "agents.insurance_claims_specialist",
        "InsuranceClaimsSpecialist",
    ),
}

# task name -> specialist agent (registry tasks dispatch through these)
TASK_SPECIALIST: dict[str, str] = {
    "contracts": "contracts_specialist",
    "merger_agreement": "contracts_specialist",
    "corporate_records": "corporate_records_specialist",
    "correspondence": "correspondence_specialist",
    "insurance_claims": "insurance_claims_specialist",
}

# Calibration task names alias the eval node behaviors (same node, decision-
# focused scoring). retry probes the extract node; classify probes classify.
_CALIBRATION_ALIAS: dict[str, str] = {
    "classify": "classification",
    "judge": "judge_arbiter",
    "retry": "__extract__",
    "intake": "intake",
    "boss": "boss",
    "arbiter": "arbiter",
    "archivist": "archivist",
}


def _canonical_task(task: str) -> str:
    """Map calibration task names onto the node behaviors they probe."""
    if task in _CALIBRATION_ALIAS:
        aliased = _CALIBRATION_ALIAS[task]
        if aliased == "__extract__":
            return task  # retry keeps its own extract-based path below
        return aliased
    return task

_BASE_DIR_STACK: list[str] = []


def drain_daemons(seconds: float = 1.0) -> None:
    """Let off-path daemon threads (relations scan, echo dispatch) finish
    their DB writes while MAILROOM_BASE_DIR still points at the isolated
    temp dir — otherwise they land writes in the restored (real) base dir
    after the run exits."""
    import time as _time

    _time.sleep(max(0.0, seconds))


class Isolation:
    """Context manager isolating MAILROOM_BASE_DIR to a temp dir."""

    def __init__(self) -> None:
        self._prev: str | None = None
        self._tmp: tempfile.TemporaryDirectory | None = None

    def __enter__(self) -> Self:
        self._prev = os.environ.get("MAILROOM_BASE_DIR")
        self._tmp = tempfile.TemporaryDirectory(prefix="mailroom-evals-")
        os.environ["MAILROOM_BASE_DIR"] = self._tmp.name
        return self

    def __exit__(self, *args: object) -> None:
        if self._prev is not None:
            os.environ["MAILROOM_BASE_DIR"] = self._prev
        else:
            os.environ.pop("MAILROOM_BASE_DIR", None)
        if self._tmp is not None:
            self._tmp.cleanup()


def install_mocks() -> None:
    """Deterministic fakes so mock mode never hits the network.

    Same shim shape as llm-mailroom's ``run_agent_eval.py:_install_mocks``:
    FakeLangChainLLM for langchain agents, a mocked OpenAI client returning a
    canonical extraction payload for the raw-OpenAI agents.
    """
    from unittest.mock import MagicMock

    from langchain_agents.base_agent import BaseAgent as LangChainBase
    from langchain_agents.mock import FakeLangChainLLM

    fake = FakeLangChainLLM()
    LangChainBase.llm = lambda self, _fake=fake: _fake  # type: ignore[method-assign]

    def _structured_json(*_a: Any, **_k: Any) -> Any:
        payload = dict(fake.extraction)
        payload.setdefault("doc_type", fake.classification.get("doc_type", "contract"))
        payload.setdefault("confidence", 0.9)
        payload.setdefault("completeness", 1.0)
        payload.setdefault("completeness_label", "complete")
        payload.setdefault("decision", "approved")
        payload.setdefault("reasoning", "mock")
        payload.setdefault("fields_to_fix", [])
        payload.setdefault("handoff_summary", "mock")
        payload.setdefault("resolution_notes", "mock")
        mock_choice = MagicMock()
        mock_choice.message.content = json.dumps(payload)
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_completion.usage = MagicMock(
            prompt_tokens=10, completion_tokens=10, total_tokens=20
        )
        return mock_completion

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = _structured_json

    import agents.base as base_mod
    import llm.client as client_mod

    def _init(self: Any, mock: Any = mock_client) -> None:
        self.client = mock
        self.model = "mock-model"
        self._langfuse_prompt = None

    base_mod.BaseAgent.__init__ = _init  # type: ignore[method-assign]
    client_mod.OpenAI = lambda *a, **k: mock_client  # type: ignore[misc]


def _write_case_text(case: dict[str, Any], base_dir: Path) -> Path:
    """Materialize the case text as a file (nodes read from disk).

    Corpus filenames may carry path separators (e.g. Enron thread paths) —
    flatten them so the case file always lands directly in the inbox.
    """
    inbox = base_dir / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    raw_name = str(case.get("filename") or "case.txt")
    filename = raw_name.replace("/", "_").replace("\\", "_").strip() or "case.txt"
    path = inbox / filename
    path.write_text(str(case.get("text") or ""), encoding="utf-8")
    return path


def build_state(case: dict[str, Any], *, doc_type: str | None = None) -> dict[str, Any]:
    """DocumentState for one corpus case (node-mode invocation)."""
    base_dir = Path(os.environ["MAILROOM_BASE_DIR"])
    file_path = _write_case_text(case, base_dir)
    return {
        "doc_id": str(case.get("row", {}).get("document_id") or case.get("id")),
        "matter_id": str(case.get("row", {}).get("matter_id") or "EVAL"),
        "original_filename": str(case.get("filename") or "case.txt"),
        "stage": "inbox",
        "doc_type": doc_type or case.get("expected_doc_class"),
        "classification_confidence": None,
        "classification_attempts": 0,
        "extracted_data": None,
        "extraction_confidence": None,
        "extraction_attempts": 0,
        "trace_id": None,
        "escalation_reason": None,
        "review_decision": None,
        "retry_count": 0,
        "conflict_detected": False,
        "file_path": str(file_path),
        "doc_text": str(case.get("text") or ""),
        "doc_pages": [],
        "error_message": None,
        "messages": [],
        "transient_error": False,
        "transient_retries_classify": 0,
        "transient_retries_extract": 0,
        "run_attempt": 0,
    }


def _invoke_node(task: str, case: dict[str, Any]) -> dict[str, Any]:
    from graph import build_graph as bg

    task = _canonical_task(task)
    if task == "pipeline_chain":
        # Full 13-node graph, one document end-to-end (isolated base dir).
        from graph.build_graph import reset_compiled_graph, run_pipeline

        base_dir = Path(os.environ["MAILROOM_BASE_DIR"])
        file_path = _write_case_text(case, base_dir)
        ground_truth = None
        if case.get("expected_doc_class"):
            ground_truth = {"expected": case.get("expected_doc_class")}
            if case.get("expected_subclass"):
                ground_truth["expected_subclass"] = case.get("expected_subclass")
        try:
            result = run_pipeline(
                file_path,
                matter_id=str(case.get("row", {}).get("matter_id") or "EVAL"),
                ground_truth=ground_truth,
            )
        finally:
            reset_compiled_graph()
        return {
            "stage": result.get("stage"),
            "doc_type": result.get("doc_type"),
            "extracted_data": result.get("extracted_data"),
            "classification_confidence": result.get("classification_confidence"),
            "extraction_confidence": result.get("extraction_confidence"),
            "review_decision": result.get("review_decision"),
            "error_message": result.get("error_message"),
        }
    if task == "intake":
        update = bg.intake_node(build_state(case))
        return _intake_result(case, update)
    if task == "classification":
        update = bg.classify_node(build_state(case))
        return {
            "doc_type": update.get("doc_type"),
            "contract_subtype": update.get("contract_subtype"),
            "doc_subclass": update.get("doc_subclass"),
            "confidence": update.get("classification_confidence"),
        }
    if task in TASK_SPECIALIST:
        state = build_state(case, doc_type=case.get("expected_doc_class"))
        update = bg.extract_node(state)
        return {
            "extracted_data": update.get("extracted_data"),
            "extraction_confidence": update.get("extraction_confidence"),
            "doc_type": update.get("doc_type", state.get("doc_type")),
        }
    if task == "judge_arbiter":
        state = build_state(case, doc_type=case.get("expected_doc_class"))
        state["extracted_data"] = dict(case.get("expected_fields") or {})
        # Control the judge gate deterministically: fixtures expect scrutiny.
        state["extraction_confidence"] = 0.75 if case.get("review_expected") else 0.95
        update = bg.judge_verify_node(state)
        return {
            "judge_verdict": update.get("judge_verdict"),
            "completeness_label": update.get("judge_verdict"),
            "completeness": update.get("judge_score"),
            "judge_findings": update.get("judge_findings"),
        }
    if task == "arbiter":
        state = build_state(case, doc_type=case.get("expected_doc_class"))
        state["extracted_data"] = dict(case.get("expected_fields") or {})
        state["judge_verdict"] = str(case.get("fixture_kind") or "incomplete")
        state["judge_findings"] = [str(case.get("failure_note") or "isolation eval")]
        state["judge_score"] = case.get("probes_confidence")
        update = bg.arbiter_node(state)
        return {"decision": update.get("arbiter_decision")}
    if task == "boss":
        state = build_state(case, doc_type=case.get("expected_doc_class"))
        state["extracted_data"] = dict(case.get("expected_fields") or {})
        state["escalation_reason"] = str(case.get("fixture_kind") or "conflict_detected")
        state["conflict_detected"] = True
        update = bg.boss_escalation_node(state)
        return {"decision": update.get("review_decision")}
    if task == "retry":
        # Retry calibration probes the extract node on failure-shaped fixtures.
        state = build_state(case, doc_type=case.get("expected_doc_class"))
        update = bg.extract_node(state)
        return {
            "extracted_data": update.get("extracted_data"),
            "extraction_confidence": update.get("extraction_confidence"),
            "doc_type": update.get("doc_type", state.get("doc_type")),
        }
    if task == "archivist":
        from pipeline.bins import archive_dir, manifests_dir

        state = build_state(case, doc_type=case.get("expected_doc_class"))
        state["stage"] = "report_compiled"
        update = bg.archive_node(state)
        # archive_node returns only {"stage": ...}; verify conformance from
        # the isolated base dir (archive bin + manifest sidecar).
        archived_file = any(
            (archive_dir() / str(case.get("filename") or "")).resolve()
            == p.resolve()
            for p in archive_dir().rglob(str(case.get("filename") or "*"))
        )
        manifest_written = any(
            str(case.get("id") or "") in p.name or str(case.get("filename") or "") in p.name
            for p in manifests_dir().glob("*.json")
        )
        return {
            "stage": update.get("stage"),
            "archive_path": str(archived_file),
            "audit_entry": manifest_written,
            "sha256_ok": archived_file,
        }
    raise ValueError(f"task {task!r} has no node-mode invocation")


def _intake_result(case: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    prep = update.get("intake_prep") or {}
    return {
        "doc_text": update.get("doc_text"),
        "cleaned": prep.get("cleaned") if isinstance(prep, dict) else None,
        "triage": (prep or {}).get("triage") if isinstance(prep, dict) else None,
        "intake_stats": update.get("intake_stats"),
    }


def _specialist_for_class(doc_class: str) -> str | None:
    return {
        "contract": "contracts_specialist",
        "merger_agreement": "contracts_specialist",
        "corporate_record": "corporate_records_specialist",
        "correspondence": "correspondence_specialist",
        "compliance_filing": "compliance_specialist",
        "insurance_claim": "insurance_claims_specialist",
    }.get(doc_class)


def _invoke_agent(task: str, case: dict[str, Any]) -> dict[str, Any]:
    text = str(case.get("text") or "")
    doc_class = str(case.get("expected_doc_class") or "")
    task = _canonical_task(task)
    if task == "retry":
        # Retry calibration probes the specialist on failure-shaped fixtures.
        specialist = TASK_SPECIALIST.get(_specialist_for_class(doc_class), "contracts_specialist")
        import importlib

        mod_name, cls_name = _SPECIALIST_CLASSES[specialist]
        cls = getattr(importlib.import_module(mod_name), cls_name)
        result = cls().extract(text)
        return {
            "extracted_data": result,
            "extraction_confidence": result.get("confidence") if isinstance(result, dict) else None,
            "doc_type": doc_class,
        }
    if task == "intake":
        from agents.intake import IntakeAgent

        return IntakeAgent().intake_run(text, filename=str(case.get("filename") or "case.txt"))
    if task == "classification":
        from agents.sorter import SorterAgent

        doc_type, subtype, confidence, reasoning = SorterAgent().classify(text)
        return {
            "doc_type": doc_type,
            "contract_subtype": subtype,
            "doc_subclass": subtype,
            "confidence": confidence,
            "reasoning": reasoning,
        }
    if task in TASK_SPECIALIST:
        import importlib

        mod_name, cls_name = _SPECIALIST_CLASSES[TASK_SPECIALIST[task]]
        cls = getattr(importlib.import_module(mod_name), cls_name)
        return cls().extract(text)
    if task == "judge_arbiter":
        from agents.judge import CompletenessJudge

        extracted = case.get("expected_fields") or {}
        return CompletenessJudge().judge_completeness(doc_class, extracted, text)
    if task == "arbiter":
        from agents.arbiter import ArbiterAgent

        return ArbiterAgent().arbitrate(
            doc_type=doc_class,
            extracted=case.get("expected_fields") or {},
            judge_verdict=str(case.get("fixture_kind") or "incomplete"),
            judge_findings=[str(case.get("failure_note") or "isolation eval")],
            judge_score=case.get("probes_confidence"),
        )
    if task == "boss":
        from agents.boss import BossAgent

        return BossAgent().adjudicate(
            {
                "doc_id": case.get("id"),
                "doc_type": doc_class,
                "extracted_data": case.get("expected_fields") or {},
                "escalation_reason": str(case.get("fixture_kind") or "isolation eval"),
            }
        )
    if task == "archivist":
        return {"stage": "archived", "archive_path": None, "audit_entry": False, "sha256_ok": False}
    raise ValueError(f"task {task!r} has no agent-mode invocation")


def invoke(task: str, case: dict[str, Any], *, mode: str = "node") -> dict[str, Any]:
    """Run one case through the task's node or agent. Returns the prediction."""
    if mode == "node":
        return _invoke_node(task, case)
    if mode == "agent":
        return _invoke_agent(task, case)
    raise ValueError(f"unknown invoke mode {mode!r} (node|agent)")
