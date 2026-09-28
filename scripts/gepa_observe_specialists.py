#!/usr/bin/env python3
"""OBSERVE — merge GEPA failure manifests across backlog runs for one specialist.

Exports failures from each run_id (same seed/sample draw), dedupes on case_id
(first run wins), and writes a merged manifest for ``prompt_engineer.py``.

Example (SAND-027 N=20 correspondence, DeepSeek + Granite + Qwen3-8b):

    uv run python scripts/gepa_observe_specialists.py \\
        --task correspondence \\
        --run-id 20260927T105317Z-eval-correspondence \\
        --run-id 20260927T052637Z-eval-correspondence \\
        --run-id 20260927T033031Z-eval-correspondence \\
        --out data/manifests/gepa/correspondence_merged.failures.jsonl
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Canonical SAND-027 N=20 specialist observe sets (seed-42 class draws).
DEFAULT_RUNS: dict[str, list[str]] = {
    "correspondence": [
        "20260927T105317Z-eval-correspondence",
        "20260927T052637Z-eval-correspondence",
        "20260927T033031Z-eval-correspondence",
    ],
    "insurance_claims": [
        "20260927T105400Z-eval-insurance_claims",
        "20260927T054211Z-eval-insurance_claims",
        "20260927T035135Z-eval-insurance_claims",
    ],
    "contracts": [
        "20260927T105549Z-eval-contracts",
        "20260927T054738Z-eval-contracts",
        "20260927T035621Z-eval-contracts",
    ],
    "merger_agreement": [
        "20260927T110153Z-eval-merger_agreement",
        "20260927T082404Z-eval-merger_agreement",
        "20260927T022750Z-eval-merger_agreement",
    ],
    "corporate_records": [
        "20260927T110828Z-eval-corporate_records",
        "20260927T065622Z-eval-corporate_records",
        "20260927T042239Z-eval-corporate_records",
    ],
}

PARENT_KEY: dict[str, str] = {
    "correspondence": "correspondence_specialist_v1",
    "insurance_claims": "insurance_claims_specialist_v1",
    "contracts": "contracts_specialist_v1",
    "merger_agreement": "merger_agreement_specialist_v1",
    "corporate_records": "corporate_records_specialist_v1",
}

EVAL_TASK: dict[str, str] = {
    "correspondence": "eval:correspondence",
    "insurance_claims": "eval:insurance_claims",
    "contracts": "eval:contracts",
    "merger_agreement": "eval:merger_agreement",
    "corporate_records": "eval:corporate_records",
}

SUBSET_CLASS: dict[str, str] = {
    "correspondence": "correspondence",
    "insurance_claims": "insurance_claim",
    "contracts": "contract",
    "merger_agreement": "merger_agreement",
    "corporate_records": "corporate_record",
}


def _export_one(run_id: str, path: Path) -> None:
    subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/score_run.py",
            "--run-id",
            run_id,
            "--export-failures",
            str(path),
        ],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    )


def merge_failures(run_ids: list[str], out_path: Path) -> tuple[int, int]:
    """Return (unique_failure_cases, source_failure_rows)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = out_path.parent / ".tmp_observe"
    tmp_dir.mkdir(exist_ok=True)  # noqa: PTH103
    by_case: dict[str, dict] = {}
    total_rows = 0
    for run_id in run_ids:
        tmp = tmp_dir / f"{run_id}.failures.jsonl"
        _export_one(run_id, tmp)
        for line in tmp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            total_rows += 1
            row = json.loads(line)
            cid = str(row.get("case_id") or row.get("filename") or "")
            if cid and cid not in by_case:
                by_case[cid] = row
    with out_path.open("w", encoding="utf-8") as fh:
        for row in by_case.values():
            fh.write(json.dumps(row, default=str) + "\n")
    return len(by_case), total_rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task", choices=sorted(DEFAULT_RUNS), help="specialist task key (uses default run-id set)")
    parser.add_argument("--run-id", action="append", dest="run_ids", default=[], help="run_id to include (repeatable)")
    parser.add_argument(
        "--out",
        default=None,
        help="merged manifest path (default: data/manifests/gepa/<task>_merged.failures.jsonl)",
    )
    parser.add_argument("--all-defaults", action="store_true", help="export all five specialist merged manifests")
    args = parser.parse_args()

    if args.all_defaults:
        for task, run_ids in DEFAULT_RUNS.items():
            out = REPO / "data/manifests/gepa" / f"{task}_merged.failures.jsonl"
            n_unique, n_rows = merge_failures(run_ids, out)
            print(f"{task}: {n_unique} unique failures ({n_rows} rows across {len(run_ids)} runs) → {out}")
        return 0

    if not args.task and not args.run_ids:
        parser.error("pass --task, --run-id ..., or --all-defaults")
    run_ids = args.run_ids or DEFAULT_RUNS[args.task]
    task = args.task or "custom"
    out = Path(args.out) if args.out else REPO / "data/manifests/gepa" / f"{task}_merged.failures.jsonl"
    n_unique, n_rows = merge_failures(run_ids, out)
    print(f"{task}: {n_unique} unique failures ({n_rows} rows across {len(run_ids)} runs) → {out}")
    if args.task:
        parent = PARENT_KEY[args.task]
        eval_task = EVAL_TASK[args.task]
        subset = SUBSET_CLASS[args.task]
        print(
            f"\nDRAFT:\n  uv run python scripts/prompt_engineer.py "
            f"--manifest {out} --parent {parent} --apply\n"
            f"A/B (same seed-42 N=20 draw):\n  uv run python scripts/run_evals.py --task {eval_task} --real "
            f"--subset class:{subset} --sample 20 --seed 42 --prompt-version <role>_v2 --model <model>"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
