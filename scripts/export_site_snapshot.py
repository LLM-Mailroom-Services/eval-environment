#!/usr/bin/env python3
"""Export the Vercel viewer snapshot (web/data/snapshot.json).

The viewer (web/) is a zero-dependency static site: this script bakes the
append-only experiment log, the task catalog, the corpus pin, the frozen
prompt lineage, and environment health into ONE tracked JSON file that
Vercel serves. Refresh discipline: run this whenever the experiment log
changes, then commit the result (the raw log stays local per .gitignore).

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
    run["headline"] = _headline(record.get("metrics") or {})
    run["n_cases"] = len(elog.load_cases(record["run_id"]))
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
    mutations = json.loads(mutations_path.read_text()) if mutations_path.exists() else []
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


def build_snapshot() -> dict:
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
        "cases": {run["run_id"]: _embed_cases(run) for run in runs},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if the committed snapshot is stale vs the log")
    args = parser.parse_args()

    snapshot = build_snapshot()
    payload = json.dumps(snapshot, indent=1, sort_keys=False)

    if args.check:
        if not SNAPSHOT_PATH.exists():
            print(f"STALE: {SNAPSHOT_PATH} missing")
            return 1
        current = SNAPSHOT_PATH.read_text()
        # Staleness = log content differs (ignore the generated_at stamp).
        current_runs = json.loads(current)["runs"] if current.strip() else []
        if json.dumps(current_runs, sort_keys=True) != json.dumps(snapshot["runs"], sort_keys=True):
            print("STALE: snapshot runs differ from the experiment log — re-run without --check")
            return 1
        print(f"OK: snapshot current ({snapshot['health']['log_records']} runs)")
        return 0

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
