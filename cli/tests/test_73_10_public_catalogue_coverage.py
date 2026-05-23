"""Story 73.10 — public CLI catalogue coverage guard.

Asserts that every command exposed by the OrbiAds CLI binary is documented in
`frontend/src/lib/data/cli-commands.ts` (the source for `/docs/cli/commands`).

Failure mode this guards against:
- A new `@app.command(...)` is added without a matching catalogue entry, so the
  public docs page silently under-reports the binary surface.
- A renamed command leaves a stale catalogue entry that promises a CLI verb
  the binary no longer exposes.

Both are doc-drift bugs; the binary remains the source of truth. This test
forces a manual catalogue refresh per Story 73.10 acceptance criteria AC-3.
"""

from __future__ import annotations

import re
from pathlib import Path

import typer.main as tm

from orbiads_cli.main import app

CATALOGUE_PATH = (
    Path(__file__).resolve().parents[3]
    / "frontend"
    / "src"
    / "lib"
    / "data"
    / "cli-commands.ts"
)


def _walk_click(group, prefix: str = "") -> list[str]:
    cmds: list[str] = []
    for name, sub in group.commands.items():
        full = f"{prefix} {name}".strip()
        if hasattr(sub, "commands") and sub.commands:
            cmds.extend(_walk_click(sub, full))
        else:
            cmds.append(full)
    return cmds


def _binary_commands() -> set[str]:
    cli = tm.get_command(app)
    return set(_walk_click(cli))


def _catalogue_commands() -> set[str]:
    content = CATALOGUE_PATH.read_text(encoding="utf-8")
    return set(re.findall(r'command:\s*"orbiads\s+([^"]+)"', content))


def test_every_cli_command_is_documented() -> None:
    binary = _binary_commands()
    catalogue = _catalogue_commands()
    missing = binary - catalogue
    assert not missing, (
        f"{len(missing)} CLI command(s) missing from public catalogue "
        f"(frontend/src/lib/data/cli-commands.ts):\n  "
        + "\n  ".join(sorted(missing))
        + "\n\nAdd a CliCommand entry per missing command (see Story 73.10 spec)."
    )


def test_no_stale_catalogue_entries() -> None:
    binary = _binary_commands()
    catalogue = _catalogue_commands()
    stale = catalogue - binary
    assert not stale, (
        f"{len(stale)} stale catalogue entry(ies) reference commands the CLI no "
        f"longer exposes:\n  "
        + "\n  ".join(sorted(stale))
        + "\n\nRemove or rename in frontend/src/lib/data/cli-commands.ts."
    )


def test_catalogue_declares_required_categories() -> None:
    """Confirms cliCategories has the Epic 73 additions (features, programmatic, api)."""
    content = CATALOGUE_PATH.read_text(encoding="utf-8")
    categories_block_match = re.search(
        r"export const cliCategories[^=]*=\s*\{([^}]+)\}", content, re.DOTALL
    )
    assert categories_block_match, "cliCategories export not found in catalogue"
    block = categories_block_match.group(1)
    for required in ("features:", "programmatic:", "api:"):
        assert required in block, f"cliCategories missing key {required!r}"
