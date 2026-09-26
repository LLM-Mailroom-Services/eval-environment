"""Task modules + preflight + subset-manifest contracts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from evals.preflight import PreflightError, run_preflight
from evals.registry import EVAL_TASKS, get_task
from evals.tasks import ALL_EVAL_TASKS, get_eval_task, list_eval_tasks
from evals.tasks.base import read_subset_manifest, write_scoring_suite, write_subset_manifest

_CASE_BASE = {
    "expected_doc_class": "contract",
    "expected_subclass": "master_services_agreement",
    "expected_specialist": "contracts_specialist",
    "expected_stage": "archived",
    "expected_fields": {"parties": ["Acme Corp", "Beta LLC"]},
    "source": "mailroom-dataset",
    "config": "ground_truth",
    "split": "train",
    "text": "MASTER SERVICES AGREEMENT between Acme Corp and Beta LLC.",
}


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
    assert len(suite["per_document"]) == 2
    assert (tmp_path / "per_document_scores.jsonl").is_file()
    lines = (tmp_path / "per_document_scores.jsonl").read_text().strip().splitlines()
    assert len(lines) == 2


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


# ── v3 fixes: resume-safe manifest, preflight-failure logging, flag plumbing ─


def _stub_loader(monkeypatch, runner, cases):
    def _load(subset, sample=None, seed=None, n=None):
        selected = cases[:n] if n is not None else cases
        return (
            selected,
            {
                "n_total": len(cases),
                "n_selected": len(selected),
                "config": "ground_truth",
                "split": "train",
                "revision": "deadbeef",
                "repo": "x",
            },
        )

    monkeypatch.setattr(runner, "load_cases", _load)


def test_resume_preserves_subset_manifest(monkeypatch, tmp_path):
    """A partial resume must never truncate the locked full case set."""
    import json

    from evals import runner

    cases = [
        {**_CASE_BASE, "id": f"corpus:ground_truth:train:doc_{i}.txt",
         "filename": f"doc_{i}.txt"}
        for i in range(3)
    ]
    _stub_loader(monkeypatch, runner, cases)
    run_dir = tmp_path / "run"

    first = runner.run_task("eval:classification", mock=True, n=2, run_dir=run_dir)
    manifest = json.loads((run_dir / "subset_manifest.json").read_text())
    assert manifest["n"] == 2

    # Resume the same run_id against a 3-case draw: 2 already run → 1 remains.
    # The manifest must still describe the original 2-case locked set.
    result = runner.run_task(
        "eval:classification", mock=True, n=3, run_dir=run_dir,
        resume_run_id=first.run_id,
    )
    after = json.loads((run_dir / "subset_manifest.json").read_text())
    assert after == manifest
    assert read_subset_manifest(run_dir)["case_ids"] == manifest["case_ids"]
    assert result.summary["dataset"]["case_ids"] == manifest["case_ids"]


def test_preflight_failure_is_logged(monkeypatch, sample_case):
    """Non-negotiable #1: a preflight-blocked run still writes a log line."""
    import json as _json

    from evals import experiment_log, runner
    from evals.preflight import PreflightError

    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GENERIC_API_KEY", raising=False)
    monkeypatch.delenv("DEFAULT_PROVIDER", raising=False)
    _stub_loader(monkeypatch, runner, [sample_case])
    before = experiment_log.load_runs()
    with pytest.raises(PreflightError):
        runner.run_task("eval:classification", mock=False, n=1)
    after = experiment_log.load_runs()
    assert len(after) == len(before) + 1
    blocked = after[-1]
    assert blocked["error"] and "PreflightError" in blocked["error"]
    assert blocked["metrics"] == {"n": 0, "errors": 0}
    assert blocked["preflight"]["ok"] is False
    # The appended record validates under the current schema.
    assert not experiment_log.validate_record(blocked)


def test_runner_skip_preflight(monkeypatch, sample_case, tmp_path):
    from evals import runner

    _stub_loader(monkeypatch, runner, [sample_case])
    result = runner.run_task(
        "eval:classification", mock=True, n=1, run_dir=tmp_path / "run",
        skip_preflight=True,
    )
    assert result.summary["preflight"] is None
    assert result.summary["task_framing"] is None


def test_preflight_require_trace_sink_blocks_none_backend(monkeypatch):
    from evals.preflight import PreflightError, run_preflight

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    spec = get_task("eval:classification")
    report = run_preflight(
        spec, mock=False, trace_backend="none", require_trace_sink=True,
    )
    assert not report.ok
    assert any(i.code == "trace_sink_required" for i in report.errors)
    with pytest.raises(PreflightError):
        report.raise_if_failed()
