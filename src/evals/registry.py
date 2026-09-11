"""Task registry — every eval/pilot/calibration task in one table.

Task ids: ``<family>:<name>`` (e.g. ``eval:classify``, ``pilot:chain``,
``calibration:judge``). Each spec pins the node's stable observation name
(trace span name), the default subset, and the scorer family. The shared
runner (``evals.runner``) executes any spec; task modules under
``evals.tasks`` / ``evals.calibration`` add task-specific behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaskSpec:
    name: str
    family: str  # eval | pilot | calibration
    node_name: str  # stable observation name (trace span name)
    default_subset: str = "full"
    scorer: str = "generic"
    description: str = ""
    supports_agent_mode: bool = True
    tags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def task_id(self) -> str:
        return f"{self.family}:{self.name}"


EVAL_TASKS: tuple[TaskSpec, ...] = (
    TaskSpec("intake", "eval", "intake-document", "full", "intake",
             "Intake node: triage/clean/prepare invariants + triage agreement"),
    TaskSpec("classification", "eval", "classify-document", "full", "classification",
             "Classify node (sorter): doc class + subclass accuracy"),
    TaskSpec("contracts", "eval", "extract-fields", "class:contract", "extraction",
             "Contracts specialist (CUAD commercial contracts)"),
    TaskSpec("merger_agreement", "eval", "extract-fields", "class:merger_agreement", "extraction",
             "Merger agreement specialist (MAUD)"),
    TaskSpec("corporate_records", "eval", "extract-fields", "class:corporate_record", "extraction",
             "Corporate records specialist (S-1 exhibits)"),
    TaskSpec("correspondence", "eval", "extract-fields", "class:correspondence", "extraction",
             "Correspondence specialist (Enron)"),
    TaskSpec("insurance_claims", "eval", "extract-fields", "class:insurance_claim", "extraction",
             "Insurance claims specialist (CMS LOB)"),
    TaskSpec("judge_arbiter", "eval", "judge-verify", "fixtures", "judge",
             "Completeness judge verdicts vs review_expected"),
    TaskSpec("arbiter", "eval", "arbitrate-verdict", "fixtures", "arbiter",
             "Arbiter decisions vs arbiter_outcome"),
    TaskSpec("boss", "eval", "adjudicate-conflict", "fixtures", "boss",
             "Boss escalation decisions on conflicting fixtures"),
    TaskSpec("archivist", "eval", "archive-document", "fixtures", "archivist",
             "Archive conformance (manifest/audit/sha256/stage)"),
    TaskSpec("pipeline_chain", "eval", "document-pipeline", "pilot", "pipeline",
             "Full chained pipeline (13-node graph) end-to-end",
             supports_agent_mode=False),
)

PILOT_TASKS: tuple[TaskSpec, ...] = tuple(
    TaskSpec(
        spec.name,
        "pilot",
        spec.node_name,
        "pilot",
        spec.scorer,
        f"[pilot] {spec.description}",
        spec.supports_agent_mode,
    )
    for spec in EVAL_TASKS
)

CALIBRATION_TASKS: tuple[TaskSpec, ...] = (
    TaskSpec("classify", "calibration", "classify-document", "fixtures", "calibration_classify",
             "Confidence calibration: 2×2 grid, reliability, ECE, review-gate threshold"),
    TaskSpec("judge", "calibration", "judge-verify", "fixtures", "calibration_judge",
             "Completeness-threshold calibration vs review_expected"),
    TaskSpec("arbiter", "calibration", "arbitrate-verdict", "fixtures", "calibration_arbiter",
             "Decision-boundary calibration vs arbiter_outcome"),
    TaskSpec("retry", "calibration", "extract-fields", "fixtures", "calibration_retry",
             "Retry-pipeline calibration vs retry_expected/failure_stage"),
    TaskSpec("boss", "calibration", "adjudicate-conflict", "fixtures", "calibration_boss",
             "Conflict adjudication calibration (conflicting fixtures)"),
    TaskSpec("intake", "calibration", "intake-document", "fixtures", "calibration_intake",
             "Intake edge cases: messy/ambiguous + bundles + streams"),
    TaskSpec("archivist", "calibration", "archive-document", "fixtures", "calibration_archivist",
             "Archival edge cases (failure_stage=archival)"),
)

ALL_TASKS: dict[str, TaskSpec] = {
    spec.task_id: spec for spec in (*EVAL_TASKS, *PILOT_TASKS, *CALIBRATION_TASKS)
}


def get_task(task_id: str) -> TaskSpec:
    try:
        return ALL_TASKS[task_id.strip()]
    except KeyError:
        known = ", ".join(sorted(ALL_TASKS))
        raise KeyError(f"unknown task {task_id!r}; known: {known}") from None


def list_tasks() -> list[TaskSpec]:
    return [ALL_TASKS[key] for key in sorted(ALL_TASKS)]
