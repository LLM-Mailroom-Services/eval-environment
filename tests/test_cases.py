"""Subset grammar + sampling tests (network-free)."""

from __future__ import annotations

import pytest

from evals.cases import parse_subset, stratified_sample


def test_parse_subset_basic():
    assert parse_subset(None) == {"kind": "full", "value": None}
    assert parse_subset("train") == {"kind": "train", "value": None}
    assert parse_subset("test") == {"kind": "test", "value": None}
    assert parse_subset("full") == {"kind": "full", "value": None}


def test_parse_subset_configs():
    for config in ("fixtures", "bundles", "streams"):
        assert parse_subset(config) == {"kind": "config", "value": config}


def test_parse_subset_corpus_aliases():
    for alias in ("pilot", "cuad", "enron", "claims"):
        assert parse_subset(alias)["kind"] == "corpus"


def test_parse_subset_class():
    assert parse_subset("class:contract") == {"kind": "class", "value": "contract"}
    with pytest.raises(ValueError):
        parse_subset("class:nope")


def test_parse_subset_subclass():
    spec = parse_subset("subclass:contract:nda")
    assert spec == {"kind": "subclass", "value": ("contract", "nda")}
    with pytest.raises(ValueError):
        parse_subset("subclass:nope:nda")
    with pytest.raises(ValueError):
        parse_subset("subclass:contract")


def test_parse_subset_unknown():
    with pytest.raises(ValueError):
        parse_subset("bogus")


def test_stratified_sample_even_per_stratum():
    rows = (
        [{"expected": "a", "i": i} for i in range(10)]
        + [{"expected": "b", "i": i} for i in range(10)]
        + [{"expected": "c", "i": i} for i in range(10)]
    )
    picked = stratified_sample(rows, 6, seed=42)
    assert len(picked) == 6
    counts = {}
    for row in picked:
        counts[row["expected"]] = counts.get(row["expected"], 0) + 1
    assert set(counts.values()) == {2}  # even allocation


def test_stratified_sample_deterministic():
    rows = [{"expected": "a", "i": i} for i in range(20)]
    assert stratified_sample(rows, 5, seed=7) == stratified_sample(rows, 5, seed=7)


def test_stratified_sample_handles_empty():
    assert stratified_sample([], 5, seed=1) == []
