"""Sandbox-parity report enrichment blocks."""

from __future__ import annotations

from evals import run_report_analytics as rra


def _rows(n: int = 3):
    base = [
        {
            "case_id": "d1",
            "expected_subclass": "email",
            "scores": {"overall_score": 0.5, "extraction_f1": 0.1},
            "latency_ms": 10000,
            "tokens": {"prompt": 1000, "completion": 200},
        },
        {
            "case_id": "d2",
            "expected_subclass": "letter",
            "scores": {"overall_score": 0.7, "extraction_f1": 0.0},
            "latency_ms": 20000,
            "tokens": {"prompt": 2000, "completion": 300},
        },
        {
            "case_id": "d3",
            "expected_subclass": "email",
            "scores": {"overall_score": 0.6, "extraction_f1": 0.0},
            "latency_ms": 15000,
            "tokens": {"prompt": 1500, "completion": 250},
        },
    ]
    return base[:n]


def test_analyst_insights_and_strata():
    summary = {"params": {"concurrency": 2}, "task": "correspondence"}
    text = "\n".join(rra.render_analyst_insights(summary, _rows(), wall=30.0, p50=15.0, p95=20.0))
    assert "Analyst insights" in text
    assert "Concurrency efficiency" in text
    strata = "\n".join(rra.render_strata(_rows()))
    assert "Strata (subclass)" in strata
    assert "email" in strata


def test_scoring_method_contracts_task():
    summary = {"task": "contracts"}
    text = "\n".join(rra.render_scoring_method(summary, _rows()))
    assert "CUAD" in text


def test_reproduce_and_artifacts():
    summary = {
        "run_id": "20260927T033031Z-eval-correspondence",
        "family": "eval",
        "task": "correspondence",
        "mode": "real",
        "params": {"sample": 20, "seed": 42, "decode_profile": "qwen3-8b", "concurrency": 8},
        "dataset": {"subset": "class:correspondence"},
        "comparison_report": "reports/api-comparisons/qwen3-8b/correspondence/runs/x.md",
    }
    repro = "\n".join(rra.render_reproduce(summary))
    assert "run_evals.py" in repro
    assert "qwen3-8b" in repro
    art = "\n".join(rra.render_artifacts(summary))
    assert "cases.jsonl" in art
    assert "comparison_report" in art or "api-comparisons" in art
