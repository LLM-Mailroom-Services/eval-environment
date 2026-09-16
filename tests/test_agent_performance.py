"""Per-agent performance attribution — the catalog and its wiring.

Pins: the pipeline usage accumulator records the calling agent; the eval
runner captures per-case ``agent_usage`` and run-level ``performance.by_agent``;
scoring aggregates per-agent cost; the registry catalogs every evaluated node's
agents; the site snapshot reports the catalog.
"""

from __future__ import annotations

from evals.registry import AGENT_CATALOG, agents_for_node, list_tasks
from evals.scoring import summarize_agent_usage, summarize_performance


# ── pipeline accumulator (agent attribution at the source) ───────────
def test_record_usage_attributes_agent():
    from pipeline.limits import record_usage, reset_run_usage, usage_summary

    reset_run_usage()
    record_usage({"prompt_tokens": 10, "completion_tokens": 5}, "m-a", agent="sorter")
    record_usage({"input_tokens": 7, "output_tokens": 3}, "m-b", agent="judge")
    record_usage({"prompt_tokens": 4, "completion_tokens": 1})  # unattributed
    summary = usage_summary()
    assert summary["calls"] == 3 and summary["total"] == 30
    by_agent = summary["by_agent"]
    assert by_agent["sorter"] == {"calls": 1, "prompt_tokens": 10, "completion_tokens": 5, "total": 15, "models": ["m-a"]}
    assert by_agent["judge"]["total"] == 10
    assert by_agent["unattributed"]["calls"] == 1


def test_record_usage_ignores_mocks_and_bad_shapes():
    from unittest.mock import MagicMock

    from pipeline.limits import record_usage, reset_run_usage, usage_summary

    reset_run_usage()
    record_usage(None, "m")
    record_usage(MagicMock(prompt_tokens="x", completion_tokens=1), "m")  # non-int
    record_usage({"prompt_tokens": 1}, "m", agent="sorter")  # missing completion
    assert usage_summary()["calls"] == 0


def test_record_usage_dedupes_models_per_agent():
    from pipeline.limits import record_usage, reset_run_usage, usage_summary

    reset_run_usage()
    record_usage({"prompt_tokens": 1, "completion_tokens": 1}, "m-a", agent="sorter")
    record_usage({"prompt_tokens": 1, "completion_tokens": 1}, "m-a", agent="sorter")
    record_usage({"prompt_tokens": 1, "completion_tokens": 1}, "m-b", agent="sorter")
    assert usage_summary()["by_agent"]["sorter"]["models"] == ["m-a", "m-b"]


# ── scoring aggregation ──────────────────────────────────────────────
def test_summarize_agent_usage_aggregates_and_costs():
    per_case = [
        {"sorter": {"calls": 2, "prompt_tokens": 100, "completion_tokens": 50, "total": 150, "models": ["qwen/qwen3.7-flash"]}},
        {"sorter": {"calls": 1, "prompt_tokens": 80, "completion_tokens": 40, "total": 120, "models": ["qwen/qwen3.7-flash"]}},
        {"judge": {"calls": 1, "prompt_tokens": 10, "completion_tokens": 5, "total": 15, "models": ["openai/gpt-4o-mini"]}},
    ]
    out = summarize_agent_usage(per_case)
    assert set(out) == {"sorter", "judge"}
    assert out["sorter"]["calls"] == 3
    assert out["sorter"]["prompt_tokens"] == 180
    assert out["sorter"]["completion_tokens"] == 90
    assert out["sorter"]["total_tokens"] == 270
    assert out["sorter"]["models"] == ["qwen/qwen3.7-flash"]
    # priced model → float cost; unpriced model → None (never raises)
    assert isinstance(out["sorter"]["cost_usd_est"], float)
    assert out["judge"]["cost_usd_est"] is None
    # sorted by spend: sorter (270 tokens) before judge (15)
    assert list(out) == ["sorter", "judge"]


