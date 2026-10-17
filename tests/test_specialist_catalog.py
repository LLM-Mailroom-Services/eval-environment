"""Regression checks for the three specialist v2 catalog promotions."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from evals.prompts import frozen_v1, lineage, mutations

REPO_ROOT = Path(__file__).resolve().parents[1]
SPECIALISTS = ("contracts_specialist", "corporate_records_specialist", "correspondence_specialist")


@pytest.mark.parametrize("role", SPECIALISTS)
def test_specialist_v2_catalog_lineage_and_mirror(role, monkeypatch):
    monkeypatch.setattr(lineage, "_production", dict)
    rows = json.loads(mutations.MUTATIONS_PATH.read_text())["mutations"]
    key = f"{role}_v2"
    matches = [row for row in rows if row["key"] == key]
    assert len(matches) == 1
    row = matches[0]
    version = lineage.resolve(key)

    assert row["parent"] == f"{role}_v1" and row["version"] == 2
    assert row["note"] and row["created_at"]
    assert row["sha256"] == hashlib.sha256(row["text"].encode("utf-8")).hexdigest()
    assert version.lineage == "mutation" and version.version == 2
    assert version.source == row["parent"]
    assert version.text == row["text"] and version.sha256 == row["sha256"]
    assert lineage.resolve(row["parent"]).text == frozen_v1.VERSIONS[row["parent"]]
    assert lineage.roles()[role] == row["parent"]
    assert (REPO_ROOT / "prompts" / f"{key}.md").read_text(encoding="utf-8") == (
        f"# {key}\n\n" + row["text"].strip("\n") + "\n"
    )


@pytest.mark.parametrize(
    ("role", "fields"),
    [
        ("contracts_specialist", {
            "reasoning", "document_name", "parties", "effective_date", "term_length",
            "governing_law", "contract_value", "renewal_terms", "cuad_family",
            "merger_consideration", "cuad_clauses", "maud_clauses", "confidence",
        }),
        ("corporate_records_specialist", {
            "entity_name", "record_type", "effective_date", "signatories", "jurisdiction",
            "filing_number", "intent", "subject_matter", "keywords",
        }),
        ("correspondence_specialist", {
            "sender", "recipient", "additional_recipients", "communication_type",
            "communication_date", "demand_amount", "action_items", "urgency", "intent",
            "subject_matter", "keywords", "confidence",
        }),
    ],
)
def test_specialist_v2_declares_only_registered_output_fields(role, fields):
    text = mutations.registered_mutations()[f"{role}_v2"]["text"]
    declarations = text.split("fields (emit all):", 1)[1]
    declared = re.findall(r"^- (\w+) \(", declarations, flags=re.MULTILINE)
    assert set(declared) == fields
    assert len(declared) == len(fields), "Each output field must be declared exactly once"
