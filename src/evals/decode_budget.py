"""Comparison decode profiles — per-run decode budgets + sampling + thinking strip.

Implements the ``apply_decode_budget()`` control surface promised in
``openrouter_roster`` (issue #18 items 3-5): per-agent completion budgets,
IBM-mandated sampling for the Granite leg, a raised per-call timeout for
thinking-ON decodes, and the client-side ``<thinking>/<response>`` strip
OpenRouter cannot do server-side (no ``chat_template_kwargs`` passthrough).

Profiles are opt-in via ``run_task(decode_profile=...)`` /
``run_evals.py --decode-profile <key>``; without the flag nothing changes
(pipeline defaults apply, matching the Modal-leg posture for the Qwen twin).
"""

from __future__ import annotations

import contextlib
import json
import re
from typing import Any, Iterator

# Issue #18 §3: per-class thinking-ON completion budgets. Class ↔ specialist
# agent is a fixed 1:1 map (graph/build_graph dispatch), so budgets are keyed
# by the specialist agent that owns the class.
CLASS_BUDGETS: dict[str, int] = {
    "correspondence_specialist": 4096,
    "insurance_claims_specialist": 6144,
    "contracts_specialist": 8192,
    "merger_agreement_specialist": 8192,
    "corporate_records_specialist": 8192,
}

# Thinking-ON decodes blow past the vendored 120 s per-call default (the
# sandbox pins 600 s for exactly this reason — DMR-072 overlay comment).
COMPARISON_CALL_TIMEOUT_S = 600

THINKING_RE = re.compile(r"<thinking>.*?</thinking>", re.DOTALL | re.IGNORECASE)
RESPONSE_OPEN_RE = re.compile(r"<response>\s*", re.IGNORECASE)
RESPONSE_CLOSE_RE = re.compile(r"\s*</response>", re.IGNORECASE)


COMPARISON_PROFILES: dict[str, dict[str, Any]] = {
    # IBM-mandated decode posture (issue #18 §5): T=1.0, top_p=0.95, seed=42
    # best-effort. Applied on BOTH legs so the comparison stays paired.
    "granite-4.2-8b": {
        "model": "ibm-granite/granite-4.2-8b",
        "max_tokens_by_agent": dict(CLASS_BUDGETS),
        "sampling": {"temperature": 1.0, "top_p": 0.95, "seed": 42},
        "call_timeout_s": COMPARISON_CALL_TIMEOUT_S,
        # N=20 probe wave hard cap (SAND-027 doctrine; 50-doc waves are
        # board-gated — the report will read over_cap until re-capped).
        "cost_cap_usd": 1.50,
    },
    # Qwen twin keeps the pipeline call-site decode posture (temperature 0.1 —
    # what the Modal Qwen/Qwen3-8B leg ran) and only lifts budgets + timeout.
    "qwen3-8b": {
        "model": "qwen/qwen3-8b",
        "max_tokens_by_agent": dict(CLASS_BUDGETS),
        "sampling": None,
        "call_timeout_s": COMPARISON_CALL_TIMEOUT_S,
        "cost_cap_usd": 1.50,
    },
}


def get_profile(key: str | None) -> dict[str, Any] | None:
    """Resolve a comparison profile (None when unset/unknown)."""
    if not key:
        return None
    return COMPARISON_PROFILES.get(key.strip().lower())


def strip_thinking_spans(text: str) -> str:
    """Strip Granite-style thinking spans and unwrap <response> envelopes.

    Granite 4.2's chat template defaults thinking ON and wraps the answer in
    ``<response>…</response>``; OpenRouter cannot pass ``chat_template_kwargs``
    to disable it (issue #18 §4), so Leg B strips client-side before the JSON
    parse. Idempotent and a no-op on already-clean text.
    """
    if not text or ("<" not in text):
        return text
    out = THINKING_RE.sub("", text)
    if RESPONSE_OPEN_RE.search(out):
        out = RESPONSE_OPEN_RE.sub("", out, count=1)
        out = RESPONSE_CLOSE_RE.sub("", out, count=1)
    return out.strip()


