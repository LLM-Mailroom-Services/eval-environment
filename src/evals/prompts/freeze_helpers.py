"""Shared live-source collection for the freeze script and the drift check.

Lives inside the prompts package so ``evals.prompts.lineage.verify_lineage``
and ``scripts/freeze_prompts.py`` agree on exactly what "the live pipeline
sources" are.
"""

from __future__ import annotations

from collections.abc import Callable


def collect(collect_frozen: Callable[[], dict[str, tuple[str, str, str]]]) -> dict[str, str]:
    """key -> live text, via the freeze map's collector."""
    return {f"{role}_v1": text for role, (text, _kind, _source) in collect_frozen().items()}


def live_frozen_texts() -> dict[str, str]:
    """The live texts behind every frozen key (drift-check source of truth).

    Resolution order: a pipeline installed in the active environment first
    (e.g. a git-source override pinned to the release the frozen v1 snapshot
    was cut against), then the editable sibling checkout ``../llm-mailroom/src``
    when ``mailroom`` is not installed. The old Digital-Mailroom monorepo
    layout (``../Digital-Mailroom/packages/llm-mailroom/src``) is gone, so it
    is no longer probed.
    """
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[3]
    try:
        import llm.prompts  # noqa: F401  # already importable (installed or on sys.path)
    except ModuleNotFoundError:
        # Fall back to the sibling checkout's source tree.
        sibling_src = str(repo_root.parent / "llm-mailroom" / "src")
        for path in (str(repo_root / "src"), str(repo_root), sibling_src):
            if Path(path).exists() and path not in sys.path:
                sys.path.insert(0, path)

    from pipeline.env import load_env

    load_env()

    from agents.intake import INTAKE_SYSTEM_PROMPT
    from llm.prompts import prompt_templates
    from scripts.sync_evaluators import PIPELINE_PROMPT, QUALITY_PROMPT

    templates = prompt_templates()

    sources = {
        "sorter_v1": templates["sorter"],
        "contracts_specialist_v1": templates["contracts_specialist"],
        "corporate_records_specialist_v1": templates["corporate_records_specialist"],
        "correspondence_specialist_v1": templates["correspondence_specialist"],
        "insurance_claims_specialist_v1": templates["insurance_claims_specialist"],
        "sorter_reviewer_v1": templates["sorter_reviewer"],
        "arbiter_v1": templates["arbiter"],
        "boss_v1": templates["boss"],
        "judge_v1": templates["judge"],
        "judge-classification_v1": templates["judge-classification"],
        "judge-correctness_v1": templates["judge-correctness"],
        "intake_v1": INTAKE_SYSTEM_PROMPT,
        "pipeline_verdict_v1": PIPELINE_PROMPT,
        "pipeline_quality_v1": QUALITY_PROMPT,
    }
    return sources