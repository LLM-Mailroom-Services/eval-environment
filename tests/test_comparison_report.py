"""Comparison-report surface: naming schema, comparable metrics, runner hook."""

from __future__ import annotations

from pathlib import Path

from evals import comparison_report


def _summary(**overrides):
    summary = {
        "run_id": "eval-20260926-test-a1b2c3",
        "family": "eval",
        "task": "correspondence",
        "mode": "mock",
        "model": "qwen/qwen3-8b",
        "prompt_version": "correspondence_specialist_v3",
        "prompt_source": "frozen",
        "trace_backend": "none",
        "started_at": "2026-09-26T18:00:00+00:00",
        "duration_s": 61.4,
        "error": None,
        "metrics": {"n": 2, "errors": 0, "overall_score_mean": 0.1234},
        "performance": {
            "latency_ms_mean": 25000.0,
            "latency_ms_p95": 30000.0,
            "tokens_prompt_total": 4000,
            "tokens_completion_total": 300,
            "expected_cost_usd": 0.12,
            "cost_usd_total": 0.0009,
            "cost_usd_est_total": 0.0009,
            "by_agent": {
                "correspondence_specialist": {
                    "calls": 2, "prompt_tokens": 4000, "completion_tokens": 300,
                    "total_tokens": 4300, "cost_usd_est": 0.0009, "models": ["qwen/qwen3-8b"],
                }
            },
        },
        "pipeline_git": "deadbee",
        "trace_ids": ["t1"],
        "params": {
            "concurrency": 1, "sample": 20, "seed": 42, "n": 2,
            "dry_run": False, "scorer": "extraction",
            "decode_profile": "qwen3-8b",
            "decode_budget_applied": {
                "sampling_injected": False,
                "max_tokens_by_agent": {"correspondence_specialist": 4096},
                "call_timeout_s": 600,
            },
            "decode_sampling": None,
            "decode_call_timeout_s": 600,
            "thinking_recovered": 1,
        },
        "dataset": {
            "subset": "class:correspondence",
            "repo": "Lucius-Morningstar/mailroom-dataset",
            "revision": "46a4d3c2",
            "n_selected": 20,
            "subset_manifest_path": "data/experiments/x/subset_manifest.json",
        },
        "cost_cap": {"cap_usd": 1.5, "cost_usd_est": 0.0009, "status": "under_cap"},
    }
    summary.update(overrides)
    return summary


_ROWS = [
    {
        "case_id": "c1", "filename": "a.txt", "expected_subclass": "email",
        "scores": {"overall_score": 0.12, "extraction_f1": 0.0},
        "latency_ms": 25000, "tokens": {"prompt": 2000, "completion": 150, "total": 2150},
        "cost_usd": 0.0005, "agent_usage": {}, "error": None,
    },
    {
        "case_id": "c2", "filename": "b.txt", "expected_subclass": "letter",
        "prediction": {"_parse_error": True, "_raw": "<response>{}</response>"},
        "scores": {}, "latency_ms": 36000,
        "tokens": {"prompt": 2000, "completion": 150, "total": 2150},
        "cost_usd": 0.0004, "agent_usage": {}, "error": None,
    },
]


# ── naming schema ─────────────────────────────────────────────────────────────


def test_report_path_mirrors_modal_naming():
    p = comparison_report.report_path(_summary())
    # Modal twin: RUN-20-CORRESPONDENCE-AWQ-REPORT.md (sandbox reports/)
    assert p.name == "RUN-20-CORRESPONDENCE-QWEN3-8B-REPORT.md"
    assert p.parent.name == "correspondence"  # filed by task/specialist
    assert p.parent.parent.name == "qwen3-8b"  # ...within the model dir
    # Great-grandparent = reports root; conftest redirects it (EVALS_COMPARISON_REPORTS_DIR).


