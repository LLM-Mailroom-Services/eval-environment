"""GEPA Braintrust backlog grounding (hermetic — no network)."""

from __future__ import annotations

from evals.gepa import braintrust_backlog as bt


def _sample_root(*, overall: float = 0.34) -> dict:
    return {
        "is_root": True,
        "root_span_id": "root-abc",
        "span_id": "span-eval-1",
        "input": {
            "case_ref": "corpus:ground_truth:train:doc#ca64ce537c8b",
            "chars": 78,
            "doc_text_sha256": "ca64ce537c8bd98cdcfa4e68ea1434ff4a915b4f00a5ee84d3e01e13addd92f9",
        },
        "metadata": {
            "run_id": "20260927T105317Z-eval-correspondence",
            "task": "eval:correspondence",
            "specialist": "correspondence_specialist",
            "prompt_version": "correspondence_specialist_v1",
            "prompt_key": "correspondence_specialist_v1",
            "model": "deepseek/deepseek-v4.1-flash",
            "filename": "dorland-c/_sent_mail/78.",
        },
        "expected": {
            "expected_doc_class": "correspondence",
            "expected_subclass": "email",
            "expected_fields": {"communication_type": "email", "intent": "other"},
        },
        "output": {
            "extracted_data": {"sender": "Chris", "communication_type": "email", "confidence": 0.75},
            "scores": {"overall_score": overall, "extraction_f1": 0.13},
            "specialist": "correspondence_specialist",
        },
        "scores": {"overall_score": overall, "extraction_f1": 0.13},
        "span_attributes": {"type": "eval", "name": "correspondence_specialist"},
    }


def _sample_llm(parent_span_id: str) -> dict:
    return {
        "is_root": False,
        "span_parents": [parent_span_id],
        "metadata": {"model": "deepseek/deepseek-v4.1-flash"},
        "output": [
            {
                "message": {
                    "content": '{"sender":"Chris","confidence":0.75}',
                    "reasoning": "Recipient is null because no named addressee in the short note.",
                }
            }
        ],
        "span_attributes": {"type": "llm", "name": "Chat Completion"},
    }


def test_index_experiment_spans():
    root = _sample_root()
    llm = _sample_llm("span-eval-1")
    roots, llm_by_parent = bt.index_experiment_spans([root, llm])
    assert "root-abc" in roots
    assert llm_by_parent["span-eval-1"][0]["span_attributes"]["type"] == "llm"


def test_root_to_observe_row_includes_trace_excerpt():
    root = _sample_root()
    llm = _sample_llm("span-eval-1")
    row = bt.root_to_observe_row(root, run_id="20260927T105317Z-eval-correspondence", llm_spans=[llm])
    assert row["braintrust"]["experiment"] == "20260927T105317Z-eval-correspondence"
    assert row["braintrust"]["prompt_version"] == "correspondence_specialist_v1"
    assert "Recipient is null" in (row["trace_excerpt"]["reasoning"] or "")
    assert row["scores"]["overall_score"] == 0.34


def test_merge_observe_rows_keeps_worst_score():
    good = bt.root_to_observe_row(_sample_root(overall=0.79), run_id="run-a", llm_spans=[])
    bad = bt.root_to_observe_row(_sample_root(overall=0.2), run_id="run-b", llm_spans=[])
    merged = bt.merge_observe_rows([good, bad])
    assert len(merged) == 1
    assert merged[0]["scores"]["overall_score"] == 0.2


def test_discover_braintrust_specialist_runs():
    runs = [
        {
            "run_id": "20260927T105317Z-eval-correspondence",
            "task": "correspondence",
            "mode": "real",
            "trace_ids": {"backend": "braintrust", "experiment": "20260927T105317Z-eval-correspondence"},
        },
        {"run_id": "mock-run", "task": "correspondence", "mode": "mock", "trace_ids": {"backend": "braintrust"}},
    ]
    by_task = bt.discover_braintrust_specialist_runs(runs)
    assert len(by_task["correspondence"]) == 1
    assert by_task["correspondence"][0]["experiment"] == "20260927T105317Z-eval-correspondence"
