"""Calibration: intake — edge cases for the intake node.

Probes messy/ambiguous fixtures plus the `bundles` (duplicate families) and
`streams` (thread scenarios) configs; asserts the no-truncation invariant
and triage agreement on edge shapes.
"""

from __future__ import annotations

from typing import Any

from . import base


def analyze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    truncation_failures = 0
    triage_agrees: list[float] = []
    n = 0
    for row in rows:
        scores = row.get("scores") or {}
        if not scores:
            continue
        n += 1
        if scores.get("no_truncation") == 0:
            truncation_failures += 1
        if scores.get("triage_agrees") is not None:
            triage_agrees.append(float(scores["triage_agrees"]))
    agreement = base.bootstrap_ci(triage_agrees)
    caveats = []
    if truncation_failures:
        caveats.append(f"{truncation_failures}/{n} intake runs violated the no-truncation invariant")
    return {
        "n_cases": n,
        "no_truncation_violations": truncation_failures,
        "triage_agreement_ci": agreement,
        "recommended_thresholds": {},
        "caveats": caveats,
    }
