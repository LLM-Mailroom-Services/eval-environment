"""Centralized, append-only experiment log — one record schema for every family.

Storage (paths overridable via ``EXPERIMENT_LOG_PATH`` /
``EXPERIMENT_LOG_MD_PATH`` / ``EVALS_EXPERIMENTS_DIR``; tests redirect them):

    reports/experiment_log.jsonl          one line per RUN (summary + pointers)
    reports/experiment_log.md             rendered human-readable tables
    data/experiments/<run_id>/cases.jsonl one line per CASE (full fidelity)
    data/experiments/<run_id>/summary.json the same run-summary record

Machine-readable: strict JSONL, ``schema_version`` on every record, flat
dotted keys (pandas.json_normalize-ready), ``load_runs`` / ``load_cases``.
Human-readable: the markdown is TABLES only — never raw JSON dumps.
"""

from __future__ import annotations

import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2
JSONL_ENV = "EXPERIMENT_LOG_PATH"
MD_ENV = "EXPERIMENT_LOG_MD_PATH"
DIR_ENV = "EVALS_EXPERIMENTS_DIR"
DEFAULT_JSONL = "reports/experiment_log.jsonl"
DEFAULT_MD = "reports/experiment_log.md"
DEFAULT_DIR = "data/experiments"
EMBED_LIMIT = 50  # inline case rows into the summary up to this many

REQUIRED_KEYS: tuple[str, ...] = (
    "schema_version",
    "record_kind",
    "run_id",
    "family",
    "task",
    "mode",
    "started_at",
    "finished_at",
    "dataset",
    "metrics",
)

# v2 additions (all optional — v1 records stay valid)
V2_OPTIONAL_KEYS: tuple[str, ...] = (
    "prompt_lineage",
    "prompt_source",
    "prompt_versions",
    "pipeline_git",
    "prompts_snapshot_path",
    "judging",
)

_SUMMARY_KEYS = (
    "schema_version", "record_kind", "run_id", "family", "task", "invoke",
    "mode", "model", "prompt_version", "trace_backend", "trace_ids",
    "dataset", "git", "started_at", "finished_at", "duration_s", "params",
    "metrics", "performance", "calibration", "cases_ref", "cases_embedded", "error",
)


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def jsonl_path() -> Path:
    return Path(os.environ.get(JSONL_ENV, DEFAULT_JSONL))


def md_path() -> Path:
    return Path(os.environ.get(MD_ENV, DEFAULT_MD))


def experiments_dir() -> Path:
    return Path(os.environ.get(DIR_ENV, DEFAULT_DIR))


