"""Correspondence specialist eval — Enron / communication extraction."""

from __future__ import annotations

from evals.tasks.base import specialist_task

TASK = specialist_task(
    name="correspondence",
    doc_class="correspondence",
    agent_role="correspondence_specialist",
    description="Correspondence specialist (Enron)",
    default_subset="class:correspondence",
)
