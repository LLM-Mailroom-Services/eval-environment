"""Analysis + comparison tests (local, sink-free)."""

from __future__ import annotations

import pytest

from evals import experiment_log
from evals.analysis import _bootstrap_delta_ci, aggregate_run, compare_runs


def _write_run(tmp_path, monkeypatch, run_id, class_correct):
    monkeypatch.setenv("EXPERIMENT_LOG_PATH", str(tmp_path / "log.jsonl"))
    monkeypatch.setenv("EXPERIMENT_LOG_MD_PATH", str(tmp_path / "log.md"))
    monkeypatch.setenv("EVALS_EXPERIMENTS_DIR", str(tmp_path / "experiments"))
    rows = [
        {
            "run_id": run_id, "case_id": f"c{i}",
            "filename": f"doc{i}.txt",
            "expected_doc_class": "contract",
            "prediction": {"doc_type": "contract" if class_correct[i] else "correspondence"},
            "scores": {"class_correct": int(class_correct[i])},
            "latency_ms": 1.0, "error": None,
        }
        for i in range(len(class_correct))
    ]
    summary = {
        "schema_version": 2, "record_kind": "run_summary", "run_id": run_id,
        "family": "eval", "task": "classification", "invoke": "node", "mode": "mock",
        "model": "m", "prompt_version": "sorter_v1", "prompt_lineage": "frozen",
        "trace_backend": "none",
        "started_at": experiment_log.utc_now(), "finished_at": experiment_log.utc_now(),
        "dataset": {"repo": "x", "n_selected": len(rows), "n_total": len(rows)},
        "params": {}, "metrics": {"n": len(rows), "class_accuracy": sum(class_correct) / len(class_correct)},
        "performance": {},
    }
    experiment_log.write_run(summary, rows)


def test_aggregate_run_confusion(tmp_path, monkeypatch):
    _write_run(tmp_path, monkeypatch, "r1", [1, 0, 0])
    agg = aggregate_run("r1")
    assert agg["metrics"]["class_accuracy"] == pytest.approx(1 / 3, abs=0.01)
    assert agg["confusion_matrix"] == {"contract": {"contract": 1, "correspondence": 2}}


def test_compare_runs_delta_and_ci(tmp_path, monkeypatch):
    _write_run(tmp_path, monkeypatch, "base", [1, 1, 1, 1])
    _write_run(tmp_path, monkeypatch, "cand", [1, 1, 1, 0])
    comparison = compare_runs("base", "cand")
    assert comparison["metric_deltas"]["class_accuracy"]["delta"] == pytest.approx(-0.25, abs=0.01)
    assert comparison["n_shared_cases"] == 4
    ci = comparison["paired_case_deltas"]["class_correct"]
    assert ci["delta"] == pytest.approx(-0.25, abs=0.01)
    assert ci["ci_lo"] <= ci["delta"] <= ci["ci_hi"]


def test_bootstrap_delta_ci_perfect_separation():
    ci = _bootstrap_delta_ci([1.0] * 10, n_boot=200, seed=1)
    assert ci["delta"] == 1.0 and ci["ci_lo"] == 1.0 and ci["ci_hi"] == 1.0
