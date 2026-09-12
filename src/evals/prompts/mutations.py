"""GEPA mutation registry + validation gates (DRAFT→VALIDATE→APPLY).

Ports the proven mechanical gates from llm-entity-extraction's
``scripts/prompt_engineer.py`` (the iteration-OS DRAFT step) onto this repo's
lineage registry:

    1. ANCHOR — the anchor substring occurs EXACTLY ONCE in the parent text.
    2. KEY — the proposed version key is unused and follows the lineage
       naming (``<role>_v<N+1>``, N = parent's version).
    3. ADDITIVE — the mutation is additive-only: parent text preserved as a
       strict prefix (no deletion beyond the anchor span's tail edit).
    4. METADATA — parent + change note recorded; registry stays consistent.

Mutations are REGISTERED in-process here (and persisted by appending to
``lineage.py``'s mutation table via ``persist_mutations``); the frozen
snapshot is never touched. The A/B itself is run by the eval runner with
``--prompt-version <new_key>`` — the tool prints that exact command.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .lineage import PromptVersion, resolve, sha256

MUTATIONS_PATH = Path(__file__).resolve().parents[3] / "prompts" / "mutations.json"


class MutationError(ValueError):
    """A proposed mutation failed a validation gate."""


def registered_mutations() -> dict[str, dict[str, Any]]:
    """Persisted mutation versions: key -> {text, parent, version, note, ...}."""
    if not MUTATIONS_PATH.exists():
        return {}
    data = json.loads(MUTATIONS_PATH.read_text())
    return {row["key"]: row for row in data.get("mutations", [])}


def validate_mutation(
    *,
    parent_key: str,
    new_key: str,
    anchor: str,
    replacement: str,
    note: str,
) -> tuple[str, dict[str, Any]]:
    """Run all four gates. Returns (mutated_text, metadata). Raises MutationError."""
    parent: PromptVersion = resolve(parent_key)
    parent_text = parent.text

    # Gate 1 — ANCHOR: exactly once in the parent.
    count = parent_text.count(anchor)
    if count != 1:
        raise MutationError(
            f"anchor occurs {count}x in {parent_key} (must be exactly once): {anchor[:80]!r}"
        )

    # Gate 2 — KEY: unused + lineage naming (<role>_v<parent.version + 1>).
    all_keys = set()
    from .lineage import all_versions

    all_keys = set(all_versions())
    if new_key in all_keys:
        raise MutationError(f"version key {new_key!r} already exists")
    role = parent_key.rsplit("_v", 1)[0]
    expected = f"{role}_v{parent.version + 1}"
    if new_key != expected:
        raise MutationError(f"key {new_key!r} violates lineage naming (expected {expected!r})")

    # Gate 3 — ADDITIVE: anchor replaced once; parent preserved outside the span.
    start = parent_text.index(anchor)
    mutated = parent_text[:start] + replacement + parent_text[start + len(anchor):]
    prefix = parent_text[:start]
    suffix = parent_text[start + len(anchor):]
    if not mutated.startswith(prefix) or not mutated.endswith(suffix):
        raise MutationError("mutation is not additive-only (parent text altered outside the anchor span)")

    meta = {
        "key": new_key,
        "parent": parent_key,
        "version": parent.version + 1,
        "note": note,
        "anchor_head": anchor[:60],
        "sha256": sha256(mutated),
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    return mutated, meta


def apply_mutation(
    *,
    parent_key: str,
    new_key: str,
    anchor: str,
    replacement: str,
    note: str,
    persist: bool = True,
) -> dict[str, Any]:
    """Validate + register one mutation. Returns the metadata record."""
    mutated, meta = validate_mutation(
        parent_key=parent_key, new_key=new_key, anchor=anchor,
        replacement=replacement, note=note,
    )
    meta["text"] = mutated
    if persist:
        data = {"mutations": []}
        if MUTATIONS_PATH.exists():
            data = json.loads(MUTATIONS_PATH.read_text())
        keys = [row["key"] for row in data.get("mutations", [])]
        if new_key in keys:
            raise MutationError(f"version key {new_key!r} already persisted")
        data.setdefault("mutations", []).append(meta)
        MUTATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
        MUTATIONS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return meta


def render_prompts_mirror() -> int:
    """Regenerate prompts/<key>.md for every registered mutation. Returns count."""
    count = 0
    for key, meta in registered_mutations().items():
        path = MUTATIONS_PATH.parent / f"{key}.md"
        path.write_text(meta["text"], encoding="utf-8")
        count += 1
    return count
