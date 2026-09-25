"""Corpus case loading — the ONE data path for every eval/pilot/calibration task.

Wraps llm-mailroom's canonical ``pipeline.hf_corpus_loader`` (pinned-revision
parquet join of the ``ground_truth`` + ``default`` configs on ``filename``,
sha256-verified) and adds the subset grammar the eval CLI speaks:

    full | train | test | class:<name> | subclass:<class>:<subclass>
    fixtures | bundles | streams | pilot | cuad | enron | claims

plus stratified sampling (``--sample N --seed S``) and hard caps (``--n N``).

Every case is a plain dict (JSONL-serializable) with a stable shape:

    id, filename, text, expected_doc_class, expected_subclass,
    expected_specialist, expected_stage, review_expected, retry_expected,
    expected_fields, source, config, split, + fixture_* keys for the
    fixtures config, + ``row`` provenance.
"""

from __future__ import annotations

import json
import random
from typing import Any

from pipeline.hf_corpora import (
    CORPORA,
    FULL_CORPUS_ID,
    FULL_CORPUS_REVISION,
    HUB_CLASSES,
    adapt_hub_row,
    resolve_corpus,
)
from pipeline.hf_corpus_loader import load_config_frame, load_corpus

# Insurance GT columns (schema v8/v9) — the expected_fields surface for the
# insurance_claims specialist eval. On v9 these arrive nested inside the
# `gt_fields` JSON payload and are hoisted by _expand_gt_fields.
INSURANCE_GT_FIELDS: tuple[str, ...] = (
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
)

# Fixture-calibration columns promoted onto the case dict (calibration tasks).
FIXTURE_FIELDS: tuple[str, ...] = (
    "fixture_kind",
    "calibration_cell",
    "probes_confidence",
    "failure_stage",
    "arbiter_outcome",
    "failure_note",
    "arbiter_note",
    "review_reason",
    "expected_correction",
    "expected_post_retry_state",
    "expected_post_correction_state",
)

_SUBSET_CORPUS = {
    "cuad": "mailroom-cuad-contracts-full",
    "enron": "enron-correspondence-dedup",
    "claims": "cms-desynpuf-insurance-claims",
    "pilot": "docclass-pilot",
}


def parse_subset(spec: str | None) -> dict[str, Any]:
    """Parse a subset spec into (kind, value) parts. Raises on unknown specs."""
    raw = (spec or "full").strip()
    if raw in ("full", "train", "test"):
        return {"kind": raw, "value": None}
    if raw in ("fixtures", "bundles", "streams"):
        return {"kind": "config", "value": raw}
    if raw in _SUBSET_CORPUS:
        return {"kind": "corpus", "value": raw}
    if raw.startswith("class:"):
        value = raw.split(":", 1)[1].strip()
        if value not in HUB_CLASSES:
            raise ValueError(f"unknown class {value!r}; known: {HUB_CLASSES}")
        return {"kind": "class", "value": value}
    if raw.startswith("subclass:"):
        parts = raw.split(":", 2)
        if len(parts) != 3 or parts[1] not in HUB_CLASSES:
            raise ValueError(f"subclass spec must be subclass:<class>:<subclass>: {raw!r}")
        return {"kind": "subclass", "value": (parts[1], parts[2].strip())}
    raise ValueError(
        f"unknown subset {raw!r}; known: full, train, test, class:<name>, "
        "subclass:<class>:<subclass>, fixtures, bundles, streams, pilot, "
        "cuad, enron, claims"
    )


def _truthy(value: Any) -> bool | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def _is_empty_container(value: Any) -> bool:
    """v9 GT empties: the literal strings '{}' / '[]' mean "no items"."""
    if isinstance(value, str) and value.strip() in ("{}", "[]"):
        return True
    if isinstance(value, (dict, list)):
        return len(value) == 0
    return False


