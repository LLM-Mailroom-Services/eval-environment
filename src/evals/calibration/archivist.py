"""Calibration: archivist — archival edge cases.

Probes `failure_stage=archival` fixtures; verifies manifest/audit/sha256/
stage conformance inside the isolated base dir.
"""

from __future__ import annotations

from typing import Any


def analyze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    checks: dict[str, dict[str, int]] = {}
    for row in rows:
        scores = row.get("scores") or {}
        if not scores:
            continue
        for key in ("archived_ok", "audit_ok", "sha256_ok", "stage_ok"):
            if key in scores:
                stats = checks.setdefault(key, {"pass": 0, "n": 0})
                stats["n"] += 1
                stats["pass"] += int(bool(scores[key]))
    caveats = []
    for key, stats in sorted(checks.items()):
        if stats["n"] and stats["pass"] < stats["n"]:
            caveats.append(f"{key}: {stats['pass']}/{stats['n']} passed")
    return {
        "checks": {
            key: {"rate": round(stats["pass"] / stats["n"], 4) if stats["n"] else None, "n": stats["n"]}
            for key, stats in sorted(checks.items())
        },
        "recommended_thresholds": {},
        "caveats": caveats,
    }
