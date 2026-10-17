"""Sandbox promotions use real lineage gates and write only isolated catalogs."""

from __future__ import annotations

import hashlib
import io
import json
import runpy
import sys
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

import pytest

import promote_sandbox_specialist as promote
from evals.prompts import frozen_v1, lineage, mutations


@pytest.fixture
def catalog(tmp_path, monkeypatch):
    """A small frozen lineage, including a role needing Python identifier escaping."""
    (tmp_path / "src/evals/prompts").mkdir(parents=True)
    (tmp_path / "prompts").mkdir()
    monkeypatch.setattr(promote, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(mutations, "MUTATIONS_PATH", tmp_path / "prompts/mutations.json")
    monkeypatch.setattr(lineage, "_production", lambda: {})
    monkeypatch.setattr(frozen_v1, "VERSIONS", {
        "contracts_specialist_v1": "Original contract prompt.\nKeep its provenance.\n",
        "judge-classification_v1": "Judge 'quotes', \\slashes, and café.\n",
    })
    monkeypatch.setattr(frozen_v1, "SOURCE_OF", {
        "contracts_specialist_v1": "production:contracts_specialist",
        "judge-classification_v1": "evaluator:judge:classification",
    })
    return tmp_path


def catalog_files(root):
    return {str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*") if path.is_file()}


def test_fetch_sandbox_prompt_uses_pinned_revision_and_preserves_utf8(monkeypatch):
    text = "  Prompt with café and € amounts.\n\n"
    response = io.BytesIO(text.encode("utf-8"))
    fetch = Mock(return_value=response)
    monkeypatch.setattr(promote.urllib.request, "urlopen", fetch)

    assert promote.fetch_sandbox_prompt("pinned-revision", "insurance_simplified") == text

    fetch.assert_called_once_with(
        "https://raw.githubusercontent.com/Exios66/local-mailroom-sandbox/"
        "pinned-revision/config/prompts/insurance_simplified.txt",
        timeout=60,
    )
    assert response.closed


@pytest.mark.parametrize("error", [
    URLError("offline"),
    HTTPError("https://example.invalid/prompt", 404, "missing", None, None),
])
def test_fetch_sandbox_prompt_propagates_download_errors(monkeypatch, error):
    monkeypatch.setattr(promote.urllib.request, "urlopen", Mock(side_effect=error))
    with pytest.raises(type(error)) as caught:
        promote.fetch_sandbox_prompt("revision", "missing")
    assert caught.value is error


def test_promote_mutation_persists_full_replacement_and_preserves_history(catalog, monkeypatch):
    previous = {
        "key": "judge-classification_v2", "parent": "judge-classification_v1",
        "version": 2, "text": "Previous mutation", "note": "keep this history",
    }
    mutations.MUTATIONS_PATH.write_text(json.dumps({"mutations": [previous]}))
    original = dict(frozen_v1.VERSIONS)
    text = "Entirely new CUAD instructions — €0 is a stated amount.\n"
    fetch = Mock(return_value=text)
    monkeypatch.setattr(promote, "fetch_sandbox_prompt", fetch)

    meta = promote.promote_mutation(
        parent_key="contracts_specialist_v1", new_key="contracts_specialist_v2",
        sandbox_sha="revision", sandbox_stem="contracts_simplified", note="catalog promotion",
    )

    fetch.assert_called_once_with("revision", "contracts_simplified")
    assert meta["text"] == text
    assert meta["parent"] == "contracts_specialist_v1"
    assert meta["version"] == 2
    assert meta["note"] == "catalog promotion"
    assert meta["sha256"] == hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert json.loads(mutations.MUTATIONS_PATH.read_text())["mutations"] == [previous, meta]
    assert lineage.resolve("contracts_specialist_v2").text == text
    assert (catalog / "prompts/contracts_specialist_v2.md").read_text() == (
        f"# contracts_specialist_v2\n\n{text}"
    )
    assert (catalog / "prompts/judge-classification_v2.md").read_text() == (
        "# judge-classification_v2\n\nPrevious mutation\n"
    )
    assert frozen_v1.VERSIONS == original
    assert not (catalog / "src/evals/prompts/frozen_v1.py").exists()


@pytest.mark.parametrize(("parent", "new_key", "error", "message"), [
    ("contracts_specialist_v1", "contracts_specialist_v1", mutations.MutationError, "already"),
    ("contracts_specialist_v1", "contracts_specialist_v3", mutations.MutationError, "naming"),
    ("contracts_specialist_v1", "different_role_v2", mutations.MutationError, "naming"),
    ("judge-classification_v1", "judge-classification_v2", mutations.MutationError, "already"),
    ("missing_v1", "missing_v2", KeyError, "unknown prompt"),
])
def test_rejected_mutation_leaves_catalog_unchanged(
    catalog, monkeypatch, parent, new_key, error, message,
):
    mutations.MUTATIONS_PATH.write_text(json.dumps({"mutations": [{
        "key": "judge-classification_v2", "parent": "judge-classification_v1",
        "version": 2, "text": "Existing mutation",
    }]}))
    monkeypatch.setattr(promote, "fetch_sandbox_prompt", Mock(return_value="New text"))
    before = catalog_files(catalog)

    with pytest.raises(error, match=message):
        promote.promote_mutation(
            parent_key=parent, new_key=new_key, sandbox_sha="revision",
            sandbox_stem="contracts_simplified", note="must be rejected",
        )

    assert catalog_files(catalog) == before


@pytest.mark.parametrize("prior_manifest", [None, {
    "lineage_id": "existing-lineage", "frozen_version": 1,
    "pipeline_git_commit": "original-pipeline-revision", "derivation": "original recipe",
    "frozen_at": "old-stamp", "versions": {},
}])
def test_write_frozen_catalog_round_trips_text_and_provenance(catalog, prior_manifest):
    if prior_manifest is not None:
        (catalog / "prompts/manifest.json").write_text(json.dumps(prior_manifest))
    frozen = {
        "contracts_specialist": ("  café 'quoted' \\path\n\n", "production", "contracts"),
        "judge-classification": ('Unicode → and "quotes"\n', "evaluator", "judge:classify"),
    }

    promote._write_frozen_catalog(frozen)

    # Import the emitted Python to catch invalid identifiers or literal escaping.
    module = runpy.run_path(str(catalog / "src/evals/prompts/frozen_v1.py"))
    assert module["LINEAGE_ID"] == "mailroom-dataset-v1"
    assert module["FROZEN_VERSION"] == 1
    assert module["VERSIONS"] == {f"{role}_v1": row[0] for role, row in frozen.items()}
    assert module["SOURCE_OF"] == {
        f"{role}_v1": f"{kind}:{source}" for role, (_, kind, source) in frozen.items()
    }
    manifest = json.loads((catalog / "prompts/manifest.json").read_text())
    for field, default in {
        "lineage_id": "mailroom-dataset-v1", "frozen_version": 1,
        "pipeline_git_commit": None,
        "derivation": "llm-mailroom production prompt_templates + intake + evaluator rubrics",
    }.items():
        assert manifest[field] == (prior_manifest or {}).get(field, default)
    assert manifest["frozen_at"] != "old-stamp"
    assert set(manifest["versions"]) == set(module["VERSIONS"])
    for role, (text, kind, source) in frozen.items():
        key = f"{role}_v1"
        assert manifest["versions"][key] == {
            "source_kind": kind, "source_key": source,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "chars": len(text),
        }
        body = text.strip("\n")
        assert (catalog / f"prompts/{key}.md").read_text() == f"# {key}\n\n{body}\n"


def test_promote_freeze_new_adds_role_without_changing_existing_prompts(catalog, monkeypatch):
    old_versions = dict(frozen_v1.VERSIONS)
    old_sources = dict(frozen_v1.SOURCE_OF)
    text = "Dedicated MAUD prompt — all_cash.\n"
    fetch = Mock(return_value=text)
    monkeypatch.setattr(promote, "fetch_sandbox_prompt", fetch)

    result = promote.promote_freeze_new(
        role="merger_agreement_specialist", sandbox_sha="revision",
        sandbox_stem="merger_simplified", source_label="merger_simplified@revision",
    )

    fetch.assert_called_once_with("revision", "merger_simplified")
    key = "merger_agreement_specialist_v1"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert result == {
        "key": key, "sha256": digest, "chars": len(text),
        "sandbox_sha": "revision", "sandbox_stem": "merger_simplified", "manifest_versions": 3,
    }
    module = runpy.run_path(str(catalog / "src/evals/prompts/frozen_v1.py"))
    assert module["VERSIONS"] == {**old_versions, key: text}
    assert module["SOURCE_OF"] == {**old_sources, key: "sandbox:merger_simplified@revision"}
    manifest = json.loads((catalog / "prompts/manifest.json").read_text())
    assert manifest["versions"][key]["source_kind"] == "sandbox"
    assert manifest["versions"][key]["source_key"] == "merger_simplified@revision"
    assert manifest["versions"][key]["sha256"] == digest
    assert not mutations.MUTATIONS_PATH.exists()


def test_promote_freeze_new_rejects_existing_role_without_writes(catalog, monkeypatch):
    monkeypatch.setattr(promote, "fetch_sandbox_prompt", Mock(return_value="Replacement"))
    before = catalog_files(catalog)
    with pytest.raises(SystemExit, match="already frozen"):
        promote.promote_freeze_new(
            role="contracts_specialist", sandbox_sha="revision",
            sandbox_stem="contracts_simplified", source_label="contracts@revision",
        )
    assert catalog_files(catalog) == before


@pytest.mark.parametrize("command", ["mutation", "freeze-new"])
def test_download_failure_does_not_write_catalog(catalog, monkeypatch, command):
    monkeypatch.setattr(promote, "fetch_sandbox_prompt", Mock(side_effect=URLError("offline")))
    before = catalog_files(catalog)
    with pytest.raises(URLError, match="offline"):
        if command == "mutation":
            promote.promote_mutation(
                parent_key="contracts_specialist_v1", new_key="contracts_specialist_v2",
                sandbox_sha="revision", sandbox_stem="contracts", note="failed download",
            )
        else:
            promote.promote_freeze_new(
                role="new_specialist", sandbox_sha="revision",
                sandbox_stem="new", source_label="new@revision",
            )
    assert catalog_files(catalog) == before


@pytest.mark.parametrize("explicit_sha", [False, True])
def test_mutation_cli_forwards_arguments_and_prints_summary(monkeypatch, capsys, explicit_sha):
    args = ["promote_sandbox_specialist.py", "mutation", "--parent", "contracts_specialist_v1",
            "--new-key", "contracts_specialist_v2", "--sandbox-stem", "contracts_simplified",
            "--note", "preserve this note"]
    if explicit_sha:
        args += ["--sandbox-sha", "custom-revision"]
    monkeypatch.setattr(sys, "argv", args)
    result = {"key": "contracts_specialist_v2", "parent": "contracts_specialist_v1",
              "sha256": "digest", "text": "not part of the CLI summary"}
    mutation = Mock(return_value=result)
    monkeypatch.setattr(promote, "promote_mutation", mutation)

    assert promote.main() == 0

    mutation.assert_called_once_with(
        parent_key="contracts_specialist_v1", new_key="contracts_specialist_v2",
        sandbox_sha="custom-revision" if explicit_sha else promote.DEFAULT_SANDBOX_SHA,
        sandbox_stem="contracts_simplified", note="preserve this note",
    )
    assert json.loads(capsys.readouterr().out) == {
        key: result[key] for key in ("key", "parent", "sha256")
    }


@pytest.mark.parametrize("source_label", [None, "explicit provenance label"])
def test_freeze_cli_defaults_source_label_to_stem_and_short_sha(monkeypatch, capsys, source_label):
    revision = "0123456789abcdef0123456789abcdef01234567"
    args = ["promote_sandbox_specialist.py", "freeze-new", "--role", "merger_agreement_specialist",
            "--sandbox-stem", "merger_simplified", "--sandbox-sha", revision]
    if source_label is not None:
        args += ["--source-label", source_label]
    monkeypatch.setattr(sys, "argv", args)
    result = {"key": "merger_agreement_specialist_v1", "sha256": "digest", "chars": 42}
    freeze = Mock(return_value=result)
    monkeypatch.setattr(promote, "promote_freeze_new", freeze)

    assert promote.main() == 0

    freeze.assert_called_once_with(
        role="merger_agreement_specialist", sandbox_sha=revision,
        sandbox_stem="merger_simplified",
        source_label=source_label or "merger_simplified@0123456789ab",
    )
    assert json.loads(capsys.readouterr().out) == result


@pytest.mark.parametrize("args", [
    [],
    ["mutation", "--parent", "contracts_specialist_v1"],
    ["freeze-new", "--role", "merger_agreement_specialist"],
    ["unknown-command"],
])
def test_cli_rejects_incomplete_or_unknown_commands_before_promotion(monkeypatch, args):
    mutation, freeze = Mock(), Mock()
    monkeypatch.setattr(promote, "promote_mutation", mutation)
    monkeypatch.setattr(promote, "promote_freeze_new", freeze)
    monkeypatch.setattr(sys, "argv", ["promote_sandbox_specialist.py", *args])
    with pytest.raises(SystemExit) as caught:
        promote.main()
    assert caught.value.code == 2
    mutation.assert_not_called()
    freeze.assert_not_called()
