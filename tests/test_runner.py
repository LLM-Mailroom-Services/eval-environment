"""Registry + runner smoke tests (mock mode, tiny local case lists)."""

from __future__ import annotations

from pathlib import Path

import pytest

from evals import experiment_log
from evals.registry import AGENT_CATALOG, get_task, list_tasks
from evals.runner import (
    EXTRACTION_TASK_SPECIALIST,
    _primary_prompt_key,
    _specialist_name,
    run_task,
)


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
    from evals.preflight import PreflightError

    with pytest.raises((ValueError, PreflightError)):
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


def test_run_task_concurrency_runs_documents_in_parallel(monkeypatch, sample_case):
    import time

    from evals import invoke as invoke_mod

    cases = [
        dict(sample_case, id=f"corpus:ground_truth:train:doc_{i}.txt", filename=f"doc_{i}.txt")
        for i in range(4)
    ]
    _stub_load_cases(monkeypatch, cases)

    def _slow(*_a, **_k):
        time.sleep(0.35)
        return {"doc_type": "contract", "confidence": 0.9}

    monkeypatch.setattr(invoke_mod, "invoke", _slow)
    started = time.perf_counter()
    result = run_task("eval:classification", mock=True, n=4, concurrency=4)
    elapsed = time.perf_counter() - started
    assert result.summary["metrics"]["n"] == 4
    assert result.summary["params"]["concurrency"] == 4
    assert elapsed < 1.0  # serial would be ~1.4s


def test_extraction_task_specialist_map_covers_all_five_and_is_1to1():
    """Each of the five extraction tasks maps to exactly one designated
    specialist, and no specialist is shared between two tasks — the "each
    specialist only maps to one class" rule, enforced structurally so it
    cannot silently drift (e.g. a new task added without an entry here)."""
    from evals.registry import EVAL_TASKS

    extraction_tasks = {spec.name for spec in EVAL_TASKS if spec.node_name == "extract-fields"}
    assert extraction_tasks == set(EXTRACTION_TASK_SPECIALIST)
    assert len(set(EXTRACTION_TASK_SPECIALIST.values())) == len(EXTRACTION_TASK_SPECIALIST)
    # Every mapped specialist really is in the shared catalog entry those
    # tasks point at.
    catalog_agents = set(AGENT_CATALOG["extract-fields"]["agents"])
    assert set(EXTRACTION_TASK_SPECIALIST.values()) == catalog_agents


@pytest.mark.parametrize(
    "task_name,expected_specialist",
    list(EXTRACTION_TASK_SPECIALIST.items()),
)
def test_primary_prompt_key_resolves_designated_specialist_not_first_in_catalog(
    task_name, expected_specialist
):
    """Regression for a real bug: every extraction task other than
    "contracts" reported prompt_version=contracts_specialist_v1 in its
    Braintrust experiment metadata (contracts_specialist is simply first in
    AGENT_CATALOG["extract-fields"]["agents"], and the old lookup returned
    whichever role appeared first in that shared list, not the one this
    task actually ran). Confirmed live on
    20260927T020724Z-eval-merger_agreement, whose case rows correctly used
    merger_agreement_specialist while the run-rollup metadata said
    contracts_specialist_v1."""
    spec = get_task(f"eval:{task_name}")
    versions = {
        role: {"key": f"{role}_v1", "lineage": "frozen"}
        for role in AGENT_CATALOG["extract-fields"]["agents"]
    }
    summary = {"prompt_versions": versions}
    assert _primary_prompt_key(spec, summary) == f"{expected_specialist}_v1"
    assert _specialist_name(spec, agent_usage=None) == expected_specialist
    # Even with (wrong-agent) usage data present, the designated mapping
    # still wins for extraction tasks — usage-sniffing must not override it.
    other_specialists = set(AGENT_CATALOG["extract-fields"]["agents"]) - {expected_specialist}
    fake_usage = {next(iter(other_specialists)): {"calls": 1}}
    assert _specialist_name(spec, agent_usage=fake_usage) == expected_specialist


def test_primary_prompt_key_falls_back_to_catalog_for_non_extraction_tasks():
    """Non-extraction tasks (single-purpose catalog entries, or
    pipeline_chain's genuinely multi-specialist entry) are unaffected by the
    extraction-task fix and keep resolving via the catalog list."""
    spec = get_task("eval:classification")
    versions = {"sorter": {"key": "sorter_v1", "lineage": "frozen"}}
    assert _primary_prompt_key(spec, {"prompt_versions": versions}) == "sorter_v1"
