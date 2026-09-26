"""Unified prompt lineage registry — frozen v1 + archived v0 + GEPA mutations + live pipeline.

Version resolution order (``evals.prompts.registry.resolve``):
    1. frozen   — ``frozen_v1.VERSIONS`` (the official v1 snapshot; concise specialists)
    2. mutation — versions appended by ``evals.prompts.mutations.apply_mutation``
                  (GEPA output; each records its parent + change note)
    3. archived — ``archived_production.VERSIONS`` (pre-concise production specialists as ``*_v0``)
    4. production — the pipeline's local templates (``llm.prompts.prompt_templates``)

Every version carries its sha256; ``verify_lineage`` detects drift between the
frozen snapshot and the live pipeline (re-freeze to cut a new version).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import frozen_v1

LINEAGE_ID = frozen_v1.LINEAGE_ID
MANIFEST_PATH = Path(__file__).resolve().parents[3] / "prompts" / "manifest.json"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PromptVersion:
    key: str
    text: str
    lineage: str  # frozen | mutation | production
    source: str  # provenance (source key or parent version)
    version: int  # lineage version number (1 for the frozen snapshot)

    @property
    def sha256(self) -> str:
        return sha256(self.text)


def _mutations() -> dict[str, dict[str, Any]]:
    """Mutation versions registered by the GEPA scaffold (evals.prompts.mutations)."""
    try:
        from . import mutations

        return mutations.registered_mutations()
    except ImportError:
        return {}


def _production() -> dict[str, str]:
    try:
        from llm.prompts import prompt_templates

        return dict(prompt_templates())
    except Exception:
        return {}


def _archived() -> dict[str, tuple[str, str]]:
    """Archived production specialist texts: key -> (text, source)."""
    try:
        from . import archived_production

        source_of = getattr(archived_production, "SOURCE_OF", {})
        return {key: (text, source_of.get(key, "archived")) for key, text in archived_production.VERSIONS.items()}
    except ImportError:
        return {}


def all_versions() -> dict[str, PromptVersion]:
    """Every resolvable version across all layers (frozen wins ties)."""
    out: dict[str, PromptVersion] = {}
    for agent_name, text in _production().items():
        out[agent_name] = PromptVersion(agent_name, text, "production", "prompt_templates", 0)
    for key, (text, source) in _archived().items():
        out[key] = PromptVersion(key, text, "archived", source, 0)
    for key, meta in sorted(_mutations().items()):
        out[key] = PromptVersion(key, meta["text"], "mutation", meta["parent"], int(meta["version"]))
    for key, text in frozen_v1.VERSIONS.items():
        out[key] = PromptVersion(
            key, text, "frozen", frozen_v1.SOURCE_OF.get(key, "frozen_v1"), frozen_v1.FROZEN_VERSION
        )
    return out


def resolve(key: str) -> PromptVersion:
    """Resolve one version key (exact match across all layers)."""
    versions = all_versions()
    if key in versions:
        return versions[key]
    known = ", ".join(sorted(versions))
    raise KeyError(f"unknown prompt version {key!r}; known: {known}")


def roles() -> dict[str, str]:
    """eval role -> default frozen key (the v1 seed for every pipeline role)."""
    return {key.rsplit("_v1", 1)[0]: key for key in frozen_v1.VERSIONS}


def verify_lineage() -> dict[str, Any]:
    """Drift check: frozen snapshot vs the live pipeline sources.

    Returns {"ok": bool, "drifted": [keys], "manifest": {...}} — a frozen key
    drifts when the live source's sha256 no longer matches the manifest.
    """
    from .freeze_helpers import live_frozen_texts

    manifest = json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.exists() else {}
    drifted: list[str] = []
    try:
        live = live_frozen_texts()
    except ModuleNotFoundError:
        live = None
    for key, meta in (manifest.get("versions") or {}).items():
        if meta.get("source_kind") == "sandbox":
            continue
        if live is None:
            continue
        if key in live and sha256(live[key]) != meta["sha256"]:
            drifted.append(key)
    return {"ok": not drifted, "drifted": drifted, "manifest": manifest}