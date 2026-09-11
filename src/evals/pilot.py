"""Pilot presets — cheap validation runs before full sweeps.

A pilot run is a task executed over a stratified micro-slice (default: 1
document per class × subclass stratum, plus a fixtures pinch) with the same
scoring/tracing/logging path as the full eval. Pilots validate wiring —
corpus loads, node invocation, scorers, trace sink, experiment log — at
near-zero cost. ``--mock`` pilots are the CI gate.
"""

from __future__ import annotations

from typing import Any

from .cases import load_cases
from .registry import TaskSpec, get_task

PILOT_PER_STRATUM = 1
PILOT_FIXTURE_PINCH = 3


def pilot_cases(task_id: str, *, seed: int = 42) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Stratified micro-slice + fixture pinch for a pilot run."""
    spec: TaskSpec = get_task(task_id)
    cases, prov = load_cases("pilot", sample=None, seed=seed)
    by_class: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        by_class.setdefault(str(case.get("expected_doc_class") or ""), []).append(case)
    picked: list[dict[str, Any]] = []
    seen: set[str] = set()
    for cls in sorted(by_class):
        for case in by_class[cls][:PILOT_PER_STRATUM]:
            if case["id"] not in seen:
                picked.append(case)
                seen.add(case["id"])
    if spec.scorer in ("judge", "arbiter", "boss", "archivist", "calibration_classify"):
        fixtures, _fprov = load_cases("fixtures", n=PILOT_FIXTURE_PINCH, seed=seed)
        for case in fixtures:
            if case["id"] not in seen:
                picked.append(case)
                seen.add(case["id"])
    prov = {
        **prov,
        "pilot": True,
        "per_stratum": PILOT_PER_STRATUM,
        "fixture_pinch": PILOT_FIXTURE_PINCH if spec.scorer in ("judge", "arbiter", "boss", "archivist") else 0,
        "n_selected": len(picked),
    }
    return picked, prov


def pilot_overrides(spec: TaskSpec) -> dict[str, Any]:
    """Runner overrides a pilot run applies on top of the task spec."""
    return {"subset": None}  # subset is replaced by pilot_cases selection
