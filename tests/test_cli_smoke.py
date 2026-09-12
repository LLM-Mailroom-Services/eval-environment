"""CLI smoke tests — every script entrypoint parses args and runs its mock /
hermetic path end-to-end. These are the in-suite version of the manual
smoke commands in AGENTS.md (mock runs stay hermetic via conftest)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))


def _main(module_name):
    """Call a script's zero-arg main() with the given argv."""
    import importlib

    mod = importlib.import_module(module_name)

    def run(*argv):
        old = sys.argv
        sys.argv = [module_name, *argv]
        try:
            return mod.main()
        finally:
            sys.argv = old

    return run


# ── run_evals.py ─────────────────────────────────────────────────────
def test_run_evals_list(capsys):
    rc = _main("run_evals")("--list")
    out = capsys.readouterr().out
    assert rc == 0
    assert "eval:classification" in out and "pilot:pipeline_chain" in out
    assert "calibration:classify" in out


def test_run_evals_mock_single(capsys):
    rc = _main("run_evals")("--task", "eval:classification", "--mock", "--n", "2")
    out = capsys.readouterr().out
    assert rc == 0
    assert "errors=0" in out


def test_run_evals_mock_all(capsys):
    rc = _main("run_evals")("--task", "all", "--mock", "--n", "1")
    out = capsys.readouterr().out
    assert rc == 0
    # every family executed without errors
    assert out.count("errors=0") >= 12


def test_run_evals_rejects_mock_and_real(capsys):
    with pytest.raises(SystemExit):
        _main("run_evals")("--task", "eval:classification", "--mock", "--real")


def test_run_evals_rejects_unknown_task():
    with pytest.raises(SystemExit):
        _main("run_evals")("--task", "eval:nope", "--mock")


# ── score_run.py ─────────────────────────────────────────────────────
@pytest.fixture
def scored_run(sample_case, monkeypatch):
    """One mock run in the hermetic log, its run_id returned."""
    from evals import runner

    monkeypatch.setattr(
        runner, "load_cases",
        lambda *a, **k: ([sample_case], {"n_total": 1, "n_selected": 1, "config": "ground_truth", "split": "train", "revision": "deadbeef", "repo": "x"}),
    )
    return runner.run_task("eval:classification", mock=True, n=1).summary["run_id"]


def test_score_run_recompute(scored_run, capsys, tmp_path):
    rc = _main("score_run")("--run-id", scored_run, "--recompute")
    assert rc == 0
    from evals import experiment_log

    rescored = experiment_log.experiments_dir() / scored_run / "rescored.jsonl"
    rows = [json.loads(l) for l in rescored.read_text().splitlines() if l.strip()]
    assert rows and rows[0]["scores_rescored"]


def test_score_run_judge_mock(scored_run, capsys):
    rc = _main("score_run")("--run-id", scored_run, "--judge", "classification", "--mock")
    assert rc == 0
    from evals import experiment_log

    judgments = experiment_log.experiments_dir() / scored_run / "judgments.jsonl"
    assert judgments.exists()


def test_score_run_export_failures(scored_run, capsys, tmp_path):
    manifest = tmp_path / "failures.jsonl"
    rc = _main("score_run")("--run-id", scored_run, "--export-failures", str(manifest))
    assert rc == 0  # zero failures still exits 0 and writes an empty manifest
    assert manifest.exists()


# ── compare_runs.py ──────────────────────────────────────────────────
def test_compare_runs_md(scored_run, capsys, tmp_path):
    from evals import runner

    second = runner.run_task("eval:classification", mock=True, n=1).summary["run_id"]
    out_dir = tmp_path / "comparisons"
    rc = _main("compare_runs")("--a", second, "--b", scored_run, "--md", str(out_dir))
    assert rc == 0
    md_files = list(out_dir.glob("*-compare.md"))
    assert md_files, "comparison markdown not written"


# ── freeze_prompts.py / render_experiment_log.py ─────────────────────
def test_freeze_prompts_check():
    assert _main("freeze_prompts")("--check") == 0


def test_render_experiment_log_validate(capsys):
    rc = _main("render_experiment_log")("--validate")
    out = capsys.readouterr().out
    assert rc == 0
    assert "OK" in out


def test_render_experiment_log_rebuild(capsys):
    rc = _main("render_experiment_log")()
    assert rc == 0
