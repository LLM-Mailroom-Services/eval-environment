"""Direct OpenRouter specialist extraction — no LangChain / graph nodes.

System message = the designated lineage prompt for that specialist.
User message = extract the registered entities from the included document.
Long merger agreements are split into overlapping chunks so one Qwen
completion can finish valid JSON (qwen/qwen3-8b silently caps near 8192
completion tokens). Chunk LLM calls stay nested under the one specialist
parent span; scoring still sees one merged prediction per document.
"""

from __future__ import annotations

import json
import math
import re
from typing import Any

import structlog

from evals.decode_budget import (
    CLASS_BUDGETS,
    active_sampling,
    mark_sampling_consumed,
    strip_thinking_spans,
)
from evals.extraction_scope import LIVE_SCHEMA_FIELDS
from evals.prompts import registry as prompts_registry
from evals.prompts.lineage import resolve, roles

logger = structlog.get_logger(__name__)

# Hub class → designated specialist role / frozen prompt key. These are 1:1;
# contracts_specialist never stands in for merger_agreement (or any other class).
CLASS_SPECIALIST: dict[str, str] = {
    "contract": "contracts_specialist",
    "merger_agreement": "merger_agreement_specialist",
    "corporate_record": "corporate_records_specialist",
    "correspondence": "correspondence_specialist",
    "insurance_claim": "insurance_claims_specialist",
}

CLASS_PROMPT_STEM: dict[str, str] = {
    "contract": "You are the contracts specialist.",
    "merger_agreement": "You are the merger-agreement specialist.",
    "corporate_record": "You are the corporate-records specialist.",
    "correspondence": "You are the correspondence specialist.",
    "insurance_claim": "You are the insurance-claims specialist.",
}

# Soft cap on source chars sent in one completion. Confirmed by a real n=2
# smoke test (run 20260927T014814Z): qwen/qwen3-8b has a 131,072-token
# *context* window, but its actual *completion* ceiling is ~8,192 tokens
# regardless of the requested max_tokens (OpenRouter's model page states
# "supports up to 8,192 completion tokens"). A single unchunked call for a
# ~390k-char merger doc truncated at exactly 8,195 completion tokens on both
# smoke-test docs -> parse_error -> 0 score. So for qwen3-8b, keep the small
# chunk size: each 48k-char chunk's extraction stays far under that ceiling
# (~1,800 completion tokens/chunk observed), which is what actually scored
# (0.529 f1 on contract_128). Do not raise this for qwen3-8b without
# re-validating against the real completion cap, not just the context window.
CHUNK_CHARS: dict[str, int] = {
    "merger_agreement": 48_000,
}
DEFAULT_CHUNK_CHARS = 120_000

# Some models have a much larger real completion ceiling than qwen3-8b's
# ~8,192 tokens, so the whole document fits in one call safely. Per
# OpenRouter's model pages: qwen/qwen3.7-flash has a 1,000,000-token context
# window and supports up to 65,536 completion tokens — 465k chars (the
# largest doc in the pinned merger_agreement N=20) is a small fraction of
# either budget. Keyed by exact model id (not a substring match) so a future
# lower-budget "qwen3.7-*" variant does not inherit this by accident.
LARGE_COMPLETION_MODELS: dict[str, int] = {
    "qwen/qwen3.7-flash": 480_000,
}


def _chunk_limit_for(doc_class: str, model: str | None) -> int:
    override = LARGE_COMPLETION_MODELS.get((model or "").strip().lower())
    if override is not None:
        return override
    return CHUNK_CHARS.get(doc_class, DEFAULT_CHUNK_CHARS)
CHUNK_OVERLAP = 1_500
CHUNK_HEADER_CHARS = 3_500

_HUGE_INT_RE = re.compile(r"-?\d{4001,}")
_ARTICLE_SPLIT = re.compile(
    r"(?=\n[ \t]*(?:ARTICLE|Article|SECTION|Section)\s+(?:[IVXLCDM]+|\d+))",
)

_JSON_NOTE = (
    "\n\nOutput must be a single json object conforming to the provided "
    "json schema (response_format is json_object). Keep values compact: "
    "clause answers are short labels or quotes of at most 80 characters; "
    "never transcribe an article; never emit a number longer than 20 digits. "
    "List fields (e.g. maud_clauses, keywords, parties) must contain at most "
    "10 of the most salient items each, not an exhaustive enumeration."
)

