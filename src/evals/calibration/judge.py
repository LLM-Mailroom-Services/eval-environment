"""Calibration: judge — completeness-threshold calibration.

Probes the `incomplete` fixtures + `review_expected` rows; sweeps the judge
completeness score for the flagging threshold that best separates documents
needing review, and cross-checks the field-scoring ambiguous band.
"""

from __future__ import annotations

from typing import Any

from . import base


def analyze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    points = []
    for row in rows:
        prediction = row.get("prediction") or {}
        scores = row.get("scores") or {}
        completeness = prediction.get("completeness")
        if completeness is None:
            continue
        points.append({
            "completeness": float(completeness),
            "want_review": bool(row.get("review_expected"))
            or str(prediction.get("judge_label") or "") in ("partial", "incomplete") and bool(row.get("review_expected")),
            "flagged": str(prediction.get("judge_label") or "") in ("partial", "incomplete"),
            "agrees": scores.get("judge_agrees"),
        })
    agreement = base.bootstrap_ci(
        [float(p["agrees"]) for p in points if p["agrees"] is not None]
    )
    curve = base.sweep_threshold(
        [
            {"score": p["completeness"], "want_review": p["want_review"]}
            for p in points
        ],
        score_key="score",
        positive=lambda r: bool(r["want_review"]),
    )
    best = base.best_threshold(curve)
    recommended = {}
    if best:
        recommended["judge_flag_max_completeness"] = {
            "threshold": best["threshold"],
            "metric": "f2",
            "value": best["f2"],
            "config_hint": "judge completeness flag boundary (KANBAN-063 lane B)",
        }
    caveats = []
    if agreement and agreement["hi"] - agreement["lo"] > 0.1:
        caveats.append(f"judge agreement CI spans {agreement['lo']}–{agreement['hi']} — insufficient evidence for a hard threshold")
    return {
        "n_flagged": sum(1 for p in points if p["flagged"]),
        "agreement_ci": agreement,
        "threshold_curve": curve,
        "recommended_thresholds": recommended,
        "caveats": caveats,
    }
