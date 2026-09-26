"""OpenRouter model roster — validation, pricing, snapshot export."""

from __future__ import annotations

import pytest

from evals.openrouter_roster import (
    estimate_cost_usd,
    get_model,
    list_models,
    load_roster,
    roster_for_snapshot,
    validate_model_slug,
)


def test_roster_includes_granite():
    slug = "ibm-granite/granite-4.2-8b"
    meta = get_model(slug)
    assert meta["input_per_million"] == 0.06
    assert meta["output_per_million"] == 0.25
    assert meta["context_tokens"] == 131072
    assert meta.get("modality") == "text"


def test_validate_rejects_unknown():
    with pytest.raises(KeyError, match="unknown OpenRouter model"):
        validate_model_slug("not/a-real-model")


def test_estimate_cost_granite():
    cost = estimate_cost_usd(1_000_000, 1_000_000, "ibm-granite/granite-4.2-8b")
    assert cost == pytest.approx(0.31, rel=1e-6)


def test_list_models_sorted():
    slugs = [m["slug"] for m in list_models()]
    assert slugs == sorted(slugs)
    assert "ibm-granite/granite-4.2-8b" in slugs


def test_snapshot_shape():
    snap = roster_for_snapshot()
    assert snap["provider"] == "openrouter"
    granite = next(m for m in snap["models"] if m["slug"] == "ibm-granite/granite-4.2-8b")
    assert granite["label"] == "IBM Granite 4.2 8B"


def test_load_roster_cached():
    assert load_roster()["models"]
