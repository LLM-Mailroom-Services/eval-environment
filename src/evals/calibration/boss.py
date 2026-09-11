"""Calibration: boss — conflict adjudication calibration.

Probes the `conflicting` fixtures; reports decision validity and whether the
Boss routed genuine conflicts to human review (its contract) instead of
approving or failing.
"""

from __future__ import annotations

from typing import Any

from . import base


def analyze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    decisions: dict[str, int] = {}
    routed_to_review = 0
    valid = 0
    n = 0
    for row in rows:
        scores = row.get("scores") or {}
        decision = str(scores.get("decision") or "")
        if not decision:
            continue
        n += 1
        decisions[decision] = decisions.get(decision, 0) + 1
        valid += int(scores.get("decision_valid") or 0)
        if decision == "review":
            routed_to_review += 1
    caveats = []
    if n and routed_to_review / n < 0.5:
        caveats.append("boss approved/failed the majority of conflicting fixtures — review routing contract at risk")
    if n < 5:
        caveats.append(f"only {n} conflicting fixtures — extend the set before drawing conclusions")
    return {
        "decision_distribution": decisions,
        "decision_valid_rate": round(valid / n, 4) if n else None,
        "routed_to_review_rate": round(routed_to_review / n, 4) if n else None,
        "recommended_thresholds": {},
        "caveats": caveats,
    }
