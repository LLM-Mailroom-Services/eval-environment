#!/usr/bin/env python3
"""Render / validate the centralized experiment log.

    python scripts/render_experiment_log.py             # rebuild the markdown
    python scripts/render_experiment_log.py --validate  # schema-check every line
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evals import experiment_log  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="schema-check every record")
    args = parser.parse_args()

    runs = experiment_log.load_runs()
    if args.validate:
        problems = []
        for run in runs:
            issues = experiment_log.validate_record(run)
            if issues:
                problems.append((run.get("run_id"), issues))
        if problems:
            for run_id, issues in problems:
                print(f"INVALID {run_id}: {issues}")
            return 1
        print(f"OK: {len(runs)} run records conform to schema v{experiment_log.SCHEMA_VERSION}")
        return 0

    path = experiment_log.write_markdown()
    print(f"rendered {len(runs)} runs → {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