# Set by invoke.install_mocks — never hits the network in mock mode.
_mock_client: Any = None


def set_mock_client(client: Any | None) -> None:
    global _mock_client
    _mock_client = client


def specialist_for_class(doc_class: str) -> str:
    """The only specialist allowed to score this Hub document class."""
    role = CLASS_SPECIALIST.get(doc_class)
    if not role:
        raise KeyError(f"no designated specialist for doc_class {doc_class!r}")
    return role


def prompt_key_for(specialist: str) -> str:
    keys = prompts_registry.active_keys() or roles()
    key = keys.get(specialist) or roles().get(specialist)
    if not key:
        raise KeyError(f"no prompt key for specialist {specialist!r}")
    return key


def specialist_system_prompt(specialist: str) -> str:
    """The designated lineage stem for this specialist (frozen unless overridden)."""
    return resolve(prompt_key_for(specialist)).text


def assert_prompt_matches_class(specialist: str, doc_class: str, system: str) -> None:
    """Fail loud if the contracts (or any other) stem is used on the wrong class."""
    expected_role = specialist_for_class(doc_class)
    if specialist != expected_role:
        raise RuntimeError(
            f"specialist {specialist!r} cannot extract class {doc_class!r}; "
            f"designated specialist is {expected_role!r}"
        )
    stem = CLASS_PROMPT_STEM[doc_class]
    if not system.startswith(stem):
        raise RuntimeError(
            f"prompt for {specialist} does not start with designated stem {stem!r}"
        )
    for other_class, other_stem in CLASS_PROMPT_STEM.items():
        if other_class == doc_class:
            continue
        if system.startswith(other_stem):
            raise RuntimeError(
                f"prompt for class {doc_class} is the {other_class} specialist stem"
            )


def user_extract_message(
    *,
    doc_class: str,
    text: str,
    subclass: str | None = None,
    chunk_index: int | None = None,
    chunk_count: int | None = None,
    chunk_span: str | None = None,
) -> str:
    fields = ", ".join(sorted(LIVE_SCHEMA_FIELDS.get(doc_class) or ())) or "(schema fields)"
    handoff = f"`{doc_class}`"
    if subclass:
        handoff += f" (subclass `{subclass}`)"
    chunk_line = ""
    if chunk_count and chunk_count > 1 and chunk_index is not None:
        chunk_line = (
            f"This is chunk {chunk_index + 1} of {chunk_count} of a longer "
            f"{doc_class.replace('_', ' ')}"
            + (f" ({chunk_span})." if chunk_span else ".")
            + " Extract only facts visible in this chunk. "
        )
    return (
        f"Extract the registered entities from this document. "
        f"The document class is {handoff}. "
        f"{chunk_line}"
        f"Return one complete JSON object with every live schema field "
        f"({fields}). Unstated values must be null or []. Never invent "
        f"facts from letterhead, filename, or general knowledge. "
        f"Keep JSON compact — short quotes, no full-article transcription.\n\n"
        f"Document:\n{text}"
    )


def needed_chunks(n_chars: int, max_chars: int) -> int:
    """Minimum windows to cover ``n_chars`` without exceeding ``max_chars``."""
    if n_chars <= 0 or max_chars <= 0:
        return 1
    if n_chars <= max_chars:
        return 1
    return math.ceil(n_chars / max_chars)


def llm_call_budget(needed: int) -> int:
    """Hard per-row LLM call cap: one retry slot per coverage chunk.

    Used to be ``ceil(needed * 1.15)`` — one shared spare call for the
    whole document, sized for occasional split-math error. A concurrency=8
    qwen/qwen3-8b repro showed that was not enough: under concurrent
    provider load, EACH chunk call can independently come back as a
    coherent-looking but non-JSON 200 response (not just network
    exceptions), and a 2+-chunk document needing two retries had only one
    spare slot (``specialist_llm_retry_blocked_by_budget``), silently
    losing the second chunk's contribution. Budget now guarantees every
    coverage call its own single retry: ``needed * 2``.
    """
    needed = max(int(needed), 1)
    return needed * 2


