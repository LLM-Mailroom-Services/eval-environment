"""Merger-agreement specialist eval — MAUD extraction."""

from __future__ import annotations

from evals.tasks.base import specialist_task

TASK = specialist_task(
    name="merger_agreement",
    doc_class="merger_agreement",
    agent_role="merger_agreement_specialist",
    description="Merger agreement specialist (MAUD)",
    default_subset="class:merger_agreement",
)
