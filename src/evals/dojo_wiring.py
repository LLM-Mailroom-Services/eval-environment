"""Corpus taxonomy -> llm-dojo-scoring wiring (the eval-env's single caller).

The harness scores extraction through
``llm_dojo_scoring.field_scoring.get_field_types(doc_class)``. Without a
wired taxonomy the field-type maps resolve to ``{}`` and every field is
typed by the dojo's per-field fallback heuristic — degraded extraction
scores (hub#62 follow-on: the dojo now centralizes this in
``configure_from_taxonomy()``, and this module is the eval-env's one wiring
point).

This module loads the corpus taxonomy — the mailroom-dataset ground_truth
doc classes -> field_types maps, canonical copy in llm-mailroom's
``config/taxonomy.yaml`` (the same source the pipeline's own
``observability.scoring_wiring`` wires, so eval numbers measure the same
rubric the pipeline runs) — and calls ``configure_from_taxonomy()`` ONCE at
process start. After wiring, ``get_field_types("contract")`` resolves real
field types (parties, effective_date, ...) instead of ``{}``.

Fail-soft by design: any wiring failure leaves the dojo's package defaults
in place (``get_field_types`` -> ``{}`` -> heuristic fallback), so the suite
stays hermetic and a run never crashes because taxonomy wiring failed.
Idempotent; safe to import repeatedly.
"""

from __future__ import annotations

import structlog

logger = structlog.get_logger(__name__)

# The taxonomy actually wired at process start (None when nothing was wired).
# Exposed for tests/introspection so callers can inspect or restore it.
WIRED_TAXONOMY: dict | None = None


def wire_taxonomy() -> dict | None:
    """Wire the corpus taxonomy into llm-dojo-scoring once (process start).

    Resolution order:
      1. llm-mailroom's ``config/taxonomy.yaml``
         (``pipeline.config.load_config``) — the canonical corpus taxonomy
         (mailroom-dataset ground_truth doc_classes -> field_types maps).
      2. Derived fallback from the ground_truth frames (cases.py's loader
         path), using the same scorable GT field surfaces cases.py hoists
         onto ``expected_fields``.
      3. ``None`` — dojo defaults left in place (hermetic; no crash).

    Returns the taxonomy that was wired, or ``None``.
    """
    global WIRED_TAXONOMY
    for loader in (_taxonomy_from_config, _taxonomy_from_ground_truth):
        try:
            taxonomy = loader()
        except Exception as exc:  # a loader failing is not a scoring failure
            logger.warning(
                "evals_dojo_taxonomy_loader_failed",
                loader=loader.__name__,
                error=f"{type(exc).__name__}: {exc}",
            )
            continue
        if not taxonomy or not taxonomy.get("doc_classes"):
            continue
        try:
            from llm_dojo_scoring import configure_from_taxonomy

            settings = configure_from_taxonomy(taxonomy)
        except Exception as exc:  # dojo absent/broken -> defaults, no crash
            logger.warning(
                "evals_dojo_taxonomy_wire_failed",
                loader=loader.__name__,
                error=f"{type(exc).__name__}: {exc}",
            )
            continue
        if settings.doc_class_field_types:
            WIRED_TAXONOMY = taxonomy
            logger.info(
                "evals_dojo_taxonomy_wired",
                source=loader.__name__,
                doc_classes=sorted(settings.doc_class_field_types),
            )
            return taxonomy
    logger.info(
        "evals_dojo_taxonomy_not_wired",
        reason="no taxonomy source available; dojo defaults in effect",
    )
    return None


# ---------------------------------------------------------------------------
# Taxonomy sources
# ---------------------------------------------------------------------------


def _taxonomy_from_config() -> dict | None:
    """Canonical corpus taxonomy: llm-mailroom's ``config/taxonomy.yaml``.

    The ``doc_classes`` blocks carry the per-class ``field_types`` maps for
    the mailroom-dataset ground_truth surface (contract -> parties,
    effective_date, ...). This is the same loader the pipeline's own
    ``observability.scoring_wiring`` uses — one rubric for pipeline and eval.
    """
    from pipeline.config import load_config

    cfg = load_config()
    if cfg and cfg.get("doc_classes"):
        return cfg
    return None


