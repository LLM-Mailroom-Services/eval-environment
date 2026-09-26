#!/usr/bin/env python
"""SAND-027 N=20 OpenRouter waves — resume-safe, spend-capped orchestration.

Skips completed waves (experiment log), resumes interrupted runs (--resume),
tracks cumulative estimated cost + wall time, and stops on over_cap per handoff.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from evals import experiment_log  # noqa: E402

SAMPLE = 20
SEED = 42
PROGRAM_CAP_USD = 15.0  # 10 waves × $1.50 profile cap (hard stop)
TRACKER = REPO / "reports" / "api-comparisons" / "spend-tracker.jsonl"
LOG = REPO / "reports" / "api-comparisons" / "sand027-n20-run.log"

WAVES: list[tuple[str, str, str, str]] = [
    ("correspondence", "eval:correspondence", "qwen/qwen3-8b", "qwen3-8b"),
    ("insurance_claim", "eval:insurance_claims", "qwen/qwen3-8b", "qwen3-8b"),
    ("contract", "eval:contracts", "qwen/qwen3-8b", "qwen3-8b"),
    ("merger_agreement", "eval:merger_agreement", "qwen/qwen3-8b", "qwen3-8b"),
    ("corporate_record", "eval:corporate_records", "qwen/qwen3-8b", "qwen3-8b"),
    ("correspondence", "eval:correspondence", "ibm-granite/granite-4.2-8b", "granite-4.2-8b"),
    ("insurance_claim", "eval:insurance_claims", "ibm-granite/granite-4.2-8b", "granite-4.2-8b"),
    ("contract", "eval:contracts", "ibm-granite/granite-4.2-8b", "granite-4.2-8b"),
    ("merger_agreement", "eval:merger_agreement", "ibm-granite/granite-4.2-8b", "granite-4.2-8b"),
    ("corporate_record", "eval:corporate_records", "ibm-granite/granite-4.2-8b", "granite-4.2-8b"),
]


@dataclass(frozen=True)
class WaveKey:
    task: str
    model: str
    decode_profile: str
    doc_class: str


def _wave_key(cls: str, task: str, model: str, profile: str) -> WaveKey:
    return WaveKey(task=task, model=model, decode_profile=profile, doc_class=cls)


def _matches_wave(run: dict, key: WaveKey) -> bool:
    if run.get("mode") != "real":
        return False
    params = run.get("params") or {}
    if params.get("sample") != SAMPLE or params.get("seed") != SEED:
        return False
    if params.get("decode_profile") != key.decode_profile:
        return False
    if run.get("model") != key.model:
        return False
    task_name = key.task.split(":", 1)[-1]
    if run.get("task") != task_name:
        return False
    subset = (run.get("dataset") or {}).get("subset") or ""
    return subset == f"class:{key.doc_class}"


def _completed_waves() -> dict[WaveKey, dict]:
    out: dict[WaveKey, dict] = {}
    for run in experiment_log.load_runs():
        for cls, task, model, profile in WAVES:
            key = _wave_key(cls, task, model, profile)
            if key in out:
                continue
            if not _matches_wave(run, key):
                continue
            n = (run.get("metrics") or {}).get("n") or 0
            if n >= SAMPLE and not run.get("error"):
                out[key] = run
    return out


def _partial_run(key: WaveKey) -> tuple[str, int] | None:
    """Best partial run dir for this wave (cases on disk, no full summary yet)."""
    exp_root = experiment_log.experiments_dir()
    if not exp_root.exists():
        return None
    best: tuple[str, int] | None = None
    for run in experiment_log.load_runs():
        if not _matches_wave(run, key):
            continue
        n = (run.get("metrics") or {}).get("n") or 0
        if 0 < n < SAMPLE:
            rid = run["run_id"]
            on_disk = len(experiment_log.load_cases(rid))
            if best is None or on_disk > best[1]:
                best = (rid, on_disk)
    for path in sorted(exp_root.iterdir(), key=lambda p: p.name, reverse=True):
        if not path.is_dir():
            continue
        manifest = path / "subset_manifest.json"
        if not manifest.exists():
            continue
        try:
            meta = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        prov = meta.get("provenance") or {}
        if prov.get("sample") != SAMPLE or prov.get("seed") != SEED:
            continue
        subset = prov.get("subset") or ""
        if subset != f"class:{key.doc_class}":
            continue
        rid = path.name
        if any(r.get("run_id") == rid and (r.get("metrics") or {}).get("n", 0) >= SAMPLE for r in experiment_log.load_runs()):
            continue
        n_cases = len(experiment_log.load_cases(rid))
        if 0 < n_cases < SAMPLE and (best is None or n_cases > best[1]):
            best = (rid, n_cases)
    return best


def _cumulative_cost(completed: dict[WaveKey, dict]) -> float:
    total = 0.0
    for run in completed.values():
        perf = run.get("performance") or {}
        c = perf.get("cost_usd_est_total")
        if isinstance(c, (int, float)):
            total += float(c)
    return round(total, 6)


def _append_tracker(entry: dict) -> None:
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    with TRACKER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")


def _run_wave(key: WaveKey, resume_id: str | None) -> int:
    cmd = [
        "uv",
        "run",
        "python",
        "scripts/run_evals.py",
        "--task",
        key.task,
        "--real",
        "--subset",
        f"class:{key.doc_class}",
        "--sample",
        str(SAMPLE),
        "--seed",
        str(SEED),
        "--model",
        key.model,
        "--decode-profile",
        key.decode_profile,
        "--require-trace-sink",
        "--prompt-source",
        "frozen",
        "--trace-backend",
        "auto",
    ]
    if resume_id:
        cmd.extend(["--resume", resume_id])
    LOG.parent.mkdir(parents=True, exist_ok=True)
    wall_start = time.time()
    with LOG.open("a", encoding="utf-8") as logfh:
        logfh.write(
            f"\n=== ORCH {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} "
            f"class={key.doc_class} model={key.model} profile={key.decode_profile} "
            f"resume={resume_id or 'none'} ===\n"
        )
        logfh.flush()
        proc = subprocess.run(cmd, cwd=REPO, stdout=logfh, stderr=subprocess.STDOUT)
    wall_s = round(time.time() - wall_start, 1)
    _append_tracker(
        {
            "ts": experiment_log.utc_now(),
            "wave": key.__dict__,
            "resume_id": resume_id,
            "exit_code": proc.returncode,
            "wall_s": wall_s,
        }
    )
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-plan", action="store_true", help="print plan only")
    args = parser.parse_args()

    completed = _completed_waves()
    spent = _cumulative_cost(completed)
    print(f"Completed waves: {len(completed)}/{len(WAVES)}  cumulative_cost_usd_est≈${spent:.4f}")

    status = 0
    for cls, task, model, profile in WAVES:
        key = _wave_key(cls, task, model, profile)
        if key in completed:
            run = completed[key]
            perf = run.get("performance") or {}
            cap = run.get("cost_cap") or {}
            print(
                f"SKIP done  {cls:18} {profile:14} run={run['run_id']} "
                f"n={(run.get('metrics') or {}).get('n')} "
                f"cost=${perf.get('cost_usd_est_total')} "
                f"wall={run.get('duration_s')}s cap={cap.get('status')}"
            )
            if cap.get("status") == "over_cap":
                print("STOP: prior N=20 wave over_cap (handoff escalation)")
                return 2
            continue

        if spent >= PROGRAM_CAP_USD:
            print(f"STOP: program cap ${PROGRAM_CAP_USD} reached (spent≈${spent})")
            return 3

        partial = _partial_run(key)
        resume_id = partial[0] if partial else None
        if args.dry_plan:
            print(
                f"RUN  plan  {cls:18} {profile:14} resume={resume_id or 'fresh'} "
                f"partial_cases={partial[1] if partial else 0}"
            )
            continue

        print(f"RUN       {cls:18} {profile:14} resume={resume_id or 'fresh'}")
        code = _run_wave(key, resume_id)
        if code != 0:
            print(f"FAIL exit={code} — re-run this script to resume")
            return code
        # refresh completed + spend after each wave
        completed = _completed_waves()
        spent = _cumulative_cost(completed)
        last = completed.get(key)
        if last:
            cap = last.get("cost_cap") or {}
            if cap.get("status") == "over_cap":
                print("STOP: wave over_cap")
                return 2

    print(f"All {len(WAVES)} waves complete. cumulative_cost_usd_est≈${spent:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
