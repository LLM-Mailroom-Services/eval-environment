#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for mailroom-evals.
# Installs uv, checks out the pipeline path source declared in pyproject.toml,
# and syncs the locked environment. Safe to re-run.
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh
fi
export PATH="/usr/local/bin:${PATH}"

# Install may run as this file, or as the environment install command with cwd
# already at the checkout. Prefer a checkout that is already the working directory.
if [[ -f "${PWD}/pyproject.toml" ]]; then
  ROOT="${PWD}"
else
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
cd "${ROOT}"

eval "$(python3 - <<'PY'
import tomllib
from pathlib import Path

root = Path.cwd()
with (root / "pyproject.toml").open("rb") as handle:
    spec = tomllib.load(handle)
rel = Path(spec["tool"]["uv"]["sources"]["mailroom"]["path"])

# Two layouts are in tree history:
# - this branch: Digital-Mailroom/packages/llm-mailroom (workspace member)
# - main: ../llm-mailroom (standalone Exios66/llm-mailroom clone)
if "Digital-Mailroom" in rel.parts:
    dest = root / "Digital-Mailroom"
    url = "https://github.com/LLM-Mailroom-Services/Digital-Mailroom.git"
    # main @ 2026-09-24, mailroom 0.7.1 + workspace llm-dojo-scoring 0.15.0
    pin = "e5eeac603edf27f9fe4f306cf086aa9c31965d9a"
else:
    dest = (root / rel).resolve()
    url = "https://github.com/Exios66/llm-mailroom.git"
    # main @ 2026-09-24, mailroom 0.7.1 with dojo git pin v0.15.0
    pin = "28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636"

print(f"DEST={dest}")
print(f"URL={url}")
print(f"PIN={pin}")
PY
)"

if [[ ! -d "${DEST}/.git" ]]; then
  parent="$(dirname "${DEST}")"
  if [[ ! -w "${parent}" ]]; then
    # main's path source is ../llm-mailroom. From /workspace that is /llm-mailroom,
    # which the agent user cannot create. Make an empty owned directory, then clone.
    sudo mkdir -p "${DEST}"
    sudo chown "$(id -un):$(id -gn)" "${DEST}"
  else
    mkdir -p "${parent}"
  fi
  git clone --depth 1 "${URL}" "${DEST}"
fi

head="$(git -C "${DEST}" rev-parse HEAD)"
if [[ "${head}" != "${PIN}" ]]; then
  git -C "${DEST}" fetch --depth 1 origin "${PIN}"
  git -C "${DEST}" checkout --detach "${PIN}"
fi

# The standalone Exios66/llm-mailroom checkout (main's path source) still
# carries the monorepo `[tool.uv.sources] workspace = true` override. Outside
# that workspace, `uv run` refuses to start. Drop the override so the git pin
# in dependencies matches uv.lock. The in-repo Digital-Mailroom checkout must
# keep the workspace source.
case "${DEST}" in
  */Digital-Mailroom) ;;
  *)
    MAILROOM_DEST="${DEST}" python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["MAILROOM_DEST"]) / "pyproject.toml"
text = path.read_text()
marker = "\n[tool.uv.sources]\n"
index = text.find(marker)
if index != -1:
    path.write_text(text[:index].rstrip() + "\n")
    print("removed tool.uv.sources from standalone llm-mailroom checkout")
PY
    ;;
esac

echo "pipeline checkout: $(git -C "${DEST}" rev-parse HEAD) at ${DEST}"
uv sync --extra dev --frozen
uv run python -c 'import evals, pipeline; print("imports ok", pipeline.__file__)'
