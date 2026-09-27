#!/usr/bin/env python
"""Sync the full pinned mailroom-dataset corpus into a Braintrust Dataset.

Pushes every row of both splits (train + test, ``ground_truth`` x
``default`` joined on ``filename``) at the pinned revision — 3,302 rows —
so the complete sample set is browsable/queryable in Braintrust and
available to any run that wants full-corpus coverage, not just a per-run
N-sample subset. Idempotent (stable case ids; safe to re-run after a
corpus re-pin).

Usage:
    uv run python scripts/sync_braintrust_dataset.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO))

from pipeline.env import load_env  # noqa: E402

load_env()

from evals.braintrust_experiment import sync_full_corpus_dataset  # noqa: E402


def main() -> int:
    import os

    if not os.environ.get("BRAINTRUST_API_KEY"):
        print("BRAINTRUST_API_KEY not set — nothing to sync.", file=sys.stderr)
        return 1
    result = sync_full_corpus_dataset()
    print(
        f"synced {result['rows_total']} rows -> project={result['project']!r} "
        f"dataset={result['dataset']!r} (train={result['rows_train']} "
        f"test={result['rows_test']} revision={result['revision']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
