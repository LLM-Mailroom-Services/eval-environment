"""Prompt lineage tests — freeze determinism, resolution, injection, mutations."""

from __future__ import annotations

import pytest

from evals.prompts import frozen_v1, mutations
from evals.prompts.lineage import all_versions, resolve, roles, verify_lineage
from evals.prompts.registry import activate, deactivate, default_keys, resolved_snapshot


def test_frozen_v1_complete():
    assert len(frozen_v1.VERSIONS) == 14
    assert frozen_v1.LINEAGE_ID == "mailroom-dataset-v1"
    assert frozen_v1.FROZEN_VERSION == 1
    for key in frozen_v1.VERSIONS:
        assert key.endswith("_v1")
        assert frozen_v1.SOURCE_OF[key]


def test_frozen_v1_production_markers():
    sorter_text = frozen_v1.VERSIONS["sorter_v1"]
    assert "PRODUCTION DOCTRINE" in sorter_text
    assert "five primary classes" in sorter_text
    assert "insurance_claim" in sorter_text
    assert "compliance_filing" not in sorter_text
    assert "compliance_specialist" not in frozen_v1.VERSIONS
    assert "INTAKE_SYSTEM_PROMPT" in frozen_v1.SOURCE_OF["intake_v1"]
    assert "CORRECT" in frozen_v1.VERSIONS["pipeline_verdict_v1"]


def test_roles_mapping():
    roles_map = roles()
    assert roles_map["sorter"] == "sorter_v1"
    assert roles_map["judge-classification"] == "judge-classification_v1"
    assert len(roles_map) == 14
    assert "compliance_specialist" not in roles_map


def test_resolve_all_layers():
    frozen = resolve("sorter_v1")
    assert frozen.lineage == "frozen" and frozen.version == 1
    prod = resolve("sorter")
    assert prod.lineage == "production"
    with pytest.raises(KeyError):
        resolve("nope_v99")


def test_verify_lineage_matches():
    result = verify_lineage()
    assert result["ok"], f"drifted: {result['drifted']}"
    assert len(result["manifest"]["versions"]) == 14


def test_injection_and_restore():
    keys = activate("frozen")
    snap = resolved_snapshot(keys)
    assert snap["sorter"]["key"] == "sorter_v1" and snap["sorter"]["lineage"] == "frozen"
    import llm.prompts as llm_prompts
    from langchain_agents import prompts as lc_prompts

    text, prompt_obj = llm_prompts.get_managed_prompt("sorter", "FALLBACK")
    assert "PRODUCTION DOCTRINE" in text and prompt_obj is None
    assert "PRODUCTION DOCTRINE" in lc_prompts.PROMPT_VERSIONS["sorter_v14"]
    deactivate()
    restored, _ = llm_prompts.get_managed_prompt("sorter", "FALLBACK")
    assert isinstance(restored, str) and len(restored) > 0
    assert "sorter_v14" in lc_prompts.PROMPT_VERSIONS


def test_default_keys_sources():
    assert default_keys("frozen")["sorter"] == "sorter_v1"
    assert default_keys("production") == {}


def test_mutation_gates_pass():
    parent = resolve("boss_v1")
    anchor = "PRODUCTION DOCTRINE (mailroom pipeline):"
    assert parent.text.count(anchor) == 1
    mutated, meta = mutations.validate_mutation(
        parent_key="boss_v1", new_key="boss_v2",
        anchor=anchor, replacement=anchor + "\n\nTEST: added by mutation test.",
        note="test",
    )
    assert meta["version"] == 2
    assert mutated.startswith(parent.text[: parent.text.index(anchor)])
    assert mutated.endswith(parent.text[parent.text.index(anchor) + len(anchor):])


def test_mutation_gates_reject():
    anchor = "PRODUCTION DOCTRINE (mailroom pipeline):"
    with pytest.raises(mutations.MutationError, match="anchor occurs"):
        mutations.validate_mutation(
            parent_key="boss_v1", new_key="boss_v2",
            anchor="never-present", replacement="x", note="n",
        )
    with pytest.raises(mutations.MutationError, match="naming"):
        mutations.validate_mutation(
            parent_key="boss_v1", new_key="boss_v9",
            anchor=anchor, replacement=anchor, note="n",
        )
    with pytest.raises(mutations.MutationError, match="already"):
        mutations.validate_mutation(
            parent_key="boss_v1", new_key="boss_v1",
            anchor=anchor, replacement=anchor, note="n",
        )


def test_all_versions_layer_priority():
    versions = all_versions()
    assert versions["sorter_v1"].lineage == "frozen"
    assert versions["sorter"].lineage == "production"
    assert "compliance_specialist_v1" not in versions