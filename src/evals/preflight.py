"""Preflight checks — validate eval-run settings before any live API spend.

Real-mode runs MUST pass :func:`run_preflight` before the first LLM call.
Mock mode still runs a lightweight check (task framing, subset grammar,
prompt resolution) but never requires network credentials.

Sinks: Braintrust or Arize Phoenix only (Langfuse is out of scope here).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import structlog

from evals.cases import parse_subset
from evals.openrouter_roster import validate_model_slug
from evals.registry import TaskSpec, agents_for_node
from evals.tracing import resolve_backend

logger = structlog.get_logger(__name__)

# Trace backends this harness supports. Langfuse is intentionally absent.
SUPPORTED_TRACE_BACKENDS = frozenset({"auto", "braintrust", "phoenix", "none"})


@dataclass
class PreflightIssue:
    code: str
    message: str
    severity: str = "error"  # error | warning

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "severity": self.severity}


@dataclass
class PreflightReport:
    ok: bool
    mode: str
    task_id: str
    checks: list[dict[str, Any]] = field(default_factory=list)
    issues: list[PreflightIssue] = field(default_factory=list)
    framing: dict[str, Any] | None = None
    resolved: dict[str, Any] = field(default_factory=dict)

    @property
    def errors(self) -> list[PreflightIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[PreflightIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    def raise_if_failed(self) -> None:
        if self.ok:
            return
        detail = "; ".join(f"{i.code}: {i.message}" for i in self.errors)
        raise PreflightError(f"preflight failed for {self.task_id}: {detail}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "mode": self.mode,
            "task_id": self.task_id,
            "checks": list(self.checks),
            "issues": [i.as_dict() for i in self.issues],
            "framing": self.framing,
            "resolved": dict(self.resolved),
        }


class PreflightError(RuntimeError):
    """Raised when preflight blocks a real (or misconfigured) run."""


def _llm_credentials_present() -> tuple[bool, str]:
    """Primary OpenRouter key, or the gateway .env alternative."""
    if os.environ.get("OPENROUTER_API_KEY"):
        return True, "OPENROUTER_API_KEY"
    provider = (os.environ.get("DEFAULT_PROVIDER") or "").strip().lower()
    if provider == "generic" and os.environ.get("GENERIC_BASE_URL") and os.environ.get("GENERIC_API_KEY"):
        return True, "GENERIC_API_KEY (Vercel AI Gateway)"
    return False, "none"


def _env_truthy(name: str) -> bool:
    return (os.environ.get(name) or "").strip().lower() in {"1", "true", "yes", "on"}


def _real_spend_allowed() -> tuple[bool, str]:
    """Operator gates before any live LLM spend (see AGENTS.md)."""
    if _env_truthy("EVALS_REAL_RUNS_DISABLED"):
        return False, "EVALS_REAL_RUNS_DISABLED is set — unset it or use --mock"
    if _env_truthy("EVALS_SPEND_APPROVAL_REQUIRED"):
        if _env_truthy("EVALS_SPEND_APPROVED"):
            return True, "EVALS_SPEND_APPROVED"
        cap = (os.environ.get("EVALS_SPEND_APPROVED_USD") or "").strip()
        try:
            if cap and float(cap) > 0:
                return True, f"EVALS_SPEND_APPROVED_USD={cap}"
        except ValueError:
            pass
        return (
            False,
            "EVALS_SPEND_APPROVAL_REQUIRED is set — export EVALS_SPEND_APPROVED=1 "
            "or EVALS_SPEND_APPROVED_USD=<cap> before --real",
        )
    return True, "open"


def run_preflight(
    spec: TaskSpec,
    *,
    mock: bool,
    invoke_mode: str = "node",
    subset: str | None = None,
    model: str | None = None,
    prompt_version: str | None = None,
    prompt_source: str = "frozen",
    trace_backend: str | None = None,
    require_trace_sink: bool = False,
) -> PreflightReport:
    """Validate settings for one task run. Does not load the corpus or call LLMs."""
    mode = "mock" if mock else "real"
    report = PreflightReport(ok=True, mode=mode, task_id=spec.task_id)
    subset = subset or spec.default_subset

    # ── Task framing (always) ──────────────────────────────────────────
    framing: dict[str, Any] | None = None
    try:
        from evals.tasks import get_eval_task

        framing = get_eval_task(spec.task_id).framing()
        report.framing = framing
        report.checks.append({"name": "task_framing", "ok": True})
    except KeyError as exc:
        # Calibration / pilot aliases without a dedicated module are fine —
        # registry still owns them. Soft-warn only.
        report.checks.append({"name": "task_framing", "ok": True, "detail": str(exc)})
        report.issues.append(
            PreflightIssue("task_framing_missing", str(exc), severity="warning")
        )

    # ── Invoke mode ────────────────────────────────────────────────────
    if invoke_mode == "agent" and not spec.supports_agent_mode:
        report.issues.append(
            PreflightIssue(
                "invoke_mode",
                f"task {spec.task_id} does not support agent-mode invocation",
            )
        )
        report.checks.append({"name": "invoke_mode", "ok": False})
    else:
        report.checks.append({"name": "invoke_mode", "ok": True, "mode": invoke_mode})

    # ── Subset grammar ─────────────────────────────────────────────────
    try:
        parsed = parse_subset(subset)
        report.checks.append({"name": "subset_grammar", "ok": True, "parsed": parsed})
        report.resolved["subset"] = subset
        report.resolved["subset_parsed"] = parsed
    except ValueError as exc:
        report.issues.append(PreflightIssue("subset_grammar", str(exc)))
        report.checks.append({"name": "subset_grammar", "ok": False})

    # ── Model roster ───────────────────────────────────────────────────
    if model:
        try:
            validate_model_slug(model)
            report.checks.append({"name": "model_roster", "ok": True, "model": model})
            report.resolved["model"] = model
        except (KeyError, FileNotFoundError, ValueError) as exc:
            report.issues.append(PreflightIssue("model_roster", str(exc)))
            report.checks.append({"name": "model_roster", "ok": False})
    else:
        report.checks.append({"name": "model_roster", "ok": True, "model": None})

    # ── Prompt lineage ─────────────────────────────────────────────────
    if prompt_version:
        try:
            from evals.prompts.lineage import resolve

            resolved = resolve(prompt_version)
            report.checks.append(
                {
                    "name": "prompt_version",
                    "ok": True,
                    "key": resolved.key,
                    "lineage": resolved.lineage,
                    "sha256": getattr(resolved, "sha256", None),
                }
            )
            report.resolved["prompt_version"] = resolved.key
            report.resolved["prompt_lineage"] = resolved.lineage
        except Exception as exc:
            report.issues.append(
                PreflightIssue("prompt_version", f"cannot resolve {prompt_version!r}: {exc}")
            )
            report.checks.append({"name": "prompt_version", "ok": False})
    else:
        report.checks.append(
            {"name": "prompt_version", "ok": True, "prompt_source": prompt_source}
        )
        report.resolved["prompt_source"] = prompt_source

    # ── Trace backend ──────────────────────────────────────────────────
    explicit = (trace_backend or "").strip().lower() or None
    if explicit and explicit not in SUPPORTED_TRACE_BACKENDS:
        report.issues.append(
            PreflightIssue(
                "trace_backend",
                f"unsupported sink {explicit!r}; supported: "
                f"{sorted(SUPPORTED_TRACE_BACKENDS)} (Langfuse is out of scope)",
            )
        )
        report.checks.append({"name": "trace_backend", "ok": False})
        backend = "none"
    else:
        try:
            backend = resolve_backend(explicit)
            report.checks.append(
                {"name": "trace_backend", "ok": True, "requested": explicit or "auto", "resolved": backend}
            )
            report.resolved["trace_backend"] = backend
        except ValueError as exc:
            report.issues.append(PreflightIssue("trace_backend", str(exc)))
            report.checks.append({"name": "trace_backend", "ok": False})
            backend = "none"

    if explicit == "braintrust" and not os.environ.get("BRAINTRUST_API_KEY"):
        report.issues.append(
            PreflightIssue(
                "braintrust_key",
                "EVALS_TRACE_BACKEND/ --trace-backend=braintrust requires BRAINTRUST_API_KEY",
            )
        )
        report.checks.append({"name": "braintrust_key", "ok": False})
    elif backend == "braintrust" and not os.environ.get("BRAINTRUST_API_KEY"):
        report.issues.append(
            PreflightIssue(
                "braintrust_key",
                "resolved sink is braintrust but BRAINTRUST_API_KEY is unset",
                severity="warning",
            )
        )
        report.checks.append({"name": "braintrust_key", "ok": False, "severity": "warning"})
    else:
        report.checks.append({"name": "braintrust_key", "ok": True})

    if require_trace_sink and backend == "none" and not mock:
        report.issues.append(
            PreflightIssue(
                "trace_sink_required",
                "require_trace_sink=True but resolved backend is none "
                "(set BRAINTRUST_API_KEY or --trace-backend phoenix)",
            )
        )

    # ── Real-mode credentials (HARD gate) ──────────────────────────────
    if not mock:
        ok_spend, spend_detail = _real_spend_allowed()
        if ok_spend:
            report.checks.append({"name": "real_spend_guard", "ok": True, "detail": spend_detail})
        else:
            report.issues.append(PreflightIssue("real_spend_guard", spend_detail))
            report.checks.append({"name": "real_spend_guard", "ok": False})
        ok_creds, source = _llm_credentials_present()
        if not ok_creds:
            report.issues.append(
                PreflightIssue(
                    "llm_credentials",
                    "real mode requires OPENROUTER_API_KEY (primary) or "
                    "DEFAULT_PROVIDER=generic + GENERIC_BASE_URL + GENERIC_API_KEY",
                )
            )
            report.checks.append({"name": "llm_credentials", "ok": False})
        else:
            report.checks.append({"name": "llm_credentials", "ok": True, "source": source})
            report.resolved["llm_credential_source"] = source
        # Accidental spend guard: dry observability provider still OK, but warn
        # when no sink will capture traces for a paid run.
        if backend == "none":
            report.issues.append(
                PreflightIssue(
                    "no_trace_sink",
                    "real run will spend LLM tokens with trace backend=none — "
                    "set BRAINTRUST_API_KEY or --trace-backend phoenix to capture spans",
                    severity="warning",
                )
            )
    else:
        report.checks.append({"name": "llm_credentials", "ok": True, "skipped": "mock"})

    # ── Agent catalog alignment ────────────────────────────────────────
    catalog = agents_for_node(spec.node_name)
    report.checks.append(
        {
            "name": "agent_catalog",
            "ok": True,
            "node": spec.node_name,
            "agents": catalog.get("agents") or [],
            "llm": catalog.get("llm"),
        }
    )
    report.resolved["agents"] = catalog.get("agents") or []

    report.ok = not report.errors
    if not report.ok:
        logger.warning(
            "evals_preflight_failed",
            task=spec.task_id,
            errors=[i.as_dict() for i in report.errors],
        )
    else:
        logger.info(
            "evals_preflight_ok",
            task=spec.task_id,
            mode=mode,
            warnings=len(report.warnings),
        )
    return report
