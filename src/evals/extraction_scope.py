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

def is_missing_scalar(value: Any) -> bool:
    """True for ``float("nan")`` and the pandas missing sentinels ``pd.NA`` /
    ``pd.NaT``. Never true for numeric zero or ``False`` — those are stated.

    ``pandas`` is imported lazily so the pure-python path stays import-cheap
    and hermetic; the ``int``/``bool``/``float`` fast paths never reach it.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, float):
        return value != value  # covers float and its numpy float64 subclass
    if isinstance(value, int):
        return False
    try:
        import pandas as pd  # noqa: PLC0415 — lazy by design
    except Exception:  # pragma: no cover - pandas is a hard dep in practice
        return False
    try:
        marker = pd.isna(value)
    except (TypeError, ValueError):
        return False
    if isinstance(marker, bool):
        return marker
    return bool(getattr(marker, "shape", None) == () and marker)


def _is_empty_array(value: Any) -> bool:
    """Emptiness of an array-like GT cell (numpy ``ndarray``, ``pandas.Series``).

    Duck-typed via ``size`` + ``ravel()`` / ``tolist()`` — no numpy import, so
    the pure-python path stays cheap. Size 0 is absence; otherwise the payload
    is classified recursively, so ``[0]`` is a *stated* value.
    """
    try:
        if int(value.size) == 0:
            return True
        payload = value.ravel().tolist() if hasattr(value, "ravel") else value.tolist()
    except (AttributeError, TypeError, ValueError):
        return is_missing_scalar(value)
    return is_empty_gt(payload)


def is_empty_gt(value: Any) -> bool:
    """True when a Hub/GT value is absence, not a stated fact.

    Numeric zero is a stated value. ``None`` / blank strings / empty containers
    / empty arrays / ``NaN`` / ``pd.NA`` / ``pd.NaT`` are not.

    The classification is an ordered ``isinstance`` cascade rather than a
    ``value in _EMPTY`` membership test: ``in`` compares with ``==``, which is
    element-wise for a numpy array, and the resulting ``bool()`` raises
    ``ValueError: The truth value of an empty array is ambiguous``. Schema-v9
    list-typed parquet cells reach here as ``numpy.ndarray`` because
    ``cases._case_from_row`` reads them back through
    ``DataFrame.to_dict(orient="records")``.
    """
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, Mapping):
        return len(value) == 0
    if isinstance(value, (list, tuple)):
        return all(is_empty_gt(item) for item in value)
    if hasattr(value, "size") and hasattr(value, "shape"):
        return _is_empty_array(value)
    return is_missing_scalar(value)


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
