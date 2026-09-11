"""Calibration: classify — confidence calibration for the sorter.

Probes the 2×2 fixtures grid (correct/wrong × high/low confidence) plus the
low/high-confidence fixture kinds, builds the reliability table + ECE from
emitted vs actual correctness, and recommends the review-gate confidence
threshold against ``review_expected``.
"""

from __future__ import annotations

from typing import Any

from . import base


def analyze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    points = []
    for row in rows:
        prediction = row.get("prediction") or {}
        scores = row.get("scores") or {}
        if scores.get("class_correct") is None:
            continue
        points.append({
            "confidence": prediction.get("confidence"),
            "correct": bool(scores.get("class_correct")),
        })
    table = base.reliability_table(points)
    ece = base.expected_calibration_error(table)

    cells: dict[str, dict[str, Any]] = {}
    for row in rows:
        cell = str((row.get("prediction") or {}).get("calibration_cell") or row.get("fixture_cell") or "")
        if not cell:
            continue
        scores = row.get("scores") or {}
        agreed = int(bool(scores.get("class_correct"))) if cell.startswith("correct") else int(not scores.get("class_correct"))
        stats = cells.setdefault(cell, {"n": 0, "agreed": 0})
        stats["n"] += 1
        stats["agreed"] += agreed
    for stats in cells.values():
        stats["agreement"] = round(stats["agreed"] / stats["n"], 4) if stats["n"] else None

    # Review-gate sweep: flag low-confidence docs for review; positive =
    # fixture expects review (wrong answers should be caught).
    curve = base.sweep_threshold(
        [
            {
                "score": (row.get("prediction") or {}).get("confidence"),
                "want_review": not (row.get("scores") or {}).get("class_correct"),
            }
            for row in rows
        ],
        score_key="score",
        positive=lambda r: bool(r["want_review"]),
    )
    best = base.best_threshold(curve)
    recommended = {}
    if best:
        recommended["review_gate_min_confidence"] = {
            "threshold": best["threshold"],
            "metric": "f2",
            "value": best["f2"],
            "config_hint": "graph.routing confidence thresholds (review gate)",
        }
    caveats = []
    if len(points) < 20:
        caveats.append(f"small fixture sample (n={len(points)}) — CIs are wide; extend fixtures before trusting thresholds")
    return {
        "reliability_table": table,
        "ece": ece,
        "cell_confusion": cells,
        "threshold_curve": curve,
        "recommended_thresholds": recommended,
        "caveats": caveats,
    }
