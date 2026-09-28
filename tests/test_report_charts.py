"""Per-document-type report charts rendered from the viewer snapshot."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from evals.viz import report_charts as rc

ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"


def _run(run_id, task, model, n, started, error=None, **metrics):
    return {"run_id": run_id, "task": task, "model": model, "mode": "real", "error": error, "prompt_lineage": "frozen",
            "started_at": started, "metrics": {"n": n, **metrics},
            "performance": {"cost_usd_total": 0.01 * n}}


def _ext_cases(n, base):
    return [{"expected_subclass": ["a", "b"][i % 2], "latency_ms": 1000 * (1 + i),
             "scores": {"overall_score": min(1.0, base + 0.01 * i)}, "prediction": {}} for i in range(n)]


def _cls_cases(n, collapse=False):
    out = []
    for i in range(n):
        exp = rc.CLASSES[i % 5]
        pred = exp if i % 10 else "unknown"
        exp_sub, pred_sub = f"s{i % 3}", ("s0" if collapse else f"s{i % 3}")
        out.append({"scores": {"expected_doc_class": exp, "predicted_doc_class": pred, "class_correct": int(pred == exp),
                               "expected_subclass": exp_sub, "predicted_subclass": pred_sub,
                               "subclass_correct": int(exp_sub == pred_sub)},
                    "prediction": {"confidence": 0.95 if i % 2 else 0.99}})
    return out


def _snapshot():
    runs = [
        _run("r1", "contracts", "qwen/qwen3-8b", 20, "2026-09-26T01:00:00", overall_score=0.3),
        _run("r2", "contracts", "qwen/qwen3-8b", 20, "2026-09-27T01:00:00", overall_score=0.6),  # latest wins
        _run("r3", "contracts", "deepseek/deepseek-v4.1-flash", 5, "2026-09-27T02:00:00", overall_score=0.9),  # n < 20
        _run("r4", "contracts", "ibm-granite/granite-4.2-8b", 20, "2026-09-27T03:00:00", error="boom"),
        {**_run("r5", "contracts", "qwen/qwen3-8b", 20, "2026-09-28T01:00:00", overall_score=0.9),
         "prompt_lineage": "mutation"},  # GEPA candidate prompt: not the baseline
        _run("c1", "classification", "deepseek/deepseek-v4.1-flash", 1, "2026-09-27T04:00:00"),  # resume segment
        _run("c1", "classification", "deepseek/deepseek-v4.1-flash", 100, "2026-09-27T04:00:00"),
        _run("c2", "classification", "qwen/qwen3-8b", 20, "2026-09-27T05:00:00"),  # below the sorter floor
        _run("c3", "classification", "ibm-granite/granite-4.2-8b", 100, "2026-09-27T06:00:00"),
    ]
    cases = {"r1": _ext_cases(20, 0.2), "r2": _ext_cases(20, 0.5), "r3": _ext_cases(5, 0.9), "r4": [], "r5": _ext_cases(20, 0.9),
             "c1": _cls_cases(100), "c2": _cls_cases(20), "c3": _cls_cases(100, collapse=True)}
    return {"generated_at": "2026-09-28T00:00:00+00:00", "runs": runs, "cases": cases}


def test_latest_runs_selection():
    got = {k: r["run_id"] for k, r in rc.latest_runs(_snapshot()).items()}
    assert got == {("contracts", "qwen/qwen3-8b"): "r2",
                   ("classification", "deepseek/deepseek-v4.1-flash"): "c1",
                   ("classification", "ibm-granite/granite-4.2-8b"): "c3"}
    runs = rc.latest_runs(_snapshot())
    assert runs[("classification", "deepseek/deepseek-v4.1-flash")]["metrics"]["n"] == 100


def test_classification_stats_confusion_and_collapse():
    st = rc.classification_stats(_cls_cases(100, collapse=True))
    assert st["confusion"]["correspondence"] == {"correspondence": 10, "unknown": 10}
    assert st["confusion"]["contract"] == {"contract": 20}
    s = st["subclass"]["contract"]
    assert s["top_pred"] == ("s0", s["n"])  # every prediction on one subclass


def test_reliability_bins_and_ece():
    rel = rc.reliability(_cls_cases(100))
    assert rel["n"] == 100 and rel["n_binned"] == 100
    assert [round(b["conf"], 2) for b in rel["bins"]] == [0.95, 0.99]
    acc = sum(b["n"] * b["acc"] for b in rel["bins"]) / 100
    assert acc == pytest.approx(0.9)
    assert rel["ece"] == pytest.approx(sum(b["n"] * abs(b["acc"] - b["conf"]) for b in rel["bins"]) / 100)


def test_render_valid_deterministic_svgs():
    a, b = rc.render(_snapshot()), rc.render(json.loads(json.dumps(_snapshot())))
    assert a == b
    assert {"extraction_score_by_type.svg", "classification_confusion_deepseek-v4.1-flash.svg",
            "classification_calibration.svg", "classification_collapse.svg"} <= set(a)
    assert "classification_confusion_qwen3-8b.svg" not in a  # n = 20 sorter run excluded
    for _, svg in a.values():
        assert ET.fromstring(svg).tag == f"{SVG}svg"


def test_committed_charts_match_snapshot():
    """web/data/charts and reports/charts/README.md are a fresh render of the committed snapshot."""
    snap = json.loads((ROOT / "web" / "data" / "snapshot.json").read_text())
    files = rc.outputs(snap, ROOT / "web" / "data" / "charts", ROOT / "reports" / "charts" / "README.md")
    for path, body in files.items():
        assert path.read_text() == body, f"{path.relative_to(ROOT)} is stale: run scripts/render_report_charts.py"
    md = (ROOT / "reports" / "charts" / "README.md").read_text()
    assert "](../../web/data/charts/extraction_score_by_type.svg)" in md
