"""Shared live-source collection for the freeze script and the drift check.

Lives inside the prompts package so ``evals.prompts.lineage.verify_lineage``
and ``scripts/freeze_prompts.py`` agree on exactly what "the live pipeline
sources" are.
"""

from __future__ import annotations

import importlib
from collections.abc import Callable
from pathlib import Path


def collect(collect_frozen: Callable[[], dict[str, tuple[str, str, str]]]) -> dict[str, str]:
    """key -> live text, via the freeze map's collector."""
    return {f"{role}_v1": text for role, (text, _kind, _source) in collect_frozen().items()}


#: Every pipeline module the live-source path needs. The probe imports ALL of
#: them, not just ``llm.prompts``: a partially-installed pipeline that passed a
#: one-module probe would surface later as an unhandled ModuleNotFoundError
#: inside ``live_frozen_texts`` instead of a loud, classified failure.
REQUIRED_PIPELINE_MODULES = (
    "pipeline.env",
    "agents.intake",
    "llm.prompts",
    "scripts.sync_evaluators",
)


class PipelineSourceUnavailable(Exception):
    """No live pipeline source resolves at all.

    Neither an installed pipeline nor the editable sibling checkout
    ``../llm-mailroom/src`` is importable. Callers
    (``evals.prompts.lineage.verify_lineage``) treat this as an explicit,
    documented skip — there is no live source to diff against — not a
    silent vacuous pass.
    """


class PartialPipelineSourceError(Exception):
    """A pipeline source is importable but incomplete.

    Some of :data:`REQUIRED_PIPELINE_MODULES` import while the rest do not,
    even after the fallback paths are added. That is a partial install and
    must fail loudly, never silently narrow the drift check.
    """

    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        super().__init__(
            "pipeline sources importable but incomplete; could not resolve: " + ", ".join(missing)
        )


def _missing_modules(import_module: Callable[[str], object]) -> list[str]:
    """Import each required module; return the ones that fail to resolve.

    Only resolution failures (:class:`ModuleNotFoundError`, including a
    transitive dependency that is missing) count as "missing" — that is what
    distinguishes a partial install from healthy sources. Any other import
    error (a module that exists but crashes on import) propagates loud.
    """
    missing: list[str] = []
    for name in REQUIRED_PIPELINE_MODULES:
        try:
            import_module(name)
        except ModuleNotFoundError:
            missing.append(name)
    return missing


def resolve_pipeline_source(
    *,
    repo_root: str | Path,
    sys_path: list[str],
    import_module: Callable[[str], object] = importlib.import_module,
    exists: Callable[[str], bool] | None = None,
) -> tuple[str, list[str]]:
    """Make every required pipeline module importable; report where they came from.

    Returns:

    - ``("installed", [])`` — all of :data:`REQUIRED_PIPELINE_MODULES` import
      without touching ``sys_path`` (a pipeline installed in the active
      environment, e.g. a git-source override pinned to the release the
      frozen v1 snapshot was cut against). Installed wins over the sibling.
    - ``("sibling", added_paths)`` — the imports only resolve after inserting
      fallback paths: the repo's own ``src/`` tree and root, then the
      editable sibling checkout ``../llm-mailroom/src`` (when the pipeline is
      not importable). The old Digital-Mailroom monorepo layout
      (``../Digital-Mailroom/packages/llm-mailroom/src``) is gone and is no
      longer probed.

    Mutates ``sys_path`` in place (the caller owns it; tests may pass a
    throwaway list). Raises :class:`PartialPipelineSourceError` when a
    partial install is detected and :class:`PipelineSourceUnavailable` when
    no source resolves at all.
    """
    import_module = import_module or importlib.import_module
    exists = exists or (lambda path: Path(path).exists())

    missing = _missing_modules(import_module)
    if not missing:
        return "installed", []

    repo_root = Path(repo_root)
    # The sibling checkout is inserted last-at-0 so it keeps the HIGHEST path
    # priority: it must shadow any same-named package in this repo (e.g. this
    # repo's own top-level ``scripts/`` directory).
    added: list[str] = []
    fallback_paths = (
        str(repo_root / "src"),
        str(repo_root),
        str(repo_root.parent / "llm-mailroom" / "src"),
    )
    for path in fallback_paths:
        if exists(path) and path not in sys_path:
            sys_path.insert(0, path)
            added.append(path)

    missing = _missing_modules(import_module)
    if not missing:
        return "sibling", added

    importable = [name for name in REQUIRED_PIPELINE_MODULES if name not in missing]
    if importable:
        raise PartialPipelineSourceError(missing)
    raise PipelineSourceUnavailable(
        "no live pipeline source found: none of "
        + ", ".join(REQUIRED_PIPELINE_MODULES)
        + " resolves from the installed environment or from the fallback paths ("
        + "; ".join(fallback_paths)
        + ")"
    )


def live_frozen_texts() -> dict[str, str]:
    """The live texts behind every frozen key (drift-check source of truth).

    Resolution order: a pipeline installed in the active environment first
    (e.g. a git-source override pinned to the release the frozen v1 snapshot
    was cut against), then the editable sibling checkout ``../llm-mailroom/src``
    when the pipeline is not importable. The old Digital-Mailroom monorepo
    layout (``../Digital-Mailroom/packages/llm-mailroom/src``) is gone, so it
    is no longer probed. See :func:`resolve_pipeline_source` for the
    partial-install and not-found failure semantics.

    Import order note: the probe imports the pipeline modules *before*
    ``pipeline.env.load_env()`` runs. That order is safe because none of the
    required modules reads the environment at import time (``llm.prompts``
    imports structlog only, ``agents.intake`` reads env lazily inside its
    functions, and ``scripts.sync_evaluators`` calls ``load_env()`` itself at
    import), and ``load_env`` just merges ``.env`` into ``os.environ`` with
    ``override=False``. If a future pipeline module ever reads env at import
    time, call ``load_env()`` before the probe instead.
    """
    import sys

    repo_root = Path(__file__).resolve().parents[3]
    resolve_pipeline_source(repo_root=repo_root, sys_path=sys.path)

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
