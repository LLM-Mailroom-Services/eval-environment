"""Direct OpenRouter specialist extraction — no LangChain / graph nodes.

System message = the designated lineage prompt for that specialist.
User message = extract the registered entities from the included document.
The OpenAI-compatible client is the pipeline's OpenRouter wrapper so Braintrust
``wrap_openai`` still records the LLM call under the specialist parent span,
and ``pipeline.limits.record_usage`` still captures tokens/cost.
"""

from __future__ import annotations

import json
from typing import Any

import structlog

from evals.decode_budget import CLASS_BUDGETS, strip_thinking_spans
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

_JSON_NOTE = (
    "\n\nOutput must be a single json object conforming to the provided "
    "json schema (response_format is json_object)."
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
) -> str:
    fields = ", ".join(sorted(LIVE_SCHEMA_FIELDS.get(doc_class) or ())) or "(schema fields)"
    handoff = f"`{doc_class}`"
    if subclass:
        handoff += f" (subclass `{subclass}`)"
    return (
        f"Extract the registered entities from this document. "
        f"The document class is {handoff}. "
        f"Return one complete JSON object with every live schema field "
        f"({fields}). Unstated values must be null or []. Never invent "
        f"facts from letterhead, filename, or general knowledge.\n\n"
        f"Document:\n{text}"
    )


def extract_entities(
    specialist: str,
    case: dict[str, Any],
) -> dict[str, Any]:
    """One OpenRouter chat completion: specialist system prompt + document user msg."""
    doc_class = str(case.get("expected_doc_class") or "")
    text = str(case.get("text") or "")
    subclass = case.get("expected_subclass")
    system = specialist_system_prompt(specialist)
    assert_prompt_matches_class(specialist, doc_class, system)
    system = system + _JSON_NOTE
    user = user_extract_message(doc_class=doc_class, text=text, subclass=subclass)
    client, model, max_tokens, temperature = _client_for(specialist)
    logger.info(
        "specialist_openrouter_call",
        agent=specialist,
        prompt_key=prompt_key_for(specialist),
        doc_class=doc_class,
        chars=len(text),
        model=model,
        max_tokens=max_tokens,
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system + "\nReply with ONLY a JSON object."},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
    _record(response, model=model, agent=specialist)
    extracted = _parse_json(_message_content(response))
    confidence = extracted.get("confidence") if isinstance(extracted, dict) else None
    return {
        "extracted_data": extracted,
        "extraction_confidence": confidence,
        "doc_type": doc_class,
        "specialist": specialist,
        "model": model,
        "prompt_key": prompt_key_for(specialist),
    }


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
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        start, end = content.find("{"), content.rfind("}")
        if start >= 0 and end > start:
            try:
                parsed = json.loads(content[start : end + 1])
            except json.JSONDecodeError:
                return {"_parse_error": True, "confidence": 0.0}
        else:
            return {"_parse_error": True, "confidence": 0.0}
    if not isinstance(parsed, dict):
        return {"_parse_error": True, "confidence": 0.0}
    return parsed
