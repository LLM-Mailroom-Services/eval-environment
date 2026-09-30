#!/usr/bin/env python
"""Finish Qwen3-8B N=20 specialist waves not yet completed.

Skips correspondence, insurance, and contracts (already n=20). Runs merger
then corporate_records as fresh OpenRouter specialist calls. No Granite / N=50.
"""
from __future__ import annotations

import json
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
# 20260927T012611Z ran under the old 48k-char/8-9-call-per-doc chunking
# formula (2 cases only, one of them a parse_error 0-score). specialist_llm's
# CHUNK_CHARS for merger_agreement is now 480k chars (single call covers
# every doc in the pinned N=20 set) — mixing those 9-call rows with the new
# 1-call rows in one report would be methodologically inconsistent, so
# merger starts a fresh run instead of resuming that partial one.
CONTRACTS_RID = "20260926T235347Z-eval-contracts"

WAVES = [
    ("eval:merger_agreement", "class:merger_agreement"),
    ("eval:corporate_records", "class:corporate_record"),
]


def _log(msg: str) -> None:
    line = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + msg
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _wave_done(task: str, subset: str) -> dict | None:
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
        if (run.get("params") or {}).get("decode_profile") != PROFILE:
            continue
        if (run.get("params") or {}).get("sample") != SAMPLE:
            continue
        if run.get("error"):
            continue
        n = (run.get("metrics") or {}).get("n") or 0
        # Unchunked merger waves truncated JSON and scored 0 — do not treat
        # those as complete even if n reached SAMPLE.
        overall = (run.get("metrics") or {}).get("overall_score")
        if n >= SAMPLE and (overall is None or overall > 0 or task != "eval:merger_agreement"):
            return run
    return None


def _cases_on_disk(run_id: str) -> int:
    path = experiment_log.experiments_dir() / run_id / "cases.jsonl"
    if not path.exists():
        return 0
    return sum(1 for _ in path.open())


def _wait_pid(pid: int) -> None:
    _log(f"wait pid={pid}")
    while Path(f"/proc/{pid}").exists():
        _log(f"still running pid={pid} contracts_cases={_cases_on_disk(CONTRACTS_RID)}")
        time.sleep(20)
    _log(f"pid {pid} exited; contracts_cases={_cases_on_disk(CONTRACTS_RID)}")
    time.sleep(2)


def _run_wave(task: str, subset: str, resume_id: str | None) -> int:
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
    if resume_id:
        cmd.extend(["--resume", resume_id])
    _log("RUN " + " ".join(cmd[3:]))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write("\n=== QWEN-N20 " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " ===\n")
        fh.flush()
        proc = subprocess.run(cmd, cwd=REPO, stdout=fh, stderr=subprocess.STDOUT, env=env)
    _log(f"exit {task} code={proc.returncode}")
    return proc.returncode


def main() -> int:
    wait_pid = int(os.environ.get("WAIT_PID") or "0")
    if wait_pid:
        _wait_pid(wait_pid)

    for task, subset in WAVES:
        done = _wave_done(task, subset)
        if done:
            _log(
                f"SKIP {task} {subset} run={done.get('run_id')} "
                f"n={(done.get('metrics') or {}).get('n')} "
                f"cost={(done.get('performance') or {}).get('cost_usd_est_total')}"
            )
            continue
        code = _run_wave(task, subset, None)
        if code != 0:
            return code
    _log("export_site_snapshot")
    subprocess.run(
        ["uv", "run", "python", "scripts/export_site_snapshot.py"],
        cwd=REPO,
        check=False,
    )
    _log("qwen n=20 remaining waves complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
