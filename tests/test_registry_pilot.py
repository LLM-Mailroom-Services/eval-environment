"""registry.py + pilot.py — task catalog integrity and pilot slice shape."""

from __future__ import annotations

import pytest

from evals.pilot import PILOT_FIXTURE_PINCH, PILOT_PER_STRATUM, pilot_cases, pilot_overrides
from evals.registry import TaskSpec, get_task, list_tasks


def test_registry_complete():
    tasks = list_tasks()
    assert len(tasks) == 31
    families = {t.family for t in tasks}
    assert families == {"eval", "pilot", "calibration"}
    ids = [t.task_id for t in tasks]
    assert len(ids) == len(set(ids)), "duplicate task_id in registry"


def test_task_ids_well_formed():
    for t in list_tasks():
        assert t.task_id == f"{t.family}:{t.name}"
        assert t.node_name, f"{t.task_id} missing node_name"
        assert t.description, f"{t.task_id} missing description"


def test_get_task_roundtrip_and_unknown():
    spec = get_task("eval:classification")
    assert spec.family == "eval" and spec.name == "classification"
    with pytest.raises(KeyError):
        get_task("eval:does_not_exist")
    with pytest.raises(KeyError):
        get_task("bogus:classification")


def test_taskspec_task_id_property():
    spec = TaskSpec("demo", "eval", "demo-node")
    assert spec.task_id == "eval:demo"


def test_pilot_cases_stratified(sample_case, monkeypatch):
    """Pilot selection: one case per doc-class stratum (per PILOT_PER_STRATUM;
    subclasses share the class stratum), provenance marked pilot."""
    from evals import pilot as pilot_mod

    strata = []
    for cls, sub in [("contract", "msa"), ("contract", "nda"), ("correspondence", "email")]:
        case = dict(sample_case)
        case["id"] = f"case-{cls}-{sub}"
        case["expected_doc_class"] = cls
        case["expected_subclass"] = sub
        strata.append(case)
    monkeypatch.setattr(pilot_mod, "load_cases", lambda subset, **kw: (strata, {"n_total": 3}) if subset == "pilot" else ([], {"n_total": 0}))

    cases, prov = pilot_cases("eval:classification")
    assert {c["expected_doc_class"] for c in cases} == {"contract", "correspondence"}
    assert len(cases) == 2  # PILOT_PER_STRATUM per class (subclass is not a split key)
    assert prov["pilot"] is True
    assert prov["per_stratum"] == PILOT_PER_STRATUM
    assert prov["n_selected"] == len(cases)


def test_pilot_dedupes_by_case_id(sample_case, monkeypatch):
    from evals import pilot as pilot_mod

    dupes = [dict(sample_case, id="same-id") for _ in range(3)]
    monkeypatch.setattr(pilot_mod, "load_cases", lambda subset, **kw: (dupes, {"n_total": 3}))
    cases, prov = pilot_cases("eval:classification")
    assert len(cases) == 1
    assert prov["n_selected"] == 1


def test_pilot_fixture_pinch_for_decision_scorers(sample_case, monkeypatch):
    """judge/arbiter/boss/archivist scorers get a fixtures pinch; classification doesn't."""
    from evals import pilot as pilot_mod

    fixture = dict(sample_case, id="fixture-1", fixture_kind="edge")
    calls = []

    def fake_load(subset, **kw):
        calls.append(subset)
        if subset == "pilot":
            return ([dict(sample_case, id="p-1", expected_doc_class="contract")], {"n_total": 1})
        return ([fixture], {"n_total": 1})

    monkeypatch.setattr(pilot_mod, "load_cases", fake_load)
    cases, prov = pilot_cases("eval:judge_arbiter")
    assert "fixtures" in calls
    assert prov["fixture_pinch"] == PILOT_FIXTURE_PINCH
    assert any(c.get("fixture_kind") for c in cases)

    calls.clear()
    _cases, prov2 = pilot_cases("eval:classification")
    assert "fixtures" not in calls
    assert prov2["fixture_pinch"] == 0


def test_pilot_overrides_neutralizes_subset():
    spec = get_task("eval:classification")
    assert pilot_overrides(spec) == {"subset": None}
