"""Corporate-records specialist eval — S-1 exhibit / record extraction."""

from __future__ import annotations

from evals.tasks.base import specialist_task

TASK = specialist_task(
    name="corporate_records",
    doc_class="corporate_record",
    agent_role="corporate_records_specialist",
    description="Corporate records specialist (S-1 exhibits)",
    default_subset="class:corporate_record",
)
