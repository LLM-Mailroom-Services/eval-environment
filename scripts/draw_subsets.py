#!/usr/bin/env python
"""Pre-draw the canonical SAND-027 comparison subsets (issue #20).

Draws each specialist class at wave sizes 20 and 50 (seed 42 — the same
deterministic stratified_sample the runner uses) and writes canonical
subset manifests under ``data/manifests/subset-draws/``:

    data/manifests/subset-draws/<class>-n<size>-seed42/subset_manifest.json
    data/manifests/subset-draws/<class>-n<size>-seed42/subset_manifest.jsonl

Every leg (OpenRouter API, Modal/vLLM) that runs the same
``--subset class:<x> --sample <20|50> --seed 42`` reproduces the identical
draw (verified nesting: 20 ⊂ 50). Before comparing two legs, diff each run's
``subset_manifest.json`` (filenames + doc_text_sha256) against the canonical
copy here — any divergence blocks the A/B.

Usage:
    uv run python scripts/draw_subsets.py            # draw all 5 × {20,50}
    uv run python scripts/draw_subsets.py --check    # verify existing draws only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from evals.cases import load_cases  # noqa: E402
from evals.tasks.base import write_subset_manifest  # noqa: E402

CLASSES = (
    "correspondence",
    "insurance_claim",
    "contract",
    "merger_agreement",
    "corporate_record",
)
SIZES = (20, 50)
SEED = 42
DRAWS_DIR = REPO / "data" / "manifests" / "subset-draws"


def draw_digest(manifest: dict) -> str:
    """Stable digest over the ordered (filename, doc_text_sha256) draw."""
    rows = list(zip(manifest["filenames"], manifest["doc_text_sha256"]))
    return hashlib.sha256(json.dumps(rows, sort_keys=False).encode()).hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify existing draws, no rewrite")
    args = parser.parse_args()

    status = 0
    for cls in CLASSES:
        for size in SIZES:
            run_dir = DRAWS_DIR / f"{cls}-n{size}-seed{SEED}"
            path = run_dir / "subset_manifest.json"
            cases, prov = load_cases(f"class:{cls}", sample=size, seed=SEED)
            if args.check:
                if not path.exists():
                    print(f"MISSING {run_dir}")
                    status = 1
                    continue
                existing = json.loads(path.read_text(encoding="utf-8"))
                fresh = write_subset_manifest(
                    cases, run_dir=Path("/tmp/opencode/draw-check"),
                    provenance={"check": True},
                )
                same = (
                    existing["filenames"] == fresh["filenames"]
                    and existing["doc_text_sha256"] == fresh["doc_text_sha256"]
                )
                print(f"{'OK  ' if same else 'DRIFT'} {cls} n={size} digest={draw_digest(existing)}")
                status |= 0 if same else 1
            else:
                manifest = write_subset_manifest(
                    cases,
                    run_dir=run_dir,
                    provenance={
                        "purpose": "SAND-027 canonical comparison draw (issue #20)",
                        **prov,
                        "subset": f"class:{cls}",
                        "seed": SEED,
                        "sample": size,
                    },
                )
                print(
                    f"DRAWN {cls} n={size} cases={len(manifest['case_ids'])} "
                    f"digest={draw_digest(manifest)} -> {run_dir}"
                )
    return status


if __name__ == "__main__":
    raise SystemExit(main())
