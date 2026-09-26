#!/usr/bin/env python
"""SAND-027 OpenRouter waves: N=20 first, N=50 only after all 20s complete.

N=100 is never scheduled. Resume-safe, spend-tracked, Braintrust-traced.
Qwen comparator is ``qwen/qwen3-8b`` (Modal Qwen3-8B twin). Extra N=20
contracts wave pins ``contracts_specialist_v33`` for Modal prompt parity.
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

SEED = 42
ALLOWED_SAMPLES = frozenset({20, 50})
FORBIDDEN_SAMPLES = frozenset({100})
N20_PROGRAM_CAP_USD = 16.5  # 11 N=20 waves × $1.50 profile cap
TRACKER = REPO / "reports" / "api-comparisons" / "spend-tracker.jsonl"
LOG = REPO / "reports" / "api-comparisons" / "sand027-n20-run.log"

SPECIALISTS: list[tuple[str, str]] = [
    ("correspondence", "eval:correspondence"),
    ("insurance_claim", "eval:insurance_claims"),
    ("contract", "eval:contracts"),
    ("merger_agreement", "eval:merger_agreement"),
    ("corporate_record", "eval:corporate_records"),
]
MODELS: list[tuple[str, str]] = [
    ("qwen/qwen3-8b", "qwen3-8b"),
    ("ibm-granite/granite-4.2-8b", "granite-4.2-8b"),
]


@dataclass(frozen=True)
class WaveKey:
    task: str
    model: str
    decode_profile: str
    doc_class: str
    sample: int
    prompt_version: str | None = None


def _matrix(sample: int) -> list[WaveKey]:
    if sample in FORBIDDEN_SAMPLES or sample not in ALLOWED_SAMPLES:
        raise ValueError(f"sample {sample} is not authorized (allowed={sorted(ALLOWED_SAMPLES)})")
    waves = [
        WaveKey(task=task, model=model, decode_profile=profile, doc_class=cls, sample=sample)
        for model, profile in MODELS
        for cls, task in SPECIALISTS
    ]
    if sample == 20:
        # Modal Leg A apples-to-apples: full v33 contracts prompt + Qwen3-8B.
        waves.insert(
            3,
            WaveKey(
                task="eval:contracts",
                model="qwen/qwen3-8b",
                decode_profile="qwen3-8b",
                doc_class="contract",
                sample=20,
                prompt_version="contracts_specialist_v33",
            ),
        )
    return waves


PHASE_20 = _matrix(20)
PHASE_50 = _matrix(50)
ALL_WAVES = PHASE_20 + PHASE_50


def _matches_wave(run: dict, key: WaveKey) -> bool:
    if run.get("mode") != "real":
        return False
    params = run.get("params") or {}
    if params.get("sample") != key.sample or params.get("seed") != SEED:
        return False
    if params.get("decode_profile") != key.decode_profile:
        return False
    if run.get("model") != key.model:
        return False
    task_name = key.task.split(":", 1)[-1]
    if run.get("task") != task_name:
        return False
    subset = (run.get("dataset") or {}).get("subset") or ""
    if subset != f"class:{key.doc_class}":
        return False
    want_pv = key.prompt_version
    got_pv = run.get("prompt_version")
    if not got_pv:
        slot = (run.get("prompt_versions") or {}).get("contracts_specialist") or {}
        if key.doc_class == "contract" and slot.get("key") == "contracts_specialist_v33":
            got_pv = "contracts_specialist_v33"
        elif key.doc_class == "contract" and slot.get("key") == "contracts_specialist_v1":
            got_pv = None
    if want_pv:
        return got_pv == want_pv
    if key.doc_class == "contract" and got_pv == "contracts_specialist_v33":
        return False
    return got_pv in (None, "", "contracts_specialist_v1")


def _completed_waves(waves: list[WaveKey]) -> dict[WaveKey, dict]:
    out: dict[WaveKey, dict] = {}
    runs = experiment_log.load_runs()
    for key in waves:
        for run in runs:
            if key in out:
                break
            if not _matches_wave(run, key):
                continue
            n = (run.get("metrics") or {}).get("n") or 0
            if n >= key.sample and not run.get("error"):
                out[key] = run
    return out


def _partial_run(key: WaveKey) -> tuple[str, int] | None:
    exp_root = experiment_log.experiments_dir()
    if not exp_root.exists():
        return None
    best: tuple[str, int] | None = None
    for run in experiment_log.load_runs():
        if not _matches_wave(run, key):
            continue
        n = (run.get("metrics") or {}).get("n") or 0
        if 0 < n < key.sample:
            rid = run["run_id"]
            on_disk = len(experiment_log.load_cases(rid))
            if best is None or on_disk > best[1]:
                best = (rid, on_disk)
    for path in sorted(exp_root.iterdir(), key=lambda p: p.name, reverse=True):
        lock_path = path / "wave_lock.json"
        if not lock_path.exists():
            continue
        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if lock.get("sample") != key.sample or lock.get("seed") != SEED:
            continue
        if lock.get("subset") != f"class:{key.doc_class}":
            continue
        if lock.get("model") != key.model:
            continue
        if lock.get("decode_profile") != key.decode_profile:
            continue
        if (lock.get("prompt_version") or None) != (key.prompt_version or None):
            continue
        rid = path.name
        if any(
            r.get("run_id") == rid and (r.get("metrics") or {}).get("n", 0) >= key.sample
            for r in experiment_log.load_runs()
        ):
            continue
        n_cases = len(experiment_log.load_cases(rid))
        if 0 < n_cases < key.sample and (best is None or n_cases > best[1]):
            best = (rid, n_cases)
    return best


def _cumulative_cost(completed: dict[WaveKey, dict]) -> float:
    total = 0.0
    for run in completed.values():
        c = (run.get("performance") or {}).get("cost_usd_est_total")
        if isinstance(c, (int, float)):
            total += float(c)
    return round(total, 6)


def _append_tracker(entry: dict) -> None:
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    with TRACKER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")


def _run_wave(key: WaveKey, resume_id: str | None) -> int:
    cmd = [
        "uv", "run", "python", "scripts/run_evals.py",
        "--task", key.task,
        "--real",
        "--subset", f"class:{key.doc_class}",
        "--sample", str(key.sample),
        "--seed", str(SEED),
        "--model", key.model,
        "--decode-profile", key.decode_profile,
        "--require-trace-sink",
        "--prompt-source", "frozen",
        "--trace-backend", "auto",
    ]
    if key.prompt_version:
        cmd.extend(["--prompt-version", key.prompt_version])
    if resume_id:
        cmd.extend(["--resume", resume_id])
    LOG.parent.mkdir(parents=True, exist_ok=True)
    wall_start = time.time()
    with LOG.open("a", encoding="utf-8") as logfh:
        logfh.write(
            f"\n=== ORCH {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} "
            f"n={key.sample} class={key.doc_class} model={key.model} "
            f"profile={key.decode_profile} prompt={key.prompt_version or 'frozen-v1'} "
            f"resume={resume_id or 'none'} ===\n"
        )
        logfh.flush()
        proc = subprocess.run(cmd, cwd=REPO, stdout=logfh, stderr=subprocess.STDOUT)
    wall_s = round(time.time() - wall_start, 1)
    _append_tracker(
        {
            "ts": experiment_log.utc_now(),
            "wave": {
                "sample": key.sample,
                "doc_class": key.doc_class,
                "model": key.model,
                "decode_profile": key.decode_profile,
                "prompt_version": key.prompt_version,
            },
            "resume_id": resume_id,
            "exit_code": proc.returncode,
            "wall_s": wall_s,
        }
    )
    return proc.returncode


def _execute_phase(
    waves: list[WaveKey],
    *,
    dry_plan: bool,
    stop_on_over_cap: bool,
    n20_spent: float,
) -> tuple[int, float]:
    completed = _completed_waves(waves)
    spent = _cumulative_cost(completed) + n20_spent
    print(
        f"Phase n={waves[0].sample}: {len(completed)}/{len(waves)} done  "
        f"phase_cost≈${_cumulative_cost(completed):.4f}"
    )
    for key in waves:
        if key in completed:
            run = completed[key]
            perf = run.get("performance") or {}
            cap = run.get("cost_cap") or {}
            print(
                f"SKIP n={key.sample:<2} {key.doc_class:18} {key.decode_profile:14} "
                f"{key.prompt_version or 'frozen-v1':28} "
                f"run={run['run_id']} cost=${perf.get('cost_usd_est_total')} "
                f"wall={run.get('duration_s')}s cap={cap.get('status')}"
            )
            if stop_on_over_cap and cap.get("status") == "over_cap":
                print("STOP: N=20 wave over_cap (handoff escalation)")
                return 2, spent
            continue

        if stop_on_over_cap and spent >= N20_PROGRAM_CAP_USD:
            print(f"STOP: N=20 program cap ${N20_PROGRAM_CAP_USD} (spent≈${spent})")
            return 3, spent

        partial = _partial_run(key)
        resume_id = partial[0] if partial else None
        label = (
            f"n={key.sample:<2} {key.doc_class:18} {key.decode_profile:14} "
            f"{key.prompt_version or 'frozen-v1':28}"
        )
        if dry_plan:
            print(f"PLAN {label} resume={resume_id or 'fresh'} partial={partial[1] if partial else 0}")
            continue

        print(f"RUN  {label} resume={resume_id or 'fresh'}")
        code = _run_wave(key, resume_id)
        if code != 0:
            print(f"FAIL exit={code} — re-run to resume")
            return code, spent
        completed = _completed_waves(waves)
        spent = _cumulative_cost(completed) + n20_spent
        last = completed.get(key)
        if last and stop_on_over_cap and (last.get("cost_cap") or {}).get("status") == "over_cap":
            print("STOP: N=20 wave over_cap")
            return 2, spent
    return 0, spent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-plan", action="store_true")
    parser.add_argument(
        "--phase",
        choices=("20", "50", "20-then-50"),
        default="20-then-50",
        help="20 only, 50 only (refuses unless all N=20 complete), or 20 then 50. Never 100.",
    )
    args = parser.parse_args()

    n20_done = _completed_waves(PHASE_20)
    print(f"N=20 complete: {len(n20_done)}/{len(PHASE_20)}  cost≈${_cumulative_cost(n20_done):.4f}")

    if args.phase in ("20", "20-then-50"):
        code, _ = _execute_phase(PHASE_20, dry_plan=args.dry_plan, stop_on_over_cap=True, n20_spent=0.0)
        if code != 0:
            return code
        n20_done = _completed_waves(PHASE_20)

    if args.phase == "20":
        print("N=20 phase complete. N=50 not started (--phase 20). N=100 never scheduled.")
        return 0

    if len(n20_done) < len(PHASE_20):
        missing = [w for w in PHASE_20 if w not in n20_done]
        print(
            f"REFUSE N=50: {len(missing)} N=20 wave(s) still incomplete "
            f"(first missing: {missing[0].doc_class} {missing[0].decode_profile} "
            f"{missing[0].prompt_version or 'frozen-v1'}). Finish 20s first."
        )
        return 4

    print("All N=20 waves complete — starting N=50 (N=100 not scheduled).")
    # $1.50 profile cap will trip over_cap on 50-doc waves; that is expected, do not halt.
    code, _ = _execute_phase(
        PHASE_50, dry_plan=args.dry_plan, stop_on_over_cap=False, n20_spent=_cumulative_cost(n20_done)
    )
    if code != 0:
        return code
    print("N=20 + N=50 complete. N=100 not scheduled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
