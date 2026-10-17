"""Sandbox promotion must preserve existing frozen prompt assignments."""

import json
import runpy

import promote_sandbox_specialist as promotion
import pytest


@pytest.fixture
def frozen_catalog(monkeypatch, tmp_path):
    versions = {
        "judge-classification_v1": "original judge prompt",
        "merger_agreement_specialist_v1": "original merger prompt",
    }
    sources = {key: f"production:{key[:-3]}" for key in versions}
    monkeypatch.setattr(promotion, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(promotion.frozen_v1, "VERSIONS", versions)
    monkeypatch.setattr(promotion.frozen_v1, "SOURCE_OF", sources)
    monkeypatch.setattr(promotion, "fetch_sandbox_prompt", lambda *_: "new sandbox prompt")
    (tmp_path / "src/evals/prompts").mkdir(parents=True)
    promotion._write_frozen_catalog({
        key[:-3]: (text, *sources[key].split(":", 1))
        for key, text in versions.items()
    })
    return tmp_path


@pytest.mark.parametrize("role", [
    "judge_classification",
    "merger-agreement-specialist",
    "judge-classification",
    "merger_agreement_specialist",
])
def test_freeze_new_rejects_collisions_without_writes(frozen_catalog, role):
    before = {p: p.read_bytes() for p in frozen_catalog.rglob("*") if p.is_file()}
    with pytest.raises(SystemExit, match="already frozen|collides"):
        promotion.promote_freeze_new(
            role=role, sandbox_sha="test-sha", sandbox_stem="test", source_label="test"
        )
    after = {p: p.read_bytes() for p in frozen_catalog.rglob("*") if p.is_file()}
    assert after == before


def test_freeze_new_preserves_existing_prompts(frozen_catalog):
    result = promotion.promote_freeze_new(
        role="new-specialist", sandbox_sha="test-sha", sandbox_stem="test", source_label="test"
    )
    catalog = runpy.run_path(str(frozen_catalog / "src/evals/prompts/frozen_v1.py"))
    assert catalog["VERSIONS"] == {
        **promotion.frozen_v1.VERSIONS,
        "new-specialist_v1": "new sandbox prompt",
    }
    assert catalog["SOURCE_OF"] == {
        **promotion.frozen_v1.SOURCE_OF,
        "new-specialist_v1": "sandbox:test",
    }
    manifest = json.loads((frozen_catalog / "prompts/manifest.json").read_text())
    assert manifest["versions"]["new-specialist_v1"]["sha256"] == result["sha256"]
    assert result["manifest_versions"] == 3
    assert (frozen_catalog / "prompts/new-specialist_v1.md").is_file()
