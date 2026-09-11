"""Calibration: arbiter — decision-boundary calibration.

Probes the `arbiter_outcome` fixtures (stands / re_extract /
escalate_human_review); reports the per-decision confusion and agreement CI,
and recommends retry-vs-human-review boundaries when the sample supports it.
"""

from __future__ import annotations

from typing import Any

from . import base

OUTCOME_MAP = {
    "stands": "accept_with_caveats",
    "re_extract": "retry_extraction",
    "escalate_human_review": "human_review",
}


def analyze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    confusion: dict[tuple[str, str], int] = {}
    agreements: list[float] = []
    for row in rows:
        scores = row.get("scores") or {}
        prediction = row.get("prediction") or {}
        expected_outcome = row.get("fixture_outcome") or row.get("arbiter_outcome")
        decision = str(scores.get("decision") or prediction.get("decision") or "")
        if expected_outcome:
            want = OUTCOME_MAP.get(str(expected_outcome).strip().lower(), "")
            confusion[(want, decision)] = confusion.get((want, decision), 0) + 1
        if scores.get("decision_agrees") is not None:
            agreements.append(float(scores["decision_agrees"]))
    cell_table = [
        {"expected": want, "decided": decided, "n": n}
        for (want, decided), n in sorted(confusion.items())
    ]
    agreement = base.bootstrap_ci(agreements)
    per_decision: dict[str, dict[str, Any]] = {}
    for want, decided, n in [(c["expected"], c["decided"], c["n"]) for c in cell_table]:
        stats = per_decision.setdefault(want, {"n": 0, "agreed": 0})
        stats["n"] += n
        if want == decided:
            stats["agreed"] += n
    for stats in per_decision.values():
        stats["agreement"] = round(stats["agreed"] / stats["n"], 4) if stats["n"] else None
    caveats = []
    if agreement and agreement["hi"] - agreement["lo"] > 0.1:
        caveats.append(f"agreement CI spans {agreement['lo']}–{agreement['hi']} — extend arbiter fixtures before pinning boundaries")
    return {
        "decision_confusion": cell_table,
        "per_expected_decision": per_decision,
        "agreement_ci": agreement,
        "recommended_thresholds": {},
        "caveats": caveats,
    }
