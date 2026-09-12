#!/usr/bin/env python3
"""Post-hoc local scoring of logged runs — zero sink dependency.

    # Recompute deterministic scores from stored predictions (scorer upgrades)
    uv run python scripts/score_run.py --run-id <run_id> --recompute

    # Local LLM-as-judge over a logged run (frozen judge rubrics)
    uv run python scripts/score_run.py --run-id <run_id> --judge verdict,quality
    uv run python scripts/score_run.py --run-id <run_id> --judge classification --mock

    # Batch over every logged run
    uv run python scripts/score_run.py --all-runs --recompute

    # Export the failed-case manifest (the GEPA OBSERVE input)
    uv run python scripts/score_run.py --run-id <run_id> --export-failures data/manifests/<run_id>.failures.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.env import load_env

load_env()

from evals import (
    experiment_log,
    scoring,
)
from evals.judges import DIMENSIONS, judge_run


def recompute_run(run_id: str) -> dict:
    """Re-score stored predictions with the CURRENT deterministic scorers.

    Writes an updated cases.jsonl section as ``rescored.jsonl`` in the run
    dir (original rows untouched) and prints the metric delta.
    """
    rows = experiment_log.load_cases(run_id)
    if not rows:
        raise KeyError(f"run {run_id!r} has no case rows")
    run = next((r for r in experiment_log.load_runs() if r.get("run_id") == run_id), {})
    scorer = ((run.get("params") or {}).get("scorer")) or "generic"
    task = run.get("task", "")

    rescored = []
    for row in rows:
        prediction = row.get("prediction") or {}
        case_stub = {
            "expected_doc_class": row.get("expected_doc_class"),
            "expected_subclass": row.get("expected_subclass"),
            "review_expected": row.get("review_expected"),
            "retry_expected": row.get("retry_expected"),
            "arbiter_outcome": row.get("fixture_outcome"),
            "fixture_kind": row.get("fixture_kind"),
            "expected_fields": {},  # field-level GT re-load happens via corpus join when needed
        }
        from evals.runner import _score_case

        fresh = _score_case(task, scorer, case_stub, prediction)
        rescored.append({**row, "scores_rescored": fresh, "scores_original": row.get("scores")})

    run_dir = experiment_log.experiments_dir() / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    out = run_dir / "rescored.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for row in rescored:
            fh.write(json.dumps(row, default=str) + "\n")

    old_metrics = scoring.summarize_scores(rows)
    new_rows = [{**row, "scores": row["scores_rescored"]} for row in rescored]
    new_metrics = scoring.summarize_scores(new_rows)
    return {"run_id": run_id, "rescored_path": str(out), "original": old_metrics, "rescored": new_metrics}


def export_failures(run_id: str, out_path: Path) -> Path:
    """The GEPA OBSERVE manifest: failed cases + evidence for the prompt engineer."""
    rows = experiment_log.load_cases(run_id)
    failures = [
        row for row in rows
        if row.get("error") or any(
            isinstance(v, (int, float)) and v == 0
            for k, v in (row.get("scores") or {}).items()
            if k.endswith(("_correct", "_agrees", "_valid", "_ok"))
        ) or (row.get("scores") or {}).get("overall_score", 1) is not None
        and isinstance((row.get("scores") or {}).get("overall_score"), (int, float))
        and row["scores"]["overall_score"] < 0.8
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for row in failures:
            fh.write(json.dumps({
                "run_id": run_id,
                "case_id": row.get("case_id"),
                "filename": row.get("filename"),
                "expected_doc_class": row.get("expected_doc_class"),
                "expected_subclass": row.get("expected_subclass"),
                "prediction": row.get("prediction"),
                "scores": row.get("scores"),
                "error": row.get("error"),
                "doc_text_sha256": row.get("doc_text_sha256"),
            }, default=str) + "\n")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--all-runs", action="store_true")
    parser.add_argument("--recompute", action="store_true", help="re-score stored predictions with current scorers")
    parser.add_argument("--judge", default=None, help=f"comma list of dimensions: {','.join(DIMENSIONS)}")
    parser.add_argument("--mock", action="store_true", help="deterministic mock judges (no network)")
    parser.add_argument("--judge-model", default=None)
    parser.add_argument("--export-failures", default=None, metavar="PATH", help="write the GEPA failure manifest")
    args = parser.parse_args()

    run_ids = (
        [r["run_id"] for r in experiment_log.load_runs()]
        if args.all_runs
        else ([args.run_id] if args.run_id else [])
    )
    if not run_ids:
        parser.error("provide --run-id or --all-runs")

    failures = 0
    for run_id in run_ids:
        if args.recompute:
            result = recompute_run(run_id)
            print(f"{run_id}: recompute → {result['rescored_path']}")
            print(f"  original: {result['original']}")
            print(f"  rescored: {result['rescored']}")
        if args.judge:
            dimensions = [d.strip() for d in args.judge.split(",") if d.strip()]
            result = judge_run(run_id, dimensions, mock=args.mock, judge_model=args.judge_model)
            print(f"{run_id}: judge[{','.join(dimensions)}] ({'mock' if args.mock else args.judge_model or 'taxonomy-judge'})")
            print(f"  metrics: {result['metrics']}")
            print(f"  judgments: {result['judgments_ref']}")
        if args.export_failures:
            path = export_failures(run_id, Path(args.export_failures))
            print(f"{run_id}: failure manifest → {path}")
        if not (args.recompute or args.judge or args.export_failures):
            parser.error("nothing to do: pass --recompute, --judge, and/or --export-failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
