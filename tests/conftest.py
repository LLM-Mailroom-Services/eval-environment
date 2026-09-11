"""Shared test fixtures — hermetic env for every test (no network, no tracing,
redirected experiment log, isolated MAILROOM_BASE_DIR)."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _hermetic_env(monkeypatch):
    tmp = tempfile.mkdtemp(prefix="mailroom-evals-test-")
    monkeypatch.setenv("MAILROOM_BASE_DIR", tmp)
    monkeypatch.setenv("OBSERVABILITY_PROVIDER", "none")
    monkeypatch.setenv("EVALS_TRACE_BACKEND", "none")
    monkeypatch.setenv("PHOENIX_TRACING", "disabled")
    monkeypatch.delenv("BRAINTRUST_API_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    monkeypatch.setenv("EXPERIMENT_LOG_PATH", str(Path(tmp) / "experiment_log.jsonl"))
    monkeypatch.setenv("EXPERIMENT_LOG_MD_PATH", str(Path(tmp) / "experiment_log.md"))
    monkeypatch.setenv("EVALS_EXPERIMENTS_DIR", str(Path(tmp) / "experiments"))
    yield


@pytest.fixture
def sample_case() -> dict:
    return {
        "id": "corpus:ground_truth:train:test_doc.txt",
        "filename": "test_doc.txt",
        "text": "MASTER SERVICES AGREEMENT between Acme Corp and Beta LLC, effective January 1, 2026. Payment terms are Net 30.",
        "expected_doc_class": "contract",
        "expected_subclass": "master_services_agreement",
        "expected_specialist": "contracts_specialist",
        "expected_stage": "archived",
        "expected_fields": {"parties": ["Acme Corp", "Beta LLC"], "payment_terms": "Net 30"},
        "source": "mailroom-corpus",
        "config": "ground_truth",
        "split": "train",
        "row": {"document_id": "DOC-test", "source_corpus": "unit_test"},
    }


@pytest.fixture
def fixture_case() -> dict:
    """A fixtures-config calibration cell (wrong_high)."""
    return {
        "id": "corpus:fixtures:train:calibration-contract-wrong_high",
        "filename": "calibration-contract-wrong_high.txt",
        "text": "AMENDMENT NO. 2 to the Master Services Agreement dated January 15. Section 4 is deleted and replaced with: 'Payment terms are Net 45.'",
        "expected_doc_class": "contract",
        "expected_subclass": None,
        "expected_specialist": "contracts_specialist",
        "expected_stage": "review",
        "review_expected": True,
        "retry_expected": False,
        "fixture_kind": "conflicting",
        "calibration_cell": "wrong_high",
        "probes_confidence": 0.985,
        "failure_stage": None,
        "arbiter_outcome": None,
        "expected_fields": {},
        "source": "mailroom-corpus",
        "config": "fixtures",
        "split": "train",
        "row": {},
    }
