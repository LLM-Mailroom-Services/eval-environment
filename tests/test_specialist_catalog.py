"""Promoted specialist prompts retain their version, provenance, and routing identity."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest

from evals.prompts import frozen_v1, lineage, mutations, registry
from evals.prompts.registry import default_keys, resolved_snapshot
from evals.registry import agents_for_node

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
PROMOTED_ROLES = (
    "contracts_specialist", "corporate_records_specialist",
    "correspondence_specialist", "insurance_claims_specialist",
)


@pytest.fixture(autouse=True)
def no_production_prompts(monkeypatch):
    # These tests verify local catalog artifacts without loading the live pipeline.
    monkeypatch.setattr(lineage, "_production", lambda: {})


@pytest.mark.parametrize("role", PROMOTED_ROLES)
def test_promoted_mutation_resolves_exact_mirror_and_parent_provenance(role):
    key, parent = f"{role}_v2", f"{role}_v1"
    version = lineage.resolve(key)
    record = mutations.registered_mutations()[key]

    assert version.key == key
    assert version.lineage == "mutation"
    assert version.version == 2
    assert version.source == parent
    assert record["parent"] == parent
    assert record["version"] == 2
    assert record["note"].strip()
    assert version.sha256 == record["sha256"]
    assert hashlib.sha256(record["text"].encode("utf-8")).hexdigest() == record["sha256"]
    assert version.text == record["text"]
    body = version.text.strip("\n")
    assert (PROMPTS_DIR / f"{key}.md").read_text() == f"# {key}\n\n{body}\n"
    assert version.text != lineage.resolve(parent).text
    assert default_keys("frozen")[role] == parent
    assert resolved_snapshot({role: key})[role] == {
        "key": key, "lineage": "mutation", "source": parent, "sha256": record["sha256"],
    }


def test_merger_frozen_prompt_manifest_mirror_and_default_agree():
    role = "merger_agreement_specialist"
    key = f"{role}_v1"
    version = lineage.resolve(key)
    manifest = json.loads((PROMPTS_DIR / "manifest.json").read_text())["versions"][key]

    assert version.lineage == "frozen"
    assert version.version == 1
    assert version.text == frozen_v1.VERSIONS[key]
    assert manifest["source_kind"] == "sandbox"
    assert manifest["source_key"] == "merger_agreement_specialist_simplified@97c0f940194f"
    assert version.source == frozen_v1.SOURCE_OF[key] == f"sandbox:{manifest['source_key']}"
    assert manifest["sha256"] == hashlib.sha256(version.text.encode("utf-8")).hexdigest()
    assert manifest["chars"] == len(version.text)
    body = version.text.strip("\n")
    assert (PROMPTS_DIR / f"{key}.md").read_text() == f"# {key}\n\n{body}\n"
    defaults = default_keys("frozen")
    assert defaults[role] == key
    assert defaults["contracts_specialist"] == "contracts_specialist_v1"
    assert version.text != lineage.resolve(defaults["contracts_specialist"]).text
    assert resolved_snapshot({role: defaults[role]})[role] == {
        "key": key, "lineage": "frozen", "source": version.source, "sha256": manifest["sha256"],
    }


@pytest.mark.parametrize("node", ["extract-fields", "document-pipeline"])
def test_merger_specialist_is_cataloged_once_alongside_cuad(node):
    entry = agents_for_node(node)
    assert entry["llm"] is True
    assert entry["agents"].count("merger_agreement_specialist") == 1
    assert entry["agents"].count("contracts_specialist") == 1


def test_frozen_activation_injects_distinct_merger_prompt_and_restores_surfaces(monkeypatch):
    llm = ModuleType("llm")
    llm.prompts = ModuleType("llm.prompts")
    original_get = Mock(return_value=("fallback", None))
    llm.prompts.get_managed_prompt = original_get
    langchain = ModuleType("langchain_agents")
    langchain.prompts = ModuleType("langchain_agents.prompts")
    original_versions = {
        "contracts_specialist_v7": "live CUAD", "merger_agreement_specialist_v4": "live MAUD",
    }
    langchain.prompts.PROMPT_VERSIONS = dict(original_versions)
    for name, module in {
        "llm": llm, "llm.prompts": llm.prompts,
        "langchain_agents": langchain, "langchain_agents.prompts": langchain.prompts,
    }.items():
        monkeypatch.setitem(sys.modules, name, module)
    monkeypatch.setattr(registry, "_state", registry.InjectionState())

    try:
        keys = registry.activate("frozen", {"contracts_specialist": "contracts_specialist_v2"})
        merger_text, prompt_object = llm.prompts.get_managed_prompt(
            "merger_agreement_specialist", "unused",
        )
        contract_text, _ = llm.prompts.get_managed_prompt("contracts_specialist", "unused")
        assert keys["merger_agreement_specialist"] == "merger_agreement_specialist_v1"
        assert merger_text == lineage.resolve("merger_agreement_specialist_v1").text
        assert contract_text == lineage.resolve("contracts_specialist_v2").text
        assert merger_text != contract_text
        assert prompt_object is None
        assert langchain.prompts.PROMPT_VERSIONS == {
            "contracts_specialist_v7": contract_text, "merger_agreement_specialist_v4": merger_text,
        }
        original_get.assert_not_called()
    finally:
        registry.deactivate()

    assert llm.prompts.get_managed_prompt is original_get
    assert langchain.prompts.PROMPT_VERSIONS == original_versions
