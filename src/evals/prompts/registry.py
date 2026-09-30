"""Prompt resolution + runtime injection into the pipeline.

``activate()`` makes the frozen/mutation lineage the LIVE prompt surface of
the llm-mailroom pipeline for the current process. The merger-agreement
specialist is not a pipeline-integrated node yet: its frozen stem must still
reach the agent class via every import binding, not only ``llm.prompts``.

Choke points:

1. ``llm.prompts.get_managed_prompt`` — BaseAgent prompts, plus any module
   that already bound ``from llm.prompts import get_managed_prompt``.
2. ``langchain_agents.prompts.PROMPT_VERSIONS`` **and** ``get_prompt`` —
   including the unversioned role key (``merger_agreement_specialist``), not
   only ``{role}_v*`` aliases. LangChain specialists call ``get_prompt``
   imported at module load.

Injection is process-local and reversible (``deactivate()``); tests use it
freely. ``--prompt-source`` maps to an explicit mode; the default injects the
frozen v1 lineage so every eval run measures the frozen seed unless a run
explicitly opts into another source.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any

import structlog

from .lineage import all_versions, resolve, roles

logger = structlog.get_logger(__name__)

SOURCES = ("frozen", "archived", "production")


@dataclass
class InjectionState:
    """What activate() changed, so deactivate() can restore it exactly."""

    original_get_managed_prompt: Any = None
    original_get_prompt: Any = None
    original_prompt_versions: dict[str, str] = field(default_factory=dict)
    rebound_managed: list[Any] = field(default_factory=list)
    rebound_get_prompt: list[Any] = field(default_factory=list)
    injected_keys: dict[str, str] = field(default_factory=dict)
    active: bool = False


_state = InjectionState()


def default_keys(source: str) -> dict[str, str]:
    """role -> version key for a source mode."""
    if source == "frozen":
        return roles()
    if source == "archived":
        keys = roles()
        from . import archived_production

        for key in archived_production.VERSIONS:
            # Default archived injection is *_v0 only. Modal-parity keys
            # (e.g. contracts_specialist_v33) are explicit --prompt-version pins.
            if not key.endswith("_v0"):
                continue
            role = key.rsplit("_v", 1)[0]
            keys[role] = key
        return keys
    # production: the agent's own live template (no injection needed)
    return {}


def activate(
    source: str = "frozen",
    overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    """Inject the chosen prompt source into the live pipeline. Idempotent.

    Returns the effective role -> version-key map actually injected.
    """
    if source not in SOURCES:
        raise ValueError(f"unknown prompt source {source!r}; known: {SOURCES}")
    if source == "production":
        deactivate()
        return {}

    keys = default_keys(source)
    for role, key in (overrides or {}).items():
        resolved = resolve(key)  # raises on unknown keys — fail loud, not silent
        keys[role] = resolved.key

    import llm.prompts as llm_prompts
    from langchain_agents import prompts as lc_prompts

    if not _state.active:
        _state.original_get_managed_prompt = llm_prompts.get_managed_prompt
        _state.original_get_prompt = lc_prompts.get_prompt
        _state.original_prompt_versions = dict(lc_prompts.PROMPT_VERSIONS)
        _state.active = True

    versions = all_versions()

    def _injected_get_managed_prompt(
        agent_name: str, default_text: str,
        variables: dict | None = None, label: str = "production",
    ) -> tuple[str, object | None]:
        key = keys.get(agent_name)
        if key and key in versions:
            return versions[key].text, None
        return _state.original_get_managed_prompt(
            agent_name, default_text, variables=variables, label=label,
        )

    def _injected_get_prompt(version: str) -> str:
        table = lc_prompts.PROMPT_VERSIONS
        if version in table:
            return table[version]
        raise KeyError(
            f"Prompt version {version!r} not found. Available versions: {list(table)}"
        )

    llm_prompts.get_managed_prompt = _injected_get_managed_prompt
    previous_managed = list(_state.rebound_managed)
    _state.rebound_managed = _rebind_attr(
        "get_managed_prompt",
        (_state.original_get_managed_prompt,),
        _injected_get_managed_prompt,
    )
    for mod in previous_managed:
        try:
            setattr(mod, "get_managed_prompt", _injected_get_managed_prompt)
        except Exception:
            pass
        if mod not in _state.rebound_managed:
            _state.rebound_managed.append(mod)

    patched = dict(_state.original_prompt_versions)
    # LangChain path: unversioned role keys (merger_agreement_specialist) AND
    # versioned aliases (sorter_v14, contracts_specialist_v33).
    for role, key in keys.items():
        if key not in versions:
            continue
        text = versions[key].text
        patched[role] = text
        for original_key in _langchain_keys_for(role, patched):
            patched[original_key] = text
    lc_prompts.PROMPT_VERSIONS = patched
    lc_prompts.get_prompt = _injected_get_prompt
    previous_prompt = list(_state.rebound_get_prompt)
    _state.rebound_get_prompt = _rebind_attr(
        "get_prompt",
        (_state.original_get_prompt,),
        _injected_get_prompt,
    )
    for mod in previous_prompt:
        try:
            setattr(mod, "get_prompt", _injected_get_prompt)
        except Exception:
            pass
        if mod not in _state.rebound_get_prompt:
            _state.rebound_get_prompt.append(mod)

    _state.injected_keys = dict(keys)
    logger.info("evals_prompts_activated", source=source, roles=sorted(keys))
    return keys


def active_keys() -> dict[str, str]:
    """role -> version key currently injected (empty when inactive)."""
    return dict(_state.injected_keys)


def _langchain_keys_for(role: str, versions: dict[str, str]) -> list[str]:
    """LangChain version keys belonging to a role (e.g. sorter + sorter_v0..v14)."""
    found: list[str] = []
    if role in versions:
        found.append(role)
    prefix = f"{role}_v"
    found.extend(key for key in versions if key.startswith(prefix) and key not in found)
    return found


def _rebind_attr(attr: str, originals: tuple[Any, ...], injected: Any) -> list[Any]:
    """Point every loaded module's ``attr`` at ``injected`` when it still holds an original."""
    rebound: list[Any] = []
    targets = {obj for obj in originals if obj is not None}
    for mod in list(sys.modules.values()):
        if mod is None:
            continue
        try:
            current = getattr(mod, attr, None)
        except Exception:
            continue
        if current not in targets:
            continue
        try:
            setattr(mod, attr, injected)
        except Exception:
            continue
        rebound.append(mod)
    return rebound