def git_snapshot() -> dict[str, Any]:
    """Best-effort repo state (commit + dirty flag) stamped onto every record."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10, check=False,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=10, check=False,
            ).stdout.strip()
        )
        return {"commit": commit or None, "dirty": dirty}
    except (OSError, subprocess.SubprocessError):
        return {"commit": None, "dirty": None}


def new_run_id(family: str, task: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{family}-{task}"


def validate_record(record: dict[str, Any]) -> list[str]:
    """Schema v1/v2 conformance checks. Returns a list of problems (empty = valid)."""
    problems: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in record:
            problems.append(f"missing required key: {key}")
    if record.get("schema_version") not in (1, SCHEMA_VERSION):
        problems.append(f"schema_version must be 1 or {SCHEMA_VERSION}")
    if record.get("record_kind") not in ("run_summary", "case"):
        problems.append("record_kind must be run_summary|case")
    judging = record.get("judging")
    if judging is not None and record.get("schema_version", 1) < 2:
        problems.append("judging block requires schema_version >= 2")
    return problems


def write_run(
    summary: dict[str, Any],
    case_rows: list[dict[str, Any]],
    *,
    run_dir: Path | None = None,
) -> dict[str, Any]:
    """Persist one run: per-case JSONL + summary.json + central JSONL line.

    The central line embeds case rows when n <= EMBED_LIMIT (self-contained
    small runs), else carries ``cases_ref`` pointing at the run dir.
    Returns the summary as written (with cases_ref/cases_embedded filled).
    """
    run_id = summary["run_id"]
    run_dir = run_dir or (experiments_dir() / run_id)
    run_dir.mkdir(parents=True, exist_ok=True)

    cases_file = run_dir / "cases.jsonl"
    with cases_file.open("a", encoding="utf-8") as fh:
        for row in case_rows:
            row.setdefault("run_id", run_id)
            row.setdefault("record_kind", "case")
            row.setdefault("schema_version", SCHEMA_VERSION)
            fh.write(json.dumps(row, default=str) + "\n")

    summary = dict(summary)
    summary["cases_ref"] = str(cases_file)
    summary["cases_embedded"] = case_rows if len(case_rows) <= EMBED_LIMIT else []
    summary.setdefault("record_kind", "run_summary")
    summary.setdefault("schema_version", SCHEMA_VERSION)
    summary.setdefault("git", git_snapshot())
    summary.setdefault("error", None)

    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )
    jsonl_path().parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(summary, default=str) + "\n")
    return summary


def load_runs(path: Path | None = None) -> list[dict[str, Any]]:
    """All run-summary records from the central JSONL (torn tail tolerated)."""
    path = path or jsonl_path()
    if not path.exists():
        return []
    runs: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                runs.append(json.loads(line))
            except json.JSONDecodeError:
                break  # torn tail from a crashed append — stop, never guess
    return runs


def load_cases(run_id: str) -> list[dict[str, Any]]:
    """Per-case rows for one run (embedded when small, else from cases_ref)."""
    for run in load_runs():
        if run.get("run_id") != run_id:
            continue
        embedded = run.get("cases_embedded") or []
        if embedded:
            return list(embedded)
        ref = run.get("cases_ref")
        if not ref or not Path(ref).exists():
            return []
        rows: list[dict[str, Any]] = []
        with Path(ref).open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        break
        return rows
    return []


# ── Markdown rendering (tables only, never raw JSON) ────────────────────────


def _fmt(value: Any, max_len: int = 60) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "✓" if value else "✗"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".") if value else "0.0"
    if isinstance(value, dict):
        text = " · ".join(f"{k}: {v}" for k, v in value.items())
    elif isinstance(value, (list, tuple)):
        text = ", ".join(str(v) for v in value) if value else "—"
    else:
        text = str(value)
    if len(text) > max_len:
        text = text[: max_len - 1] + "…"
    return text


def _table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(_fmt(cell) for cell in row) + " |")
    return lines


def render_run_md(summary: dict[str, Any]) -> str:
    """One run as markdown sections (metadata, data, metrics, performance)."""
    lines = [f"## {summary.get('run_id')}", ""]
    lines += _table(
        ["Key", "Value"],
        [
            ["family / task", f"{summary.get('family')} / {summary.get('task')}"],
            ["invoke / mode", f"{summary.get('invoke')} / {summary.get('mode')}"],
            ["model / prompt", f"{summary.get('model')} / {summary.get('prompt_version')}"],
            ["trace backend", summary.get("trace_backend")],
            ["git", summary.get("git")],
            ["started / finished", f"{summary.get('started_at')} → {summary.get('finished_at')}"],
            ["duration_s", summary.get("duration_s")],
            ["error", summary.get("error")],
        ],
    )
    lines += ["", "### Dataset", ""]
    lines += _table(["Key", "Value"], sorted((summary.get("dataset") or {}).items()))
    lines += ["", "### Metrics", ""]
    lines += _table(["Metric", "Value"], sorted((summary.get("metrics") or {}).items()))
    perf = summary.get("performance") or {}
    if perf:
        by_agent = perf.get("by_agent") or {}
        flat = {k: v for k, v in perf.items() if k != "by_agent"}
        lines += ["", "### Performance", ""]
        lines += _table(["Metric", "Value"], sorted(flat.items()))
        if by_agent:
            lines += ["", "### Per-agent performance", ""]
            lines += _table(
                ["agent", "calls", "prompt_tokens", "completion_tokens", "total_tokens", "cost_usd_est", "models"],
                [
                    [
                        agent,
                        slot.get("calls"),
                        slot.get("prompt_tokens"),
                        slot.get("completion_tokens"),
                        slot.get("total_tokens"),
                        slot.get("cost_usd_est"),
                        ", ".join(slot.get("models") or []) or "—",
                    ]
                    for agent, slot in by_agent.items()
                ],
            )
    cal = summary.get("calibration") or {}
    if cal:
        lines += ["", "### Calibration", ""]
        for key, value in cal.items():
            if isinstance(value, dict):
                lines += ["", f"**{key}**", ""]
                lines += _table(["Key", "Value"], sorted(value.items()))
            elif isinstance(value, list):
                lines += ["", f"**{key}**", ""]
                lines += _table(
                    ["value"], [[item] for item in value]
                )
            else:
                lines += _table([key], [[value]])
    embedded = summary.get("cases_embedded") or []
    if embedded:
        lines += ["", "### Cases", ""]
        headers = ["case_id", "scores", "latency_ms", "error"]
        rows = [
            [
                c.get("case_id"),
                {k: v for k, v in (c.get("scores") or {}).items() if not isinstance(v, dict)},
                c.get("latency_ms"),
                c.get("error"),
            ]
            for c in embedded
        ]
        lines += _table(headers, rows)
    return "\n".join(lines) + "\n"


def render_full_log(path: Path | None = None) -> str:
    """Title + experiment index over the whole history."""
    runs = load_runs(path)
    lines = ["# mailroom-evals — experiment log", ""]
    lines += _table(
        ["run_id", "family", "task", "mode", "model", "subset", "n", "key metric", "errors"],
        [
            [
                r.get("run_id"),
                r.get("family"),
                r.get("task"),
                r.get("mode"),
                r.get("model"),
                (r.get("dataset") or {}).get("subset"),
                (r.get("metrics") or {}).get("n"),
                _headline_metric(r),
                (r.get("metrics") or {}).get("errors"),
            ]
            for r in runs
        ],
    )
    lines += ["", "---", ""]
    for run in runs:
        lines.append(render_run_md(run))
        lines.append("")
    return "\n".join(lines)


def _headline_metric(run: dict[str, Any]) -> Any:
    metrics = run.get("metrics") or {}
    for key in (
        "class_accuracy", "extraction_overall_mean", "judge_agrees_accuracy",
        "decision_agrees_accuracy", "stage_agrees_accuracy", "archived_ok_accuracy",
    ):
        if key in metrics:
            return f"{key}={metrics[key]}"
    return "—"


def write_markdown(path: Path | None = None) -> Path:
    """Rebuild the markdown log from the JSONL (idempotent)."""
    target = path or md_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_full_log(), encoding="utf-8")
    return target


def record_judging(
    run_id: str,
    *,
    dimensions: list[str],
    judge_model: str | None,
    mock: bool,
    metrics: dict[str, Any],
    prompt_versions: dict[str, Any] | None = None,
    judgments_ref: str | None = None,
) -> dict[str, Any]:
    """Append a follow-up run-summary record carrying the judging block.

    History is append-only: the original run record is never edited — the
    judging outcome is a NEW line referencing the same run_id.
    """
    original = next((r for r in load_runs() if r.get("run_id") == run_id), None)
    if original is None:
        raise KeyError(f"unknown run_id {run_id!r}")
    follow_up = {
        **original,
        "schema_version": SCHEMA_VERSION,
        "record_kind": "run_summary",
        "started_at": original.get("started_at"),
        "finished_at": utc_now(),
        "cases_embedded": [],
        "judging": {
            "dimensions": dimensions,
            "judge_model": judge_model,
            "mock": mock,
            "metrics": metrics,
            "prompt_versions": prompt_versions or {},
            "judgments_ref": judgments_ref,
            "judged_at": utc_now(),
        },
    }
    with jsonl_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(follow_up, default=str) + "\n")
    return follow_up


def export_run(run_id: str, fmt: str = "csv", path: Path | None = None) -> Path | None:
    """Export one run's case rows as csv/parquet (pandas round-trip)."""
    rows = load_cases(run_id)
    if not rows:
        return None
    import pandas as pd

    frame = pd.json_normalize(rows, sep=".")
    if fmt == "parquet":
        target = path or (experiments_dir() / run_id / "cases.parquet")
        frame.to_parquet(target, index=False)
    elif fmt == "csv":
        target = path or (experiments_dir() / run_id / "cases.csv")
        frame.to_csv(target, index=False)
    else:
        raise ValueError(f"unknown export format {fmt!r} (csv|parquet)")
    return target
