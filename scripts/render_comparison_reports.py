#!/usr/bin/env python3
"""Regenerate Modal-comparable API-leg reports from the experiment log.

Reads each report-worthy run (``--decode-profile`` or real eval n≥20), reloads
case rows from ``data/experiments/<run_id>/``, recomputes performance cost
fields (expected / actual / estimated), and rewrites
``reports/api-comparisons/<model>/<task>/RUN-*.md``.

    uv run python scripts/render_comparison_reports.py
    uv run python scripts/render_comparison_reports.py --run-id 20260927T033031Z-eval-correspondence
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from evals import comparison_report, experiment_log, scoring
from evals.decode_budget import expected_cost_for_wave


def _wave_n(summary: dict) -> int:
    params = summary.get("params") or {}
    return int(
        params.get("sample")
        or params.get("n")
        or (summary.get("metrics") or {}).get("n")
        or 0
    )


def _enriched_summary(summary: dict, case_rows: list[dict]) -> dict:
    out = dict(summary)
    params = out.get("params") or {}
    wave = _wave_n(out)
    model = out.get("model")
    if not model and case_rows:
        by_agent = scoring.summarize_agent_usage(
            [r.get("agent_usage") for r in case_rows if r.get("agent_usage")]
        )
        dominant = max(
            by_agent.items(),
            key=lambda kv: kv[1].get("total_tokens") or 0,
            default=(None, {}),
        )[0]
        model = ((by_agent.get(dominant) or {}).get("models") or [None])[0]
        out["model"] = model
    out["performance"] = scoring.summarize_performance(
        case_rows,
        run_model=model,
        expected_cost_usd=expected_cost_for_wave(params.get("decode_profile"), wave),
    )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", action="append", help="regenerate only these run ids")
    args = parser.parse_args()

    runs = experiment_log.load_runs()
    if args.run_id:
        want = set(args.run_id)
        runs = [r for r in runs if r.get("run_id") in want]

    written: list[Path] = []
    for run in runs:
        if run.get("record_kind") not in ("run_summary", None):
            continue
        params = run.get("params") or {}
        if not params.get("decode_profile") and not comparison_report.is_wave_run(run):
            continue
        run_id = run.get("run_id")
        if not run_id:
            continue
        case_rows = experiment_log.load_cases(run_id)
        if not case_rows:
            print(f"skip {run_id}: no case rows on disk", file=sys.stderr)
            continue
        summary = _enriched_summary(run, case_rows)
        path = comparison_report.write_report(summary, case_rows)
        if path:
            written.append(path)
            print(path)

    print(f"rendered {len(written)} comparison report(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