def test_report_path_v33_contracts_does_not_clobber_frozen_stem():
    summary = _summary()
    summary["task"] = "contracts"
    summary["prompt_version"] = "contracts_specialist_v33"
    summary["dataset"] = {"subset": "class:contract"}
    summary["params"]["decode_profile"] = "qwen3-8b"
    p = comparison_report.report_path(summary)
    assert p.name == "RUN-20-CONTRACT-V33-QWEN3-8B-REPORT.md"
    assert p.parent.name == "contracts"
    frozen = dict(summary)
    frozen["prompt_version"] = "contracts_specialist_v1"
    frozen["prompt_versions"] = {"contracts_specialist": {"key": "contracts_specialist_v1"}}
    p2 = comparison_report.report_path(frozen)
    assert p2.name == "RUN-20-CONTRACT-QWEN3-8B-REPORT.md"
    assert p2.parent.name == "contracts"


def test_report_path_falls_back_to_model_slug():
    summary = _summary()
    summary["params"] = {"sample": 50}
    summary["model"] = "ibm-granite/granite-4.2-8b"
    p = comparison_report.report_path(summary)
    # No decode profile -> slugified model id; subset class still names the stem.
    assert p.name == "RUN-50-CORRESPONDENCE-GRANITE-4.2-8B-REPORT.md"
    assert p.parent.name == "correspondence"
    assert p.parent.parent.name == "granite-4.2-8b"


def test_model_short_aliases_qwen_slug_to_decode_profile_dir():
    summary = _summary()
    summary["params"] = {"sample": 20, "n": 2}
    p = comparison_report.report_path(summary)
    assert p.parent.parent.name == "qwen3-8b"
    summary["params"] = {"sample": 20}
    summary["model"] = "qwen/qwen3-8b"
    p2 = comparison_report.report_path(summary)
    assert p2.parent.parent.name == "qwen3-8b"


def test_run_report_path_lives_under_runs_subdir():
    p = comparison_report.run_report_path(_summary())
    assert p.parent.name == "runs"
    assert p.name.endswith("-test-a1b2c3.md") or "eval" in p.name


def test_report_path_separates_by_task_within_same_model_dir():
    correspondence = comparison_report.report_path(_summary())
    insurance = comparison_report.report_path(_summary(task="insurance_claims"))
    assert correspondence.parent.parent == insurance.parent.parent  # same model dir
    assert correspondence.parent != insurance.parent  # different task subdir
    assert insurance.parent.name == "insurance_claims"


# ── comparable metric surface ─────────────────────────────────────────────────


def test_render_report_carries_modal_comparable_metrics():
    text = comparison_report.render_report(_summary(), _ROWS)
    # Modal-table analogs, each on its own row:
    for needle in (
        "wall (run duration)", "concurrency",
        "cold boot | N/A", "gpu_seconds | N/A",
        "cost expected (wave planning)", "cost actual (derived from case rows)",
        "cost estimated (roster token rates)", "cost per document (actual)",
        "latency e2e / p50 / p95 / max",
        "prompt / completion / total tokens", "cost cap",
        "Serial-vs-batched", "Decode posture",
        "Run configuration", "Runtime performance",
        "Per-agent usage", "Per-document scores",
        "docs ok / total",
        "Analyst insights & findings",
        "Strata (subclass)",
        "## Reproduce",
        "## Artifacts",
    ):
        assert needle in text, f"missing comparable metric: {needle}"
    # Per-doc rows keep the Modal columns incl. the parse_error flag.
    assert "`c1`" in text and "`c2`" in text
    assert "parse_error" in text
    # Provenance lands (pairing depends on it).
    assert "RUN-20-CORRESPONDENCE-AWQ-REPORT.md" in text


def test_cap_status_flags_over_cap():
    summary = _summary()
    summary["performance"]["cost_usd_total"] = 2.0
    summary["performance"]["cost_usd_est_total"] = 2.0
    status = comparison_report.cap_status(summary, {"cost_cap_usd": 1.5})
    assert status == {
        "cap_usd": 1.5,
        "cost_usd_est": 2.0,
        "cost_usd_total": 2.0,
        "status": "over_cap",
    }
    assert comparison_report.cap_status(summary, {}) is None


