#!/usr/bin/env python3
"""Export the Vercel viewer snapshot (web/data/snapshot.json).

The viewer (web/) is a zero-dependency static site: this script bakes the
append-only experiment log, the task catalog, the corpus pin, the frozen
prompt lineage, and environment health into ONE tracked JSON file that
Vercel serves. Refresh discipline: run this whenever the experiment log,
corpus pin, prompts, tasks, skills or tests change, then commit `reports/`
and the snapshot together.

`--check` compares every top-level section except `generated_at` (wall
clock) and `cases` content (gitignored run artifacts; shape-checked only),
so a stale environment/prompt/task surface fails CI instead of passing
silently. The snapshot must be generated under the pipeline pin CI installs
(see `scripts/cloud-agent-install.sh`); `environment.corpus` and
`health.lineage_*` probe the installed `mailroom` package.

    uv run python scripts/export_site_snapshot.py            # write snapshot
    uv run python scripts/export_site_snapshot.py --check    # exit 1 if stale
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from evals import experiment_log as elog
from evals.prompts import lineage as plineage
from evals.registry import list_tasks

SNAPSHOT_PATH = REPO_ROOT / "web" / "data" / "snapshot.json"
CASE_CAP = 250  # max case rows embedded per run
SCHEMA = "eval-site-snapshot"
VERSION = 1

# Run-summary keys the viewer needs (drop bulky provenance blocks).
# trace_ids + the judging block stay: they make follow-up records
# (post-hoc judging re-appends share the run_id) distinguishable from
# their originals and keep log rows ↔ trace-sink cross-references possible.
_RUN_KEYS = (
    "run_id", "family", "task", "invoke", "mode", "model", "prompt_version",
    "prompt_lineage", "prompt_source", "trace_backend", "started_at",
    "finished_at", "duration_s", "error", "metrics", "performance",
    "dataset", "git", "schema_version", "calibration", "trace_ids",
    "judging", "pipeline_git", "prompt_versions",
)

# Case-row keys the viewer needs (drop doc text / raw predictions).
_CASE_KEYS = (
    "case_id", "filename", "expected_doc_class", "expected_subclass",
    "expected_specialist", "expected_stage", "review_expected",
    "retry_expected", "fixture_kind", "fixture_cell", "fixture_outcome",
    "failure_stage", "doc_text_sha256", "scores", "latency_ms", "error",
)

_HEADLINE_KEYS = (
    "class_accuracy", "accuracy", "overall_score", "extraction_f1",
    "verdict_agreement", "mean_score", "intake_pass_rate",
)


def _headline(metrics: dict) -> Any:
    for key in _HEADLINE_KEYS:
        if key in metrics:
            return metrics[key]
    return None


def _trim_prediction(prediction: Any) -> Any:
    """Keep only short scalar prediction fields (doc_type/stage/confidence…)."""
    if not isinstance(prediction, dict):
        return prediction if isinstance(prediction, (str, int, float, bool)) or prediction is None else None
    out = {}
    for key, value in prediction.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            out[key] = value
    return out


def _trim_run(record: dict) -> dict:
    run = {key: record.get(key) for key in _RUN_KEYS}
    metrics = record.get("metrics") or {}
    run["headline"] = _headline(metrics)
    # Use the run-summary count so --check stays hermetic: data/experiments/
    # case files are gitignored and absent in CI.
    n = metrics.get("n")
    run["n_cases"] = int(n) if n is not None else len(elog.load_cases(record["run_id"]))
    return run


def _embed_cases(run: dict) -> list[dict]:
    cases = elog.load_cases(run["run_id"])
    trimmed = []
    for case in cases[:CASE_CAP]:
        row = {key: case.get(key) for key in _CASE_KEYS if case.get(key) is not None}
        row["prediction"] = _trim_prediction(case.get("prediction"))
        trimmed.append(row)
    return trimmed


def _corpus() -> dict:
    from pipeline.hf_corpora import CORPORA, FULL_CORPUS_ID, FULL_CORPUS_REVISION, HUB_CLASSES

    configs = []
    for slug, spec in sorted(CORPORA.items()):
        if spec.get("id") != FULL_CORPUS_ID:
            continue
        configs.append({
            "slug": slug,
            "schema": spec.get("schema"),
            "role": spec.get("role"),
            "pipeline": bool(spec.get("pipeline")),
            "n_docs": spec.get("n_docs"),
            "classes": spec.get("classes"),
        })
    return {
        "repo": FULL_CORPUS_ID,
        "revision": FULL_CORPUS_REVISION,
        "hub_classes": list(HUB_CLASSES),
        "configs": configs,
    }


def _prompts() -> dict:
    manifest = json.loads((REPO_ROOT / "prompts" / "manifest.json").read_text())
    versions = [
        {
            "key": key,
            "source_kind": meta.get("source_kind"),
            "source_key": meta.get("source_key"),
            "sha256": meta.get("sha256"),
            "chars": meta.get("chars"),
        }
        for key, meta in sorted(manifest["versions"].items())
    ]
    mutations_path = REPO_ROOT / "prompts" / "mutations.json"
    mutations_raw = json.loads(mutations_path.read_text()) if mutations_path.exists() else []
    # Current file schema is {"mutations": [...]}; accept the legacy bare
    # list too. Passing the wrapper object through made the viewer render
    # `mutations.length` as undefined and fail its smoke test.
    mutations = (
        mutations_raw.get("mutations", [])
        if isinstance(mutations_raw, dict)
        else mutations_raw
    )
    return {
        "lineage_id": manifest["lineage_id"],
        "frozen_version": manifest["frozen_version"],
        "frozen_at": manifest["frozen_at"],
        "pipeline_git_commit": manifest["pipeline_git_commit"],
        "versions": versions,
        "mutations": mutations,
    }


def _agents() -> list[dict]:
    """The agent catalog: every evaluated node → the pipeline agents behind
    it, the tasks that evaluate it, and the models observed per agent across
    the log (from run performance.by_agent blocks)."""
    from evals.registry import AGENT_CATALOG, list_tasks

    models_seen: dict[str, set] = {}
    for run in elog.load_runs():
        for agent, slot in ((run.get("performance") or {}).get("by_agent") or {}).items():
            models_seen.setdefault(agent, set()).update(slot.get("models") or [])

    tasks_by_node: dict[str, list] = {}
    for t in list_tasks():
        tasks_by_node.setdefault(t.node_name, []).append(t.task_id)

    catalog = []
    for node, meta in AGENT_CATALOG.items():
        for agent in meta["agents"]:
            catalog.append({
                "agent": agent,
                "node": node,
                "role": meta["role"],
                "llm": meta["llm"],
                "evaluated_by": tasks_by_node.get(node, []),
                "models_seen": sorted(models_seen.get(agent, [])),
            })
        if not meta["agents"]:
            catalog.append({
                "agent": f"(procedural) {node}",
                "node": node,
                "role": meta["role"],
                "llm": False,
                "evaluated_by": tasks_by_node.get(node, []),
                "models_seen": [],
            })
    return catalog


def _tasks() -> list[dict]:
    return [
        {
            "task_id": t.task_id,
            "family": t.family,
            "node_name": t.node_name,
            "default_subset": t.default_subset,
            "scorer": t.scorer,
            "description": t.description,
            "supports_agent_mode": t.supports_agent_mode,
            "tags": list(t.tags),
        }
        for t in list_tasks()
    ]


def _openrouter_models() -> dict:
    from evals.openrouter_roster import roster_for_snapshot

    return roster_for_snapshot()


def _inventory() -> dict:
    def names(folder: str) -> list[str]:
        base = REPO_ROOT / folder
        if not base.is_dir():
            return []
        return sorted(
            p.parent.name if p.name == "SKILL.md" else p.stem
            for p in base.rglob("*.md")
            if p.is_file() and p.name != "PROMPT_ENGINEER_GEPA_PROVENANCE.md"
        )

    test_count = sum(
        text.count("def test_")
        for path in (REPO_ROOT / "tests").glob("test_*.py")
        for text in [path.read_text()]
    )
    schemas = sorted(p.stem for p in (REPO_ROOT / "schemas").glob("*.json"))
    return {
        "skills": names(".opencode/skills"),
        "subagents": names(".opencode/agents"),
        "schemas": schemas,
        "test_count": test_count,
    }


def _health(raw_runs: list[dict]) -> dict:
    problems = [p for run in raw_runs for p in elog.validate_record(run)]
    drift = plineage.verify_lineage()
    return {
        "log_valid": not problems,
        "log_problems": problems[:10],
        "log_records": len(raw_runs),
        "lineage_drift_free": bool(drift.get("ok", drift.get("drift_free", False))),
        "lineage_detail": drift,
    }


def _totals(runs: list[dict]) -> dict:
    by_family: dict[str, int] = {}
    by_mode: dict[str, int] = {}
    by_task: dict[str, dict] = {}
    by_day: dict[str, int] = {}
    for run in runs:
        by_family[run["family"]] = by_family.get(run["family"], 0) + 1
        by_mode[run["mode"]] = by_mode.get(run["mode"], 0) + 1
        by_day[run["started_at"][:10]] = by_day.get(run["started_at"][:10], 0) + 1
        slot = by_task.setdefault(run["task"], {"runs": 0, "latest": None})
        slot["runs"] += 1
        if slot["latest"] is None or run["started_at"] > slot["latest"]["started_at"]:
            slot["latest"] = {
                "run_id": run["run_id"],
                "started_at": run["started_at"],
                "mode": run["mode"],
                "headline": run.get("headline"),
                "n_cases": run.get("n_cases"),
            }
    return {
        "total_runs": len(runs),
        "by_family": by_family,
        "by_mode": by_mode,
        "by_day": dict(sorted(by_day.items())),
        "by_task": by_task,
    }


def build_snapshot(embed_cases: bool = True) -> dict:
    raw_runs = elog.load_runs()
    run_records = [r for r in raw_runs if r.get("record_kind") != "comparison_result"]
    runs = [_trim_run(r) for r in run_records]
    runs.sort(key=lambda r: r["started_at"], reverse=True)
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "health": _health(run_records),
        "environment": {
            "tasks": _tasks(),
            "agents": _agents(),
            "corpus": _corpus(),
            "prompts": _prompts(),
            "inventory": _inventory(),
            "openrouter_models": _openrouter_models(),
        },
        "totals": _totals(runs),
        "runs": runs,
        # --check embeds no cases: data/experiments/ is gitignored and absent
        # in CI. The committed file's case structure is shape-checked instead.
        "cases": {run["run_id"]: _embed_cases(run) for run in runs} if embed_cases else {},
    }


# --check compare set: everything except the wall clock and gitignored case
# content. `runs` is compared as a canonical multiset (resume segments can
# share a run_id); `cases` is shape-checked against the committed file.
_CHECK_SECTIONS = ("schema", "version", "health", "environment", "totals")
_MAX_PROBLEMS = 12


def _clip(value: Any, limit: int = 90) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _keys(items: list) -> list[str]:
    out = []
    for item in items:
        if isinstance(item, dict):
            out.append(str(item.get("key") or item.get("task_id") or item.get("agent") or item))
        else:
            out.append(str(item))
    return out


def _list_note(committed: list, fresh: list) -> str:
    old = dict(zip(_keys(committed), committed))
    new = dict(zip(_keys(fresh), fresh))
    added, removed = sorted(set(new) - set(old)), sorted(set(old) - set(new))
    changed = sorted(
        key
        for key in set(old) & set(new)
        if json.dumps(old[key], sort_keys=True) != json.dumps(new[key], sort_keys=True)
    )
    parts = []
    if added:
        parts.append("added " + ", ".join(added[:5]) + ("…" if len(added) > 5 else ""))
    if removed:
        parts.append("removed " + ", ".join(removed[:5]) + ("…" if len(removed) > 5 else ""))
    if changed:
        parts.append("changed " + ", ".join(changed[:5]) + ("…" if len(changed) > 5 else ""))
    return f" ({'; '.join(parts)})" if parts else ""


def _walk_diffs(committed: Any, fresh: Any, path: str) -> list[str]:
    if isinstance(committed, dict) and isinstance(fresh, dict):
        diffs: list[str] = []
        for key in sorted(set(committed) | set(fresh)):
            child = f"{path}.{key}" if path else str(key)
            if key not in committed:
                diffs.append(f"{child}: missing in snapshot -> fresh {_clip(fresh[key])}")
            elif key not in fresh:
                diffs.append(f"{child}: snapshot {_clip(committed[key])} -> missing in fresh")
            else:
                diffs.extend(_walk_diffs(committed[key], fresh[key], child))
        return diffs
    if isinstance(committed, list) and isinstance(fresh, list):
        if committed != fresh:
            return [
                f"{path}: snapshot {len(committed)} entries -> fresh {len(fresh)}"
                f"{_list_note(committed, fresh)}"
            ]
        return []
    if committed != fresh:
        return [f"{path}: snapshot {_clip(committed)} -> fresh {_clip(fresh)}"]
    return []


def _run_diffs(committed: list, fresh: list) -> list[str]:
    old = sorted(json.dumps(run, sort_keys=True) for run in committed)
    new = sorted(json.dumps(run, sort_keys=True) for run in fresh)
    if old == new:
        return []
    old_ids = [json.loads(row).get("run_id") for row in old]
    new_ids = [json.loads(row).get("run_id") for row in new]
    if old_ids == new_ids:
        return ["runs: same run ids differ in content"]
    return [
        f"runs: snapshot {len(old)} rows -> fresh {len(new)} rows"
        f" ({len(set(new_ids) - set(old_ids))} new, {len(set(old_ids) - set(new_ids))} removed)"
    ]


def _case_problems(cases: Any, runs: list) -> list[str]:
    if not isinstance(cases, dict):
        return ["cases: snapshot value is not an object"]
    run_ids = {run.get("run_id") for run in runs}
    missing = sorted(str(run_id) for run_id in run_ids - set(cases))
    orphans = sorted(str(run_id) for run_id in set(cases) - run_ids)
    problems: list[str] = []
    if missing:
        problems.append(f"cases: missing entries for {len(missing)} run(s), e.g. {missing[0]}")
    if orphans:
        problems.append(f"cases: {len(orphans)} orphan entry/entries, e.g. {orphans[0]}")
    for run_id, rows in cases.items():
        if not isinstance(rows, list):
            problems.append(f"cases.{run_id}: not a list")
        elif len(rows) > CASE_CAP:
            problems.append(f"cases.{run_id}: {len(rows)} rows > cap {CASE_CAP}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if the committed snapshot is stale vs the log")
    args = parser.parse_args()

    if args.check:
        if not SNAPSHOT_PATH.exists():
            print(f"STALE: {SNAPSHOT_PATH} missing")
            return 1
        try:
            # JSON-normalize the fresh build (tuples -> lists) so it compares
            # exactly like the committed file that is loaded from disk.
            snapshot = json.loads(json.dumps(build_snapshot(embed_cases=False)))
        except ModuleNotFoundError as exc:
            print(
                f"ERROR: cannot probe the pipeline ({exc}); run bash scripts/cloud-agent-install.sh",
                file=sys.stderr,
            )
            return 2
        try:
            current = json.loads(SNAPSHOT_PATH.read_text())
        except json.JSONDecodeError as exc:
            print(f"STALE: {SNAPSHOT_PATH} is not valid JSON ({exc})")
            return 1

        problems: list[str] = []
        for key in _CHECK_SECTIONS:
            problems.extend(_walk_diffs(current.get(key), snapshot.get(key), key))
        problems.extend(_run_diffs(current.get("runs") or [], snapshot["runs"]))
        problems.extend(_case_problems(current.get("cases") or {}, snapshot["runs"]))

        if problems:
            print(f"STALE: {SNAPSHOT_PATH} is out of date:", file=sys.stderr)
            for problem in problems[:_MAX_PROBLEMS]:
                print(f"  - {problem}", file=sys.stderr)
            if len(problems) > _MAX_PROBLEMS:
                print(f"  … {len(problems) - _MAX_PROBLEMS} more problem(s)", file=sys.stderr)
            if any(problem.startswith(("environment.corpus", "health.lineage")) for problem in problems):
                print(
                    "  NOTE: environment.corpus and health.lineage_* probe the installed mailroom;"
                    " a difference means this machine's pipeline pin differs. Regenerate under the"
                    " pinned pipeline (bash scripts/cloud-agent-install.sh) or bump the pin.",
                    file=sys.stderr,
                )
            print(
                "  Fix: uv run python scripts/export_site_snapshot.py &&"
                " uv run python scripts/render_report_charts.py",
                file=sys.stderr,
            )
            return 1
        print(f"OK: snapshot current ({snapshot['health']['log_records']} runs)")
        return 0

    snapshot = build_snapshot()
    payload = json.dumps(snapshot, indent=1, sort_keys=False)
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(payload + "\n")
    size = SNAPSHOT_PATH.stat().st_size
    digest = hashlib.sha256(payload.encode()).hexdigest()[:12]
    print(f"wrote {SNAPSHOT_PATH}  {size/1024:.0f} KB  sha256:{digest}")
    print(f"runs={snapshot['health']['log_records']} tasks={len(snapshot['environment']['tasks'])} "
          f"lineage_versions={len(snapshot['environment']['prompts']['versions'])} "
          f"log_valid={snapshot['health']['log_valid']} "
          f"drift_free={snapshot['health']['lineage_drift_free']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
