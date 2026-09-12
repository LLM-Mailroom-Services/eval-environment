"""Registry + runner smoke tests (mock mode, tiny local case lists)."""

from __future__ import annotations

from pathlib import Path

import pytest

from evals import experiment_log
from evals.registry import get_task, list_tasks
from evals.runner import run_task


def test_registry_complete():
    ids = {spec.task_id for spec in list_tasks()}
    for expected in (
        "eval:intake", "eval:classification", "eval:contracts", "eval:merger_agreement",
        "eval:corporate_records", "eval:correspondence", "eval:insurance_claims",
        "eval:judge_arbiter", "eval:arbiter", "eval:boss", "eval:archivist",
        "eval:pipeline_chain",
        "pilot:classification", "pilot:pipeline_chain",
        "calibration:classify", "calibration:judge", "calibration:arbiter",
        "calibration:retry", "calibration:boss", "calibration:intake", "calibration:archivist",
    ):
        assert expected in ids, f"missing {expected}"


def test_get_task_unknown():
    with pytest.raises(KeyError):
        get_task("eval:nope")


def test_agent_mode_rejected_for_chain():
    with pytest.raises(ValueError):
        run_task("eval:pipeline_chain", invoke_mode="agent", mock=True)


def _stub_load_cases(monkeypatch, cases):
    from evals import runner

    monkeypatch.setattr(runner, "load_cases", lambda *a, **k: (cases, {"n_total": len(cases), "n_selected": len(cases), "config": "ground_truth", "split": "train", "revision": "deadbeef", "repo": "x"}))


def test_run_task_mock_classification(monkeypatch, sample_case):
    _stub_load_cases(monkeypatch, [sample_case])
    result = run_task("eval:classification", mock=True, n=1)
    summary = result.summary
    assert summary["family"] == "eval" and summary["task"] == "classification"
    assert summary["mode"] == "mock" and summary["trace_backend"] == "none"
    assert summary["metrics"]["n"] == 1
    assert summary["dataset"]["n_selected"] == 1
    # prompt lineage: frozen v1 by default, provenance recorded
    assert summary["prompt_lineage"] == "frozen"
    assert summary["prompt_versions"]["sorter"]["key"] == "sorter_v1"
    assert summary["pipeline_git"]
    assert summary["prompts_snapshot_path"] and Path(summary["prompts_snapshot_path"]).exists()
    # case rows carry the post-hoc text-integrity key
    assert result.case_rows[0]["doc_text_sha256"]
    # experiment log landed
    runs = experiment_log.load_runs()
    assert any(r["run_id"] == summary["run_id"] for r in runs)
    assert experiment_log.md_path().exists()


def test_run_task_mock_specialist(monkeypatch, sample_case):
    _stub_load_cases(monkeypatch, [sample_case])
    result = run_task("eval:contracts", mock=True, invoke_mode="agent", n=1)
    assert result.summary["metrics"]["n"] == 1
    assert result.summary["metrics"]["errors"] == 0


def test_run_task_mock_judge(monkeypatch, fixture_case):
    _stub_load_cases(monkeypatch, [fixture_case])
    result = run_task("eval:judge_arbiter", mock=True, invoke_mode="agent", n=1)
    assert result.summary["metrics"]["n"] == 1


def test_run_task_mock_calibration(monkeypatch, fixture_case):
    _stub_load_cases(monkeypatch, [dict(fixture_case, calibration_cell="correct_high", probes_confidence=0.95)])
    result = run_task("calibration:classify", mock=True, invoke_mode="agent", n=1)
    summary = result.summary
    assert "calibration" in summary
    assert summary["calibration"].get("report_paths")
    assert Path(summary["calibration"]["report_paths"]["md"]).exists()


def test_run_task_error_recorded(monkeypatch, sample_case):
    from evals import invoke as invoke_mod

    _stub_load_cases(monkeypatch, [sample_case])
    monkeypatch.setattr(invoke_mod, "invoke", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    result = run_task("eval:classification", mock=True, n=1)
    assert result.summary["metrics"]["errors"] == 1
    assert result.case_rows[0]["error"]
