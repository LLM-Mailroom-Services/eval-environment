"""Direct OpenRouter specialist extraction — no LangChain nodes."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from evals.decode_budget import apply_decode_budget, get_profile
from evals.prompts import frozen_v1
from evals.prompts.registry import activate, deactivate
from evals.specialist_llm import (
    CLASS_PROMPT_STEM,
    CLASS_SPECIALIST,
    chunk_document,
    extract_entities,
    llm_call_budget,
    merge_extracted,
    needed_chunks,
    prompt_key_for,
    set_mock_client,
    specialist_system_prompt,
    user_extract_message,
)


def test_merger_system_prompt_is_frozen_maud_not_cuad():
    keys = activate("frozen")
    try:
        text = specialist_system_prompt("merger_agreement_specialist")
        assert text == frozen_v1.VERSIONS["merger_agreement_specialist_v1"]
        assert "Agreement and Plan of Merger" in text
        assert "You are the contracts specialist" not in text
        cuad = specialist_system_prompt("contracts_specialist")
        assert cuad == frozen_v1.VERSIONS["contracts_specialist_v1"]
        assert cuad != text
        assert keys["merger_agreement_specialist"] == "merger_agreement_specialist_v1"
    finally:
        deactivate()


def test_user_message_asks_to_extract_included_document():
    msg = user_extract_message(
        doc_class="merger_agreement",
        text="AGREEMENT AND PLAN OF MERGER of Parent and Target.",
        subclass="all_cash",
    )
    assert "Extract the registered entities from this document" in msg
    assert "AGREEMENT AND PLAN OF MERGER of Parent and Target." in msg
    assert "merger_agreement" in msg
    assert "maud_clauses" in msg
    assert "cuad_family" not in msg


def test_each_class_uses_its_designated_frozen_prompt():
    activate("frozen")
    try:
        stems = {}
        for doc_class, role in CLASS_SPECIALIST.items():
            text = specialist_system_prompt(role)
            key = prompt_key_for(role)
            assert key == f"{role}_v1"
            assert text == frozen_v1.VERSIONS[key]
            assert text.startswith(CLASS_PROMPT_STEM[doc_class])
            stems[doc_class] = text
        assert len(set(stems.values())) == 5
        assert stems["merger_agreement"].startswith("You are the merger-agreement specialist.")
        assert not stems["merger_agreement"].startswith("You are the contracts specialist.")
        assert "Agreement and Plan of Merger" in stems["merger_agreement"]
    finally:
        deactivate()


def test_wrong_specialist_for_class_is_rejected():
    activate("frozen")
    try:
        set_mock_client(MagicMock())
        try:
            extract_entities(
                "contracts_specialist",
                {"text": "PLAN OF MERGER", "expected_doc_class": "merger_agreement"},
            )
            raise AssertionError("contracts specialist must not extract merger_agreement")
        except RuntimeError as exc:
            assert "designated specialist is 'merger_agreement_specialist'" in str(exc)
    finally:
        set_mock_client(None)
        deactivate()


def test_extract_entities_openrouter_shape_not_langchain():
    activate("frozen")
    try:
        captured: dict = {}

        def _create(**kwargs):
            captured["messages"] = kwargs["messages"]
            captured["model"] = kwargs["model"]
            mock = MagicMock()
            mock.choices[0].message.content = '{"document_name": "Plan of Merger", "confidence": 0.4}'
            mock.usage.prompt_tokens = 11
            mock.usage.completion_tokens = 5
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        out = extract_entities(
            "merger_agreement_specialist",
            {
                "text": "AGREEMENT AND PLAN OF MERGER",
                "expected_doc_class": "merger_agreement",
                "expected_subclass": "all_cash",
            },
        )
        assert out["specialist"] == "merger_agreement_specialist"
        assert out["prompt_key"] == "merger_agreement_specialist_v1"
        assert out["extracted_data"]["document_name"] == "Plan of Merger"
        system = captured["messages"][0]["content"]
        user = captured["messages"][1]["content"]
        assert system.startswith("You are the merger-agreement specialist")
        assert "Extract the registered entities" in user
        assert "AGREEMENT AND PLAN OF MERGER" in user
        assert captured["model"] == "mock-model"
        assert out["chunks"] == 1
        assert out["llm_calls"] == 1
        assert out["llm_call_budget"] == 2
        assert "extra_body" not in captured  # mock-model is not qwen
    finally:
        set_mock_client(None)
        deactivate()


def test_chunk_document_splits_long_merger_on_articles():
    body = "\n".join(
        f"\nARTICLE {i}\n" + ("merger consideration cash.\n" * 40)
        for i in range(1, 12)
    )
    preamble = "AGREEMENT AND PLAN OF MERGER\n" + body
    chunks = chunk_document(preamble, max_chars=800)
    assert len(chunks) > 1
    assert sum(len(c) for c in chunks) >= len(preamble)
    assert any("ARTICLE 1" in c or "ARTICLE 2" in c for c in chunks)


def test_chunk_document_windows_when_no_articles():
    text = "x" * 10_000
    chunks = chunk_document(text, max_chars=3_000, overlap=500)
    assert len(chunks) == needed_chunks(10_000, 3_000)
    assert "".join(chunks) == text or sum(len(c) for c in chunks) >= len(text)


def test_merge_extracted_unions_chunk_fields():
    merged = merge_extracted(
        [
            {"document_name": "Plan", "parties": ["Parent"], "maud_clauses": {"mae": "yes"}, "confidence": 0.4},
            {"document_name": None, "parties": ["Target"], "maud_clauses": {"fiduciary_out": "yes"}, "confidence": 0.8},
            {"_parse_error": True, "confidence": 0.0},
        ]
    )
    assert merged["document_name"] == "Plan"
    assert merged["parties"] == ["Parent", "Target"]
    assert merged["maud_clauses"]["mae"] == "yes"
    assert merged["maud_clauses"]["fiduciary_out"] == "yes"
    assert merged["confidence"] == 0.6


def test_long_merger_issues_one_call_per_chunk_same_system_prompt(monkeypatch):
    activate("frozen")
    try:
        from evals import specialist_llm as sl

        monkeypatch.setitem(sl.CHUNK_CHARS, "merger_agreement", 1_200)
        captured: list[dict] = []

        def _create(**kwargs):
            captured.append(kwargs)
            n = len(captured)
            mock = MagicMock()
            mock.choices[0].message.content = json.dumps(
                {"document_name": "Plan", "parties": [f"P{n}"], "confidence": 0.5}
            )
            mock.usage.prompt_tokens = 3
            mock.usage.completion_tokens = 2
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        text = ("\nARTICLE 1\n" + ("cash merger of Parent and Target.\n" * 40)) * 8
        out = extract_entities(
            "merger_agreement_specialist",
            {"text": text, "expected_doc_class": "merger_agreement"},
        )
        assert 1 < len(captured) <= out["llm_call_budget"]
        assert out["chunks"] == needed_chunks(len(text), 1_200)
        assert out["llm_calls"] == len(captured)
        assert out["llm_calls"] <= out["llm_call_budget"]
        assert out["prompt_key"] == "merger_agreement_specialist_v1"
        assert out["extracted_data"]["parties"][0] == "P1"
        for call in captured:
            system = call["messages"][0]["content"]
            user = call["messages"][1]["content"]
            assert system.startswith("You are the merger-agreement specialist")
            assert "You are the contracts specialist" not in system
            assert "chunk" in user.lower()
            assert "Extract the registered entities" in user
    finally:
        set_mock_client(None)
        deactivate()


def test_merger_chunk_chars_stays_small_for_qwen3_8b_real_completion_cap():
    """qwen/qwen3-8b truncates completions at ~8,192 tokens regardless of
    max_tokens (confirmed live: run 20260927T014814Z, a single unchunked
    ~390k-char merger call truncated at exactly 8,195 completion tokens on
    both docs -> parse_error -> 0 score). CHUNK_CHARS must stay small enough
    that per-chunk completions land far under that ceiling — do not let this
    silently balloon back toward "one call per doc" for this model."""
    import evals.specialist_llm as sl

    assert sl.CHUNK_CHARS["merger_agreement"] == 48_000
    assert needed_chunks(464_926, sl.CHUNK_CHARS["merger_agreement"]) > 1


def test_merger_large_completion_model_covers_pinned_corpus_in_one_call():
    """qwen/qwen3.7-flash (1M context / 65,536 completion tokens per
    OpenRouter) safely covers the largest pinned merger doc (464,926 chars)
    in a single completion — the model-specific override that lets it stand
    in without the qwen3-8b chunking penalty."""
    import evals.specialist_llm as sl

    limit = sl._chunk_limit_for("merger_agreement", "qwen/qwen3.7-flash")
    assert limit >= 465_000
    assert needed_chunks(464_926, limit) == 1
    assert llm_call_budget(1) == 2
    # Model-agnostic default (or an unrecognized model) keeps the small,
    # validated chunk size — no accidental inheritance of the override.
    assert sl._chunk_limit_for("merger_agreement", "qwen/qwen3-8b") == 48_000
    assert sl._chunk_limit_for("merger_agreement", None) == 48_000


def test_merger_granite_uses_large_context_chunks_not_qwen3_8b_penalty():
    import evals.specialist_llm as sl

    limit = sl._chunk_limit_for("merger_agreement", "ibm-granite/granite-4.2-8b")
    assert limit > sl.CHUNK_CHARS["merger_agreement"]
    assert needed_chunks(464_926, limit) <= 2
    assert needed_chunks(200_000, limit) == 1


def test_deepseek_v41_one_coverage_call_all_pinned_n20_maxima():
    import evals.specialist_llm as sl

    model = "deepseek/deepseek-v4.1-flash"
    for doc_class, n_chars in (
        ("contract", 173_240),
        ("corporate_record", 312_280),
        ("merger_agreement", 464_926),
    ):
        limit = sl._chunk_limit_for(doc_class, model)
        assert needed_chunks(n_chars, limit) == 1
        assert llm_call_budget(1) == 2


def test_correspondence_never_inherits_merger_large_completion_span():
    import evals.specialist_llm as sl

    assert sl._chunk_limit_for("correspondence", "ibm-granite/granite-4.2-8b") == (
        sl.SINGLE_COVERAGE_CHUNK_LIMIT
    )
    assert needed_chunks(34_310, sl._chunk_limit_for("correspondence", "qwen/qwen3-8b")) == 1


def test_needed_chunks_and_call_budget_grant_one_retry_per_chunk():
    assert needed_chunks(48_000, 48_000) == 1
    assert llm_call_budget(1) == 2
    assert needed_chunks(387_592, 48_000) == 9
    assert llm_call_budget(9) == 18
    assert llm_call_budget(8) == 16
    text = "y" * 387_592
    pieces = chunk_document(text, max_chars=48_000)
    assert len(pieces) == 9
    assert all(len(p) <= 48_000 for p in pieces[:-1])


def test_qwen_think_span_stripped_before_json_parse():
    activate("frozen")
    try:
        def _create(**kwargs):
            mock = MagicMock()
            mock.choices[0].message.content = (
                '<think>{"not": "the answer"}</think>{"document_name": "Plan", "confidence": 0.4}'
            )
            mock.usage.prompt_tokens = 4
            mock.usage.completion_tokens = 8
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        out = extract_entities(
            "merger_agreement_specialist",
            {"text": "PLAN OF MERGER", "expected_doc_class": "merger_agreement"},
        )
        assert out["extracted_data"]["document_name"] == "Plan"
        assert "_parse_error" not in out["extracted_data"]
    finally:
        set_mock_client(None)
        deactivate()


def test_qwen_completion_disables_thinking():
    from evals.specialist_llm import _completion_kwargs

    kw = _completion_kwargs(
        model="qwen/qwen3-8b",
        system="sys",
        user="usr",
        max_tokens=16,
        temperature=0.1,
        json_object=True,
    )
    assert kw["extra_body"]["chat_template_kwargs"]["enable_thinking"] is False
    assert kw["extra_body"]["reasoning"]["exclude"] is True
    activate("frozen")
    try:
        def _create(**kwargs):
            mock = MagicMock()
            mock.choices[0].message.content = (
                '{"document_name": "Plan", "parties": ["Parent"], "n": '
                + ("9" * 8191)
                + "}"
            )
            mock.usage.prompt_tokens = 4
            mock.usage.completion_tokens = 8192
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        out = extract_entities(
            "merger_agreement_specialist",
            {"text": "PLAN OF MERGER", "expected_doc_class": "merger_agreement"},
        )
        assert out["extracted_data"].get("document_name") == "Plan"
        assert out["extracted_data"].get("parties") == ["Parent"]
        assert "_parse_error" not in out["extracted_data"]
    finally:
        set_mock_client(None)
        deactivate()


def test_unterminated_huge_int_json_is_parse_error_not_exception():
    activate("frozen")
    try:
        def _create(**kwargs):
            mock = MagicMock()
            mock.choices[0].message.content = '{"document_name": "Plan", "n": ' + ("9" * 8191)
            mock.usage.prompt_tokens = 4
            mock.usage.completion_tokens = 8192
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        out = extract_entities(
            "merger_agreement_specialist",
            {"text": "PLAN OF MERGER", "expected_doc_class": "merger_agreement"},
        )
        assert out["extracted_data"].get("_parse_error") is True
    finally:
        set_mock_client(None)
        deactivate()


def test_row_llm_call_budget_blocks_retry_runaway():
    activate("frozen")
    try:
        captured = {"n": 0}

        def _create(**kwargs):
            captured["n"] += 1
            raise RuntimeError("simulated openrouter failure")

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        text = "short merger"
        out = extract_entities(
            "merger_agreement_specialist",
            {"text": text, "expected_doc_class": "merger_agreement"},
        )
        assert out["needed_chunks"] == 1
        assert out["llm_call_budget"] == 2
        assert captured["n"] == 2
        assert out["llm_calls"] == 2
        assert out["extracted_data"].get("_parse_error") is True
    finally:
        set_mock_client(None)
        deactivate()


def test_complete_json_retries_on_garbled_non_json_200_response():
    """Regression for the concurrency=8 qwen3-8b repro: a 200 response whose
    content is coherent-looking placeholder text (not JSON) must trigger the
    same meter-gated retry as a network exception, not just be scored 0."""
    activate("frozen")
    try:
        calls: list[dict] = []

        def _create(**kwargs):
            calls.append(kwargs)
            mock = MagicMock()
            if len(calls) == 1:
                mock.choices[0].message.content = (
                    '">// JSON output here (as per the instructions) //</json>'
                )
            else:
                mock.choices[0].message.content = (
                    '{"document_name": "Plan of Merger", "confidence": 0.6}'
                )
            mock.usage.prompt_tokens = 11
            mock.usage.completion_tokens = 5
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        out = extract_entities(
            "merger_agreement_specialist",
            {"text": "AGREEMENT AND PLAN OF MERGER", "expected_doc_class": "merger_agreement"},
        )
        assert len(calls) == 2
        assert out["llm_calls"] == 2
        assert out["extracted_data"].get("_parse_error") is not True
        assert out["extracted_data"]["document_name"] == "Plan of Merger"
        # The retry falls back to a plain (non-json_object) completion with
        # an explicit instruction, same strategy as the exception-retry path.
        assert calls[1].get("response_format") is None
        assert "Reply with ONLY a JSON object." in calls[1]["messages"][0]["content"]
    finally:
        set_mock_client(None)
        deactivate()


def test_complete_json_gives_up_when_retry_also_garbled():
    activate("frozen")
    try:
        calls: list[dict] = []

        def _create(**kwargs):
            calls.append(kwargs)
            mock = MagicMock()
            mock.choices[0].message.content = "still not json, sorry"
            mock.usage.prompt_tokens = 11
            mock.usage.completion_tokens = 5
            return mock

        client = MagicMock()
        client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
        set_mock_client(client)
        out = extract_entities(
            "merger_agreement_specialist",
            {"text": "AGREEMENT AND PLAN OF MERGER", "expected_doc_class": "merger_agreement"},
        )
        assert len(calls) == 2
        assert out["llm_calls"] == 2
        assert out["extracted_data"].get("_parse_error") is True
    finally:
        set_mock_client(None)
        deactivate()


def _mock_extract_client(calls: list[dict]) -> MagicMock:
    def _create(**kwargs):
        calls.append(kwargs)
        mock = MagicMock()
        mock.choices[0].message.content = '{"document_name": "Memo", "confidence": 0.5}'
        mock.usage.prompt_tokens = 11
        mock.usage.completion_tokens = 5
        return mock

    client = MagicMock()
    client.chat.completions.create.side_effect = lambda **kw: _create(**kw)
    return client


def test_extract_entities_applies_active_profile_sampling_to_wire():
    """Mandated profile sampling must reach the specialist direct-client path.

    Regression: ``apply_decode_budget`` only wrapped ``retry_chat_completion``
    + LangChain ``ChatOpenAI``, which ``specialist_llm._complete_json`` never
    uses — so the Granite T=1.0/top_p=0.95/seed=42 mandate silently stayed at
    the taxonomy temperature (0.1) while the report printed the override.
    """
    activate("frozen")
    try:
        calls: list[dict] = []
        set_mock_client(_mock_extract_client(calls))
        with apply_decode_budget(get_profile("granite-4.2-8b")) as applied:
            out = extract_entities(
                "correspondence_specialist",
                {"text": "MEMO", "expected_doc_class": "correspondence"},
            )
            assert out["extracted_data"]["document_name"] == "Memo"
            assert calls[0]["temperature"] == 1.0
            assert calls[0]["top_p"] == 0.95
            assert calls[0]["seed"] == 42
            assert applied["sampling_injected"] is True
    finally:
        set_mock_client(None)
        deactivate()


def test_extract_entities_wire_shape_unchanged_without_profile():
    """No active profile: taxonomy temperature, no top_p/seed keys on the wire."""
    activate("frozen")
    try:
        calls: list[dict] = []
        set_mock_client(_mock_extract_client(calls))
        with apply_decode_budget(get_profile("qwen3-8b")) as applied:
            extract_entities(
                "correspondence_specialist",
                {"text": "MEMO", "expected_doc_class": "correspondence"},
            )
            assert calls[0]["temperature"] == 0.1
            assert "top_p" not in calls[0]
            assert "seed" not in calls[0]
            assert applied["sampling_injected"] is False
    finally:
        set_mock_client(None)
        deactivate()
