"""Local run-log analysis — aggregate and compare runs without any sink.

All evaluation of run logs happens here from the experiment log's JSONL:
aggregates, confusion matrices, calibration readouts, and A/B comparisons
with bootstrap CIs. Sinks stay tracing + essential scores only.
"""

from __future__ import annotations

import random
from collections import Counter
from typing import Any

from . import experiment_log


def aggregate_run(run_id: str) -> dict[str, Any]:
    """Full local aggregate of one run: metrics, performance, confusion."""
    run = next((r for r in experiment_log.load_runs() if r.get("run_id") == run_id), None)
    if run is None:
        raise KeyError(f"unknown run {run_id!r}")
    rows = experiment_log.load_cases(run_id)
    out: dict[str, Any] = {
        "run_id": run_id,
        "family": run.get("family"),
        "task": run.get("task"),
        "mode": run.get("mode"),
        "model": run.get("model"),
        "prompt_version": run.get("prompt_version"),
        "prompt_lineage": run.get("prompt_lineage"),
        "metrics": run.get("metrics"),
        "performance": run.get("performance"),
        "judging": run.get("judging"),
    }
    pairs = [
        (str(r.get("expected_doc_class") or ""), str((r.get("prediction") or {}).get("doc_type") or ""))
        for r in rows
        if r.get("expected_doc_class") and (r.get("prediction") or {}).get("doc_type")
    ]
    if pairs:
        matrix: dict[str, Counter] = {}
        for expected, predicted in pairs:
            matrix.setdefault(expected, Counter())[predicted] += 1
        out["confusion_matrix"] = {
            expected: dict(counts) for expected, counts in sorted(matrix.items())
        }
    return out


def compare_runs(
    run_id_a: str,
    run_id_b: str,
    *,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    """A/B two runs: metric deltas + bootstrap CIs over per-case score diffs.

    Only metrics present in BOTH runs are compared; per-case bootstrap uses
    the shared numeric score keys (paired by case_id where possible).
    """
    a = aggregate_run(run_id_a)
    b = aggregate_run(run_id_b)
    deltas = {
        key: {"a": a["metrics"].get(key), "b": b["metrics"].get(key),
              "delta": round(b["metrics"][key] - a["metrics"][key], 4)}
        for key in sorted(set(a["metrics"]) & set(b["metrics"]))
        if isinstance(a["metrics"].get(key), (int, float)) and isinstance(b["metrics"].get(key), (int, float))
    }
    rows_a = {r.get("case_id"): r for r in experiment_log.load_cases(run_id_a)}
    rows_b = {r.get("case_id"): r for r in experiment_log.load_cases(run_id_b)}
    shared_ids = sorted(set(rows_a) & set(rows_b))
    paired: dict[str, list[float]] = {}
    for key in ("class_correct", "overall_score", "judge_agrees", "decision_agrees", "stage_agrees"):
        diffs = []
        for case_id in shared_ids:
            va = (rows_a[case_id].get("scores") or {}).get(key)
            vb = (rows_b[case_id].get("scores") or {}).get(key)
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                diffs.append(float(vb) - float(va))
        if diffs:
            paired[key] = _bootstrap_delta_ci(diffs, n_boot=n_boot, seed=seed)
    return {
        "run_a": {"run_id": run_id_a, "prompt_version": a.get("prompt_version"), "model": a.get("model")},
        "run_b": {"run_id": run_id_b, "prompt_version": b.get("prompt_version"), "model": b.get("model")},
        "metric_deltas": deltas,
        "paired_case_deltas": paired,
        "n_shared_cases": len(shared_ids),
    }


def _bootstrap_delta_ci(diffs: list[float], *, n_boot: int, seed: int) -> dict[str, float]:
    rng = random.Random(seed)
    n = len(diffs)
    means = sorted(sum(rng.choices(diffs, k=n)) / n for _ in range(n_boot))
    point = sum(diffs) / n
    return {
        "delta": round(point, 4),
        "ci_lo": round(means[int(0.025 * n_boot)], 4),
        "ci_hi": round(means[min(n_boot - 1, int(0.975 * n_boot))], 4),
        "n": n,
    }
