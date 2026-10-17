"""Offline unit tests for Braintrust OBSERVE orchestration and manifest output."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from unittest.mock import Mock, call

import gepa_observe_specialists as observe
import pytest


@pytest.fixture(autouse=True)
def _isolated_observe(monkeypatch, tmp_path):
    monkeypatch.setattr(observe, "REPO", tmp_path)
    monkeypatch.setattr(observe.experiment_log, "load_runs", Mock(return_value=[]))
    monkeypatch.setattr(
        observe.bt,
        "fetch_experiment_events",
        Mock(side_effect=AssertionError("unexpected SDK fetch")),
    )
    monkeypatch.setattr(
        observe, "_export_one", Mock(side_effect=AssertionError("unexpected export subprocess"))
    )


def _run(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["gepa_observe_specialists.py", *args])
    return observe.main()


def _logged_run(task, run_id):
    return {
        "task": task,
        "run_id": run_id,
        "mode": "real",
        "trace_ids": {"backend": "braintrust", "experiment": run_id},
    }


def _read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_jsonl_writer_creates_parents_round_trips_rows_and_overwrites(tmp_path):
    path = tmp_path / "nested" / "manifest.jsonl"
    rows = [{"case_id": "café", "artifact": Path("local.json")}, {"case_id": "second"}]

    assert observe._write_jsonl(path, rows) == 2
    assert _read_jsonl(path) == [
        {"case_id": "café", "artifact": "local.json"},
        {"case_id": "second"},
    ]
    assert path.read_text(encoding="utf-8").endswith("\n")
    assert observe._write_jsonl(path, []) == 0
    assert path.read_text(encoding="utf-8") == ""


def test_log_enrichment_keeps_successes_when_an_experiment_fails(monkeypatch, capsys):
    rows = [{"case_id": "case-a"}]
    before = deepcopy(rows)
    first = [{**rows[0], "braintrust": {"experiment": "first"}}]
    last = [{**rows[0], "braintrust": {"experiment": "last"}}]
    enrich = Mock(side_effect=[first, RuntimeError("offline"), last])
    monkeypatch.setattr(observe.bt, "enrich_manifest_from_braintrust", enrich)

    assert observe._enrich_from_log_runs(rows, ["first", "broken", "last"]) == last
    assert enrich.call_args_list == [
        call(rows, experiment_name="first"),
        call(first, experiment_name="broken"),
        call(first, experiment_name="last"),
    ]
    assert rows == before
    assert "braintrust enrich skipped for broken: RuntimeError: offline" in capsys.readouterr().out


@pytest.mark.parametrize("rows", [[], [{"case_id": "failure", "scores": {"overall_score": 0.2}}]])
def test_backlog_helper_writes_rows_and_returns_count(monkeypatch, tmp_path, rows):
    entries = [{"experiment": "exp", "run_id": "run"}]
    build = Mock(return_value=rows)
    monkeypatch.setattr(observe.bt, "build_task_backlog_manifest", build)
    path = tmp_path / "nested" / "failures.jsonl"

    assert observe._braintrust_backlog_for_task("contracts", entries, path) == len(rows)
    build.assert_called_once_with("contracts", entries)
    assert _read_jsonl(path) == rows


@pytest.mark.parametrize(
    ("args", "selected"),
    [
        (["--braintrust-backlog"], ["contracts", "correspondence"]),
        (["--braintrust-backlog", "--task", "contracts"], ["contracts"]),
        (["--braintrust-backlog", "--all-defaults"], ["contracts", "correspondence"]),
    ],
)
def test_backlog_cli_selects_tasks_and_updates_index_counts(
    monkeypatch, tmp_path, capsys, args, selected
):
    runs = [_logged_run("correspondence", "mail-run"), _logged_run("contracts", "contract-run")]
    monkeypatch.setattr(observe.experiment_log, "load_runs", Mock(return_value=runs))
    rows = {
        "contracts": [{"case_id": "contract-a"}, {"case_id": "contract-b"}],
        "correspondence": [{"case_id": "mail-a"}],
    }
    build = Mock(side_effect=lambda task, entries: rows[task])
    monkeypatch.setattr(observe.bt, "build_task_backlog_manifest", build)
    merge = Mock(side_effect=AssertionError("backlog must not export local runs"))
    monkeypatch.setattr(observe, "merge_failures", merge)

    assert _run(monkeypatch, *args, "--index-out", "catalog/index.json") == 0

    assert [args[0] for args, _ in build.call_args_list] == selected
    for task in selected:
        assert (
            _read_jsonl(
                tmp_path / "data/manifests/gepa" / f"{task}_braintrust_backlog.failures.jsonl"
            )
            == rows[task]
        )
    index = json.loads((tmp_path / "catalog/index.json").read_text(encoding="utf-8"))
    for task, task_rows in rows.items():
        expected_count = len(task_rows) if task in selected else None
        assert index["tasks"][task]["n_failures_merged"] == expected_count
        assert index["tasks"][task]["n_runs"] == 1
    merge.assert_not_called()
    if "--all-defaults" in args:
        assert "insurance_claims: no Braintrust runs in log — skip" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("args", "message"),
    [
        ([], "pass --task"),
        (["--braintrust-backlog"], "no Braintrust specialist runs found"),
        (["--task", "unknown"], "invalid choice"),
    ],
)
def test_cli_rejects_invalid_or_unavailable_selection(monkeypatch, capsys, args, message):
    with pytest.raises(SystemExit) as exc:
        _run(monkeypatch, *args)
    assert exc.value.code == 2
    assert message in capsys.readouterr().err


def test_backlog_cli_skips_requested_task_without_runs(monkeypatch, tmp_path, capsys):
    build = Mock()
    monkeypatch.setattr(observe.bt, "build_task_backlog_manifest", build)

    assert _run(monkeypatch, "--braintrust-backlog", "--task", "contracts") == 0
    assert "contracts: no Braintrust runs in log — skip" in capsys.readouterr().out
    build.assert_not_called()
    assert not (tmp_path / "data").exists()


@pytest.mark.parametrize("all_defaults", [False, True])
@pytest.mark.parametrize("enrich", [False, True])
def test_log_export_cli_enriches_only_when_requested(monkeypatch, tmp_path, all_defaults, enrich):
    original = [{"case_id": "failure", "scores": {"overall_score": 0.3}}]
    enriched = [{**original[0], "trace_excerpt": {"reasoning": "evidence"}}]

    def export(run_ids, path):
        observe._write_jsonl(path, original)
        return 1, len(run_ids)

    merge = Mock(side_effect=export)
    enrich_rows = Mock(return_value=enriched)
    monkeypatch.setattr(observe, "merge_failures", merge)
    monkeypatch.setattr(observe, "_enrich_from_log_runs", enrich_rows)
    args = (
        ["--all-defaults"]
        if all_defaults
        else [
            "--task",
            "contracts",
            "--run-id",
            "custom-a",
            "--run-id",
            "custom-b",
            "--out",
            str(tmp_path / "custom.jsonl"),
        ]
    )
    if enrich:
        args.append("--enrich-braintrust")

    assert _run(monkeypatch, *args) == 0

    expected = (
        [
            (run_ids, tmp_path / "data/manifests/gepa" / f"{task}_merged.failures.jsonl")
            for task, run_ids in observe.DEFAULT_RUNS.items()
        ]
        if all_defaults
        else [(["custom-a", "custom-b"], tmp_path / "custom.jsonl")]
    )
    assert merge.call_args_list == [call(run_ids, path) for run_ids, path in expected]
    assert enrich_rows.call_args_list == (
        [call(original, run_ids) for run_ids, _ in expected] if enrich else []
    )
    for _, path in expected:
        assert _read_jsonl(path) == (enriched if enrich else original)


def test_log_export_uses_default_task_runs_and_writes_discovered_index(monkeypatch, tmp_path):
    run = _logged_run("contracts", "logged-run")
    monkeypatch.setattr(observe.experiment_log, "load_runs", Mock(return_value=[run]))
    merge = Mock(return_value=(0, 0))
    monkeypatch.setattr(observe, "merge_failures", merge)

    assert _run(monkeypatch, "--task", "contracts") == 0

    merge.assert_called_once_with(
        observe.DEFAULT_RUNS["contracts"],
        tmp_path / "data/manifests/gepa/contracts_merged.failures.jsonl",
    )
    index = json.loads((tmp_path / "reports/gepa/braintrust_backlog_index.json").read_text())
    assert index["tasks"]["contracts"]["runs"][0]["run_id"] == "logged-run"
    assert index["tasks"]["contracts"]["n_failures_merged"] is None