def test_summarize_agent_usage_handles_garbage():
    assert summarize_agent_usage([None, "x", 42, {}]) == {}


def test_summarize_performance_includes_by_agent():
    rows = [
        {"latency_ms": 100.0, "prompt_tokens": 10, "completion_tokens": 5,
         "agent_usage": {"sorter": {"calls": 1, "prompt_tokens": 10, "completion_tokens": 5, "total": 15, "models": ["m"]}}},
        {"latency_ms": 200.0, "prompt_tokens": 0, "completion_tokens": 0},
    ]
    summary = summarize_performance(rows)
    assert summary["by_agent"]["sorter"]["calls"] == 1
    assert summary["latency_ms_mean"] == 150.0


def test_summarize_performance_omits_empty_by_agent():
    summary = summarize_performance([{"latency_ms": 5.0, "prompt_tokens": 0, "completion_tokens": 0}])
    assert "by_agent" not in summary


# ── registry catalog ─────────────────────────────────────────────────
def test_agent_catalog_covers_every_eval_node():
    node_names = {t.node_name for t in list_tasks()}
    assert node_names - set(AGENT_CATALOG) == set(), "every evaluated node must be cataloged"


def test_agent_catalog_entries_shape():
    for node, meta in AGENT_CATALOG.items():
        assert meta["role"], f"{node} missing role"
        assert isinstance(meta["agents"], list)
        assert isinstance(meta["llm"], bool)
        if meta["llm"]:
            assert meta["agents"], f"{node} claims llm but lists no agents"


def test_agents_for_node_lookup():
    sorter_entry = agents_for_node("classify-document")
    assert "sorter" in sorter_entry["agents"]
    assert agents_for_node("unknown-node") == {}


def test_specialist_node_lists_all_four_specialists():
    agents = agents_for_node("extract-fields")["agents"]
    for name in ("contracts_specialist", "merger_agreement" if False else "corporate_records_specialist",
                 "correspondence_specialist", "insurance_claims_specialist"):
        assert name in agents


# ── runner wiring (mock path records agent usage) ────────────────────
def test_mock_run_captures_agent_usage(monkeypatch, sample_case):
    from evals import runner

    monkeypatch.setattr(
        runner, "load_cases",
        lambda *a, **k: ([sample_case], {"n_total": 1, "n_selected": 1, "config": "ground_truth", "split": "train", "revision": "deadbeef", "repo": "x"}),
    )
    result = runner.run_task("eval:classification", mock=True, n=1)
    row = result.case_rows[0]
    assert row["agent_usage"], "case row must carry per-agent usage"
    sorter = row["agent_usage"].get("sorter")
    assert sorter and sorter["calls"] >= 1
    assert sorter["models"]
    summary = result.summary
    by_agent = summary["performance"]["by_agent"]
    assert by_agent["sorter"]["calls"] >= 1
    assert by_agent["sorter"]["cost_usd_est"] is not None


# ── site snapshot reports the catalog ────────────────────────────────
def test_snapshot_agent_catalog(monkeypatch, sample_case):
    import importlib.util
    import sys

    script = __import__("pathlib").Path(__file__).resolve().parents[1] / "scripts" / "export_site_snapshot.py"
    spec = importlib.util.spec_from_file_location("export_site_snapshot_agents", script)
    snap = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("export_site_snapshot_agents", snap)
    spec.loader.exec_module(snap)

    snapshot = snap.build_snapshot()
    catalog = snapshot["environment"]["agents"]
    assert len(catalog) >= 20
    sorter_entries = [a for a in catalog if a["agent"] == "sorter"]
    assert sorter_entries and sorter_entries[0]["llm"] is True
    assert any("eval:classification" in a["evaluated_by"] for a in sorter_entries)
    archivist = [a for a in catalog if "archivist" in a["agent"] or "archive" in a["node"]]
    assert archivist and any(a["llm"] is False for a in archivist)