def chunk_document(text: str, *, max_chars: int, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split a long source into the minimum covering windows (ARTICLE-aware)."""
    if max_chars <= 0 or len(text) <= max_chars:
        return [text] if text else [""]
    needed = needed_chunks(len(text), max_chars)
    overlap = _clamp_overlap(max_chars, overlap)
    packed = _pack_articles(text, max_chars=max_chars, overlap=overlap)
    pieces = packed if packed else _windows(text, max_chars=max_chars, overlap=overlap)
    if len(pieces) != needed or any(len(p) > max_chars for p in pieces):
        size = max(1, (len(text) + needed - 1) // needed)
        pieces = [text[i : i + size] for i in range(0, len(text), size)]
    if len(pieces) > needed:
        pieces = pieces[:needed]
        pieces[-1] = text[sum(len(p) for p in pieces[:-1]) :]
    return pieces


def extract_entities(
    specialist: str,
    case: dict[str, Any],
) -> dict[str, Any]:
    """OpenRouter chat completion(s): designated system prompt + document user msg."""
    doc_class = str(case.get("expected_doc_class") or "")
    text = str(case.get("text") or "")
    subclass = case.get("expected_subclass")
    system = specialist_system_prompt(specialist)
    assert_prompt_matches_class(specialist, doc_class, system)
    system = system + _JSON_NOTE
    client, model, max_tokens, temperature = _client_for(specialist)
    # Mandated profile sampling (e.g. Granite T=1.0/top_p=0.95/seed=42) must
    # reach the wire here too: this direct-client path bypasses both wrapped
    # families in ``decode_budget._install_sampling_injection``, so without
    # this call-time override specialists would silently run at the taxonomy
    # temperature (0.1) while the report printed the profile override.
    top_p: float | None = None
    seed: int | None = None
    sampling = active_sampling()
    if sampling:
        temperature = float(sampling.get("temperature", temperature))
        if sampling.get("top_p") is not None:
            top_p = float(sampling["top_p"])
        if sampling.get("seed") is not None:
            seed = int(sampling["seed"])
        mark_sampling_consumed()
    limit = _chunk_limit_for(doc_class, model)
    needed = needed_chunks(len(text), limit)
    budget = llm_call_budget(needed)
    pieces = chunk_document(text, max_chars=limit)
    if len(pieces) > budget:
        pieces = pieces[:budget]
    if len(pieces) > 1:
        header = text[:CHUNK_HEADER_CHARS]
        decorated: list[str] = []
        for i, piece in enumerate(pieces):
            if i == 0 or piece.startswith(header[: min(len(header), 80)]):
                decorated.append(piece)
            else:
                decorated.append(
                    header
                    + "\n\n[...document continues; extract from this span...]\n\n"
                    + piece
                )
        pieces = decorated
    meter = _RowCallBudget(budget)
    logger.info(
        "specialist_openrouter_call",
        agent=specialist,
        prompt_key=prompt_key_for(specialist),
        doc_class=doc_class,
        chars=len(text),
        chunks=len(pieces),
        needed_chunks=needed,
        llm_call_budget=budget,
        chunk_limit=limit,
        model=model,
        max_tokens=max_tokens,
    )
    parsed_chunks: list[dict[str, Any]] = []
    for i, piece in enumerate(pieces):
        if meter.remaining <= 0:
            logger.warning(
                "specialist_llm_call_budget_exhausted",
                agent=specialist,
                used=meter.used,
                budget=budget,
                chunk=i,
                chunks=len(pieces),
            )
            break
        user = user_extract_message(
            doc_class=doc_class,
            text=piece,
            subclass=subclass,
            chunk_index=i,
            chunk_count=len(pieces),
            chunk_span=f"part {i + 1}/{len(pieces)}",
        )
        parsed_chunks.append(
            _complete_json(
                client,
                system=system,
                user=user,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                seed=seed,
                agent=specialist,
                meter=meter,
            )
        )
    extracted = merge_extracted(parsed_chunks)
    confidence = extracted.get("confidence") if isinstance(extracted, dict) else None
    return {
        "extracted_data": extracted,
        "extraction_confidence": confidence,
        "doc_type": doc_class,
        "specialist": specialist,
        "model": model,
        "prompt_key": prompt_key_for(specialist),
        "chunks": len(pieces),
        "needed_chunks": needed,
        "llm_call_budget": budget,
        "llm_calls": meter.used,
    }


def merge_extracted(parts: list[dict[str, Any]]) -> dict[str, Any]:
    """Union non-empty fields across chunk extractions. One document, one payload."""
    good = [
        p for p in parts
        if isinstance(p, dict) and not p.get("_parse_error")
    ]
    if not good:
        return {"_parse_error": True, "confidence": 0.0}
    out: dict[str, Any] = {}
    for payload in good:
        for key, value in payload.items():
            if key.startswith("_") or key == "reasoning":
                continue
            out[key] = _merge_value(out.get(key), value)
    confs = [
        float(p["confidence"])
        for p in good
        if isinstance(p.get("confidence"), (int, float))
    ]
    if confs:
        out["confidence"] = round(sum(confs) / len(confs), 4)
    return out


def _merge_value(current: Any, incoming: Any) -> Any:
    if _is_empty(incoming):
        return current
    if _is_empty(current):
        return incoming
    if isinstance(current, dict) and isinstance(incoming, dict):
        keys = set(current) | set(incoming)
        return {k: _merge_value(current.get(k), incoming.get(k)) for k in keys}
    if isinstance(current, list) and isinstance(incoming, list):
        return _merge_lists(current, incoming)
    if isinstance(current, str) and isinstance(incoming, str):
        return current if len(current) >= len(incoming) else incoming
    return current


def _merge_lists(left: list[Any], right: list[Any]) -> list[Any]:
    out: list[Any] = []
    seen: set[str] = set()
    for item in [*left, *right]:
        try:
            sig = json.dumps(item, sort_keys=True, default=str)
        except TypeError:
            sig = str(item)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(item)
    return out


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _clamp_overlap(max_chars: int, overlap: int) -> int:
    if max_chars <= 2:
        return 0
    return min(max(overlap, 0), max_chars // 5)


def _pack_articles(text: str, *, max_chars: int, overlap: int) -> list[str] | None:
    parts = _ARTICLE_SPLIT.split(text)
    if len(parts) < 3:
        return None
    bins: list[str] = []
    buf = parts[0]
    for part in parts[1:]:
        if buf and len(buf) + len(part) > max_chars:
            bins.append(buf)
            tail = buf[-overlap:] if overlap and overlap < len(buf) else ""
            buf = tail + part
        else:
            buf += part
    if buf:
        bins.append(buf)
    if len(bins) <= 1:
        return None
    expanded: list[str] = []
    for block in bins:
        if len(block) <= max_chars:
            expanded.append(block)
        else:
            expanded.extend(_windows(block, max_chars=max_chars, overlap=overlap))
    return expanded or None


def _windows(text: str, *, max_chars: int, overlap: int) -> list[str]:
    overlap = _clamp_overlap(max_chars, overlap)
    step = max(max_chars - overlap, 1)
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += step
    return chunks


def _completion_kwargs(
    *,
    model: str,
    system: str,
    user: str,
    max_tokens: int,
    temperature: float,
    json_object: bool,
    top_p: float | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    # Profile-mandated sampling (Granite leg); omitted entirely when no
    # profile is active so default-decode runs keep their exact wire shape.
    if top_p is not None:
        kwargs["top_p"] = top_p
    if seed is not None:
        kwargs["seed"] = seed
    if json_object:
        kwargs["response_format"] = {"type": "json_object"}
    # Qwen3 defaults thinking ON; <think> blobs poison json_object parse and
    # burn the completion budget. Ask OpenRouter to exclude reasoning tokens.
    if "qwen" in (model or "").lower():
        kwargs["extra_body"] = {
            "reasoning": {"exclude": True},
            "chat_template_kwargs": {"enable_thinking": False},
        }
    return kwargs


class _RowCallBudget:
    """Hard stop on OpenRouter create() calls for one scored document row."""

    def __init__(self, limit: int) -> None:
        self.limit = max(int(limit), 1)
        self.used = 0

    @property
    def remaining(self) -> int:
        return max(self.limit - self.used, 0)

    def consume(self) -> bool:
        if self.used >= self.limit:
            return False
        self.used += 1
        return True


def _complete_json(
    client: Any,
    *,
    system: str,
    user: str,
    model: str,
    max_tokens: int,
    temperature: float,
    agent: str,
    meter: _RowCallBudget,
    top_p: float | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    """One chat completion, JSON-parsed, with a single meter-gated retry.

    The retry fires on EITHER a network exception OR a "successful" 200
    response that still fails to parse as JSON. The latter is not
    hypothetical: under concurrent load (multiple simultaneous OpenRouter
    requests for a cheap/free-tier model like qwen/qwen3-8b), the provider
    can return coherent-looking but non-JSON placeholder text (e.g.
    ``// JSON output here (as per the instructions) //``) even with
    ``response_format=json_object`` and thinking explicitly disabled —
    confirmed via a concurrency=8 repro that showed 0 parse errors at
    concurrency=1 vs. 18/20 at concurrency=8 on the same model/prompts/docs.
    A single retry (falling back to a plain, non-json_object completion
    with an explicit "reply with ONLY a JSON object" instruction) is cheap
    insurance against that provider-side flakiness.
    """
    if not meter.consume():
        return {"_parse_error": True, "confidence": 0.0, "_budget_exhausted": True}

    def _attempt(*, plain_fallback: bool) -> dict[str, Any]:
        response = client.chat.completions.create(
            **_completion_kwargs(
                model=model,
                system=system if not plain_fallback else system + "\nReply with ONLY a JSON object.",
                user=user,
                max_tokens=max_tokens,
                temperature=temperature,
                json_object=not plain_fallback,
                top_p=top_p,
                seed=seed,
            )
        )
        _record(response, model=model, agent=agent)
        return _parse_json(_message_content(response))

    try:
        parsed = _attempt(plain_fallback=False)
        needs_retry = bool(parsed.get("_parse_error"))
    except Exception:
        parsed = {"_parse_error": True, "confidence": 0.0}
        needs_retry = True

    if not needs_retry:
        return parsed

    if not meter.consume():
        logger.warning(
            "specialist_llm_retry_blocked_by_budget",
            agent=agent,
            used=meter.used,
            budget=meter.limit,
        )
        parsed["_budget_exhausted"] = True
        return parsed

    try:
        return _attempt(plain_fallback=True)
    except Exception:
        logger.warning("specialist_llm_retry_failed", agent=agent, exc_info=True)
        return {"_parse_error": True, "confidence": 0.0}


def _client_for(specialist: str) -> tuple[Any, str, int, float]:
    if _mock_client is not None:
        return _mock_client, "mock-model", CLASS_BUDGETS.get(specialist, 4096), 0.1
    from llm.client import get_llm
    from pipeline.config import get_agent_config

    client, model = get_llm(specialist)
    cfg = get_agent_config(specialist)
    max_tokens = int(cfg.get("max_tokens") or CLASS_BUDGETS.get(specialist, 4096))
    temperature = float(cfg.get("temperature") if cfg.get("temperature") is not None else 0.1)
    return client, model, max_tokens, temperature


def _record(response: Any, *, model: str, agent: str) -> None:
    try:
        from pipeline.limits import record_usage

        record_usage(getattr(response, "usage", None), model=model, agent=agent)
    except Exception:
        logger.warning("specialist_usage_record_failed", agent=agent, exc_info=True)


def _message_content(response: Any) -> str:
    try:
        return str(response.choices[0].message.content or "")
    except Exception:
        return ""


def _parse_json(raw: str) -> dict[str, Any]:
    content = strip_thinking_spans(raw).strip()
    if content.startswith("```"):
        content = content.strip("`")
        content = content.removeprefix("json").strip()
    # Truncated completions often end on a 8k-digit "number". Python 3.11+
    # raises ValueError (not JSONDecodeError) at 4300 digits — that must
    # never escape as evals_case_failed.
    content = _HUGE_INT_RE.sub("null", content)
    try:
        parsed = json.loads(content)
    except (json.JSONDecodeError, ValueError, RecursionError):
        start, end = content.find("{"), content.rfind("}")
        if start >= 0 and end > start:
            try:
                parsed = json.loads(content[start : end + 1])
            except (json.JSONDecodeError, ValueError, RecursionError):
                return {"_parse_error": True, "confidence": 0.0}
        else:
            return {"_parse_error": True, "confidence": 0.0}
    if not isinstance(parsed, dict):
        return {"_parse_error": True, "confidence": 0.0}
    return parsed