def _expand_gt_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Hoist the v9 nested ``gt_fields`` JSON payload onto flat row keys.

    Schema v9 moved the 13 insurance GT fields plus ``cuad_clause_labels`` /
    ``maud_clause_labels`` into a single ``gt_fields`` JSON-string column.
    Scoring reads flat keys, so expand here (empty values and empty
    containers stay absent — an empty payload must not shadow a flat key).
    """
    raw = row.get("gt_fields")
    if raw is None or raw == "":
        return row
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return row
    else:
        parsed = raw
    if not isinstance(parsed, dict):
        return row
    merged = dict(row)
    for key, value in parsed.items():
        if isinstance(value, str) and value.strip()[:1] in ("{", "["):
            # list-typed GT fields arrive as JSON-array strings (v9 contract)
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                pass
        if value is None or value == "" or _is_empty_container(value):
            continue
        merged.setdefault(key, value)
    return merged


def _expected_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Non-empty GT fields for the row's class, in the pipeline's canonical
    scoring shape (the suite expects flattened ``cuad_clauses`` /
    ``maud_clauses`` lists, not the raw Hub label JSON — a perfect prediction
    scores 0.0 against the raw shape)."""
    row = _expand_gt_fields(row)
    fields: dict[str, Any] = {}
    if str(row.get("expected") or "") == "insurance_claim":
        for key in INSURANCE_GT_FIELDS:
            value = row.get(key)
            if (
                value is not None
                and str(value).strip() != ""
                and not _is_empty_container(value)
            ):
                fields[key] = value
    labels = {}
    for key in ("cuad_clause_labels", "maud_clause_labels"):
        value = row.get(key)
        if (
            isinstance(value, list) and value
            or isinstance(value, str) and value.strip() and not _is_empty_container(value)
        ):
            labels[key] = value
    # The pipeline's own GT catalog maps subclass → canonical field tokens
    # (corporate_record → record_type; contract/merger subclass → family
    # tokens) — class-labeled rows without field GT still get a scorable
    # expected_fields surface.
    if not fields and not labels:
        try:
            from observability.extraction_gt import catalog_expected_fields

            fields.update(catalog_expected_fields({**row, "expected": row.get("expected"), "expected_subclass": row.get("expected_subclass")}))
        except Exception as exc:  # fail open: catalog is a fallback surface
            import structlog

            structlog.get_logger(__name__).warning(
                "evals_gt_catalog_unavailable", error=f"{type(exc).__name__}: {exc}"
            )
    if labels:
        try:
            from observability.extraction_gt import catalog_expected_fields

            fields.update(catalog_expected_fields({**row, **labels}))
        except Exception:
            fields.update(labels)  # fail open: raw labels still better than nothing
    # The raw label JSON is source material only — the scoring surface is the
    # flattened shape (the suite scores unknown fields as 0).
    for key in ("cuad_clause_labels", "maud_clause_labels"):
        fields.pop(key, None)
    from evals.extraction_scope import applicable_expected_fields

    return applicable_expected_fields(str(row.get("expected") or ""), fields)


def _case_from_row(row: dict[str, Any], *, config: str, split: str) -> dict[str, Any]:
    filename = str(row.get("filename") or "doc.txt")
    case: dict[str, Any] = {
        "id": f"corpus:{config}:{split}:{filename}",
        "filename": filename,
        "text": str(row.get("doc_text") or ""),
        "expected_doc_class": str(row.get("expected") or "") or None,
        "expected_subclass": str(row.get("expected_subclass") or "") or None,
        "expected_specialist": str(row.get("expected_specialist") or "") or None,
        "expected_stage": str(row.get("expected_stage") or "") or None,
        "review_expected": _truthy(row.get("review_expected")),
        "retry_expected": _truthy(row.get("retry_expected")),
        "expected_fields": _expected_fields(row),
        "source": "mailroom-dataset",
        "config": config,
        "split": split,
    }
    for key in FIXTURE_FIELDS:
        value = row.get(key)
        if value is not None and str(value).strip() != "":
            case[key] = value
    if _truthy(row.get("review_expected")) is None:
        case.pop("review_expected", None)
    if _truthy(row.get("retry_expected")) is None:
        case.pop("retry_expected", None)
    case["row"] = {
        k: row.get(k)
        for k in ("document_id", "source_corpus", "matter_id", "group_id", "synthetic")
        if row.get(k) not in (None, "")
    }
    return case


