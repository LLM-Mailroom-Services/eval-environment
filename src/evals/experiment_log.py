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
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 3
JSONL_ENV = "EXPERIMENT_LOG_PATH"
MD_ENV = "EXPERIMENT_LOG_MD_PATH"
RUNS_DIR_ENV = "EXPERIMENT_LOG_RUNS_DIR"
DIR_ENV = "EVALS_EXPERIMENTS_DIR"
DEFAULT_JSONL = "reports/experiment_log.jsonl"
DEFAULT_MD = "reports/experiment_log.md"
DEFAULT_RUNS_DIR = "reports/experiment_log"
# A run counts as a "wave" (the substantive, report-worthy unit) once it
# clears this many cases — smoke/debug real runs and the `--mock --n 2` CI
# gate stay well under it. Purely a markdown-layout threshold; the JSONL
# index is unaffected and still carries every run regardless of size.
WAVE_MIN_N = 10
DEFAULT_DIR = "data/experiments"
EMBED_LIMIT = 50  # inline case rows into the summary up to this many
_CASE_IO = threading.Lock()

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

# v2 additions (all optional — v1/v2 records stay valid)
V2_OPTIONAL_KEYS: tuple[str, ...] = (
    "prompt_lineage",
    "prompt_source",
    "prompt_versions",
    "pipeline_git",
    "prompts_snapshot_path",
    "judging",
)

# v3 additions (all optional — v1/v2/v3 records stay valid): task-framing +
# preflight provenance, the locked-subset artifacts, and the full scoring
# suite pointer. See schemas/experiment_record.v3.json.
V3_OPTIONAL_KEYS: tuple[str, ...] = (
    "preflight",
    "task_framing",
    "scoring_suite",
    "flush",
)

