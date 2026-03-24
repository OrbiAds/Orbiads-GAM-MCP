"""Output formatters and global helpers for OrbiAds CLI.

All data output goes to stdout (table / JSON / CSV).
All messages (info, error, success, confirm) go to stderr.
"""

import csv
import json
import sys
from dataclasses import dataclass

import typer
from rich.console import Console
from rich.table import Table

_stderr = Console(stderr=True)


@dataclass
class OutputContext:
    """Carries resolved output format and --yes flag through the CLI context."""

    format: str = "table"  # table | json | csv
    yes: bool = False

    @classmethod
    def from_flags(
        cls,
        json_flag: bool,
        output: str | None,
        yes: bool,
    ) -> "OutputContext":
        """Build from CLI flags with auto-detect for non-TTY."""
        fmt = "json" if json_flag else (output or "table")
        # Non-TTY auto-detect: default to JSON when piped
        if fmt == "table" and not sys.stdout.isatty():
            fmt = "json"
        return cls(format=fmt, yes=yes)


# ---------------------------------------------------------------------------
# List output
# ---------------------------------------------------------------------------


def render(data: list[dict], columns: list[str], ctx: OutputContext) -> None:
    """Render a list of dicts to stdout in the requested format."""
    if ctx.format == "json":
        print(json.dumps(data, indent=2, default=str))
    elif ctx.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            writer.writerow({c: row.get(c, "") for c in columns})
    else:
        console = Console()
        table = Table()
        for col in columns:
            table.add_column(col)
        for row in data:
            table.add_row(*[str(row.get(c, "")) for c in columns])
        console.print(table)


# ---------------------------------------------------------------------------
# Detail (single-object) output
# ---------------------------------------------------------------------------


def render_detail(data: dict, ctx: OutputContext) -> None:
    """Render a single dict to stdout (JSON or key-value pairs)."""
    if ctx.format == "json":
        print(json.dumps(data, indent=2, default=str))
    elif ctx.format == "csv":
        # CSV for a single object: one header row + one data row
        columns = list(data.keys())
        writer = csv.DictWriter(sys.stdout, fieldnames=columns)
        writer.writeheader()
        writer.writerow(data)
    else:
        console = Console()
        for key, val in data.items():
            console.print(f"[bold]{key}:[/bold] {val}")


# ---------------------------------------------------------------------------
# Stderr helpers
# ---------------------------------------------------------------------------


def info(msg: str) -> None:
    """Print an informational message to stderr."""
    _stderr.print(msg)


def error(msg: str) -> None:
    """Print an error message to stderr (red)."""
    _stderr.print(f"[red]{msg}[/red]")


def success(msg: str) -> None:
    """Print a success message to stderr (green)."""
    _stderr.print(f"[green]{msg}[/green]")


# ---------------------------------------------------------------------------
# Confirmation prompt
# ---------------------------------------------------------------------------


def confirm(msg: str, ctx: OutputContext) -> bool:
    """Ask for confirmation on stderr. Auto-accept if --yes or non-TTY."""
    if ctx.yes or not sys.stderr.isatty():
        return True
    return typer.confirm(msg, err=True)
