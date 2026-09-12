"""Essential-scores, judge engine, and post-hoc scoring tests."""

from __future__ import annotations

import json

from evals import experiment_log, scoring
from evals.judges import DIMENSION_PROMPT_KEY, _mock_verdict, judge_run
from evals.runner import _score_case


def test_essential_metrics_curation():
    scores = {
        "class_correct": 1, "subclass_correct": 0,
        "predicted_doc_class": "x",  # non-numeric, never forwarded
    }
    essential = scoring.essential_metrics("classification", scores)
    assert set(essential) == {"class_correct", "subclass_correct"}


def test_essential_rollup():
    rows = [
        {"scores": {"class_correct": 1, "subclass_correct": 1}},
        {"scores": {"class_correct": 0, "subclass_correct": 0}},
    ]
    rollup = scoring.essential_rollup("classification", rows)
    assert rollup == {"class_correct": 0.5, "subclass_correct": 0.5}


def test_sha256_text():
    assert scoring.sha256_text("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def _write_run(tmp_path, monkeypatch, *, n_cases=2):
    monkeypatch.setenv("EXPERIMENT_LOG_PATH", str(tmp_path / "log.jsonl"))
    monkeypatch.setenv("EXPERIMENT_LOG_MD_PATH", str(tmp_path / "log.md"))
    monkeypatch.setenv("EVALS_EXPERIMENTS_DIR", str(tmp_path / "experiments"))
    summary = {
        "schema_version": 2, "record_kind": "run_summary",
        "run_id": experiment_log.new_run_id("eval", "classification"),
        "family": "eval", "task": "classification", "invoke": "node", "mode": "mock",
        "model": "mock-model", "prompt_version": "sorter_v1", "prompt_lineage": "frozen",
        "trace_backend": "none",
        "started_at": experiment_log.utc_now(), "finished_at": experiment_log.utc_now(),
        "dataset": {"repo": "x", "config": "ground_truth", "split": "train",
                    "revision": "rev", "subset": "train", "n_selected": n_cases, "n_total": 10, "seed": 42},
        "params": {"scorer": "classification"},
        "metrics": {"n": n_cases, "errors": 0},
        "performance": {},
        "git": {"commit": "abc", "dirty": False},
    }
    rows = [
        {
            "run_id": summary["run_id"], "case_id": f"c{i}",
            "filename": f"doc{i}.txt",
            "expected_doc_class": "contract", "expected_subclass": None,
            "doc_text_sha256": scoring.sha256_text(f"text {i}"),
            "prediction": {"doc_type": "contract" if i == 0 else "correspondence", "confidence": 0.9},
            "scores": {"class_correct": 1 if i == 0 else 0},
            "latency_ms": 1.0, "error": None,
        }
        for i in range(n_cases)
    ]
    experiment_log.write_run(summary, rows)
    return summary["run_id"]


def test_mock_judge_run(tmp_path, monkeypatch):
    run_id = _write_run(tmp_path, monkeypatch)
    result = judge_run(run_id, ["classification", "verdict"], mock=True)
    assert result["metrics"]["n"] == 2
    assert result["metrics"]["classification_mean"] == 0.5  # one correct of two
    judgments_path = tmp_path / "experiments" / run_id / "judgments.jsonl"
    assert judgments_path.exists()
    lines = [json.loads(l) for l in judgments_path.read_text().splitlines() if l]
    assert len(lines) == 4  # 2 cases x 2 dimensions
    # follow-up record appended with judging block
    runs = experiment_log.load_runs()
    judged = [r for r in runs if r.get("judging")]
    assert len(judged) == 1
    assert judged[0]["judging"]["mock"] is True
    assert judged[0]["judging"]["prompt_versions"]["classification"]["key"] == "judge-classification_v1"


def test_mock_verdict_shapes():
    row = {"scores": {"class_correct": 1}}
    assert _mock_verdict("classification", row) == {"classification_correct": "correct", "classification_quality": 1.0}
    row = {"scores": {"overall_score": 0.7}}
    assert _mock_verdict("verdict", row) == {"verdict": "PARTIAL"}
    row = {"scores": {}}
    assert _mock_verdict("verdict", row) == {"verdict": "MISS"}


def test_judge_dimensions_use_frozen_prompts():
    from evals.prompts.lineage import resolve

    for dim, key in DIMENSION_PROMPT_KEY.items():
        version = resolve(key)
        assert version.lineage == "frozen", f"{dim} must use the frozen rubric"


def test_record_judging_appends_only(tmp_path, monkeypatch):
    run_id = _write_run(tmp_path, monkeypatch)
    before = len(experiment_log.load_runs())
    experiment_log.record_judging(
        run_id, dimensions=["quality"], judge_model="mock", mock=True,
        metrics={"quality_mean": 0.5}, judgments_ref="x",
    )
    runs = experiment_log.load_runs()
    assert len(runs) == before + 1  # append-only: new line, original untouched
    assert runs[-1]["judging"]["dimensions"] == ["quality"]


def test_score_case_recompute_stable(tmp_path, monkeypatch, sample_case):
    prediction = {"doc_type": "contract", "doc_subclass": "nda"}
    case = dict(sample_case, expected_doc_class="contract", expected_subclass="nda")
    first = _score_case("classification", "classification", case, prediction)
    second = _score_case("classification", "classification", case, prediction)
    assert first == second  # recompute is deterministic