def test_render_master_report_lists_canonical_suites():
    qwen = _summary(
        run_id="20260927T033031Z-eval-correspondence",
        task="correspondence",
        mode="real",
    )
    qwen["params"] = {"sample": 20, "seed": 42, "decode_profile": "qwen3-8b"}
    qwen["metrics"] = {"n": 20, "overall_score": 0.513, "errors": 0, "scorer_errors": 0}
    granite = _summary(
        run_id="20260927T053647Z-eval-correspondence",
        task="correspondence",
        mode="real",
        model="ibm-granite/granite-4.2-8b",
    )
    granite["params"] = {"sample": 20, "seed": 42, "decode_profile": "granite-4.2-8b"}
    granite["metrics"] = {"n": 20, "overall_score": 0.4065, "errors": 0, "scorer_errors": 0}
    text = comparison_report.render_master_report(
        [qwen, granite],
        [
            {"run_id": qwen["run_id"], "canonical_report": "qwen3-8b/correspondence/x.md"},
            {"run_id": granite["run_id"], "canonical_report": "granite-4.2-8b/correspondence/y.md"},
        ],
    )
    assert "API leg — master comparison" in text
    assert "Paired comparison" in text
    assert "20260927T033031Z-eval-correspondence" in text


def test_render_model_suite_readme_links_canonical_stems():
    summary = _summary(mode="real")
    summary["params"] = {"sample": 20, "decode_profile": "qwen3-8b"}
    summary["metrics"] = {"n": 20, "overall_score": 0.5, "errors": 0, "scorer_errors": 0}
    text = comparison_report.render_model_suite_readme("qwen3-8b", [summary])
    assert "Final runs" in text
    assert "correspondence/RUN-" in text


def test_render_report_warns_when_correspondence_calls_exceed_doc_count():
    summary = _summary(mode="real")
    summary["performance"]["by_agent"]["correspondence_specialist"]["calls"] = 39
    rows = [
        {
            **_ROWS[0],
            "prediction": {"needed_chunks": 1, "chunks": 1, "llm_calls": 2},
        }
        for _ in range(20)
    ]
    text = comparison_report.render_report(summary, rows)
    assert "not** source chunking" in text
    assert "39" in text
    assert "High retry rate" in text


# ── runner hook ───────────────────────────────────────────────────────────────


def test_run_task_decode_profile_writes_report(monkeypatch, sample_case):
    from evals import runner
    from evals.runner import run_task

    monkeypatch.setattr(
        runner, "load_cases",
        lambda *a, **k: (
            [sample_case],
            {"n_total": 1, "n_selected": 1, "config": "ground_truth",
             "split": "train", "revision": "deadbeef", "repo": "x"},
        ),
    )
    result = run_task(
        "eval:contracts", mock=True, invoke_mode="agent", n=1,
        decode_profile="qwen3-8b",
    )
    summary = result.summary
    assert summary["params"]["decode_profile"] == "qwen3-8b"
    assert summary["comparison_report"]
    report = Path(summary["comparison_report"])
    assert report.exists()
    assert report.parent.name == "runs"
    canonical = report.parent.parent / "RUN-1-CONTRACT-QWEN3-8B-REPORT.md"
    assert canonical.exists()
    assert "Decode posture" in report.read_text(encoding="utf-8")
    assert summary["cost_cap"]["status"] == "under_cap"
    # No profile -> no report (pipeline-default runs don't emit it).
    result2 = run_task("eval:contracts", mock=True, invoke_mode="agent", n=1)
    assert not result2.summary.get("comparison_report")


def test_render_report_labels_resumed_wall_and_skips_serial_ratio():
    summary = _summary()
    summary["params"] = {**(summary.get("params") or {}),
                         "skipped_already_run": 99}
    text = comparison_report.render_report(summary, _ROWS)
    assert "resume segment only; 99 earlier cases" in text
    assert "Serial-vs-batched" not in text
