"""Prompt lineage tests — freeze determinism, resolution, injection, mutations."""

from __future__ import annotations

import pytest

from evals.prompts import frozen_v1, mutations
from evals.prompts.lineage import all_versions, resolve, roles, verify_lineage
from evals.prompts.registry import activate, deactivate, default_keys, resolved_snapshot


def test_frozen_v1_complete():
    assert len(frozen_v1.VERSIONS) == 15
    assert frozen_v1.LINEAGE_ID == "mailroom-evals-v1"
    assert frozen_v1.FROZEN_VERSION == 1
    for key in frozen_v1.VERSIONS:
        assert key.endswith("_v1")
        assert frozen_v1.SOURCE_OF[key]


def test_frozen_v1_docclass_markers():
    # docclass-derived keys carry the pure-append marker; intake does not
    assert "DOCCLASS ARM CONTEXT" in frozen_v1.VERSIONS["sorter_v1"]
    assert "Docclass variant: sorter_docclass_v0 (KANBAN-090)." in frozen_v1.VERSIONS["sorter_v1"]
    assert "DOCCLASS ARM CONTEXT" not in frozen_v1.VERSIONS["intake_v1"]
    assert "CORRECT" in frozen_v1.VERSIONS["pipeline_verdict_v1"]


def test_roles_mapping():
    roles_map = roles()
    assert roles_map["sorter"] == "sorter_v1"
    assert roles_map["judge-classification"] == "judge-classification_v1"
    assert len(roles_map) == 15


def test_resolve_all_layers():
    frozen = resolve("sorter_v1")
    assert frozen.lineage == "frozen" and frozen.version == 1
    live = resolve("sorter_docclass_v0")
    assert live.lineage == "live-docclass"
    prod = resolve("sorter")
    assert prod.lineage == "production"
    with pytest.raises(KeyError):
        resolve("nope_v99")


def test_verify_lineage_matches():
    result = verify_lineage()
    assert result["ok"], f"drifted: {result['drifted']}"
    assert len(result["manifest"]["versions"]) == 15


def test_injection_and_restore():
    keys = activate("frozen")
    snap = resolved_snapshot(keys)
    assert snap["sorter"]["key"] == "sorter_v1" and snap["sorter"]["lineage"] == "frozen"
    from langchain_agents import prompts as lc_prompts
    from pipeline import docclass_mode

    name, text = docclass_mode.managed_prompt_lookup("sorter", "FALLBACK")
    assert name == "sorter_v1" and "DOCCLASS ARM CONTEXT" in text
    assert "DOCCLASS ARM CONTEXT" in lc_prompts.PROMPT_VERSIONS["sorter_v14"]
    deactivate()
    name, _text = docclass_mode.managed_prompt_lookup("sorter", "FALLBACK")
    assert name == "sorter"
    assert "DOCCLASS ARM CONTEXT" not in lc_prompts.PROMPT_VERSIONS["sorter_v14"]


def test_default_keys_sources():
    assert default_keys("frozen")["sorter"] == "sorter_v1"
    assert default_keys("live-docclass")["sorter"] == "sorter_docclass_v0"
    assert default_keys("production") == {}


def test_mutation_gates_pass():
    parent = resolve("sorter_v1")
    anchor = "Docclass variant: sorter_docclass_v0 (KANBAN-090)."
    assert parent.text.count(anchor) == 1
    mutated, meta = mutations.validate_mutation(
        parent_key="sorter_v1", new_key="sorter_v2",
        anchor=anchor, replacement=anchor + "\n\nTEST RULE: x.",
        note="test",
    )
    assert meta["version"] == 2
    assert mutated.startswith(parent.text[: parent.text.index(anchor)])
    assert mutated.endswith(parent.text[parent.text.index(anchor) + len(anchor):])


def test_mutation_gates_reject():
    anchor = "Docclass variant: sorter_docclass_v0 (KANBAN-090)."
    with pytest.raises(mutations.MutationError, match="anchor occurs"):
        mutations.validate_mutation(
            parent_key="sorter_v1", new_key="sorter_v2",
            anchor="never-present", replacement="x", note="n",
        )
    with pytest.raises(mutations.MutationError, match="naming"):
        mutations.validate_mutation(
            parent_key="sorter_v1", new_key="sorter_v9",
            anchor=anchor, replacement=anchor, note="n",
        )
    with pytest.raises(mutations.MutationError, match="already"):
        mutations.validate_mutation(
            parent_key="sorter_v1", new_key="sorter_v1",
            anchor=anchor, replacement=anchor, note="n",
        )


def test_all_versions_layer_priority():
    versions = all_versions()
    # frozen wins over live-docclass for the same role seed
    assert versions["sorter_v1"].lineage == "frozen"
    assert versions["sorter_docclass_v0"].lineage == "live-docclass"
