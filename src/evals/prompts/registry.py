"""Prompt resolution + runtime injection into the pipeline.

``activate()`` makes the frozen/mutation lineage the LIVE prompt surface of
the llm-mailroom pipeline for the current process, at the two verified choke
points:

1. ``llm.prompts.get_managed_prompt`` — BaseAgent prompts
   (``agents.base.system_prompt`` → ``llm.prompts.get_managed_prompt``).
2. ``langchain_agents.prompts.PROMPT_VERSIONS`` — the vendored LangChain
   versioned path (sorter chain keys like ``sorter_v14``).

Injection is process-local and reversible (``deactivate()``); tests use it
freely. ``--prompt-source`` maps to an explicit mode; the default injects the
frozen v1 lineage so every eval run measures the frozen seed unless a run
explicitly opts into another source.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog

from .lineage import all_versions, resolve, roles

logger = structlog.get_logger(__name__)

SOURCES = ("frozen", "production")


@dataclass
class InjectionState:
    """What activate() changed, so deactivate() can restore it exactly."""

    original_get_managed_prompt: Any = None
    original_prompt_versions: dict[str, str] = field(default_factory=dict)
    active: bool = False


_state = InjectionState()


def default_keys(source: str) -> dict[str, str]:
    """role -> version key for a source mode."""
    if source == "frozen":
        return roles()
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

    llm_prompts.get_managed_prompt = _injected_get_managed_prompt

    patched = dict(_state.original_prompt_versions)
    # LangChain versioned path: map every role's key to the chosen text so a
    # pinned lineage key (e.g. sorter_v14) resolves to the injected version.
    role_to_key = {role: key for role, key in keys.items()}
    for role, key in role_to_key.items():
        if key in versions:
            for original_key in _langchain_keys_for(role, patched):
                patched[original_key] = versions[key].text
    lc_prompts.PROMPT_VERSIONS = patched

    logger.info("evals_prompts_activated", source=source, roles=sorted(keys))
    return keys


def _langchain_keys_for(role: str, versions: dict[str, str]) -> list[str]:
    """LangChain version keys belonging to a role (e.g. sorter_v0..v14)."""
    prefix = f"{role}_v"
    return [key for key in versions if key.startswith(prefix)]


def deactivate() -> None:
    """Restore the pipeline's original prompt surfaces."""
    if not _state.active:
        return
    import llm.prompts as llm_prompts
    from langchain_agents import prompts as lc_prompts

    llm_prompts.get_managed_prompt = _state.original_get_managed_prompt
    lc_prompts.PROMPT_VERSIONS = dict(_state.original_prompt_versions)
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