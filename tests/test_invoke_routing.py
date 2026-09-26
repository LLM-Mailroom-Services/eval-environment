"""Specialist dispatch wiring — no pipeline import required."""

from __future__ import annotations

from evals.invoke import TASK_SPECIALIST, _SPECIALIST_CLASSES, _specialist_for_class


def test_merger_agreement_uses_dedicated_specialist():
    assert TASK_SPECIALIST["merger_agreement"] == "merger_agreement_specialist"
    assert _specialist_for_class("merger_agreement") == "merger_agreement_specialist"
    assert "merger_agreement_specialist" in _SPECIALIST_CLASSES
