#!/usr/bin/env python3
"""Compare logged runs locally — A/B deltas with bootstrap CIs, zero sinks.

    uv run python scripts/compare_runs.py --a <run_id_a> --b <run_id_b>
    uv run python scripts/compare_runs.py --a ... --b ... --md reports/comparisons/
    uv run python scripts/compare_runs.py --a ... --b ... --record

--record appends a comparison_result record to the experiment log, recording
whether the mutation was accepted (CI lo > 0) or rejected, and promoting the
winning prompt version when accepted. Losing runs are preserved in the log
for archival and future training.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evals.analysis import compare_runs


def render_md(comparison: dict) -> str:
    lines = [
        f"# Run comparison — {comparison['run_b']['run_id']} vs {comparison['run_a']['run_id']}", "",
        (f"Generated {datetime.now(UTC).isoformat(timespec='seconds')} · "
        f"shared cases: {comparison['n_shared_cases']}"), "",
        "| metric | A | B | delta |",
        "|---|---|---|---|",
    ]
    for key, delta in comparison["metric_deltas"].items():
        lines.append(f"| {key} | {delta['a']} | {delta['b']} | {delta['delta']} |")
    paired = comparison.get("paired_case_deltas") or {}
    if paired:
        lines += ["", "## Paired per-case deltas (bootstrap 95% CI)", "",
                  "| score key | delta | CI lo | CI hi | n |", "|---|---|---|---|---|"]
        for key, ci in paired.items():
            lines.append(f"| {key} | {ci['delta']} | {ci['ci_lo']} | {ci['ci_hi']} | {ci['n']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", required=True, help="baseline run_id")
    parser.add_argument("--b", required=True, help="candidate run_id")
    parser.add_argument("--md", default=None, metavar="DIR", help="also write a markdown report under DIR")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--record", action="store_true", help="record comparison to experiment log (accepted|rejected)")
    args = parser.parse_args()

    comparison = compare_runs(args.a, args.b)
    if args.json:
        print(json.dumps(comparison, indent=2, default=str))
    else:
        print(render_md(comparison))
    if args.md:
        out_dir = Path(args.md)
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        (out_dir / f"{stamp}-compare.md").write_text(render_md(comparison), encoding="utf-8")
        (out_dir / f"{stamp}-compare.json").write_text(json.dumps(comparison, indent=2, default=str), encoding="utf-8")

    if args.record:
        from evals import experiment_log

        paired = comparison.get("paired_case_deltas") or {}
        primary = next(iter(paired.values()), None)
        accepted = primary is not None and primary["ci_lo"] > 0
        b_version = comparison.get("run_b", {}).get("prompt_version")
        promoted = b_version if accepted else None
        result = experiment_log.record_comparison(
            args.a, args.b,
            comparison=comparison,
            accepted=accepted,
            promoted_version=promoted,
        )
        status = "ACCEPTED" if accepted else "REJECTED"
        print(f"{status}: comparison recorded (promoted={promoted})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
