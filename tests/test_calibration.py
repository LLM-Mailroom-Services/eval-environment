"""Calibration machinery tests — binning, ECE, threshold sweep, CIs, reports."""

from __future__ import annotations

from evals.calibration import base


def test_bin_label():
    assert base.bin_label(0.98) == "0.95-1.00"
    assert base.bin_label(0.72) == "0.70-0.80"
    assert base.bin_label(None) == "none"


def test_reliability_and_ece():
    rows = [
        {"confidence": 0.97, "correct": True},
        {"confidence": 0.97, "correct": True},
        {"confidence": 0.60, "correct": False},
        {"confidence": 0.60, "correct": True},
    ]
    table = base.reliability_table(rows)
    assert len(table) == 2
    by_bin = {row["bin"]: row for row in table}
    assert by_bin["0.95-1.00"]["accuracy"] == 1.0
    assert by_bin["0.50-0.70"]["accuracy"] == 0.5
    ece = base.expected_calibration_error(table)
    assert ece is not None and ece >= 0


def test_sweep_threshold_perfect_separation():
    rows = [
        {"score": 0.2, "want": True},
        {"score": 0.2, "want": True},
        {"score": 0.9, "want": False},
        {"score": 0.9, "want": False},
    ]
    curve = base.sweep_threshold(rows, score_key="score", positive=lambda r: r["want"])
    # low threshold flags everything (recall 1, precision 0.5); high threshold
    # flags nothing (recall 0). Best F2 should sit at a low threshold.
    best = base.best_threshold(curve)
    assert best is not None and best["threshold"] <= 0.25


def test_bootstrap_ci_shape():
    ci = base.bootstrap_ci([1.0] * 10 + [0.0] * 10, n_boot=200, seed=1)
    assert ci is not None
    assert ci["lo"] <= ci["mean"] <= ci["hi"]
    assert ci["n"] == 20


def test_write_report(tmp_path):
    payload = {
        "generated_at": "now",
        "n_cases": 3,
        "errors": 0,
        "ece": 0.02,
        "cell_confusion": {"correct_high": {"n": 2, "agreed": 2, "agreement": 1.0}},
        "reliability_table": [{"bin": "0.95-1.00", "n": 2, "accuracy": 1.0}],
        "threshold_curve": [{"threshold": 0.5, "tp": 1, "fp": 0, "fn": 0, "precision": 1.0, "recall": 1.0, "f2": 1.0}],
        "recommended_thresholds": {"review_gate_min_confidence": {"threshold": 0.5, "metric": "f2", "value": 1.0, "config_hint": "hint"}},
        "caveats": ["small sample"],
    }
    json_path, md_path = base.write_report("classify", payload, report_dir=tmp_path)
    assert json_path.exists() and md_path.exists()
    text = md_path.read_text()
    assert "Calibration report — classify" in text
    assert "REPORT-ONLY" in text
    assert "small sample" in text
