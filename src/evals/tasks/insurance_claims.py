"""Insurance-claims specialist eval — CMS LOB claim extraction."""

from __future__ import annotations

from evals.tasks.base import specialist_task

TASK = specialist_task(
    name="insurance_claims",
    doc_class="insurance_claim",
    agent_role="insurance_claims_specialist",
    description="Insurance claims specialist (CMS LOB)",
    default_subset="class:insurance_claim",
)
