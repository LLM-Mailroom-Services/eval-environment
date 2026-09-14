"""Experiment log tests — write → load → render round-trip + schema checks."""

from __future__ import annotations

from evals import experiment_log


def _summary() -> dict:
    return {
        "schema_version": experiment_log.SCHEMA_VERSION,
        "record_kind": "run_summary",
        "run_id": experiment_log.new_run_id("eval", "classification"),
        "family": "eval",
        "task": "classification",
        "invoke": "node",
        "mode": "mock",
        "model": "mock-model",
        "prompt_version": None,
        "trace_backend": "none",
        "started_at": experiment_log.utc_now(),
        "finished_at": experiment_log.utc_now(),
        "dataset": {"repo": "Lucius-Morningstar/mailroom-dataset", "config": "ground_truth",
                    "split": "train", "revision": "deadbeef", "subset": "train",
                    "n_selected": 2, "n_total": 2979, "seed": 42},
        "params": {"concurrency": 1},
        "metrics": {"n": 2, "errors": 0, "class_accuracy": 0.5},
        "performance": {"latency_ms_mean": 10.0, "tokens_prompt_total": 20},
    }


def _case_rows(run_id: str) -> list[dict]:
    return [
        {"run_id": run_id, "case_id": f"c{i}", "scores": {"class_correct": i % 2},
         "latency_ms": 10.0, "error": None}
        for i in range(2)
    ]


def test_write_load_roundtrip():
    summary = _summary()
    written = experiment_log.write_run(summary, _case_rows(summary["run_id"]))
    assert written["cases_embedded"]  # small run inlines cases
    runs = experiment_log.load_runs()
    assert len(runs) == 1
    assert runs[0]["run_id"] == summary["run_id"]
    cases = experiment_log.load_cases(summary["run_id"])
    assert len(cases) == 2 and cases[0]["case_id"] == "c0"


def test_large_run_uses_cases_ref():
    summary = _summary()
    rows = _case_rows(summary["run_id"]) * 30  # 60 rows > EMBED_LIMIT
    written = experiment_log.write_run(summary, rows)
    assert not written["cases_embedded"]
    assert written["cases_ref"]
    loaded = experiment_log.load_cases(summary["run_id"])
    assert len(loaded) == 60


def test_validate_record():
    summary = _summary()
    assert experiment_log.validate_record(summary) == []
    bad = dict(summary)
    bad.pop("dataset")
    issues = experiment_log.validate_record(bad)
    assert any("dataset" in issue for issue in issues)


def test_render_markdown_tables_only():
    summary = _summary()
    experiment_log.write_run(summary, _case_rows(summary["run_id"]))
    path = experiment_log.write_markdown()
    text = path.read_text()
    assert "| run_id |" in text or "run_id" in text
    assert "## " in text  # per-run sections
    # never a raw JSON dump of the whole record
    assert '"record_kind": "run_summary"' not in text


def test_torn_tail_tolerated(tmp_path):
    log = tmp_path / "log.jsonl"
    log.write_text('{"a": 1}\n{"tor', encoding="utf-8")
    runs = experiment_log.load_runs(log)
    assert len(runs) == 1
