"""Task modules + preflight + subset-manifest contracts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from evals.preflight import PreflightError, run_preflight
from evals.registry import EVAL_TASKS, get_task
from evals.tasks import ALL_EVAL_TASKS, get_eval_task, list_eval_tasks
from evals.tasks.base import write_scoring_suite, write_subset_manifest


def test_eval_task_modules_match_registry():
    """Every registry eval TaskSpec has a framing module with aligned metadata."""
    modules = {t.name: t for t in ALL_EVAL_TASKS}
    assert len(modules) == len(EVAL_TASKS)
    for spec in EVAL_TASKS:
        task = modules[spec.name]
        assert task.node_name == spec.node_name
        assert task.default_subset == spec.default_subset
        assert task.scorer == spec.scorer
        assert task.supports_agent_mode == spec.supports_agent_mode
        assert task.request, f"{spec.name} missing request framing"
        assert task.to_spec().task_id == spec.task_id


def test_specialist_tasks_carry_entity_fields():
    for name in (
        "contracts",
        "merger_agreement",
        "corporate_records",
        "correspondence",
        "insurance_claims",
    ):
        task = get_eval_task(f"eval:{name}")
        assert task.doc_class
        assert task.prompt_role.endswith("_specialist")
        assert len(task.entity_fields) >= 5
        assert "extract" in task.request.lower()
        assert task.entity_fields[0]  # non-empty strings


def test_get_eval_task_aliases():
    assert get_eval_task("contracts").name == "contracts"
    assert get_eval_task("eval:classification").name == "classification"
    assert get_eval_task("pilot:contracts").name == "contracts"
    assert get_eval_task("calibration:classify").name == "classification"
    with pytest.raises(KeyError):
        get_eval_task("eval:does_not_exist")


def test_list_eval_tasks_ordered():
    names = [t.name for t in list_eval_tasks()]
    assert names[0] == "intake"
    assert names[-1] == "pipeline_chain"
    assert "contracts" in names


def test_subset_manifest_lock(tmp_path, sample_case):
    cases = [sample_case, dict(sample_case, id="case-2", filename="b.txt")]
    lock = write_subset_manifest(cases, run_dir=tmp_path, provenance={"seed": 42})
    assert lock["n"] == 2
    assert Path(lock["manifest_json"]).is_file()
    assert Path(lock["manifest_jsonl"]).is_file()
    data = json.loads(Path(lock["manifest_json"]).read_text())
    assert data["filenames"] == ["test_doc.txt", "b.txt"]
    assert data["provenance"]["seed"] == 42
    lines = Path(lock["manifest_jsonl"]).read_text().strip().splitlines()
    assert len(lines) == 2
    assert all("doc_text_sha256" in json.loads(line) for line in lines)


def test_scoring_suite_artifact(tmp_path):
    rows = [
        {"scores": {"overall_score": 0.8, "class_correct": 1}, "latency_ms": 10, "tokens": {"prompt": 1, "completion": 1, "total": 2}, "cost_usd": 0.0, "error": None},
        {"scores": {"overall_score": 0.6, "class_correct": 0}, "latency_ms": 20, "tokens": {"prompt": 1, "completion": 1, "total": 2}, "cost_usd": 0.0, "error": None},
    ]
    suite = write_scoring_suite(rows, run_dir=tmp_path, scorer="extraction")
    assert Path(suite["path"]).is_file()
    assert "metrics_full" in suite
    assert "metrics_essential" in suite
    assert suite["n_cases"] == 2


def test_preflight_mock_ok():
    spec = get_task("eval:contracts")
    report = run_preflight(spec, mock=True, subset="class:contract")
    assert report.ok
    assert report.framing is not None
    assert report.framing["prompt_role"] == "contracts_specialist"
    assert report.as_dict()["resolved"]["subset"] == "class:contract"


def test_preflight_real_requires_credentials(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GENERIC_API_KEY", raising=False)
    monkeypatch.delenv("DEFAULT_PROVIDER", raising=False)
    spec = get_task("eval:classification")
    report = run_preflight(spec, mock=False)
    assert not report.ok
    assert any(i.code == "llm_credentials" for i in report.errors)
    with pytest.raises(PreflightError):
        report.raise_if_failed()


def test_preflight_rejects_langfuse_backend():
    spec = get_task("eval:intake")
    report = run_preflight(spec, mock=True, trace_backend="langfuse")
    assert not report.ok
    assert any(i.code == "trace_backend" for i in report.errors)


def test_preflight_bad_subset():
    spec = get_task("eval:contracts")
    report = run_preflight(spec, mock=True, subset="class:not_a_class")
    assert not report.ok
    assert any(i.code == "subset_grammar" for i in report.errors)


def test_preflight_explicit_braintrust_needs_key(monkeypatch):
    monkeypatch.delenv("BRAINTRUST_API_KEY", raising=False)
    spec = get_task("eval:contracts")
    report = run_preflight(spec, mock=True, trace_backend="braintrust")
    assert not report.ok
    assert any(i.code == "braintrust_key" for i in report.errors)


def test_runner_records_preflight_and_manifest(monkeypatch, sample_case, tmp_path):
    from evals import runner

    monkeypatch.setattr(
        runner,
        "load_cases",
        lambda *a, **k: (
            [sample_case],
            {
                "n_total": 1,
                "n_selected": 1,
                "config": "ground_truth",
                "split": "train",
                "revision": "deadbeef",
                "repo": "x",
            },
        ),
    )
    result = runner.run_task(
        "eval:classification",
        mock=True,
        n=1,
        run_dir=tmp_path / "run",
    )
    assert result.summary.get("preflight", {}).get("ok") is True
    assert result.summary.get("task_framing", {}).get("prompt_role") == "sorter"
    assert (tmp_path / "run" / "subset_manifest.json").is_file()
    assert (tmp_path / "run" / "scoring_suite.json").is_file()
    assert result.summary["dataset"].get("filenames") == [sample_case["filename"]]


def test_runner_real_blocked_without_key(monkeypatch, sample_case):
    from evals import runner
    from evals.preflight import PreflightError

    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GENERIC_API_KEY", raising=False)
    monkeypatch.delenv("DEFAULT_PROVIDER", raising=False)
    monkeypatch.setattr(
        runner,
        "load_cases",
        lambda *a, **k: ([sample_case], {"n_total": 1, "n_selected": 1}),
    )
    with pytest.raises(PreflightError):
        runner.run_task("eval:classification", mock=False, n=1)