def recover_prediction(prediction: dict[str, Any] | None) -> tuple[dict[str, Any] | None, bool]:
    """Re-parse a failed specialist prediction after stripping thinking spans.

    The pipeline's ``json.loads`` fails on a Granite ``<response>{json}</response>``
    envelope, returning ``{"_raw": …, "_parse_error": True}`` and zeroing the
    case at confidence 0.3. When the raw text carries the envelope, strip and
    re-parse. Returns ``(prediction, recovered)``.
    """
    if not isinstance(prediction, dict) or not prediction.get("_parse_error"):
        return prediction, False
    raw = prediction.get("_raw")
    if not isinstance(raw, str):
        return prediction, False
    cleaned = strip_thinking_spans(raw)
    try:
        parsed = json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        return prediction, False
    if not isinstance(parsed, dict):
        return prediction, False
    recovered = {**parsed, "_thinking_stripped": True}
    recovered.pop("_parse_error", None)
    recovered.pop("_raw", None)
    return recovered, True


@contextlib.contextmanager
def apply_decode_budget(profile: dict[str, Any] | None) -> Iterator[dict[str, Any]]:
    """Scope a comparison profile's decode controls to the enclosed block.

    Three mechanisms, all restored on exit:
    1. Taxonomy merge (same monkeypatch as ``apply_model_override``): per-agent
       ``max_tokens`` budgets + ``run_limits.llm_call_timeout_seconds``.
    2. Sampling injection: wraps ``llm.retry.retry_chat_completion`` (native
       agents) and the LangChain ``ChatOpenAI`` constructor so the profile's
       temperature/top_p/seed reach the wire even past explicit call-site
       values. ``None`` sampling (Qwen twin) injects nothing.
    3. Inert by default: ``profile=None`` yields immediately.
    """
    applied: dict[str, Any] = {"sampling_injected": False, "max_tokens_by_agent": {}}
    if not profile:
        yield applied
        return

    import pipeline.config as pc

    original_load = pc.load_config
    budgets = profile.get("max_tokens_by_agent") or {}

    def _merged_load_config(*args: Any, **kwargs: Any) -> dict[str, Any]:
        cfg = dict(original_load(*args, **kwargs) or {})
        agents = {name: dict(acfg) for name, acfg in (cfg.get("agents") or {}).items()}
        for name, acfg in agents.items():
            budget = budgets.get(name)
            if budget:
                acfg["max_tokens"] = budget
                applied["max_tokens_by_agent"][name] = budget
        cfg["agents"] = agents
        limits = dict(cfg.get("run_limits") or {})
        timeout = profile.get("call_timeout_s")
        if timeout:
            limits["llm_call_timeout_seconds"] = timeout
        cfg["run_limits"] = limits
        return cfg

    pc.load_config = _merged_load_config
    try:
        pc.clear_config_cache()
    except Exception:
        pass

    restore_fns: list[Any] = []
    sampling = profile.get("sampling")
    if sampling:
        restore_fns.append(_install_sampling_injection(sampling, applied))

    try:
        yield applied
    finally:
        for restore in restore_fns:
            try:
                restore()
            except Exception:
                pass
        pc.load_config = original_load
        try:
            pc.clear_config_cache()
        except Exception:
            pass


def _install_sampling_injection(sampling: dict[str, Any], applied: dict[str, Any]):
    """Force profile sampling params into every LLM call (both call families)."""
    import llm.retry as llm_retry

    original_retry = llm_retry.retry_chat_completion

    def _retry_with_sampling(client: Any, **kwargs: Any) -> Any:
        kwargs.update(sampling)
        applied["sampling_injected"] = True
        return original_retry(client, **kwargs)

    llm_retry.retry_chat_completion = _retry_with_sampling

    restore_langchain = None
    try:
        import langchain_agents.base_agent as lc_base

        original_cls = lc_base.ChatOpenAI

        class _SamplingChatOpenAI(original_cls):  # type: ignore[misc, valid-type]
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                kwargs.setdefault("temperature", sampling.get("temperature"))
                if sampling.get("top_p") is not None:
                    kwargs.setdefault("top_p", sampling["top_p"])
                model_kwargs = dict(kwargs.get("model_kwargs") or {})
                if sampling.get("seed") is not None:
                    model_kwargs.setdefault("seed", sampling["seed"])
                if model_kwargs:
                    kwargs["model_kwargs"] = model_kwargs
                applied["sampling_injected"] = True
                super().__init__(*args, **kwargs)

        lc_base.ChatOpenAI = _SamplingChatOpenAI

        def _restore() -> None:
            lc_base.ChatOpenAI = original_cls

        restore_langchain = _restore
    except Exception:
        restore_langchain = None

    def _restore_all() -> None:
        llm_retry.retry_chat_completion = original_retry
        if restore_langchain:
            restore_langchain()

    return _restore_all
