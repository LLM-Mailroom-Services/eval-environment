"""OpenRouter model roster for eval real runs.

``config/openrouter_models.yaml`` is the allow-list for ``--model`` and the
pricing source for cost estimates when the dojo table lacks a slug. During a
run, :func:`apply_model_override` merges roster pricing into the pipeline
taxonomy and rewrites OpenRouter agent models to the chosen slug.
"""

from __future__ import annotations

import copy
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

import structlog
import yaml

logger = structlog.get_logger(__name__)

ROSTER_PATH = Path(__file__).resolve().parents[2] / "config" / "openrouter_models.yaml"

# Agents that must keep taxonomy defaults (free lane / optional LLM / procedural).
_SKIP_MODEL_OVERRIDE = frozenset({"gmail_triage", "relations", "reporter"})


@lru_cache(maxsize=1)
def load_roster() -> dict[str, Any]:
    if not ROSTER_PATH.is_file():
        raise FileNotFoundError(f"OpenRouter roster missing: {ROSTER_PATH}")
    data = yaml.safe_load(ROSTER_PATH.read_text(encoding="utf-8")) or {}
    models = data.get("models") or {}
    if not isinstance(models, dict) or not models:
        raise ValueError(f"OpenRouter roster has no models: {ROSTER_PATH}")
    return data


def list_models() -> list[dict[str, Any]]:
    """Sorted roster entries for CLI / viewer."""
    roster = load_roster()
    out: list[dict[str, Any]] = []
    for slug, meta in sorted((roster.get("models") or {}).items()):
        if not isinstance(meta, dict):
            continue
        out.append({"slug": slug, **meta})
    return out


def get_model(slug: str) -> dict[str, Any]:
    meta = (load_roster().get("models") or {}).get(slug)
    if not isinstance(meta, dict):
        known = ", ".join(sorted((load_roster().get("models") or {})))
        raise KeyError(f"unknown OpenRouter model {slug!r}; roster: {known}")
    return dict(meta)


def validate_model_slug(slug: str) -> None:
    get_model(slug)


def cost_spec(slug: str) -> dict[str, float] | None:
    meta = get_model(slug)
    try:
        inp = float(meta.get("input_per_million", -1))
        out = float(meta.get("output_per_million", -1))
    except (TypeError, ValueError):
        return None
    if inp < 0 or out < 0:
        return None
    return {"input_per_million": inp, "output_per_million": out}


def estimate_cost_usd(prompt_tokens: int, completion_tokens: int, model: str | None) -> float | None:
    if not model or not (prompt_tokens or completion_tokens):
        return None
    spec = cost_spec(model)
    if not spec:
        return None
    total = (prompt_tokens / 1e6) * spec["input_per_million"]
    total += (completion_tokens / 1e6) * spec["output_per_million"]
    return round(total, 6)


def roster_for_snapshot() -> dict[str, Any]:
    roster = load_roster()
    models = []
    for slug, meta in sorted((roster.get("models") or {}).items()):
        if not isinstance(meta, dict):
            continue
        models.append(
            {
                "slug": slug,
                "label": meta.get("label") or slug,
                "modality": meta.get("modality"),
                "context_tokens": meta.get("context_tokens"),
                "input_per_million": meta.get("input_per_million"),
                "output_per_million": meta.get("output_per_million"),
            }
        )
    return {"provider": roster.get("provider", "openrouter"), "models": models}


@contextmanager
def apply_model_override(model_slug: str | None) -> Iterator[None]:
    """Merge roster pricing + uniform agent model into pipeline taxonomy."""
    if not model_slug:
        yield
        return
    validate_model_slug(model_slug)
    try:
        import pipeline.config as pc
    except ImportError:
        logger.warning("openrouter_roster_no_pipeline", model=model_slug)
        yield
        return

    original_load = pc.load_config
    price = cost_spec(model_slug)

    @lru_cache(maxsize=1)
    def _merged_load_config() -> dict[str, Any]:
        cfg = copy.deepcopy(original_load())
        if price:
            costs = dict(cfg.get("cost_models") or {})
            costs[model_slug] = price
            cfg["cost_models"] = costs
        agents = dict(cfg.get("agents") or {})
        for name, acfg in list(agents.items()):
            if name in _SKIP_MODEL_OVERRIDE:
                continue
            if not isinstance(acfg, dict):
                continue
            if acfg.get("procedural"):
                continue
            merged = dict(acfg)
            merged["provider"] = "openrouter"
            merged["model"] = model_slug
            agents[name] = merged
        cfg["agents"] = agents
        return cfg

    pc.load_config = _merged_load_config  # type: ignore[method-assign]
    pc.clear_config_cache()
    logger.info("evals_openrouter_model_override", model=model_slug)
    try:
        yield
    finally:
        pc.load_config = original_load  # type: ignore[method-assign]
        pc.clear_config_cache()
