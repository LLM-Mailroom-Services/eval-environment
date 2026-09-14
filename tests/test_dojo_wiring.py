"""Dojo taxonomy wiring regression tests.

The eval harness scores extraction through
``llm_dojo_scoring.field_scoring.get_field_types(doc_class)``; without the
process-start taxonomy wiring (``evals.dojo_wiring``) the field-type maps
resolve to ``{}`` and extraction scores are degraded (every field falls back
to the dojo's per-field heuristic). These tests pin the wiring contract:

- ``configure_from_taxonomy()`` wiring makes ``get_field_types("contract")``
  return a real, non-empty field-type map;
- the eval-env's own wiring is active at import time (``evals`` import);
- wiring is idempotent and fails open (no taxonomy -> defaults, no crash).
"""

from __future__ import annotations

from evals import dojo_wiring
from llm_dojo_scoring import configure_from_taxonomy, get_field_types

# A minimal taxonomy fixture: the shape configure_from_taxonomy consumes.
_FIXTURE_TAXONOMY = {
    "doc_classes": [
        {
            "key": "contract",
            "field_types": {"effective_date": "date", "parties": "entity_list:name"},
        }
    ]
}


def test_configure_from_taxonomy_wiring_resolves_contract_field_types():
    """Regression: wiring a taxonomy makes get_field_types("contract")
    return a non-empty dict with real field types (not {})."""
    configure_from_taxonomy(_FIXTURE_TAXONOMY)
    try:
        types = get_field_types("contract")
        assert isinstance(types, dict) and types, "get_field_types resolved {}"
        assert types["effective_date"] == "date"
        assert types["parties"] == "entity_list:name"
    finally:
        # Restore whatever the process-start wiring installed so later tests
        # observe the canonical corpus taxonomy, not this minimal fixture.
        configure_from_taxonomy(dojo_wiring.WIRED_TAXONOMY)


def test_eval_env_wiring_active_at_import():
    """Importing evals wires the corpus taxonomy once; contract resolves."""
    assert dojo_wiring.WIRED_TAXONOMY is not None, (
        "expected evals.dojo_wiring to wire the corpus taxonomy at import"
    )
    assert dojo_wiring.WIRED_TAXONOMY.get("doc_classes")
    types = get_field_types("contract")
    assert isinstance(types, dict) and types, "get_field_types resolved {}"
    assert "effective_date" in types and "parties" in types


def test_wiring_is_idempotent_and_fail_soft():
    """wire_taxonomy() is safe to call repeatedly and never raises."""
    before = dict(get_field_types("contract") or {})
    assert dojo_wiring.wire_taxonomy() is not None  # still wired
    assert get_field_types("contract") == before  # unchanged
    # Explicitly no taxonomy -> no-op, no crash (hermetic fallback contract).
    assert configure_from_taxonomy(None) is not None