# Multi-value GT fields -> entity_list typing for the frame-derived fallback
# (mirrors the canonical taxonomy's list fields).
_LIST_FIELDS: frozenset[str] = frozenset(
    {
        "parties",
        "signatories",
        "additional_recipients",
        "supporting_documents",
        "keywords",
        "action_items",
        "claim_checklist",
        "referenced_communications",
    }
)
_FREE_TEXT_LIST_FIELDS: frozenset[str] = frozenset(
    {"cuad_clauses", "maud_clauses", "denial_reasons", "key_requirements"}
)


def _field_type(name: str) -> str:
    """Small name-based type heuristic for the derived fallback taxonomy.

    Mirrors the dojo's own ``field_scoring._heuristic_field_type`` so the
    derived fallback agrees with the canonical taxonomy on the common cases.
    """
    lowered = name.lower()
    if lowered in _LIST_FIELDS or lowered in _FREE_TEXT_LIST_FIELDS:
        element = "free_text" if lowered in _FREE_TEXT_LIST_FIELDS else "name"
        return f"entity_list:{element}"
    if "date" in lowered:
        return "date"
    if any(
        k in lowered
        for k in (
            "value",
            "amount",
            "fee",
            "compensation",
            "price",
            "cost",
            "salary",
            "consideration",
            "total",
        )
    ):
        return "money"
    if any(k in lowered for k in ("number", "id", "docket", "reference", "filing")):
        return "id"
    return "name"


def _taxonomy_from_ground_truth() -> dict | None:
    """Derived fallback: a minimal doc_classes -> field_types taxonomy from
    the mailroom-dataset ground_truth frames (cases.py's loader path).

    Reuses the same scorable GT field surfaces cases.py hoists onto
    ``expected_fields`` (per-class field inventories + CUAD/MAUD label
    columns), typed by ``_field_type``. Lower fidelity than the canonical
    taxonomy.yaml — this is a resilience net, not the primary source.
    """
    from evals import cases
    from langchain_agents.doc_inventories import (
        CORPORATE_GT_KEYS,
        CORRESPONDENCE_GT_KEYS,
        INSURANCE_GT_KEYS,
    )
    from observability.extraction_gt import CONTRACT_GT_KEYS
    from pipeline.hf_corpora import FULL_CORPUS_REVISION, HUB_CLASSES
    from pipeline.hf_corpus_loader import load_corpus

    per_class = {
        "contract": CONTRACT_GT_KEYS,
        "merger_agreement": CONTRACT_GT_KEYS,
        "corporate_record": CORPORATE_GT_KEYS,
        "correspondence": CORRESPONDENCE_GT_KEYS,
        "insurance_claim": tuple(cases.INSURANCE_GT_FIELDS) + tuple(INSURANCE_GT_KEYS),
    }
    frame, _ = load_corpus(split="train", revision=FULL_CORPUS_REVISION)
    present: dict[str, set[str]] = {cls: set() for cls in HUB_CLASSES}
    for row in frame.to_dict(orient="records"):
        cls = str(row.get("expected") or "")
        if cls not in per_class:
            continue
        present[cls].update(
            key for key in per_class[cls] if row.get(key) not in (None, "")
        )
        for key in ("cuad_clause_labels", "maud_clause_labels"):
            if row.get(key) not in (None, ""):
                present[cls].add(key)
    doc_classes = [
        {
            "key": cls,
            "field_types": {field: _field_type(field) for field in sorted(fields)},
        }
        for cls in HUB_CLASSES
        if (fields := present[cls])
    ]
    return {"doc_classes": doc_classes} if doc_classes else None


# Wire once at process start (module import). Import this module anywhere
# scoring runs and the dojo taxonomy is in place before the first
# get_field_types()/score_with_suite() call.
wire_taxonomy()