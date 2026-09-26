#!/usr/bin/env bash
# CI / cloud bootstrap: materialize the sibling llm-mailroom checkout that
# pyproject.toml's editable path source points at:
#
#     mailroom = { path = "../llm-mailroom", editable = true }
#
# On GitHub Actions the repo lives under ~/work/<org>/<repo>/, so the parent
# directory is writable. On some cloud VMs only the repo root is writable; set
# MAILROOM_DEST to an in-repo path (e.g. Digital-Mailroom/packages/llm-mailroom)
# and re-point [tool.uv.sources] locally for that session.
#
# Pin is the single source of truth for CI; do not float on branch tips.
#
# Idempotent: an existing checkout at the pinned SHA is reused. Set
# CI_BOOTSTRAP_FORCE=1 to replace a mismatched or dirty tree.

set -euo pipefail

MAILROOM_REPO="https://github.com/Exios66/llm-mailroom.git"
MAILROOM_REV="28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MAILROOM_DEST="${MAILROOM_DEST:-$(cd "$REPO_ROOT/.." && pwd)/llm-mailroom}"

export GIT_TERMINAL_PROMPT=0

log() { printf 'bootstrap: %s\n' "$*"; }
fail() { printf 'bootstrap: ERROR: %s\n' "$*" >&2; exit 1; }

materialize() {
  local url="$1" rev="$2" dest="$3" name head dirty

  name="$(basename "$dest")"

  if [ -e "$dest" ]; then
    [ -d "$dest/.git" ] || fail "$dest exists and is not a git checkout; move it aside or set CI_BOOTSTRAP_FORCE=1"
    head="$(git -C "$dest" rev-parse HEAD 2>/dev/null || echo none)"
    dirty="$(git -C "$dest" status --porcelain | head -1)"
    if [ "$head" = "$rev" ] && [ -z "$dirty" ]; then
      log "$name already at $rev — reusing ($dest)"
      return 0
    fi
    if [ "${CI_BOOTSTRAP_FORCE:-0}" != "1" ]; then
      fail "$dest is at ${head:-unknown} (want $rev)${dirty:+ and dirty}; refusing to clobber. Set CI_BOOTSTRAP_FORCE=1 to override."
    fi
    log "$name at $head (want $rev) — force-removing"
    rm -rf "$dest"
  fi

  mkdir -p "$(dirname "$dest")"
  git init -q "$dest"
  git -C "$dest" remote add origin "$url"

  if git -C "$dest" fetch -q --depth 1 origin "$rev"; then
    log "$name fetched $rev (depth 1)"
  else
    log "$name depth-1 SHA fetch unsupported — fetching full history"
    git -C "$dest" fetch -q --tags origin
  fi
  git -C "$dest" checkout -q --detach FETCH_HEAD

  head="$(git -C "$dest" rev-parse HEAD)"
  [ "$head" = "$rev" ] || fail "$name resolved to $head, expected $rev"
  log "$name @ $head OK → $dest"
}

materialize "$MAILROOM_REPO" "$MAILROOM_REV" "$MAILROOM_DEST"
log "mailroom=$MAILROOM_REV dest=$MAILROOM_DEST"
