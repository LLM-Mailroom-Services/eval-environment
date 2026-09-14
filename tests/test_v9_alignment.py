"""v9 alignment + defect-fix regression tests (2026-09-13 remediation).

Covers: gt_fields expansion (schema v9), empty-container GT handling,
archivist content-integrity verification, run_id collision guard,
no-op resume guard, scorer_error surfacing, and the GEPA failure predicate.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from evals import cases, experiment_log, scoring


# ── gt_fields expansion (schema v9) ─────────────────────────────────────────


def _v9_insurance_row() -> dict:
    return {
        "filename": "carrier:887013387879564.txt",
        "doc_text": "CLAIM DENIAL NOTICE",
        "expected": "insurance_claim",
        "expected_subclass": "carrier",
        "gt_fields": json.dumps({
            "claim_number": "887013387879564",
            "policy_number": "PN-1",
            "claim_type": "carrier",
            "adjuster": "",
            "cuad_clause_labels": "{}",
            "maud_clause_labels": "{}",
            "denial_reasons": "[]",
            "supporting_documents": '["provider NPI 5040521237"]',
        }),
    }


def test_expand_gt_fields_hoists_payload():
    row = cases._expand_gt_fields(_v9_insurance_row())
    assert row["claim_type"] == "carrier"
    assert row["supporting_documents"] == ["provider NPI 5040521237"]


def test_expand_gt_fields_never_shadows_flat_keys():
    row = _v9_insurance_row()
    row["claim_type"] = "flat-wins"
    merged = cases._expand_gt_fields(row)
    assert merged["claim_type"] == "flat-wins"


def test_expand_gt_fields_tolerates_malformed_and_empty():
    assert cases._expand_gt_fields({"gt_fields": "not json"})["gt_fields"] == "not json"
    assert cases._expand_gt_fields({"gt_fields": "{}"}) == {"gt_fields": "{}"}
    assert cases._expand_gt_fields({"gt_fields": None}) == {"gt_fields": None}
    assert cases._expand_gt_fields({"gt_fields": ["x"]}) == {"gt_fields": ["x"]}


def test_expected_fields_v9_insurance_surface():
    fields = cases._expected_fields(_v9_insurance_row())
    # real fields present, empties ('{}' / '[]' / "") absent
    assert fields.get("claim_type") == "carrier"
    assert fields.get("claim_number") == "887013387879564"
    assert "adjuster" not in fields
    assert "cuad_clause_labels" not in fields  # empty container, dropped
    assert fields.get("supporting_documents") == ["provider NPI 5040521237"]


def test_expected_fields_v9_contract_labels_flatten():
    row = {
        "expected": "contract",
        "expected_subclass": "affiliate_license",
        "cuad_clause_labels": json.dumps({"Affiliate License-Licensor": [{"start": 0, "text": "x"}]}),
        "maud_clause_labels": "{}",
    }
    fields = cases._expected_fields(row)
    # the pipeline flattener emits "Clause: evidence" items
    assert fields.get("cuad_clauses") == ["Affiliate License-Licensor: x"]
    assert not fields.get("maud_clauses")  # empty GT -> absent or empty list
    assert "cuad_clause_labels" not in fields  # raw JSON popped after flatten


# ── score_label_lists: JSON-aware, empty-GT skip ────────────────────────────


def test_score_label_lists_skips_empty_containers():
    for empty in ("{}", "[]", "", None, {}, []):
        assert scoring.score_label_lists({}, {"cuad_clause_labels": empty}, "cuad_clause_labels") == {}


def test_score_label_lists_json_object_precision_recall():
    gt = json.dumps({"Affiliate License": [{"start": 1}], "Agreement Date": [{"start": 2}]})
    pred = json.dumps({
        "Affiliate License": [{"start": 1}],
        "Extra Clause": [{"start": 9}],  # empty-valued keys count as unlabeled
    })
    out = scoring.score_label_lists(pred, {"cuad_clause_labels": gt}, "cuad_clause_labels")
    assert out["cuad_clause_labels_precision"] == 0.5
    assert out["cuad_clause_labels_recall"] == 0.5
    assert out["cuad_clause_labels_f1"] == 0.5


def test_score_label_lists_empty_valued_dict_keys_are_unlabeled():
    gt = json.dumps({"Affiliate License": [{"start": 1}]})
    pred = json.dumps({"Affiliate License": [{"start": 1}], "Extra Clause": []})
    out = scoring.score_label_lists(pred, {"cuad_clause_labels": gt}, "cuad_clause_labels")
    assert out["cuad_clause_labels_f1"] == 1.0


def test_score_label_lists_legacy_comma_strings():
    out = scoring.score_label_lists({"k": ["a", "c"]}, {"k": "a, b"}, "k")
    assert out["k_f1"] == 0.5


# ── summarize_scores: scorer_errors surface ─────────────────────────────────


def test_summarize_scores_counts_scorer_errors():
    rows = [
        {"scores": {"class_correct": 1}},
        {"scores": {"class_correct": 0, "scorer_error": True}},
        {"scores": {"scorer_error": True}},
    ]
    out = scoring.summarize_scores(rows)
    assert out["scorer_errors"] == 2
    assert out["errors"] == 0


def test_summarize_scores_no_scorer_errors_is_zero():
    out = scoring.summarize_scores([{"scores": {"class_correct": 1}}])
    assert out["scorer_errors"] == 0


# ── run_id collision guard ──────────────────────────────────────────────────


class _FixedDatetime(datetime):
    @classmethod
    def now(cls, tz=None):  # noqa: ARG003
        return datetime(2026, 9, 13, 12, 0, 0, tzinfo=UTC)


def test_new_run_id_suffixes_on_collision(monkeypatch, tmp_path):
    log = tmp_path / "log.jsonl"
    monkeypatch.setenv("EXPERIMENT_LOG_PATH", str(log))
    monkeypatch.setattr(experiment_log, "datetime", _FixedDatetime)
    base = experiment_log.new_run_id("eval", "x")
    assert base == "20260913T120000Z-eval-x"
    log.write_text(json.dumps({"run_id": base}) + "\n", encoding="utf-8")
    second = experiment_log.new_run_id("eval", "x")
    assert second == f"{base}-a1"
    log.write_text(
        json.dumps({"run_id": base}) + "\n" + json.dumps({"run_id": second}) + "\n",
        encoding="utf-8",
    )
    assert experiment_log.new_run_id("eval", "x") == f"{base}-a2"


def test_run_id_exists_tolerates_torn_tail(monkeypatch, tmp_path):
    log = tmp_path / "log.jsonl"
    log.write_text('{"run_id": "known-id"}\n{"run_id": "tor', encoding="utf-8")
    monkeypatch.setenv("EXPERIMENT_LOG_PATH", str(log))
    assert experiment_log._run_id_exists("known-id") is True
    assert experiment_log._run_id_exists("other") is False


# ── no-op resume guard ──────────────────────────────────────────────────────


def test_noop_resume_returns_without_logging(monkeypatch, sample_case):
    from evals import runner

    monkeypatch.setattr(
        runner,
        "load_cases",
        lambda *a, **k: ([sample_case], {"n_total": 1, "n_selected": 1, "config": "ground_truth", "split": "train", "revision": "deadbeef", "repo": "x"}),
    )
    monkeypatch.setattr(
        experiment_log, "load_cases", lambda run_id: [{"case_id": sample_case["id"]}]
    )
    result = runner.run_task(
        "eval:classification", mock=True, n=1, resume_run_id="20260913T000000Z-eval-classification"
    )
    assert result.summary["noop_resume"] is True
    assert result.summary["skipped_already_run"] == 1
    assert experiment_log.load_runs() == []  # no fabricated n=0 summary row


# ── archivist verification (flattened name + content integrity) ─────────────


def test_archivist_sha256_ok_on_flattened_filenames(monkeypatch, fixture_case):
    """Enron-style pathed filename + trailing dot: archive verify must pass."""
    from evals import runner

    fixture_case["filename"] = "bailey-s/deleted_items/288."
    monkeypatch.setattr(
        runner,
        "load_cases",
        lambda *a, **k: ([fixture_case], {"n_total": 1, "n_selected": 1, "config": "fixtures", "split": "train", "revision": "deadbeef", "repo": "x"}),
    )
    result = runner.run_task("eval:archivist", mock=True, n=1)
    row = result.case_rows[0]
    assert row["error"] is None
    assert row["scores"]["archived_ok"] == 1
    assert row["scores"]["sha256_ok"] == 1  # was silently 0 before the fix
    assert row["scores"]["audit_ok"] == 1
    assert row["scores"]["stage_ok"] == 1


# ── family corpora fail loudly on empty loads ───────────────────────────────


def test_family_corpus_empty_load_raises(monkeypatch):
    def _boom(*a, **k):
        raise RuntimeError("hub parquet conversion failed")

    monkeypatch.setattr(cases, "load_config_frame", _boom)
    monkeypatch.setattr(
        cases, "resolve_corpus", lambda slug: {"id": "Lucius-Morningstar/mailroom-cuad-contracts-full"}
    )
    with pytest.raises(RuntimeError, match="yielded 0 cases"):
        cases.load_cases("cuad")


# ── GEPA failure manifest predicate ─────────────────────────────────────────


def test_export_failures_predicate(tmp_path, monkeypatch):
    import importlib.util
    import sys

    _script = Path(__file__).resolve().parents[1] / "scripts" / "score_run.py"
    _spec = importlib.util.spec_from_file_location("score_run_test", _script)
    score_run = importlib.util.module_from_spec(_spec)
    sys.modules.setdefault("score_run_test", score_run)
    _spec.loader.exec_module(score_run)

    rows = [
        {"case_id": "ok", "scores": {"overall_score": 0.95}},
        {"case_id": "low", "scores": {"overall_score": 0.4}},
        {"case_id": "err", "error": "ValueError: boom", "scores": {}},
        {"case_id": "scorer", "scores": {"scorer_error": True}},
        {"case_id": "gate", "scores": {"class_correct": 0}},
    ]
    monkeypatch.setattr(experiment_log, "load_cases", lambda run_id: rows)
    out = score_run.export_failures("r1", tmp_path / "f.jsonl")
    ids = {json.loads(line)["case_id"] for line in out.read_text().splitlines()}
    assert ids == {"low", "err", "scorer", "gate"}
