#!/usr/bin/env bash
# CI bootstrap: materialize the Digital-Mailroom uv workspace that this repo's
# `pyproject.toml` path source points at, so `uv sync` resolves on a bare
# runner. pyproject.toml declares:
#
#     mailroom = { path = "../Digital-Mailroom/packages/llm-mailroom", editable = true }
#
# and ../Digital-Mailroom is a private monorepo, absent from GitHub-hosted
# runners. This script reconstructs the minimum tree that makes the path source
# resolvable, pinned by immutable commit SHA. It is the single source of truth
# for those pins; do not duplicate them in the workflow.
#
# WHY THIS SHAPE (the documented git-source fallback does not work):
# llm-mailroom's own pyproject declares
#     [tool.uv.sources] llm-dojo-scoring = { workspace = true }
# so a standalone git source for `mailroom` fails outside its workspace with
# "`llm-dojo-scoring` references a workspace in `tool.uv.sources` ... but is not
# a workspace member", and adding an explicit dojo git source in this repo does
# not help (workspace members must source members as `{ workspace = true }`;
# a second URL is rejected as a conflicting URL). Reconstructing the workspace
# root with a two-line pyproject makes the transitive `workspace = true`
# resolve. Neither pin floats on a branch.
#
# Idempotent: an existing checkout already at the pinned SHA is reused as-is.
# A checkout at a different SHA, or a dirty one, is refused rather than
# clobbered (set CI_BOOTSTRAP_FORCE=1 to override deliberately).

set -euo pipefail

MAILROOM_REPO="https://github.com/Exios66/llm-mailroom.git"
MAILROOM_REV="28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636"

DOJO_REPO="https://github.com/Exios66/llm-dojo-scoring.git"
DOJO_REV="c49393a91ad7f6bcff537652a85fa3338859beae" # tag v0.15.0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# Mirrors the relative path in pyproject.toml's [tool.uv.sources].
WORKSPACE_ROOT="$(cd "$REPO_ROOT/.." && pwd)/Digital-Mailroom"
PKG_ROOT="$WORKSPACE_ROOT/packages"

# Never block a CI job on an interactive git credential prompt.
export GIT_TERMINAL_PROMPT=0

log() { printf 'bootstrap: %s\n' "$*"; }
fail() { printf 'bootstrap: ERROR: %s\n' "$*" >&2; exit 1; }

# materialize <url> <rev> <dest>
materialize() {
  local url="$1" rev="$2" dest="$3" name head dirty

  name="$(basename "$dest")"

  if [ -e "$dest" ]; then
    [ -d "$dest/.git" ] || fail "$dest exists and is not a git checkout; move it aside or set CI_BOOTSTRAP_FORCE=1"
    head="$(git -C "$dest" rev-parse HEAD 2>/dev/null || echo none)"
    dirty="$(git -C "$dest" status --porcelain | head -1)"
    if [ "$head" = "$rev" ] && [ -z "$dirty" ]; then
      log "$name already at $rev — reusing"
      return 0
    fi
    if [ "${CI_BOOTSTRAP_FORCE:-0}" != "1" ]; then
      fail "$dest is at ${head:-unknown} (want $rev)${dirty:+ and dirty}; refusing to clobber. Set CI_BOOTSTRAP_FORCE=1 to override."
    fi
    log "$name at $head (want $rev) — force-removing"
    rm -rf "$dest"
  fi

  mkdir -p "$dest"
  git init -q "$dest"
  git -C "$dest" remote add origin "$url"

  # Primary: depth-1 fetch of the exact commit. Never fetch a branch tip.
  if git -C "$dest" fetch -q --depth 1 origin "$rev"; then
    log "$name fetched $rev (depth 1)"
  else
    # Fallback: full history, still resolved to the exact immutable SHA.
    log "$name depth-1 SHA fetch unsupported — fetching full history"
    git -C "$dest" fetch -q --tags origin
  fi
  git -C "$dest" checkout -q --detach FETCH_HEAD

  head="$(git -C "$dest" rev-parse HEAD)"
  [ "$head" = "$rev" ] || fail "$name resolved to $head, expected $rev"
  log "$name @ $head OK"
}

mkdir -p "$PKG_ROOT"
materialize "$MAILROOM_REPO" "$MAILROOM_REV" "$PKG_ROOT/llm-mailroom"
materialize "$DOJO_REPO" "$DOJO_REV" "$PKG_ROOT/llm-dojo-scoring"

# The two lines that make llm-mailroom's `{ workspace = true }` source for
# llm-dojo-scoring resolve outside the original monorepo. Intentionally the
# only content: this file is a resolution stub, not a copy of the real
# workspace manifest.
cat > "$WORKSPACE_ROOT/pyproject.toml" <<'TOML'
[tool.uv.workspace]
members = ["packages/*"]
TOML

log "workspace stub written: $WORKSPACE_ROOT/pyproject.toml"
log "mailroom=$MAILROOM_REV dojo=$DOJO_REV"
