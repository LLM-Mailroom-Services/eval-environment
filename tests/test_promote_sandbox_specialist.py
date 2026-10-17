"""Sandbox promotion unit tests: no network and no writes to the live catalog."""

from __future__ import annotations

import io
import json
import sys
from types import ModuleType
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

import pytest

from evals.prompts import frozen_v1, lineage, mutations
from scripts import promote_sandbox_specialist as promote


@pytest.fixture(autouse=True)
def isolated_catalog(tmp_path, monkeypatch):
    """Contain every catalog write and fail immediately on unexpected HTTP."""
    prompts = tmp_path / "prompts"
    prompts.mkdir()
    monkeypatch.setattr(promote, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(mutations, "MUTATIONS_PATH", prompts / "mutations.json")
    monkeypatch.setattr(lineage, "_production", dict)
    monkeypatch.setattr(
        promote.urllib.request, "urlopen", Mock(side_effect=AssertionError("unexpected HTTP"))
    )
    return prompts


@pytest.fixture
def fetched_prompt(monkeypatch):
    fetch = Mock(return_value="  Extract only visible facts — café.\n\n")
    monkeypatch.setattr(promote, "fetch_sandbox_prompt", fetch)
    return fetch


@pytest.fixture
def freeze_writer(isolated_catalog, monkeypatch):
    """Replace the pipeline-dependent writer at its public module boundary."""
    def write(frozen):
        manifest = {"versions": {f"{role}_v1": {} for role in frozen}}
        (isolated_catalog / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    writer = Mock(side_effect=write)
    module = ModuleType("scripts.freeze_prompts")
    module.write_frozen = writer
    monkeypatch.setitem(sys.modules, "scripts.freeze_prompts", module)
    return writer


def _promote_mutation(**overrides):
    args = {
        "parent_key": "boss_v1",
        "new_key": "boss_v2",
        "sandbox_sha": "a" * 40,
        "sandbox_stem": "boss_simplified",
        "note": "Sandbox promotion at a pinned revision",
    }
    return promote.promote_mutation(**(args | overrides))


def _promote_freeze_new(**overrides):
    args = {
        "role": "new_specialist",
        "sandbox_sha": "b" * 40,
        "sandbox_stem": "new_specialist_simplified",
        "source_label": "sandbox:prompt@bbbbbbbbbbbb",
    }
    return promote.promote_freeze_new(**(args | overrides))


@pytest.mark.parametrize(
    ("text", "digest"),
    [
        ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
        ("é", "4a99557e4033c3539de2eb65472017cad5f9557f7a0625a09f1c3f6e2ba69c4c"),
    ],
)
def test_sha256_known_utf8_vectors(text, digest):
    assert promote.sha256(text) == digest


@pytest.mark.parametrize("text", ["", "  Evidence — café 📨.\r\n\n"])
def test_fetch_uses_pinned_url_and_preserves_utf8(text, monkeypatch):
    response = io.BytesIO(text.encode("utf-8"))
    urlopen = Mock(return_value=response)
    monkeypatch.setattr(promote.urllib.request, "urlopen", urlopen)

    assert promote.fetch_sandbox_prompt("a" * 40, "contracts_simplified") == text

    urlopen.assert_called_once_with(
        "https://raw.githubusercontent.com/Exios66/local-mailroom-sandbox/"
        + "a" * 40
        + "/config/prompts/contracts_simplified.txt",
        timeout=60,
    )
    assert response.closed


@pytest.mark.parametrize(
    "error",
    [
        HTTPError("https://example.invalid", 404, "Not found", {}, None),
        URLError("offline"),
        TimeoutError("timed out"),
    ],
    ids=["http-404", "network", "timeout"],
)
def test_fetch_propagates_transport_errors(error, monkeypatch):
    monkeypatch.setattr(promote.urllib.request, "urlopen", Mock(side_effect=error))
    with pytest.raises(type(error)) as caught:
        promote.fetch_sandbox_prompt("revision", "missing")
    assert caught.value is error


@pytest.mark.parametrize("failure", ["read", "decode"])
def test_fetch_closes_response_on_read_or_decode_error(failure, monkeypatch):
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    if failure == "read":
        response.read.side_effect = OSError("response interrupted")
        expected = OSError
    else:
        response.read.return_value = b"\xff"
        expected = UnicodeDecodeError
    monkeypatch.setattr(promote.urllib.request, "urlopen", Mock(return_value=response))

    with pytest.raises(expected):
        promote.fetch_sandbox_prompt("revision", "broken")

    response.__exit__.assert_called_once()


def test_mutation_replaces_whole_parent_and_preserves_history(isolated_catalog, fetched_prompt):
    previous = {
        "key": "sorter_v2", "parent": "sorter_v1", "version": 2,
        "text": "Earlier mutation.\n", "note": "Keep this provenance",
    }
    path = isolated_catalog / "mutations.json"
    path.write_text(json.dumps({"mutations": [previous], "catalog_note": "preserve me"}))
    parent = lineage.resolve("boss_v1")

    meta = _promote_mutation()

    fetched_prompt.assert_called_once_with("a" * 40, "boss_simplified")
    assert meta["key"] == "boss_v2"
    assert meta["parent"] == "boss_v1" and meta["version"] == 2
    assert meta["text"] == fetched_prompt.return_value
    assert meta["sha256"] == promote.sha256(fetched_prompt.return_value)
    assert meta["note"] == "Sandbox promotion at a pinned revision"
    assert meta["created_at"]
    data = json.loads(path.read_text())
    assert data == {"mutations": [previous, meta], "catalog_note": "preserve me"}
    assert lineage.resolve("boss_v1") == parent
    assert lineage.resolve("boss_v2").text == fetched_prompt.return_value
    assert (isolated_catalog / "boss_v2.md").read_text() == (
        "# boss_v2\n\n" + fetched_prompt.return_value.strip("\n") + "\n"
    )
    assert (isolated_catalog / "sorter_v2.md").read_text() == (
        "# sorter_v2\n\nEarlier mutation.\n"
    )


def test_mutation_can_promote_a_mutated_parent(isolated_catalog, fetched_prompt):
    first = _promote_mutation()
    fetched_prompt.return_value = "Entirely new third version.\n"

    second = _promote_mutation(parent_key="boss_v2", new_key="boss_v3")

    assert second["version"] == 3 and second["parent"] == "boss_v2"
    assert second["text"] == "Entirely new third version.\n"
    assert json.loads((isolated_catalog / "mutations.json").read_text())["mutations"] == [
        first, second,
    ]
    assert lineage.resolve("boss_v2").text == first["text"]


@pytest.mark.parametrize(
    ("overrides", "error", "message"),
    [
        ({"parent_key": "unknown_v1"}, KeyError, "unknown prompt version"),
        ({"new_key": "boss_v1"}, mutations.MutationError, "already exists"),
        ({"new_key": "boss_v3"}, mutations.MutationError, "lineage naming"),
        ({"new_key": "sorter_v2"}, mutations.MutationError, "lineage naming"),
    ],
    ids=["unknown-parent", "existing-key", "skipped-version", "different-role"],
)
def test_mutation_rejects_invalid_lineage_without_writes(
    overrides, error, message, isolated_catalog, fetched_prompt,
):
    with pytest.raises(error, match=message):
        _promote_mutation(**overrides)
    assert list(isolated_catalog.iterdir()) == []


def test_mutation_cannot_overwrite_an_existing_promotion(isolated_catalog, fetched_prompt):
    _promote_mutation()
    before = {p.name: p.read_bytes() for p in isolated_catalog.iterdir()}
    fetched_prompt.return_value = "Attempted overwrite"

    with pytest.raises(mutations.MutationError, match="already exists"):
        _promote_mutation()

    assert {p.name: p.read_bytes() for p in isolated_catalog.iterdir()} == before


def test_mutation_preserves_registration_when_mirror_fails(
    isolated_catalog, fetched_prompt, monkeypatch,
):
    monkeypatch.setattr(
        mutations, "render_prompts_mirror", Mock(side_effect=OSError("mirror unwritable"))
    )
    with pytest.raises(OSError, match="mirror unwritable"):
        _promote_mutation()

    row, = json.loads((isolated_catalog / "mutations.json").read_text())["mutations"]
    assert row["key"] == "boss_v2" and row["text"] == fetched_prompt.return_value


def test_mutation_propagates_catalog_write_failure(fetched_prompt, monkeypatch):
    apply = Mock(side_effect=OSError("catalog unwritable"))
    render = Mock()
    monkeypatch.setattr(mutations, "apply_mutation", apply)
    monkeypatch.setattr(mutations, "render_prompts_mirror", render)

    with pytest.raises(OSError, match="catalog unwritable"):
        _promote_mutation()

    render.assert_not_called()


def test_mutation_rejects_malformed_catalog(isolated_catalog, fetched_prompt):
    path = isolated_catalog / "mutations.json"
    path.write_text("{broken")
    with pytest.raises(json.JSONDecodeError):
        _promote_mutation()
    assert path.read_text() == "{broken"
    assert list(isolated_catalog.iterdir()) == [path]


def test_freeze_preserves_existing_text_and_provenance(
    isolated_catalog, fetched_prompt, freeze_writer, monkeypatch,
):
    versions = {"legacy_v1_helper_v1": "Keep these bytes.\n", "judge-classification_v1": "Judge"}
    sources = {
        "legacy_v1_helper_v1": "production:legacy",
        "judge-classification_v1": "evaluator:script:prompt",
    }
    original_versions, original_sources = versions.copy(), sources.copy()
    monkeypatch.setattr(frozen_v1, "VERSIONS", versions)
    monkeypatch.setattr(frozen_v1, "SOURCE_OF", sources)

    meta = _promote_freeze_new()

    fetched_prompt.assert_called_once_with("b" * 40, "new_specialist_simplified")
    freeze_writer.assert_called_once_with({
        "legacy_v1_helper": ("Keep these bytes.\n", "production", "legacy"),
        "judge-classification": ("Judge", "evaluator", "script:prompt"),
        "new_specialist": (
            fetched_prompt.return_value, "sandbox", "sandbox:prompt@bbbbbbbbbbbb",
        ),
    })
    assert meta == {
        "key": "new_specialist_v1",
        "sha256": promote.sha256(fetched_prompt.return_value),
        "chars": len(fetched_prompt.return_value),
        "sandbox_sha": "b" * 40,
        "sandbox_stem": "new_specialist_simplified",
        "manifest_versions": 3,
    }
    assert (isolated_catalog / "new_specialist_v1.md").read_text() == (
        "# new_specialist_v1\n\n" + fetched_prompt.return_value.strip("\n") + "\n"
    )
    assert frozen_v1.VERSIONS == original_versions
    assert frozen_v1.SOURCE_OF == original_sources


def test_freeze_rejects_existing_role_without_writes(
    isolated_catalog, fetched_prompt, freeze_writer,
):
    with pytest.raises(SystemExit, match="role 'boss' already frozen"):
        _promote_freeze_new(role="boss")
    freeze_writer.assert_not_called()
    assert list(isolated_catalog.iterdir()) == []


@pytest.mark.parametrize(
    ("sources", "error"), [({}, KeyError), ({"legacy_v1": "missing-separator"}, ValueError)],
    ids=["missing-provenance", "malformed-provenance"],
)
def test_freeze_rejects_invalid_existing_provenance(
    sources, error, isolated_catalog, fetched_prompt, freeze_writer, monkeypatch,
):
    monkeypatch.setattr(frozen_v1, "VERSIONS", {"legacy_v1": "Preserve this"})
    monkeypatch.setattr(frozen_v1, "SOURCE_OF", sources)

    with pytest.raises(error):
        _promote_freeze_new()

    freeze_writer.assert_not_called()
    assert list(isolated_catalog.iterdir()) == []


def test_freeze_propagates_writer_failure(isolated_catalog, fetched_prompt, freeze_writer):
    freeze_writer.side_effect = OSError("frozen module unwritable")
    with pytest.raises(OSError, match="frozen module unwritable"):
        _promote_freeze_new()
    assert list(isolated_catalog.iterdir()) == []


def test_freeze_reports_malformed_manifest_after_writing_mirror(
    isolated_catalog, fetched_prompt, freeze_writer,
):
    freeze_writer.side_effect = lambda frozen: (
        isolated_catalog / "manifest.json"
    ).write_text("{broken")

    with pytest.raises(json.JSONDecodeError):
        _promote_freeze_new()

    assert (isolated_catalog / "new_specialist_v1.md").exists()


@pytest.mark.parametrize("operation", [_promote_mutation, _promote_freeze_new])
def test_failed_fetch_leaves_catalog_untouched(
    operation, isolated_catalog, fetched_prompt, freeze_writer,
):
    fetched_prompt.side_effect = URLError("sandbox unavailable")
    with pytest.raises(URLError, match="sandbox unavailable"):
        operation()
    freeze_writer.assert_not_called()
    assert list(isolated_catalog.iterdir()) == []


@pytest.mark.parametrize("revision", [None, "c" * 40], ids=["default-sha", "explicit-sha"])
def test_mutation_cli_dispatch_and_json(revision, monkeypatch, capsys):
    meta = {"key": "boss_v2", "sha256": "digest", "parent": "boss_v1", "text": "private body"}
    mutation = Mock(return_value=meta)
    freeze = Mock()
    monkeypatch.setattr(promote, "promote_mutation", mutation)
    monkeypatch.setattr(promote, "promote_freeze_new", freeze)
    argv = [
        "promote", "mutation", "--parent", "boss_v1", "--new-key", "boss_v2",
        "--sandbox-stem", "boss", "--note", "Pinned provenance",
    ]
    if revision:
        argv += ["--sandbox-sha", revision]
    monkeypatch.setattr(sys, "argv", argv)

    assert promote.main() == 0

    mutation.assert_called_once_with(
        parent_key="boss_v1", new_key="boss_v2", sandbox_stem="boss",
        sandbox_sha=revision or promote.DEFAULT_SANDBOX_SHA, note="Pinned provenance",
    )
    freeze.assert_not_called()
    assert json.loads(capsys.readouterr().out) == {
        "key": "boss_v2", "sha256": "digest", "parent": "boss_v1",
    }


@pytest.mark.parametrize(
    ("options", "revision", "label"),
    [
        ([], promote.DEFAULT_SANDBOX_SHA, "new@97c0f940194f"),
        (["--sandbox-sha", "c" * 40], "c" * 40, "new@cccccccccccc"),
        (["--source-label", "reviewed:source"], promote.DEFAULT_SANDBOX_SHA, "reviewed:source"),
    ],
    ids=["default-provenance", "explicit-revision", "explicit-source"],
)
def test_freeze_cli_dispatch_and_json(options, revision, label, monkeypatch, capsys):
    meta = {"key": "new_v1", "chars": 42, "manifest_versions": 15}
    freeze = Mock(return_value=meta)
    mutation = Mock()
    monkeypatch.setattr(promote, "promote_freeze_new", freeze)
    monkeypatch.setattr(promote, "promote_mutation", mutation)
    monkeypatch.setattr(sys, "argv", [
        "promote", "freeze-new", "--role", "new", "--sandbox-stem", "new", *options,
    ])

    assert promote.main() == 0

    freeze.assert_called_once_with(
        role="new", sandbox_sha=revision, sandbox_stem="new", source_label=label,
    )
    mutation.assert_not_called()
    assert json.loads(capsys.readouterr().out) == meta


@pytest.mark.parametrize(
    "argv",
    [
        [], ["unknown"],
        ["mutation", "--new-key", "boss_v2", "--sandbox-stem", "boss", "--note", "n"],
        ["mutation", "--parent", "boss_v1", "--sandbox-stem", "boss", "--note", "n"],
        ["mutation", "--parent", "boss_v1", "--new-key", "boss_v2", "--note", "n"],
        ["mutation", "--parent", "boss_v1", "--new-key", "boss_v2", "--sandbox-stem", "boss"],
        ["freeze-new", "--sandbox-stem", "new"],
        ["freeze-new", "--role", "new"],
    ],
    ids=["no-command", "unknown-command", "no-parent", "no-key", "no-mutation-stem",
         "no-note", "no-role", "no-freeze-stem"],
)
def test_cli_rejects_missing_arguments_before_promotion(argv, monkeypatch, capsys):
    mutation, freeze = Mock(), Mock()
    monkeypatch.setattr(promote, "promote_mutation", mutation)
    monkeypatch.setattr(promote, "promote_freeze_new", freeze)
    monkeypatch.setattr(sys, "argv", ["promote", *argv])

    with pytest.raises(SystemExit) as caught:
        promote.main()

    assert caught.value.code == 2
    assert "error:" in capsys.readouterr().err
    mutation.assert_not_called()
    freeze.assert_not_called()


@pytest.mark.parametrize(
    ("command", "argv"),
    [
        ("promote_mutation", ["mutation", "--parent", "boss_v1", "--new-key", "boss_v2",
                              "--sandbox-stem", "boss", "--note", "n"]),
        ("promote_freeze_new", ["freeze-new", "--role", "new", "--sandbox-stem", "new"]),
    ],
)
def test_cli_propagates_promotion_failure_without_success_json(command, argv, monkeypatch, capsys):
    monkeypatch.setattr(promote, command, Mock(side_effect=OSError("promotion failed")))
    monkeypatch.setattr(sys, "argv", ["promote", *argv])

    with pytest.raises(OSError, match="promotion failed"):
        promote.main()

    assert capsys.readouterr().out == ""
