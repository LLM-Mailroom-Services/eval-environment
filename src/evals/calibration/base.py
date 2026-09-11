"""Shared calibration machinery: binning, reliability, ECE, threshold sweeps.

Every calibration task: load fixtures → invoke the node → score the DECISION
(not field extraction) → bin by emitted confidence → reliability table +
ECE → sweep the decision threshold for the recommended operating point →
bootstrap CIs → write JSON+MD under ``reports/calibration/<task>/``.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import structlog

logger = structlog.get_logger(__name__)

# Confidence bin edges for the reliability table.
BIN_EDGES: tuple[float, ...] = (0.0, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0)


def bin_label(confidence: float | None) -> str:
    if confidence is None:
        return "none"
    for lo, hi in zip(BIN_EDGES, BIN_EDGES[1:]):
        if lo <= confidence < hi or (hi == 1.0 and confidence <= 1.0 and confidence >= lo):
            return f"{lo:.2f}-{hi:.2f}"
    return "none"


def reliability_table(
    rows: list[dict[str, Any]],
    *,
    confidence_key: str = "confidence",
    correct_key: str = "correct",
) -> list[dict[str, Any]]:
    """Per-bin n / accuracy — the calibration (reliability) table."""
    bins: dict[str, list[int]] = {}
    for row in rows:
        label = bin_label(row.get(confidence_key))
        correct = row.get(correct_key)
        if correct is None:
            continue
        n, hits = bins.get(label, (0, 0))
        bins[label] = (n + 1, hits + int(bool(correct)))
    out = []
    for label in [f"{lo:.2f}-{hi:.2f}" for lo, hi in zip(BIN_EDGES, BIN_EDGES[1:])]:
        if label in bins:
            n, hits = bins[label]
            out.append({"bin": label, "n": n, "accuracy": round(hits / n, 4)})
    return out


def expected_calibration_error(table: list[dict[str, Any]]) -> float | None:
    """ECE over the reliability table (|accuracy − bin center| weighted by n)."""
    scored = [
        (row["n"], abs(row["accuracy"] - (float(row["bin"].split("-")[0]) + float(row["bin"].split("-")[1])) / 2))
        for row in table
    ]
    total = sum(n for n, _ in scored)
    if not total:
        return None
    return round(sum(n * gap for n, gap in scored) / total, 4)


def sweep_threshold(
    rows: list[dict[str, Any]],
    *,
    score_key: str,
    positive: Callable[[dict[str, Any]], bool],
    thresholds: list[float] | None = None,
) -> list[dict[str, Any]]:
    """Precision/recall/F2 of `positive(row)` gated by `row[score_key] >= t`."""
    if thresholds is None:
        thresholds = [round(0.05 * i, 2) for i in range(1, 20)]
    out = []
    for t in thresholds:
        tp = fp = fn = 0
        for row in rows:
            value = row.get(score_key)
            if value is None:
                continue
            flagged = float(value) >= t
            want = positive(row)
            if flagged and want:
                tp += 1
            elif flagged and not want:
                fp += 1
            elif want and not flagged:
                fn += 1
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        if precision is None or recall is None or precision + recall == 0:
            f2 = None
        else:
            f2 = 5 * precision * recall / (4 * precision + recall)
        out.append({
            "threshold": t,
            "tp": tp, "fp": fp, "fn": fn,
            "precision": round(precision, 4) if precision is not None else None,
            "recall": round(recall, 4) if recall is not None else None,
            "f2": round(f2, 4) if f2 is not None else None,
        })
    return out


def best_threshold(curve: list[dict[str, Any]], *, metric: str = "f2") -> dict[str, Any] | None:
    scored = [row for row in curve if row.get(metric) is not None]
    if not scored:
        return None
    return max(scored, key=lambda row: row[metric])


def bootstrap_ci(
    values: list[float],
    *,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, float] | None:
    """Percentile bootstrap CI over a mean (mailroom's bootstrap semantics)."""
    if not values:
        return None
    rng = random.Random(seed)
    n = len(values)
    means = sorted(
        sum(rng.choices(values, k=n)) / n for _ in range(n_boot)
    )
    return {
        "mean": round(sum(values) / n, 4),
        "lo": round(means[int(0.025 * n_boot)], 4),
        "hi": round(means[int(0.975 * n_boot)], 4),
        "n": n,
    }


def write_report(
    task: str,
    payload: dict[str, Any],
    *,
    report_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Write the calibration JSON+MD report; returns (json_path, md_path)."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = (report_dir or Path("reports") / "calibration" / task) / stamp
    base.mkdir(parents=True, exist_ok=True)
    json_path = base / "report.json"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path = base / "report.md"
    md_path.write_text(render_md(task, payload), encoding="utf-8")
    return json_path, md_path


def _table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    def fmt(value: Any) -> str:
        if value is None:
            return "—"
        if isinstance(value, bool):
            return "✓" if value else "✗"
        if isinstance(value, float):
            return f"{value:.4f}".rstrip("0").rstrip(".") or "0.0"
        return str(value)

    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(cell) for cell in row) + " |")
    return lines


def render_md(task: str, payload: dict[str, Any]) -> str:
    lines = [f"# Calibration report — {task}", ""]
    lines += _table(
        ["Key", "Value"],
        [
            ["generated_at", payload.get("generated_at")],
            ["n_cases", payload.get("n_cases")],
            ["errors", payload.get("errors")],
            ["ece", payload.get("ece")],
        ],
    )
    cells = payload.get("cell_confusion") or {}
    if cells:
        lines += ["", "## Calibration-cell confusion", ""]
        lines += _table(
            ["cell", "n", "agreed", "agreement"],
            [[cell, v.get("n"), v.get("agreed"), v.get("agreement")] for cell, v in sorted(cells.items())],
        )
    table = payload.get("reliability_table") or []
    if table:
        lines += ["", "## Reliability (confidence bin → accuracy)", ""]
        lines += _table(
            ["bin", "n", "accuracy"],
            [[row["bin"], row["n"], row["accuracy"]] for row in table],
        )
    curve = payload.get("threshold_curve") or []
    if curve:
        lines += ["", "## Threshold sweep", ""]
        lines += _table(
            ["threshold", "tp", "fp", "fn", "precision", "recall", "f2"],
            [[r["threshold"], r["tp"], r["fp"], r["fn"], r["precision"], r["recall"], r["f2"]] for r in curve],
        )
    best = payload.get("recommended_thresholds") or {}
    if best:
        lines += ["", "## Recommended thresholds (REPORT-ONLY)", ""]
        lines += _table(
            ["decision", "threshold", "metric", "value", "config hint"],
            [[k, v.get("threshold"), v.get("metric"), v.get("value"), v.get("config_hint")] for k, v in best.items()],
        )
    caveats = payload.get("caveats") or []
    if caveats:
        lines += ["", "## Caveats", ""]
        lines += [f"- {c}" for c in caveats]
    return "\n".join(lines) + "\n"
