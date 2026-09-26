"""Contracts specialist eval — CUAD commercial-contract extraction."""

from __future__ import annotations

from evals.tasks.base import specialist_task

TASK = specialist_task(
    name="contracts",
    doc_class="contract",
    agent_role="contracts_specialist",
    description="Contracts specialist (CUAD commercial contracts)",
    default_subset="class:contract",
)
