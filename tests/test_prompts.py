"""Prompt lineage tests — freeze determinism, resolution, injection, mutations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from evals.prompts import frozen_v1, mutations
from evals.prompts.lineage import all_versions, resolve, roles, verify_lineage
from evals.prompts.mirror_md import prompt_mirror_markdown, strip_mirror_heading
from evals.prompts.registry import activate, deactivate, default_keys, resolved_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((REPO_ROOT / "prompts" / "manifest.json").read_text())

# The five concise sandbox extraction specialists frozen as v1. Their sha256
# values are pinned here: adding a new role must never rewrite these bytes
# (PR #17 silently replaced the merger specialist; this guard catches a repeat).
SANDBOX_SPECIALIST_KEYS = (
    "contracts_specialist_v1",
    "corporate_records_specialist_v1",
    "correspondence_specialist_v1",
    "insurance_claims_specialist_v1",
    "merger_agreement_specialist_v1",
)
PRE_EXISTING_SANDBOX_SHA256 = {
    "contracts_specialist_v1": "d91de3967cc3b12cbd222cc5a4ae167b39578125abc83be7422498dc5024fd24",
    "corporate_records_specialist_v1": "484e64dd847b7bb35afebca74edc1fb6c381f0f7d5e9367ad8673bec0b8af45c",
    "correspondence_specialist_v1": "eab63b5afd29906b1ad3aca2d7698bf5c15d4b7f4ce9ade3b744be535d18d4f3",
    "insurance_claims_specialist_v1": "6c2776bcbe00091200aecbcfd21c99f197398d929143dd0c7c722811fa100034",
    "merger_agreement_specialist_v1": "003232584d6890054d956398135f439b86692a1123683f58914c0393b5e1a00b",
}


def test_frozen_v1_complete():
    assert len(frozen_v1.VERSIONS) == 15
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
    contracts = frozen_v1.VERSIONS["contracts_specialist_v1"]
    assert "You are the contracts specialist" in contracts
    assert "COMPLETENESS IS THE PRIORITY" not in contracts
    assert frozen_v1.SOURCE_OF["contracts_specialist_v1"].startswith("sandbox:")
    for role in (
        "corporate_records_specialist_v1",
        "correspondence_specialist_v1",
        "insurance_claims_specialist_v1",
        "merger_agreement_specialist_v1",
    ):
        assert frozen_v1.SOURCE_OF[role].startswith("sandbox:")
    merger = frozen_v1.VERSIONS["merger_agreement_specialist_v1"]
    assert "You are the merger-agreement specialist" in merger
    for key in (
        "contracts_specialist_v1",
        "corporate_records_specialist_v1",
        "correspondence_specialist_v1",
        "insurance_claims_specialist_v1",
        "merger_agreement_specialist_v1",
    ):
        assert "sorter handed you" in frozen_v1.VERSIONS[key]


def test_merger_agreement_specialist_frozen_key():
    """The MAUD specialist has its own frozen key (Refs #8; lost in PR #17)."""
    key = "merger_agreement_specialist_v1"
    assert key in frozen_v1.VERSIONS
    text = frozen_v1.VERSIONS[key]
    assert frozen_v1.SOURCE_OF[key] == (
        "sandbox:merger_agreement_specialist_simplified@303e7f0bb05d"
    )
    assert "You are the merger-agreement specialist" in text
    assert "merger_consideration" in text and "maud_clauses" in text
    # the CUAD prompt forbids MAUD output, so the two roles are not swappable
    contracts = frozen_v1.VERSIONS["contracts_specialist_v1"]
    assert "maud_clauses is [] on every CUAD commercial contract" in contracts
    assert text != contracts

    manifest = json.loads((Path(__file__).resolve().parents[1] / "prompts" / "manifest.json").read_text())
    sandbox_keys = {
        "contracts_specialist_v1",
        "corporate_records_specialist_v1",
        "correspondence_specialist_v1",
        "insurance_claims_specialist_v1",
        "merger_agreement_specialist_v1",
    }
    for key in sandbox_keys:
        assert manifest["versions"][key]["source_kind"] == "sandbox"
        assert "@303e7f0bb05d" in manifest["versions"][key]["source_key"]


def test_sandbox_specialist_keys_unchanged():
    """Guard against re-regressing: the sandbox v1 bytes are immutable."""
    for key, expected in PRE_EXISTING_SANDBOX_SHA256.items():
        assert hashlib.sha256(frozen_v1.VERSIONS[key].encode("utf-8")).hexdigest() == expected, key
        assert MANIFEST["versions"][key]["sha256"] == expected, key
        assert MANIFEST["versions"][key]["source_kind"] == "sandbox"
        assert "@303e7f0bb05d" in MANIFEST["versions"][key]["source_key"]


def test_frozen_mirror_matches_frozen_text():
    """prompts/<key>.md is the generated mirror of the frozen text, never a hand edit."""
    for key, text in frozen_v1.VERSIONS.items():
        mirror = REPO_ROOT / "prompts" / f"{key}.md"
        assert mirror.exists(), f"missing mirror for {key}"
        body = strip_mirror_heading(key, mirror.read_text(encoding="utf-8"))
        assert body == text.strip("\n"), key
        assert mirror.read_text(encoding="utf-8") == prompt_mirror_markdown(key, text), key


def test_frozen_manifest_matches_frozen_text():
    for key, text in frozen_v1.VERSIONS.items():
        meta = MANIFEST["versions"][key]
        assert meta["sha256"] == hashlib.sha256(text.encode("utf-8")).hexdigest(), key
        assert meta["chars"] == len(text), key
    assert set(MANIFEST["versions"]) == set(frozen_v1.VERSIONS)


def test_frozen_concise_specialists_manifest():
    manifest = MANIFEST
    for key in SANDBOX_SPECIALIST_KEYS:
        assert manifest["versions"][key]["source_kind"] == "sandbox"
        assert "@303e7f0bb05d" in manifest["versions"][key]["source_key"]


def test_roles_mapping():
    roles_map = roles()
    assert roles_map["sorter"] == "sorter_v1"
    assert roles_map["judge-classification"] == "judge-classification_v1"
    assert roles_map["merger_agreement_specialist"] == "merger_agreement_specialist_v1"
    assert len(roles_map) == 15
    assert "compliance_specialist" not in roles_map


def test_resolve_all_layers():
    frozen = resolve("sorter_v1")
    assert frozen.lineage == "frozen" and frozen.version == 1
    prod = resolve("sorter")
    assert prod.lineage == "production"
    with pytest.raises(KeyError):
        resolve("nope_v99")


def test_resolve_merger_agreement_specialist():
    version = resolve("merger_agreement_specialist_v1")
    assert version.lineage == "frozen" and version.version == 1
    assert version.text is frozen_v1.VERSIONS["merger_agreement_specialist_v1"]
    assert version.sha256 == PRE_EXISTING_SANDBOX_SHA256["merger_agreement_specialist_v1"]
    assert resolve("merger_agreement_specialist_v1").text != resolve("contracts_specialist_v1").text


def test_verify_lineage_matches():
    result = verify_lineage()
    assert result["ok"], f"drifted: {result['drifted']}"
    assert len(result["manifest"]["versions"]) == 15


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
    assert default_keys("frozen")["contracts_specialist"] == "contracts_specialist_v1"
    assert default_keys("frozen")["merger_agreement_specialist"] == "merger_agreement_specialist_v1"
    assert default_keys("archived")["contracts_specialist"] == "contracts_specialist_v0"
    assert default_keys("archived")["sorter"] == "sorter_v1"
    assert default_keys("production") == {}


def test_injection_reaches_the_merger_agent():
    """The frozen MAUD stem must reach agents.merger_agreement_specialist.

    Regression guard for the P0 break: with no merger key in the frozen lineage
    the agent silently kept the production template, so the Granite/Qwen
    comparison measured a stem nobody pinned.
    """
    keys = activate("frozen")
    try:
        import llm.prompts as llm_prompts

        text, prompt_obj = llm_prompts.get_managed_prompt("merger_agreement_specialist", "FALLBACK")
        assert text == frozen_v1.VERSIONS["merger_agreement_specialist_v1"]
        assert text != "FALLBACK" and prompt_obj is None
        snap = resolved_snapshot(keys)
        assert snap["merger_agreement_specialist"]["lineage"] == "frozen"
        assert snap["merger_agreement_specialist"]["sha256"] == PRE_EXISTING_SANDBOX_SHA256[
            "merger_agreement_specialist_v1"
        ]
        # the CUAD agent keeps its own distinct stem
        cuad, _ = llm_prompts.get_managed_prompt("contracts_specialist", "FALLBACK")
        assert cuad == frozen_v1.VERSIONS["contracts_specialist_v1"]
        assert cuad != text
    finally:
        deactivate()


def test_archived_production_specialists():
    from evals.prompts import archived_production

    for role in (
        "contracts_specialist",
        "corporate_records_specialist",
        "correspondence_specialist",
        "insurance_claims_specialist",
    ):
        archived = resolve(f"{role}_v0")
        frozen = resolve(f"{role}_v1")
        assert archived.lineage == "archived" and archived.version == 0
        assert frozen.lineage == "frozen" and frozen.version == 1
        assert archived.text != frozen.text
        assert archived_production.SOURCE_OF[f"{role}_v0"].startswith("production:")
    assert "COMPLETENESS IS THE PRIORITY" not in frozen_v1.VERSIONS["contracts_specialist_v1"]
    assert "COMPLETENESS IS THE PRIORITY" in resolve("contracts_specialist_v0").text
    assert len(resolve("contracts_specialist_v0").text) > len(frozen_v1.VERSIONS["contracts_specialist_v1"])


def test_contracts_specialist_v33_modal_parity():
    v33 = resolve("contracts_specialist_v33")
    frozen = resolve("contracts_specialist_v1")
    assert v33.lineage == "archived"
    assert v33.source == "sandbox:contracts_specialist_v33@303e7f0bb05d"
    assert v33.text != frozen.text
    assert len(v33.text) > len(frozen.text)
    from evals.prompts.registry import default_keys

    assert default_keys("archived")["contracts_specialist"] == "contracts_specialist_v0"


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


def test_mutation_gate_length_budget():
    parent = resolve("boss_v1")
    anchor = "PRODUCTION DOCTRINE (mailroom pipeline):"
    assert parent.text.count(anchor) == 1
    bloated = anchor + (" X" * 200)
    with pytest.raises(mutations.MutationError, match="net prompt growth"):
        mutations.validate_mutation(
            parent_key="boss_v1",
            new_key="boss_v2",
            anchor=anchor,
            replacement=bloated,
            note="test length gate",
        )


def test_all_versions_layer_priority():
    versions = all_versions()
    assert versions["sorter_v1"].lineage == "frozen"
    assert versions["sorter"].lineage == "production"
    assert "compliance_specialist_v1" not in versions