#!/usr/bin/env python3
"""mailroom-evals CLI — run eval, pilot, and calibration tasks.

Usage:
    python scripts/run_evals.py --list
    python scripts/run_evals.py --task eval:classify --mock --n 3
    python scripts/run_evals.py --task pilot:chain --mock
    python scripts/run_evals.py --task calibration:judge --mock
    python scripts/run_evals.py --task eval:insurance_claims --real \
        --subset class:insurance_claim --sample 25 --seed 42
    python scripts/run_evals.py --task all --mock --n 3          # CI smoke

Trace sink: Braintrust when BRAINTRUST_API_KEY is set, else local Arize
Phoenix; override with --trace-backend. Every run appends one line to
reports/experiment_log.jsonl (see src/evals/experiment_log.py).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.env import load_env  # noqa: E402

load_env()

from evals.registry import list_tasks  # noqa: E402
from evals.runner import run_task  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task", default="", help="task id (<family>:<name>) or 'all'")
    parser.add_argument("--list", action="store_true", help="list registered tasks")
    parser.add_argument("--invoke", choices=("node", "agent"), default="node",
                        help="node-function or underlying-agent invocation (default: node)")
    parser.add_argument("--subset", default=None, help="subset spec (see evals.cases.parse_subset)")
    parser.add_argument("--sample", type=int, default=None, help="stratified sample size")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n", type=int, default=None, help="hard cap on cases")
    parser.add_argument("--mock", action="store_true", help="deterministic fake LLM (no network)")
    parser.add_argument("--real", action="store_true", help="real LLM (OPENROUTER_API_KEY)")
    parser.add_argument("--trace-backend", choices=("auto", "braintrust", "phoenix", "none"), default=None)
    parser.add_argument("--model", default=None, help="model override recorded in the log")
    parser.add_argument("--prompt-version", default=None, help="prompt version tag for iteration A/Bs")
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="load + invoke one case only")
    parser.add_argument("--json", action="store_true", help="print the run summary as JSON")
    args = parser.parse_args()

    if args.list or not args.task:
        print("Registered tasks:")
        for spec in list_tasks():
            print(f"  {spec.task_id:26s} subset={spec.default_subset:24s} {spec.description}")
        return 0 if args.list else 2

    mock = not args.real
    task_ids = [spec.task_id for spec in list_tasks() if spec.family == "eval"] if args.task == "all" else [args.task]
    failures = 0
    for task_id in task_ids:
        result = run_task(
            task_id,
            invoke_mode=args.invoke,
            subset=args.subset,
            sample=args.sample,
            seed=args.seed,
            n=args.n,
            mock=mock,
            trace_backend=args.trace_backend,
            model=args.model,
            prompt_version=args.prompt_version,
            concurrency=args.concurrency,
            dry_run=args.dry_run,
            pilot=args.task.startswith("pilot:"),
        )
        summary = result.summary
        if args.json:
            print(json.dumps(summary, indent=2, default=str))
        else:
            metrics = summary.get("metrics") or {}
            perf = summary.get("performance") or {}
            print(
                f"{summary['run_id']}: n={metrics.get('n')} errors={metrics.get('errors')} "
                f"latency_ms_mean={perf.get('latency_ms_mean')} "
                f"tokens={perf.get('tokens_prompt_total')}+{perf.get('tokens_completion_total')}"
            )
            calibration = summary.get("calibration") or {}
            if calibration.get("report_paths"):
                print(f"  calibration report: {calibration['report_paths']['md']}")
        if summary.get("error") or (metrics.get("errors") or 0) > (metrics.get("n") or 1):
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
