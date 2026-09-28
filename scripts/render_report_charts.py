#!/usr/bin/env python3
"""Render the per-document-type report charts from the viewer snapshot.

Writes SVGs plus an index.json manifest to web/data/charts/ (served by the
viewer's Charts tab) and a markdown gallery to reports/charts/README.md.
Run it after export_site_snapshot.py, and commit the outputs with the snapshot.

    uv run python scripts/render_report_charts.py            # write
    uv run python scripts/render_report_charts.py --check    # exit 1 if stale
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from evals.viz.report_charts import outputs

SNAPSHOT = REPO_ROOT / "web" / "data" / "snapshot.json"
CHARTS_DIR = REPO_ROOT / "web" / "data" / "charts"
GALLERY = REPO_ROOT / "reports" / "charts" / "README.md"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if the committed charts differ from a fresh render")
    args = ap.parse_args(argv)
    files = outputs(json.loads(SNAPSHOT.read_text()), CHARTS_DIR, GALLERY)
    owned = {p for p in CHARTS_DIR.glob("*")} if CHARTS_DIR.exists() else set()
    if args.check:
        stale = sorted(str(p.relative_to(REPO_ROOT)) for p, body in files.items()
                       if not p.exists() or p.read_text() != body)
        stale += sorted(str(p.relative_to(REPO_ROOT)) + " (orphan)" for p in owned - set(files))
        if stale:
            print("STALE: " + ", ".join(stale) + " — re-run without --check", file=sys.stderr)
            return 1
        print(f"ok: {len(files) - 2} charts match the snapshot")
        return 0
    for p in owned - set(files):
        p.unlink()
    for p, body in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    print(f"wrote {len(files) - 2} charts to {CHARTS_DIR.relative_to(REPO_ROOT)} and {GALLERY.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