def _rows_for_main_corpus(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Rows from the mailroom-corpus ground_truth join for full/train/test/class/subclass."""
    split = "train" if spec["kind"] in ("full", "train", "class", "subclass") else "test"
    frame, provenance = load_corpus(split=split, revision=FULL_CORPUS_REVISION)
    rows = frame.to_dict(orient="records")
    if spec["kind"] == "class":
        rows = [r for r in rows if str(r.get("expected") or "") == spec["value"]]
    elif spec["kind"] == "subclass":
        want_class, want_sub = spec["value"]
        rows = [
            r
            for r in rows
            if str(r.get("expected") or "") == want_class
            and str(r.get("expected_subclass") or "") == want_sub
        ]
    for row in rows:
        row["_provenance"] = {
            "revision": provenance.get("revision_requested"),
            "integrity": provenance.get("integrity"),
        }
    return rows


def _rows_for_config(config: str) -> list[dict[str, Any]]:
    """Rows from a self-contained corpus config (fixtures/bundles/streams), both splits."""
    rows: list[dict[str, Any]] = []
    for split in ("train", "test"):
        frame, _prov = load_config_frame(FULL_CORPUS_ID, config, split=split, revision=FULL_CORPUS_REVISION)
        rows.extend(frame.to_dict(orient="records"))
    return rows


def _rows_for_family_corpus(alias: str) -> list[dict[str, Any]]:
    """Rows from a family corpus (pilot/cuad/enron/claims) via the corpora registry.

    Family corpora split labels (``ground_truth``) from text (``default``) the
    same way the main corpus does — join on ``filename`` when both configs
    exist; fall back to whichever loads. Family corpora are NOT sha-pinned
    (they float on Hub tip) unless the registry carries a revision. Loads
    that fail loudly raise — a silently-empty corpus would zero out a run.
    """
    slug = _SUBSET_CORPUS[alias]
    corp = resolve_corpus(slug)
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for split in ("train", "test"):
        try:
            frame, _prov = load_config_frame(corp["id"], "ground_truth", split=split, revision=corp.get("revision"))
        except Exception as exc:
            frame = None
            failures.append(f"{slug}:ground_truth:{split}: {type(exc).__name__}: {exc}")
        try:
            blind, _bprov = load_config_frame(corp["id"], "default", split=split, revision=corp.get("revision"))
        except Exception as exc:
            blind = None
            failures.append(f"{slug}:default:{split}: {type(exc).__name__}: {exc}")
        if frame is None and blind is None:
            continue
        if frame is not None and blind is not None and "doc_text" in blind.columns:
            text_cols = [c for c in blind.columns if c not in ("filename",)]
            merged = frame.merge(
                blind[["filename", *text_cols]], on="filename", how="left", validate="one_to_one"
            )
            rows.extend(merged.to_dict(orient="records"))
        else:
            rows.extend((frame if frame is not None else blind).to_dict(orient="records"))
    out: list[dict[str, Any]] = []
    for raw in rows:
        row = adapt_hub_row(raw, corp)
        row.setdefault("expected", corp.get("default_class") or row.get("expected"))
        out.append(row)
    if not out:
        detail = "; ".join(failures) if failures else "no rows returned"
        raise RuntimeError(
            f"family corpus {slug!r} (subset {alias!r}) yielded 0 cases — "
            f"refusing to proceed on an empty corpus ({detail})"
        )
    return out


def stratified_sample(rows: list[dict[str, Any]], n: int, *, seed: int, by: str = "expected") -> list[dict[str, Any]]:
    """Even-per-stratum sample (round-robin), shuffled within strata. Deterministic."""
    if n <= 0 or not rows:
        return []
    strata: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        strata.setdefault(str(row.get(by) or ""), []).append(row)
    rng = random.Random(seed)
    for key, bucket in strata.items():
        rng.shuffle(bucket)
    keys = sorted(strata)
    out: list[dict[str, Any]] = []
    i = 0
    while len(out) < n:
        progressed = False
        for key in keys:
            if len(out) >= n:
                break
            bucket = strata[key]
            if i < len(bucket):
                out.append(bucket[i])
                progressed = True
        if not progressed:
            break
        i += 1
    return out


def load_cases(
    subset: str | None = None,
    *,
    sample: int | None = None,
    seed: int = 42,
    n: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load eval cases for a subset spec. Returns (cases, selection_provenance)."""
    spec = parse_subset(subset)
    if spec["kind"] == "config":
        raw_rows = _rows_for_config(spec["value"])
        config, split = spec["value"], "train+test"
    elif spec["kind"] == "corpus":
        raw_rows = _rows_for_family_corpus(spec["value"])
        corp = resolve_corpus(_SUBSET_CORPUS[spec["value"]])
        config, split = corp["id"], "train+test"
    else:
        raw_rows = _rows_for_main_corpus(spec)
        config, split = "ground_truth", ("test" if spec["kind"] == "test" else "train")
    cases = [_case_from_row(r, config=config, split=split) for r in raw_rows]
    selected = cases
    if sample is not None:
        selected = stratified_sample(cases, int(sample), seed=seed)
    if n is not None:
        selected = selected[: max(0, int(n))]
    provenance = {
        "subset_spec": spec,
        "repo": FULL_CORPUS_ID,
        "revision": FULL_CORPUS_REVISION,
        "config": config,
        "split": split,
        "n_total": len(cases),
        "n_selected": len(selected),
        "sample": sample,
        "seed": seed,
    }
    if spec["kind"] == "corpus":
        provenance["repo"] = resolve_corpus(_SUBSET_CORPUS[spec["value"]])["id"]
        provenance["revision"] = None
    return selected, provenance


def fixture_cases(*, split: str | None = None) -> list[dict[str, Any]]:
    """Just the fixtures-config cases (calibration primary data)."""
    cases: list[dict[str, Any]] = []
    splits = (split,) if split else ("train", "test")
    for one in splits:
        frame, _prov = load_config_frame(
            FULL_CORPUS_ID, "fixtures", split=one, revision=FULL_CORPUS_REVISION
        )
        cases.extend(_case_from_row(r, config="fixtures", split=one) for r in frame.to_dict(orient="records"))
    return cases


def known_corpora() -> dict[str, dict[str, Any]]:
    """The corpora registry (for --list output and docs)."""
    return dict(CORPORA)
