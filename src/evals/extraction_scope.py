"""Scope extraction GT/predictions to the live class schema before scoring.

Refs LLM-Mailroom-Services/eval-environment#9; aligned with local-mailroom-sandbox
``extraction_scope`` (merge ``97c0f940``).

Hub ``ground_truth`` / ``gt_fields`` often carries a **union** of specialist
keys. Empty insurance-claim placeholders on a correspondence row (and the
symmetric case) must not count as extraction misses.

Vendor ``llm-dojo-scoring`` already skips ``None`` / ``""`` but **does not**
skip empty lists. An expected ``denial_reasons: []`` with a missing
prediction scores 0.0 and pulls ``overall_score`` down. This module drops those
empties *and* keys that do not belong to the scored document class before
``observability.suite_scoring.score_with_suite`` runs.

We do **not** edit ``llm-dojo-scoring``. The eval harness seam is
``evals.scoring.score_extraction`` (and ``cases._expected_fields`` for the
logged ``expected_fields`` surface).
"""

from __future__ import annotations

from typing import Any, Mapping

# Live extraction keys that the class suite scores. Keep in lockstep with
# vendored ``schemas.documents`` / ``langchain_agents.specialist_agents`` for
# the five live classes — **not** with dojo ``DEFAULT_FIELD_TYPES`` for
# merger (that map still lists CUAD leftovers: term_length, cuad_family,
# cuad_clauses). Trace-only keys (``reasoning``, ``confidence``) are never
# scoring events.
LIVE_SCHEMA_FIELDS: dict[str, frozenset[str]] = {
    "contract": frozenset(
        {
            "document_name",
            "parties",
            "effective_date",
            "term_length",
            "governing_law",
            "contract_value",
            "renewal_terms",
            "cuad_family",
            "merger_consideration",
            "cuad_clauses",
            "maud_clauses",
        }
    ),
    "merger_agreement": frozenset(
        {
            "document_name",
            "parties",
            "effective_date",
            "effective_time",
            "governing_law",
            "merger_consideration",
            "maud_clauses",
            "intent",
            "subject_matter",
            "keywords",
        }
    ),
    "corporate_record": frozenset(
        {
            "entity_name",
            "record_type",
            "effective_date",
            "signatories",
            "jurisdiction",
            "filing_number",
            "intent",
            "subject_matter",
            "keywords",
        }
    ),
    "correspondence": frozenset(
        {
            "sender",
            "recipient",
            "additional_recipients",
            "communication_type",
            "communication_date",
            "demand_amount",
            "action_items",
            "urgency",
            "intent",
            "subject_matter",
            "keywords",
        }
    ),
    "insurance_claim": frozenset(
        {
            "claim_number",
            "policy_number",
            "insurer",
            "insured_party",
            "claim_type",
            "date_of_loss",
            "date_filed",
            "claimed_amount",
            "adjuster",
            "damages_description",
            "coverage_determination",
            "denial_reasons",
            "supporting_documents",
            "intent",
            "subject_matter",
            "keywords",
            "claim_checklist",
        }
    ),
}

# Corpus differentiators scored as content extras, not extraction fields.
# Left on the pair so downstream peelers still see them.
NON_EXTRACTION_KEEP: frozenset[str] = frozenset(
    {
        "content_topic",
        "topic_evidence",
        "sentiment_label",
        "sentiment_score",
        "sentiment_evidence",
        "label_evidence",
        "maud_clause_labels",
        "cuad_clause_labels",
    }
)

# Never scoring events — even when Hub/GT copies them onto the row.
TRACE_ONLY_KEYS: frozenset[str] = frozenset({"reasoning", "confidence"})

# Hub annotation metadata, not extraction schema.
HUB_METADATA_KEYS: frozenset[str] = frozenset(
    {"intent_source", "intent_confidence", "intent_status"}
)

# Hub union keys that name the same fact under another class's schema.
HUB_FIELD_ALIASES: dict[str, dict[str, str]] = {
    "correspondence": {"claimed_amount": "demand_amount"},
}

_EMPTY: tuple[Any, ...] = (None, "", [], {})


def is_empty_gt(value: Any) -> bool:
    """True when a Hub/GT value is absence, not a stated fact.

    Numeric zero is a stated value. Empty lists / dicts / blank strings are not.
    """
    if value in _EMPTY:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, (list, tuple)):
        return all(is_empty_gt(item) for item in value)
    return False


def _apply_hub_aliases(doc_type: str, fields: Mapping[str, Any] | None) -> dict[str, Any]:
    """Copy Hub union-key values onto the live schema name when dest is empty."""
    out = dict(fields or {})
    aliases = HUB_FIELD_ALIASES.get(str(doc_type or "").strip()) or {}
    for src, dest in aliases.items():
        if src not in out:
            continue
        src_val = out[src]
        dest_val = out.get(dest)
        if not is_empty_gt(src_val) and is_empty_gt(dest_val):
            out[dest] = src_val
    return out


def applicable_expected_fields(
    doc_type: str,
    expected: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """GT keys that may count as extraction events for ``doc_type``.

    Drops (1) empty placeholders, (2) trace/Hub-metadata keys, and (3) keys
    that belong to another live class's schema. Unknown ``doc_type`` still
    drops empties / trace / metadata but keeps remaining keys (no invented
    allow-list).
    """
    allowed = LIVE_SCHEMA_FIELDS.get(str(doc_type or "").strip())
    out: dict[str, Any] = {}
    for key, value in _apply_hub_aliases(doc_type, expected).items():
        if key in TRACE_ONLY_KEYS or key in HUB_METADATA_KEYS:
            continue
        if is_empty_gt(value):
            continue
        if key in NON_EXTRACTION_KEEP:
            out[key] = value
            continue
        if allowed is not None and key not in allowed:
            continue
        out[key] = value
    return out


def scope_predicted_fields(
    doc_type: str,
    predicted: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Drop class-mismatched predicted keys so they are not false positives."""
    allowed = LIVE_SCHEMA_FIELDS.get(str(doc_type or "").strip())
    out: dict[str, Any] = {}
    for key, value in _apply_hub_aliases(doc_type, predicted).items():
        if key in TRACE_ONLY_KEYS or key in HUB_METADATA_KEYS:
            continue
        if allowed is None:
            out[key] = value
            continue
        if key in NON_EXTRACTION_KEEP or key in allowed:
            out[key] = value
    return out


def scope_extraction_pair(
    doc_type: str,
    predicted: Mapping[str, Any] | None,
    expected: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(predicted, expected)`` scoped to this class before scoring."""
    return (
        scope_predicted_fields(doc_type, predicted),
        applicable_expected_fields(doc_type, expected),
    )
