#!/usr/bin/env python3
"""Regenerate Modal-comparable API-leg write-ups under ``reports/api-comparisons``.

For every report-worthy run (``--decode-profile`` or real eval n≥20 with case
rows on disk):

- ``<model>/<task>/runs/<run_id>.md`` — immutable per-run write-up
- ``<model>/<task>/RUN-<wave>-<CLASS>-<MODEL>-REPORT.md`` — latest canonical
  stem for that model/task/wave/class (overwrites in place)
- ``INDEX.md`` — catalog linking every run to its write-up

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


def _report_worthy(run: dict) -> bool:
    if run.get("record_kind") not in ("run_summary", None):
        return False
    params = run.get("params") or {}
    return bool(params.get("decode_profile")) or comparison_report.is_wave_run(run)


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


def _rel_to_reports(path: Path, reports_root: Path) -> str:
    try:
        return path.relative_to(reports_root).as_posix()
    except ValueError:
        return comparison_report.repo_relative_path(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", action="append", help="regenerate only these run ids")
    args = parser.parse_args()

    reports_root = comparison_report.reports_dir()
    runs = experiment_log.load_runs()
    if args.run_id:
        want = set(args.run_id)
        runs = [r for r in runs if r.get("run_id") in want]

    prepared: list[tuple[dict, list[dict]]] = []
    for run in runs:
        if not _report_worthy(run):
            continue
        run_id = run.get("run_id")
        if not run_id:
            continue
        case_rows = experiment_log.load_cases(run_id)
        if not case_rows:
            print(f"skip {run_id}: no case rows on disk", file=sys.stderr)
            continue
        prepared.append((_enriched_summary(run, case_rows), case_rows))

    # Per-run write-ups (every report-worthy experiment).
    index_entries: list[dict] = []
    canonical_latest: dict[Path, tuple[dict, list[dict]]] = {}
    for summary, case_rows in prepared:
        run_path = comparison_report.write_report(
            summary, case_rows, reports_root, write_canonical=False
        )
        if not run_path:
            continue
        wave_key = comparison_report.report_path(summary, reports_root)
        prev = canonical_latest.get(wave_key)
        if not prev or (summary.get("run_id") or "") > (prev[0].get("run_id") or ""):
            canonical_latest[wave_key] = (summary, case_rows)
        index_entries.append(
            {
                "run_id": summary.get("run_id"),
                "task": summary.get("task"),
                "model": summary.get("model"),
                "n": _wave_n(summary),
                "run_report": _rel_to_reports(run_path, reports_root),
                "canonical_report": _rel_to_reports(wave_key, reports_root),
            }
        )
        print(comparison_report.repo_relative_path(run_path))

    # Latest canonical stem per model/task/wave/class.
    for summary, case_rows in canonical_latest.values():
        wave_path = comparison_report.write_report(
            summary, case_rows, reports_root, write_canonical=True
        )
        # write_report also wrote run file again — idempotent same body.
        if wave_path:
            print(comparison_report.repo_relative_path(comparison_report.report_path(summary, reports_root)))

    index_path = reports_root / "INDEX.md"
    index_path.write_text(
        comparison_report.render_index(index_entries, reports_root),
        encoding="utf-8",
    )
    print(comparison_report.repo_relative_path(index_path))

    canonical_summaries = [s for s, _ in canonical_latest.values()]
    master_path = reports_root / "API-LEG-MASTER-REPORT.md"
    master_path.write_text(
        comparison_report.render_master_report(
            canonical_summaries, index_entries, reports_root
        ),
        encoding="utf-8",
    )
    print(comparison_report.repo_relative_path(master_path))

    for model_key in ("qwen3-8b", "granite-4.2-8b", "deepseek-v4.1-flash"):
        readme = reports_root / model_key / "README.md"
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(
            comparison_report.render_model_suite_readme(
                model_key, canonical_summaries, reports_root
            ),
            encoding="utf-8",
        )
        print(comparison_report.repo_relative_path(readme))

    print(f"rendered {len(index_entries)} run write-up(s); {len(canonical_latest)} canonical stem(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
