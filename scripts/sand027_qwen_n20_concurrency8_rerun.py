#!/usr/bin/env python
"""Re-run the Qwen3-8B N=20 correspondence/insurance/contracts waves at
concurrency=8 so they are comparable to the concurrency=8 merger_agreement,
corporate_records, and sorter waves.

The original concurrency=1 rows (20260926T234358Z-eval-correspondence,
20260926T234603Z-eval-insurance_claims, 20260926T235347Z-eval-contracts)
stay untouched in the append-only experiment log — this always starts fresh
runs (new run_ids) rather than resuming or overwriting them, per the
"history is append-only" rule. ``params.concurrency`` on each row is what
distinguishes the new comparable rows from the old ones.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from evals import experiment_log  # noqa: E402

LOG = REPO / "reports" / "api-comparisons" / "sand027-n20-run.log"
MODEL = "qwen/qwen3-8b"
PROFILE = "qwen3-8b"
SAMPLE = 20
SEED = 42
CONCURRENCY = int(os.environ.get("EVAL_CONCURRENCY") or "8")

WAVES = [
    ("eval:correspondence", "class:correspondence"),
    ("eval:insurance_claims", "class:insurance_claim"),
    ("eval:contracts", "class:contract"),
]


def _log(msg: str) -> None:
    line = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + msg
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _wave_done_at_concurrency(task: str, subset: str, concurrency: int) -> dict | None:
    task_name = task.split(":", 1)[-1]
    for run in reversed(experiment_log.load_runs()):
        if run.get("mode") != "real":
            continue
        if run.get("task") != task_name:
            continue
        if (run.get("dataset") or {}).get("subset") != subset:
            continue
        if run.get("model") != MODEL:
            continue
        params = run.get("params") or {}
        if params.get("decode_profile") != PROFILE:
            continue
        if params.get("sample") != SAMPLE:
            continue
        if params.get("concurrency") != concurrency:
            continue
        if run.get("error"):
            continue
        n = (run.get("metrics") or {}).get("n") or 0
        if n >= SAMPLE:
            return run
    return None


def _run_wave(task: str, subset: str) -> int:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env.setdefault("BRAINTRUST_PROJECT", "Mailroom-Evals")
    cmd = [
        "uv", "run", "python", "-u", "scripts/run_evals.py",
        "--task", task,
        "--real",
        "--subset", subset,
        "--sample", str(SAMPLE),
        "--seed", str(SEED),
        "--model", MODEL,
        "--decode-profile", PROFILE,
        "--require-trace-sink",
        "--prompt-source", "frozen",
        "--trace-backend", "braintrust",
        "--concurrency", str(CONCURRENCY),
    ]
    _log("RUN " + " ".join(cmd[3:]))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(
            "\n=== QWEN-N20-CONCURRENCY8-RERUN "
            + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            + f" task={task} subset={subset} ===\n"
        )
        fh.flush()
        proc = subprocess.run(cmd, cwd=REPO, stdout=fh, stderr=subprocess.STDOUT, env=env)
    _log(f"exit {task} code={proc.returncode}")
    return proc.returncode


def main() -> int:
    for task, subset in WAVES:
        done = _wave_done_at_concurrency(task, subset, CONCURRENCY)
        if done:
            _log(
                f"SKIP {task} {subset} concurrency={CONCURRENCY} "
                f"run={done.get('run_id')} n={(done.get('metrics') or {}).get('n')} "
                f"cost={(done.get('performance') or {}).get('cost_usd_est_total')}"
            )
            continue
        code = _run_wave(task, subset)
        if code != 0:
            return code
    _log("qwen n=20 concurrency=8 rerun complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
