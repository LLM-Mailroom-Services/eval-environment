"""Human-readable Markdown mirrors for frozen / mutation prompt text."""

from __future__ import annotations


def prompt_mirror_markdown(key: str, text: str) -> str:
    """Render ``prompts/<key>.md`` — H1 label plus exact prompt body (not sent to LLMs)."""
    body = text.strip("\n")
    return f"# {key}\n\n{body}\n"


def strip_mirror_heading(key: str, content: str) -> str:
    """Return prompt body only (for drift checks against live pipeline text)."""
    stripped = content.lstrip("\n")
    prefix = f"# {key}\n"
    if stripped.startswith(prefix):
        return stripped[len(prefix) :].lstrip("\n").rstrip("\n")
    if stripped.startswith("# "):
        _first, _, rest = stripped.partition("\n")
        return rest.lstrip("\n").rstrip("\n")
    return stripped.rstrip("\n")
