"""Site snapshot exporter (scripts/export_site_snapshot.py) — hermetic tests."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from evals import experiment_log

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "export_site_snapshot.py"
_spec = importlib.util.spec_from_file_location("export_site_snapshot", _SCRIPT)
# The script inserts <repo>/src into sys.path itself; guard against double-load.
snap = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("export_site_snapshot", snap)
_spec.loader.exec_module(snap)


@pytest.fixture
def logged_run(sample_case, monkeypatch):
    """One recorded mock run in the hermetic log."""
    from evals import runner

    monkeypatch.setattr(runner, "load_cases", lambda *a, **k: ([sample_case], {"n_total": 1, "n_selected": 1, "config": "ground_truth", "split": "train", "revision": "deadbeef", "repo": "x"}))
    result = runner.run_task("eval:classification", mock=True, n=1)
    return result.summary


def test_build_snapshot_shape(logged_run):
    snapshot = snap.build_snapshot()
    assert snapshot["schema"] == "eval-site-snapshot" and snapshot["version"] == 1
    assert snapshot["generated_at"]
    # health: the hermetic log validates, lineage drift-free
    assert snapshot["health"]["log_valid"] is True
    assert snapshot["health"]["log_records"] >= 1
    assert snapshot["health"]["lineage_drift_free"] is True
    # environment sections populated
    env = snapshot["environment"]
    assert len(env["tasks"]) == 31
    assert env["corpus"]["revision"] == "46a4d3c240a36671cde0182fff4960f6b8b73aca"
    assert len(env["prompts"]["versions"]) == 15
    assert "prompt-lineage" in env["inventory"]["skills"]
    assert "prompt-engineer" in env["inventory"]["subagents"]
    assert env["inventory"]["test_count"] > 60
    # the logged run appears with trimmed shape + headline + embedded cases
    run = next(r for r in snapshot["runs"] if r["run_id"] == logged_run["run_id"])
    assert run["headline"] is not None
    assert run["n_cases"] == 1
    assert "cases_ref" not in run and "prompts_snapshot_path" not in run
    cases = snapshot["cases"][logged_run["run_id"]]
    assert len(cases) == 1
    assert cases[0]["filename"] == "test_doc.txt"
    assert cases[0]["scores"]
    assert "prediction" in cases[0]


def test_case_trim_drops_bulk(sample_case, monkeypatch, logged_run):
    """Case rows keep scores/expectations but never raw doc text or big payloads."""
    big = dict(sample_case)
    big["text"] = "x" * 5000
    big["prediction"] = {"doc_type": "contract", "extracted_data": {"blob": "y" * 5000}, "stage": "archived"}
    monkeypatch.setattr(experiment_log, "load_cases", lambda run_id: [big])
    snapshot = snap.build_snapshot()
    case = snapshot["cases"][logged_run["run_id"]][0]
    assert "text" not in case
    assert case["prediction"] == {"doc_type": "contract", "stage": "archived"}
    assert len(json.dumps(case)) < 2000


def test_check_mode_detects_stale(logged_run, tmp_path, monkeypatch):
    monkeypatch.setattr(snap, "SNAPSHOT_PATH", tmp_path / "snapshot.json")
    # missing -> stale
    assert _run_main(["--check"]) == 1
    # current -> ok
    snapshot = snap.build_snapshot()
    (tmp_path / "snapshot.json").write_text(json.dumps(snapshot))
    assert _run_main(["--check"]) == 0
    # tampered runs -> stale
    snapshot["runs"] = []
    (tmp_path / "snapshot.json").write_text(json.dumps(snapshot))
    assert _run_main(["--check"]) == 1


def _run_main(argv):
    old = sys.argv
    sys.argv = ["export_site_snapshot.py", *argv]
    try:
        return snap.main()
    finally:
        sys.argv = old
