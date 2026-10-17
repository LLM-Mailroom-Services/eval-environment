"""GEPA Braintrust backlog grounding (hermetic — no network)."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

from evals.gepa import braintrust_backlog as bt


def _sample_root(*, overall: float = 0.34) -> dict:
    return {
        "is_root": True,
        "root_span_id": "root-abc",
        "span_id": "span-eval-1",
        "input": {
            "case_ref": "corpus:ground_truth:train:doc#ca64ce537c8b",
            "chars": 78,
            "doc_text_sha256": "ca64ce537c8bd98cdcfa4e68ea1434ff4a915b4f00a5ee84d3e01e13addd92f9",
        },
        "metadata": {
            "run_id": "20260927T105317Z-eval-correspondence",
            "task": "eval:correspondence",
            "specialist": "correspondence_specialist",
            "prompt_version": "correspondence_specialist_v1",
            "prompt_key": "correspondence_specialist_v1",
            "model": "deepseek/deepseek-v4.1-flash",
            "filename": "dorland-c/_sent_mail/78.",
        },
        "expected": {
            "expected_doc_class": "correspondence",
            "expected_subclass": "email",
            "expected_fields": {"communication_type": "email", "intent": "other"},
        },
        "output": {
            "extracted_data": {
                "sender": "Chris",
                "communication_type": "email",
                "confidence": 0.75,
            },
            "scores": {"overall_score": overall, "extraction_f1": 0.13},
            "specialist": "correspondence_specialist",
        },
        "scores": {"overall_score": overall, "extraction_f1": 0.13},
        "span_attributes": {"type": "eval", "name": "correspondence_specialist"},
    }


def _sample_llm(parent_span_id: str) -> dict:
    return {
        "is_root": False,
        "span_parents": [parent_span_id],
        "metadata": {"model": "deepseek/deepseek-v4.1-flash"},
        "output": [
            {
                "message": {
                    "content": '{"sender":"Chris","confidence":0.75}',
                    "reasoning": "Recipient is null because no named addressee in the short note.",
                }
            }
        ],
        "span_attributes": {"type": "llm", "name": "Chat Completion"},
    }


def test_index_experiment_spans():
    root = _sample_root()
    llm = _sample_llm("span-eval-1")
    roots, llm_by_parent = bt.index_experiment_spans([root, llm])
    assert "root-abc" in roots
    assert llm_by_parent["span-eval-1"][0]["span_attributes"]["type"] == "llm"


def test_root_to_observe_row_includes_trace_excerpt():
    root = _sample_root()
    llm = _sample_llm("span-eval-1")
    row = bt.root_to_observe_row(
        root, run_id="20260927T105317Z-eval-correspondence", llm_spans=[llm]
    )
    assert row["braintrust"]["experiment"] == "20260927T105317Z-eval-correspondence"
    assert row["braintrust"]["prompt_version"] == "correspondence_specialist_v1"
    assert "Recipient is null" in (row["trace_excerpt"]["reasoning"] or "")
    assert row["scores"]["overall_score"] == 0.34


def test_merge_observe_rows_keeps_worst_score():
    good = bt.root_to_observe_row(_sample_root(overall=0.79), run_id="run-a", llm_spans=[])
    bad = bt.root_to_observe_row(_sample_root(overall=0.2), run_id="run-b", llm_spans=[])
    merged = bt.merge_observe_rows([good, bad])
    assert len(merged) == 1
    assert merged[0]["scores"]["overall_score"] == 0.2


def test_discover_braintrust_specialist_runs():
    runs = [
        {
            "run_id": "20260927T105317Z-eval-correspondence",
            "task": "correspondence",
            "mode": "real",
            "trace_ids": {
                "backend": "braintrust",
                "experiment": "20260927T105317Z-eval-correspondence",
            },
        },
        {
            "run_id": "mock-run",
            "task": "correspondence",
            "mode": "mock",
            "trace_ids": {"backend": "braintrust"},
        },
    ]
    by_task = bt.discover_braintrust_specialist_runs(runs)
    assert len(by_task["correspondence"]) == 1
    assert by_task["correspondence"][0]["experiment"] == "20260927T105317Z-eval-correspondence"


@pytest.mark.parametrize("task", sorted(bt.SPECIALIST_TASKS))
def test_discovery_preserves_metadata_sorts_runs_and_falls_back_to_run_id(task):
    later = {
        "run_id": "run-b",
        "task": task,
        "mode": "real",
        "trace_ids": {"backend": "braintrust"},
        "model": "unit-model",
        "prompt_version": "specialist_v2",
        "metrics": {"overall_score": 0.4},
    }
    earlier = {
        **later,
        "run_id": "run-a",
        "trace_ids": {"backend": "braintrust", "experiment": "named-experiment"},
    }
    runs = [later, earlier]
    before = deepcopy(runs)

    entries = bt.discover_braintrust_specialist_runs(runs)[task]

    assert entries == [
        {
            key: run.get(key)
            for key in ("run_id", "task", "model", "prompt_version", "trace_ids", "metrics")
        }
        | {"experiment": experiment}
        for run, experiment in [(earlier, "named-experiment"), (later, "run-b")]
    ]
    assert runs == before


@pytest.mark.parametrize(
    "overrides",
    [
        {"mode": "mock"},
        {"mode": None},
        {"task": "classification"},
        {"task": None},
        {"trace_ids": {"backend": "phoenix"}},
        {"trace_ids": None},
        {"run_id": None, "trace_ids": {"backend": "braintrust"}},
    ],
)
def test_discovery_ignores_runs_without_real_specialist_braintrust_evidence(overrides):
    run = {
        "run_id": "run-a",
        "task": "contracts",
        "mode": "real",
        "trace_ids": {"backend": "braintrust"},
    }
    assert bt.discover_braintrust_specialist_runs([{**run, **overrides}]) == {}


@pytest.mark.parametrize(
    ("event", "expected"),
    [
        ({}, False),
        ({"error": "provider failed"}, True),
        ({"error": "", "scores": {"overall_score": 0.8}}, False),
        ({"scores": {"overall_score": 0.799999}}, True),
        ({"scores": {"overall_score": 0.8}}, False),
        ({"scores": {"overall_score": 1.0}}, False),
        ({"scores": {"overall_score": 0}}, True),
        ({"metrics": {"overall_score": 0.2}}, True),
        ({"scores": {"overall_score": None}, "metrics": {"overall_score": 0.2}}, True),
        ({"scores": {"overall_score": 0.9}, "metrics": {"overall_score": 0.2}}, False),
        ({"scores": {"overall_score": "0.2"}}, False),
        ({"scores": {"extraction_f1": 0, "n_expected_fields": 0}}, False),
    ],
)
def test_observe_failure_selection_boundaries_and_score_fallback(event, expected):
    assert bt._is_observe_failure(event) is expected


@pytest.mark.parametrize("gate", ["class_correct", "judge_agrees", "schema_valid", "route_ok"])
@pytest.mark.parametrize(
    ("value", "expected"), [(0, True), (0.0, True), (1, False), ("0", False), (None, False)]
)
def test_observe_failure_gate_values(gate, value, expected):
    assert bt._is_observe_failure({"scores": {"overall_score": 0.95, gate: value}}) is expected


@pytest.mark.parametrize(
    ("project", "env_project", "expected_project", "set_current"),
    [
        (None, None, "Mailroom-Evals", False),
        (None, "env-project", "env-project", False),
        ("explicit-project", "env-project", "explicit-project", True),
    ],
)
def test_fetch_opens_existing_experiment_and_materializes_events(
    monkeypatch, project, env_project, expected_project, set_current
):
    monkeypatch.delenv("BRAINTRUST_PROJECT", raising=False)
    if env_project:
        monkeypatch.setenv("BRAINTRUST_PROJECT", env_project)
    events = [_sample_root(), _sample_llm("span-eval-1")]
    fetch = Mock(return_value=iter(events))
    init = Mock(return_value=SimpleNamespace(fetch=fetch))
    monkeypatch.setitem(sys.modules, "braintrust", SimpleNamespace(init=init))

    assert (
        bt.fetch_experiment_events("experiment-a", project=project, set_current=set_current)
        == events
    )
    init.assert_called_once_with(
        project=expected_project, experiment="experiment-a", open=True, set_current=set_current
    )
    fetch.assert_called_once_with()


@pytest.mark.parametrize("stage", ["init", "fetch"])
def test_fetch_propagates_sdk_errors(monkeypatch, stage):
    fetch = Mock()
    init = Mock(return_value=SimpleNamespace(fetch=fetch))
    failure = RuntimeError("SDK unavailable")
    {"init": init, "fetch": fetch}[stage].side_effect = failure
    monkeypatch.setitem(sys.modules, "braintrust", SimpleNamespace(init=init))

    with pytest.raises(RuntimeError, match="SDK unavailable"):
        bt.fetch_experiment_events("experiment-a")


def test_span_index_ignores_unrelated_events_and_keeps_llm_order():
    root = _sample_root()
    replacement = {**root, "metadata": {"model": "replacement"}}
    first = _sample_llm("span-eval-1")
    first["span_parents"].append("other-parent")
    second = _sample_llm("span-eval-1")
    second["output"] = []
    ignored = [
        {},
        {"span_attributes": None},
        {**root, "is_root": False, "root_span_id": "non-root"},
        {**root, "span_attributes": {"type": "task"}, "root_span_id": "task-root"},
        {"span_attributes": {"type": "llm"}, "span_parents": []},
    ]

    roots, children = bt.index_experiment_spans([root, first, *ignored, replacement, second])

    assert roots == {"root-abc": replacement}
    assert dict(children) == {"span-eval-1": [first, second]}


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        (None, None),
        ([], None),
        ("not a message", None),
        ({"reasoning": "  direct reason  "}, "direct reason"),
        (
            [
                None,
                "bad",
                {"message": None},
                {"message": {"reasoning": "  "}},
                {"message": {"reasoning": "  first  "}},
                {"reasoning": "second"},
            ],
            "first",
        ),
    ],
)
def test_reasoning_excerpt_handles_sparse_sdk_output(output, expected):
    assert bt._reasoning_excerpt({"output": output}) == expected


@pytest.mark.parametrize(("length", "expected"), [(8, "xxxxxxxx"), (9, "xxxxx...")])
def test_reasoning_excerpt_truncates_only_above_limit(length, expected):
    assert bt._reasoning_excerpt({"output": {"reasoning": "x" * length}}, limit=8) == expected


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        (None, None),
        ({"message": {"content": "{}"}}, None),
        (
            [
                None,
                {"message": None},
                {"message": {"content": "plain text"}},
                {"message": {"content": '  {"confidence": 0.7}  '}},
            ],
            {"confidence": 0.7},
        ),
        ([{"message": {"content": "[1, 2]"}}], None),
        (
            [{"message": {"content": "{invalid}"}}, {"message": {"content": '{"later": true}'}}],
            None,
        ),
    ],
)
def test_json_content_fallback_rejects_invalid_or_unsupported_output(output, expected):
    assert bt._parse_json_content({"output": output}) == expected


def test_observe_row_preserves_evidence_without_exporting_document_text():
    root = _sample_root()
    root["input"]["text"] = "PRIVATE RAW DOCUMENT"
    root["metadata"]["text"] = "PRIVATE RAW DOCUMENT"
    before = deepcopy(root)

    row = bt.root_to_observe_row(root, run_id="export-run", project="custom-project")

    assert row["run_id"] == "export-run"
    assert row["braintrust"] == {
        "project": "custom-project",
        "experiment": root["metadata"]["run_id"],
        "span_id": "span-eval-1",
        "root_span_id": "root-abc",
        "prompt_version": "correspondence_specialist_v1",
        "model": "deepseek/deepseek-v4.1-flash",
    }
    assert row["case_id"] == root["input"]["case_ref"]
    assert row["filename"] == root["metadata"]["filename"]
    assert row["expected_fields"] == root["expected"]["expected_fields"]
    assert row["doc_text_sha256"] == root["input"]["doc_text_sha256"]
    assert row["prediction"]["extracted_data"] == root["output"]["extracted_data"]
    assert row["trace_excerpt"] == {"reasoning": None, "output_confidence": 0.75}
    assert "PRIVATE RAW DOCUMENT" not in json.dumps(row)
    assert root == before


@pytest.mark.parametrize("extracted", [None, {}, {"confidence": 0.9, "sender": "Root"}])
def test_observe_row_uses_llm_fallback_and_last_nonblank_reasoning(monkeypatch, extracted):
    monkeypatch.setenv("BRAINTRUST_PROJECT", "env-project")
    root = _sample_root()
    root["output"]["extracted_data"] = extracted
    root["scores"] = {}
    root["metadata"].pop("run_id")
    root["metadata"].pop("prompt_key")
    first = _sample_llm("span-eval-1")
    last = {
        **_sample_llm("span-eval-1"),
        "metadata": {"model": "last-model"},
        "output": [{"message": {"reasoning": "last reason"}}],
    }
    blank = {"output": [{"message": {"reasoning": " "}}]}

    row = bt.root_to_observe_row(root, run_id="export-run", llm_spans=[first, last, blank])

    assert row["prediction"]["extracted_data"] == (
        extracted or {"sender": "Chris", "confidence": 0.75}
    )
    assert row["prediction"]["prompt_key"] == "correspondence_specialist_v1"
    assert row["prediction"]["model"] == "last-model"
    assert row["braintrust"]["experiment"] == "export-run"
    assert row["braintrust"]["project"] == "env-project"
    assert row["scores"] == root["output"]["scores"]
    assert row["trace_excerpt"] == {
        "reasoning": "last reason",
        "output_confidence": 0.9 if extracted else 0.75,
    }


@pytest.mark.parametrize(
    ("case_ref", "filename"),
    [
        ("corpus:ground_truth:train:folder/nested/file.txt", "file.txt"),
        ("corpus:ground_truth:train:doc#abc123", "doc#abc123"),
        ("standalone.txt", "standalone.txt"),
        (None, None),
    ],
)
def test_observe_row_metadata_fallbacks_and_missing_optional_fields(case_ref, filename):
    root = {
        "metadata": {
            "case_ref": case_ref,
            "doc_text_sha256": "meta-hash",
            "expected_doc_class": "contract",
        },
        "expected": {"expected_doc_class": "contract"},
    }

    row = bt.root_to_observe_row(root, run_id="minimal")

    assert row["case_id"] == case_ref
    assert row["filename"] == filename
    assert row["doc_text_sha256"] == "meta-hash"
    assert row["prediction"]["doc_type"] == "contract"
    assert row["prediction"]["extracted_data"] is None
    assert row["scores"] == {}
    assert row["trace_excerpt"] == {"reasoning": None, "output_confidence": None}


@pytest.mark.parametrize("run_id", [None, "export-run"])
def test_failures_from_experiment_filters_roots_and_joins_direct_llm_children(monkeypatch, run_id):
    failed = _sample_root(overall=0.2)
    passing = {**_sample_root(overall=0.8), "root_span_id": "passing", "span_id": "passing-span"}
    child = _sample_llm("span-eval-1")
    unrelated = _sample_llm("passing-span")
    unrelated["output"][0]["message"]["reasoning"] = "unrelated reason"
    fetch = Mock(return_value=[failed, passing, child, unrelated])
    monkeypatch.setattr(bt, "fetch_experiment_events", fetch)

    rows = bt.failures_from_experiment("experiment", run_id=run_id, project="project")

    fetch.assert_called_once_with("experiment", project="project")
    assert len(rows) == 1
    assert rows[0]["run_id"] == (run_id or "experiment")
    assert rows[0]["trace_excerpt"]["reasoning"] == child["output"][0]["message"]["reasoning"]


def test_failures_from_experiment_returns_no_rows_when_no_roots_fail(monkeypatch):
    monkeypatch.setattr(bt, "fetch_experiment_events", Mock(return_value=[_sample_root(overall=1)]))
    assert bt.failures_from_experiment("passing-experiment") == []


def test_merge_preserves_case_identity_order_and_unique_tied_provenance():
    first = {
        "case_id": "case-a",
        "filename": "shared.txt",
        "run_id": "a",
        "scores": {"overall_score": 0.3},
    }
    other_case = {"case_id": "case-b", "filename": "shared.txt", "run_id": "b"}
    filename_only = {"filename": "fallback.txt", "run_id": "c"}
    tie = {**first, "run_id": "second-source"}
    worse = {**first, "run_id": "worse", "scores": {"overall_score": 0.7}}

    rows = bt.merge_observe_rows(
        [first, other_case, filename_only, tie, tie, worse, {}, {"case_id": "", "filename": ""}]
    )

    assert rows == [first, other_case, filename_only]
    assert rows[0] is first
    assert first["source_run_ids"] == ["a", "second-source"]


@pytest.mark.parametrize("scores", [None, {}, {"overall_score": "bad"}])
def test_merge_prefers_numeric_failure_over_missing_or_invalid_score(scores):
    unknown = {"case_id": "same", "scores": scores}
    failure = {"case_id": "same", "scores": {"overall_score": 0.5}}
    assert bt.merge_observe_rows([unknown, failure]) == [failure]
    assert bt.merge_observe_rows([failure, unknown]) == [failure]


def test_build_backlog_skips_failed_experiment_and_merges_remaining_failures(monkeypatch):
    good = {"case_id": "case-a", "scores": {"overall_score": 0.7}}
    bad = {"case_id": "case-a", "scores": {"overall_score": 0.2}}
    fetch = Mock(side_effect=[[good], RuntimeError("offline"), [bad]])
    warning = Mock()
    monkeypatch.setattr(bt, "failures_from_experiment", fetch)
    monkeypatch.setattr(bt.logger, "warning", warning)

    rows = bt.build_task_backlog_manifest(
        "contracts",
        [
            {},
            {"run_id": "a", "experiment": "experiment-a"},
            {"run_id": "broken"},
            {"run_id": "b"},
        ],
        project="project",
    )

    assert rows == [bad]
    assert fetch.call_args_list == [
        call("experiment-a", run_id="a", project="project"),
        call("broken", run_id="broken", project="project"),
        call("b", run_id="b", project="project"),
    ]
    warning.assert_called_once_with(
        "gepa_braintrust_fetch_failed", task="contracts", experiment="broken", exc_info=True
    )


def test_enrichment_prefers_hash_then_case_and_preserves_manifest_data(monkeypatch):
    hash_root = _sample_root(overall=1)
    case_root = deepcopy(hash_root)
    case_root.update(root_span_id="case-root", span_id="case-span")
    case_root["input"].update(case_ref="case-match", doc_text_sha256="other-hash")
    child = _sample_llm("span-eval-1")
    fetch = Mock(return_value=[hash_root, case_root, child])
    monkeypatch.setattr(bt, "fetch_experiment_events", fetch)
    rows = [
        {
            "case_id": "case-match",
            "doc_text_sha256": hash_root["input"]["doc_text_sha256"],
            "prediction": {"source": "local"},
            "scores": {"overall_score": 0.1},
            "braintrust": {"old": True},
            "trace_excerpt": {"reasoning": "old"},
        },
        {"case_id": "case-match", "doc_text_sha256": "unknown-hash"},
        {"case_id": "unmatched"},
    ]
    before = deepcopy(rows)

    enriched = bt.enrich_manifest_from_braintrust(rows, experiment_name="exp", project="project")

    fetch.assert_called_once_with("exp", project="project")
    assert enriched[0]["braintrust"]["root_span_id"] == "root-abc"
    assert enriched[0]["trace_excerpt"]["reasoning"] == child["output"][0]["message"]["reasoning"]
    assert enriched[1]["braintrust"]["root_span_id"] == "case-root"
    assert enriched[2] is rows[2]
    assert enriched[0] is not rows[0]
    assert enriched[0]["prediction"] == before[0]["prediction"]
    assert enriched[0]["scores"] == before[0]["scores"]
    assert rows == before


@pytest.mark.parametrize(
    "operation", [bt.failures_from_experiment, bt.enrich_manifest_from_braintrust]
)
def test_experiment_readers_propagate_fetch_errors(monkeypatch, operation):
    monkeypatch.setattr(bt, "fetch_experiment_events", Mock(side_effect=RuntimeError("offline")))
    with pytest.raises(RuntimeError, match="offline"):
        if operation is bt.failures_from_experiment:
            operation("exp")
        else:
            operation([{"case_id": "case"}], experiment_name="exp")


@pytest.mark.parametrize("project", [None, "custom-project"])
def test_backlog_index_creates_parents_and_records_zero_and_unknown_counts(
    monkeypatch, tmp_path, project
):
    monkeypatch.delenv("BRAINTRUST_PROJECT", raising=False)
    if project:
        monkeypatch.setenv("BRAINTRUST_PROJECT", project)
    entries = [{"run_id": "run-a", "experiment": "exp-a"}]
    path = tmp_path / "nested" / "index.json"

    assert (
        bt.write_backlog_index(
            {"contracts": entries, "correspondence": []}, path, manifest_stats={"contracts": 0}
        )
        == path
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload == {
        "schema": "gepa-braintrust-backlog-index",
        "version": 1,
        "project": project or "Mailroom-Evals",
        "tasks": {
            "contracts": {"n_runs": 1, "runs": entries, "n_failures_merged": 0},
            "correspondence": {"n_runs": 0, "runs": [], "n_failures_merged": None},
        },
    }
    assert list(payload["tasks"]) == ["contracts", "correspondence"]
    bt.write_backlog_index({}, path)
    assert json.loads(path.read_text(encoding="utf-8"))["tasks"] == {}
