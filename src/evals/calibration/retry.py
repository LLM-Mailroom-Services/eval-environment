"""Calibration: retry — retry-pipeline calibration.

Probes `retry_expected` rows + `failure_stage` coverage; sweeps the
extraction-confidence threshold that best predicts which documents the
pipeline SHOULD retry, and reports per-stage failure coverage.
"""

from __future__ import annotations

from typing import Any

from . import base


def analyze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    points = []
    stage_coverage: dict[str, dict[str, int]] = {}
    for row in rows:
        retry_expected = row.get("retry_expected")
        stage = str(row.get("failure_stage") or "")
        if stage:
            stats = stage_coverage.setdefault(stage, {"n": 0})
            stats["n"] += 1
        if retry_expected is None:
            continue
        prediction = row.get("prediction") or {}
        scores = row.get("scores") or {}
        confidence = prediction.get("extraction_confidence") or prediction.get("confidence")
        points.append({
            "confidence": float(confidence) if isinstance(confidence, (int, float)) else None,
            "should_retry": bool(retry_expected),
            "error": bool(row.get("error") or scores.get("scorer_error")),
        })
    curve = base.sweep_threshold(
        [
            {"score": p["confidence"], "should_retry": p["should_retry"]}
            for p in points
            if p["confidence"] is not None
        ],
        score_key="score",
        positive=lambda r: r["should_retry"],
    )
    best = base.best_threshold(curve)
    recommended = {}
    if best:
        recommended["retry_trigger_max_confidence"] = {
            "threshold": best["threshold"],
            "metric": "f2",
            "value": best["f2"],
            "config_hint": "extraction retry gate (confidence low threshold)",
        }
    caveats = []
    missing = {"ingestion", "classification", "extraction", "grouping", "adjudication", "archival"} - set(stage_coverage)
    if missing:
        caveats.append(f"failure stages without fixture coverage: {sorted(missing)}")
    return {
        "failure_stage_coverage": stage_coverage,
        "threshold_curve": curve,
        "recommended_thresholds": recommended,
        "caveats": caveats,
    }
