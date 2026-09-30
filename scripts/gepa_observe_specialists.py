#!/usr/bin/env python3
"""OBSERVE — merge GEPA failure manifests across backlog runs for one specialist.

Two evidence sources (combine with ``--enrich-braintrust``):

1. **Experiment log** — ``score_run.py --export-failures`` on selected ``run_id``s.
2. **Braintrust backlog** — readonly fetch of every logged real specialist
   experiment in ``Mailroom-Evals`` (eval roots + LLM reasoning excerpts).

Example (SAND-027 N=20 correspondence, DeepSeek + Granite + Qwen3-8b):

    uv run python scripts/gepa_observe_specialists.py \\
        --task correspondence \\
        --run-id 20260927T105317Z-eval-correspondence \\
        --run-id 20260927T052637Z-eval-correspondence \\
        --run-id 20260927T033031Z-eval-correspondence \\
        --enrich-braintrust \\
        --out data/manifests/gepa/correspondence_merged.failures.jsonl

Full specialist backlog from Braintrust (all models / runs in the log):

    uv run python scripts/gepa_observe_specialists.py --braintrust-backlog --all-defaults
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO))

from pipeline.env import load_env

load_env()

from evals import experiment_log
from evals.gepa import braintrust_backlog as bt

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
    tmp_dir.mkdir(exist_ok=True)
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


def _enrich_from_log_runs(rows: list[dict], run_ids: list[str]) -> list[dict]:
    enriched = list(rows)
    for run_id in run_ids:
        exp = run_id  # experiment name == run_id in this repo
        try:
            enriched = bt.enrich_manifest_from_braintrust(enriched, experiment_name=exp)
        except Exception as exc:
            print(f"  braintrust enrich skipped for {run_id}: {type(exc).__name__}: {exc}")
    return enriched


def _write_jsonl(path: Path, rows: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, default=str) + "\n")
    return len(rows)


def _braintrust_backlog_for_task(task: str, entries: list[dict], out_path: Path) -> int:
    rows = bt.build_task_backlog_manifest(task, entries)
    return _write_jsonl(out_path, rows)


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
    parser.add_argument(
        "--braintrust-backlog",
        action="store_true",
        help="build manifests from ALL Braintrust specialist experiments in the experiment log (not just DEFAULT_RUNS)",
    )
    parser.add_argument(
        "--enrich-braintrust",
        action="store_true",
        help="attach Braintrust span ids + LLM reasoning excerpts to log-exported failures",
    )
    parser.add_argument(
        "--index-out",
        default="reports/gepa/braintrust_backlog_index.json",
        help="write discovered Braintrust run catalog (default: reports/gepa/braintrust_backlog_index.json)",
    )
    args = parser.parse_args()

    backlog = bt.discover_braintrust_specialist_runs(experiment_log.load_runs())
    manifest_stats: dict[str, int] = {}
    index_path = REPO / args.index_out
    if backlog:
        bt.write_backlog_index(backlog, index_path, manifest_stats=manifest_stats)
        total_runs = sum(len(v) for v in backlog.values())
        print(f"braintrust backlog index: {total_runs} runs across {len(backlog)} tasks → {index_path}")

    if args.braintrust_backlog:
        tasks = sorted(backlog.keys()) if backlog else []
        if args.all_defaults:
            tasks = sorted(set(tasks) | set(DEFAULT_RUNS))
        elif args.task:
            tasks = [args.task]
        if not tasks:
            parser.error("no Braintrust specialist runs found in experiment log")
        for task in tasks:
            entries = backlog.get(task, [])
            if not entries:
                print(f"{task}: no Braintrust runs in log — skip")
                continue
            out = REPO / "data/manifests/gepa" / f"{task}_braintrust_backlog.failures.jsonl"
            n = _braintrust_backlog_for_task(task, entries, out)
            manifest_stats[task] = n
            print(f"{task}: {n} unique failures from {len(entries)} Braintrust experiments → {out}")
        if backlog:
            bt.write_backlog_index(backlog, index_path, manifest_stats=manifest_stats)
        return 0

    if args.all_defaults:
        for task, run_ids in DEFAULT_RUNS.items():
            out = REPO / "data/manifests/gepa" / f"{task}_merged.failures.jsonl"
            n_unique, n_rows = merge_failures(run_ids, out)
            if args.enrich_braintrust:
                rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines() if line.strip()]
                rows = _enrich_from_log_runs(rows, run_ids)
                n_unique = _write_jsonl(out, rows)
            print(f"{task}: {n_unique} unique failures ({n_rows} rows across {len(run_ids)} runs) → {out}")
        return 0

    if not args.task and not args.run_ids:
        parser.error("pass --task, --run-id ..., --all-defaults, or --braintrust-backlog")
    run_ids = args.run_ids or DEFAULT_RUNS[args.task]
    task = args.task or "custom"
    out = Path(args.out) if args.out else REPO / "data/manifests/gepa" / f"{task}_merged.failures.jsonl"
    n_unique, n_rows = merge_failures(run_ids, out)
    if args.enrich_braintrust:
        rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines() if line.strip()]
        rows = _enrich_from_log_runs(rows, run_ids)
        n_unique = _write_jsonl(out, rows)
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
