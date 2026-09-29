"""Long eval runs publish mailroom.beacon/v1 heartbeats (shown by `sandbox board`)."""

import hashlib
import json
from pathlib import Path

from evals.runner import run_task
from tests.test_runner import _stub_load_cases  # noqa: F401 — shared stub


def _beacons(root: Path) -> dict:
    return {p.stem: json.loads(p.read_text()) for p in root.glob("*.json")}


def test_run_task_publishes_and_finishes_a_beacon(monkeypatch, sample_case, tmp_path):
    monkeypatch.setenv("MAILROOM_BEACON_DIR", str(tmp_path))
    _stub_load_cases(monkeypatch, [sample_case])
    result = run_task("eval:classification", mock=True, n=1)
    rid = result.summary["run_id"]
    jobs = _beacons(tmp_path)
    assert len(jobs) == 1
    job = next(iter(jobs.values()))
    assert job["schema"] == "mailroom.beacon/v1" and job["package"] == "eval-environment"
    assert rid in job["job_id"] or job["job_id"] in rid.replace(":", "-")
    assert (job["done"], job["total"], job["state"]) == (1, 1, "done")
    assert "eval:classification" in job["title"]


def test_vendored_beacon_matches_its_declared_source_hash():
    src = Path(__file__).resolve().parents[1] / "src" / "evals" / "beacon.py"
    lines = src.read_text().splitlines(keepends=True)
    declared = next(l for l in lines[:3] if "sha256" in l).split("sha256 ")[1].split(")")[0]
    body = "".join(lines[3:])  # everything after the 3-line vendoring header
    assert hashlib.sha256(body.encode()).hexdigest() == declared