def deactivate() -> None:
    """Restore the pipeline's original prompt surfaces."""
    if not _state.active:
        return
    import llm.prompts as llm_prompts
    from langchain_agents import prompts as lc_prompts

    for mod in _state.rebound_managed:
        try:
            setattr(mod, "get_managed_prompt", _state.original_get_managed_prompt)
        except Exception:
            pass
    for mod in _state.rebound_get_prompt:
        try:
            setattr(mod, "get_prompt", _state.original_get_prompt)
        except Exception:
            pass
    llm_prompts.get_managed_prompt = _state.original_get_managed_prompt
    lc_prompts.get_prompt = _state.original_get_prompt
    lc_prompts.PROMPT_VERSIONS = dict(_state.original_prompt_versions)
    _state.rebound_managed = []
    _state.rebound_get_prompt = []
    _state.injected_keys = {}
    _state.active = False
    logger.info("evals_prompts_deactivated")


def resolved_snapshot(keys: dict[str, str]) -> dict[str, Any]:
    """Per-agent provenance for the run record: key, lineage, sha256."""
    snapshot: dict[str, Any] = {}
    for role, key in sorted(keys.items()):
        version = resolve(key)
        snapshot[role] = {
            "key": version.key,
            "lineage": version.lineage,
            "source": version.source,
            "sha256": version.sha256,
        }
    return snapshot