COMPARISON_KEYS: tuple[str, ...] = (
    "schema_version",
    "record_kind",
    "run_a",
    "run_b",
    "recorded_at",
    "comparison",
    "accepted",
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


def runs_dir() -> Path:
    """One rendered markdown file per run_id — never appended-to-forever."""
    return Path(os.environ.get(RUNS_DIR_ENV, DEFAULT_RUNS_DIR))


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
    """Fresh run id `<UTC stamp>-<family>-<task>`, collision-guarded.

    Two same-task launches within one second (or a resume racing a fresh
    launch) would otherwise be indistinguishable — the JSONL index and the
    run-dir keyed by run_id would silently interleave. A deterministic
    `-a<N>` suffix disambiguates while keeping the id format greppable.
    """
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    base = f"{stamp}-{family}-{task}"
    if not _run_id_exists(base):
        return base
    counter = 0
    while True:
        counter += 1
        candidate = f"{base}-a{counter}"
        if not _run_id_exists(candidate):
            return candidate


def _run_id_exists(run_id: str) -> bool:
    try:
        with open(jsonl_path(), encoding="utf-8") as fh:
            for line in fh:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue  # torn tail — not a collision witness
                if isinstance(record, dict) and record.get("run_id") == run_id:
                    return True
    except OSError:
        return False
    return False


def validate_record(record: dict[str, Any]) -> list[str]:
    """Schema v1/v2/v3 conformance checks. Returns a list of problems (empty = valid)."""
    problems: list[str] = []
    record_kind = record.get("record_kind")
    if record_kind == "comparison_result":
        check_keys = COMPARISON_KEYS
    else:
        check_keys = REQUIRED_KEYS
    for key in check_keys:
        if key not in record:
            problems.append(f"missing required key: {key}")
    if record.get("schema_version") not in (1, 2, SCHEMA_VERSION):
        problems.append(f"schema_version must be 1, 2, or {SCHEMA_VERSION}")
    if record_kind not in ("run_summary", "case", "comparison_result"):
        problems.append("record_kind must be run_summary|case|comparison_result")
    judging = record.get("judging")
    if judging is not None and record.get("schema_version", 1) < 2:
        problems.append("judging block requires schema_version >= 2")
    return problems


def cases_file_path(run_id: str) -> Path:
    """Per-run case JSONL (may exist before a run-summary is appended)."""
    return experiments_dir() / run_id / "cases.jsonl"


def _read_cases_file(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                break
    return rows


def _dedupe_cases(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the first row per case_id (checkpoint + write_run must not double-count)."""
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        cid = row.get("case_id")
        if cid:
            if cid in seen:
                continue
            seen.add(cid)
        out.append(row)
    return out


def append_case_row(run_dir: Path, run_id: str, row: dict[str, Any]) -> None:
    """Checkpoint one case row (resume-safe; survives interrupted runs)."""
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "cases.jsonl"
    payload = dict(row)
    payload.setdefault("run_id", run_id)
    payload.setdefault("record_kind", "case")
    payload.setdefault("schema_version", SCHEMA_VERSION)
    with _CASE_IO:
        if payload.get("case_id"):
            existing = {r.get("case_id") for r in _read_cases_file(path) if r.get("case_id")}
            if payload.get("case_id") in existing:
                return
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, default=str) + "\n")


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
    existing_ids = {
        row.get("case_id")
        for row in _read_cases_file(cases_file)
        if row.get("case_id")
    }
    with cases_file.open("a", encoding="utf-8") as fh:
        for row in case_rows:
            cid = row.get("case_id")
            if cid and cid in existing_ids:
                continue
            row.setdefault("run_id", run_id)
            row.setdefault("record_kind", "case")
            row.setdefault("schema_version", SCHEMA_VERSION)
            fh.write(json.dumps(row, default=str) + "\n")
            if cid:
                existing_ids.add(cid)

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
    """Per-case rows for one run (embedded when small, else from cases_ref).

    Falls back to ``data/experiments/<run_id>/cases.jsonl`` when no run-summary
    exists yet (interrupted real runs checkpoint per case).
    """
    on_disk = _dedupe_cases(_read_cases_file(cases_file_path(run_id)))
    for run in load_runs():
        if run.get("run_id") != run_id:
            continue
        embedded = run.get("cases_embedded") or []
        if embedded:
            return list(embedded)
        ref = run.get("cases_ref")
        if ref and Path(ref).exists():
            from_ref = _dedupe_cases(_read_cases_file(Path(ref)))
            return from_ref if from_ref else on_disk
        return on_disk
    return on_disk


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


def _run_link(run_id: str) -> str:
    return f"[{run_id}](experiment_log/{run_id}.md)"


def _index_table(runs: list[dict[str, Any]]) -> list[str]:
    """Like :func:`_table`, but the run_id column is a markdown link that
    must NOT go through ``_fmt``'s 60-char truncation (it would mangle the
    link syntax itself, e.g. ``[id](experiment_log/id…`` with no closing
    paren)."""
    headers = ["run_id", "family", "task", "mode", "model", "subset", "n", "key metric", "errors"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in runs:
        cells = [
            _run_link(r.get("run_id")),
            _fmt(r.get("family")),
            _fmt(r.get("task")),
            _fmt(r.get("mode")),
            _fmt(r.get("model")),
            _fmt((r.get("dataset") or {}).get("subset")),
            _fmt((r.get("metrics") or {}).get("n")),
            _fmt(_headline_metric(r)),
            _fmt((r.get("metrics") or {}).get("errors")),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def _is_wave(run: dict[str, Any]) -> bool:
    """A report-worthy run: real mode, at or above ``WAVE_MIN_N`` cases."""
    n = (run.get("metrics") or {}).get("n") or 0
    return run.get("mode") == "real" and n >= WAVE_MIN_N


def render_full_log(path: Path | None = None) -> str:
    """Title + a short, grouped experiment index — never the full per-run
    detail dump (that lives one file per run under ``runs_dir()``, see
    :func:`write_run_detail_files`). Grouping keeps the substantive N-doc
    real waves ("our reports") visually separate from mock CI-smoke and
    small real debug/exploratory runs, so the index stays scannable no
    matter how much calibration/debug history accumulates underneath it.
    """
    runs = load_runs(path)
    run_records = [r for r in runs if r.get("record_kind") in ("run_summary", None)]
    comparisons = [r for r in runs if r.get("record_kind") == "comparison_result"]

    waves = [r for r in run_records if _is_wave(r)]
    debug_real = [r for r in run_records if r.get("mode") == "real" and not _is_wave(r)]
    mock_runs = [r for r in run_records if r.get("mode") != "real"]

    lines = [
        "# mailroom-evals — experiment log",
        "",
        f"One row per run (append-only source of truth: `{jsonl_path()}`). "
        "Each run's full detail (dataset provenance, metrics, per-agent "
        "performance, case table) lives in its own file under "
        f"`{runs_dir()}/<run_id>.md` — this index never grows a per-run "
        "section inline, so it stays readable regardless of history size. "
        "OpenRouter/Braintrust N-doc waves also get a standalone, "
        "Modal-comparable report under `reports/api-comparisons/<model>/`.",
        "",
        f"## Real evaluation waves (real mode, n≥{WAVE_MIN_N} cases) — {len(waves)}",
        "",
    ]
    lines += _index_table(sorted(waves, key=lambda r: r.get("run_id") or "", reverse=True))
    lines += [
        "",
        f"## Exploratory / debug real runs (real mode, n<{WAVE_MIN_N} cases) — {len(debug_real)}",
        "",
    ]
    lines += _index_table(sorted(debug_real, key=lambda r: r.get("run_id") or "", reverse=True))
    lines += ["", f"## Mock / CI-smoke runs — {len(mock_runs)}", ""]
    lines += _index_table(sorted(mock_runs, key=lambda r: r.get("run_id") or "", reverse=True))

    if comparisons:
        lines += ["", "## A/B comparisons", ""]
        lines += _table(
            ["recorded_at", "run_a", "run_b", "accepted", "promoted_version"],
            [
                [
                    c.get("recorded_at"),
                    c.get("run_a"),
                    c.get("run_b"),
                    "ACCEPTED" if c.get("accepted") else "REJECTED",
                    c.get("promoted_version") or "—",
                ]
                for c in comparisons
            ],
        )
    return "\n".join(lines) + "\n"


def _headline_metric(run: dict[str, Any]) -> Any:
    metrics = run.get("metrics") or {}
    for key in (
        "class_accuracy", "extraction_overall_mean", "judge_agrees_accuracy",
        "decision_agrees_accuracy", "stage_agrees_accuracy", "archived_ok_accuracy",
    ):
        if key in metrics:
            return f"{key}={metrics[key]}"
    return "—"


def write_run_detail_files(path: Path | None = None, out_dir: Path | None = None) -> list[Path]:
    """One markdown file per run_id (idempotent, overwrite-in-place).

    Follow-up records (e.g. post-hoc judging appends — same ``run_id``,
    later in the JSONL) render into the SAME file, keeping only the latest,
    most-complete state; the immutable append-only history stays in the
    JSONL regardless. This is a rendered *view*, not the source of truth.
    """
    runs = load_runs(path)
    run_records = [r for r in runs if r.get("record_kind") in ("run_summary", None)]
    latest_by_id: dict[str, dict[str, Any]] = {}
    for r in run_records:
        run_id = r.get("run_id")
        if run_id:
            latest_by_id[run_id] = r  # later records in file order win

    target_dir = out_dir or runs_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for run_id, run in latest_by_id.items():
        detail_path = target_dir / f"{run_id}.md"
        detail_path.write_text(render_run_md(run), encoding="utf-8")
        written.append(detail_path)
    return written


def write_markdown(path: Path | None = None) -> Path:
    """Rebuild the markdown log from the JSONL (idempotent): a short grouped
    index at ``path`` (default ``reports/experiment_log.md``) plus one
    detail file per run under ``runs_dir()``.
    """
    target = path or md_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_full_log(), encoding="utf-8")
    write_run_detail_files()
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


def record_comparison(
    run_id_a: str,
    run_id_b: str,
    *,
    comparison: dict[str, Any],
    accepted: bool,
    promoted_version: str | None = None,
) -> dict[str, Any]:
    """Append an A/B comparison result as a new log line (append-only).

    Winning prompt versions are recorded as ``promoted_version`` so downstream
    tools can promote the champion; losing runs stay in the log for archival and
    future training.
    """
    record: dict[str, Any] = {
        "record_kind": "comparison_result",
        "schema_version": SCHEMA_VERSION,
        "run_a": run_id_a,
        "run_b": run_id_b,
        "accepted": accepted,
        "promoted_version": promoted_version,
        "comparison": comparison,
        "recorded_at": utc_now(),
    }
    with jsonl_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str) + "\n")
    return record


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
