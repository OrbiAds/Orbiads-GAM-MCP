"""MCM commands."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render_detail

app = typer.Typer(help="Multi-Customer Management", no_args_is_help=True)


@app.command("earnings")
def mcm_earnings(
    ctx: typer.Context,
    month: int = typer.Option(..., "--month", help="Month (1-12)"),
    year: int = typer.Option(..., "--year", help="Year (4-digit)"),
) -> None:
    """Fetch MCM earnings for a given month."""
    try:
        data = get_client().get(
            "/api/gam/mcm/earnings",
            params={"month": month, "year": year},
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)
