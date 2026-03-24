"""Check credits and billing."""

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail

app = typer.Typer(help="Check credits and billing", no_args_is_help=True)


@app.command()
def balance(ctx: typer.Context):
    """Show current credit balance and plan info."""
    try:
        client = get_client()
        data = client.get("/api/billing")

        # Display key billing fields
        detail = {
            "credits": data.get("balance", 0),
            "plan": data.get("plan", "unknown"),
            "nextRenewal": data.get("cycleStart", "N/A"),
            "overdue": data.get("overdue", False),
        }
        render_detail(detail, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def transactions(
    ctx: typer.Context,
    limit: int = typer.Option(20, "--limit", help="Max results"),
):
    """List recent credit transactions."""
    try:
        client = get_client()
        data = client.get("/api/billing/transactions", params={"limit": limit})

        rows = data if isinstance(data, list) else []
        columns = ["timestamp", "type", "amount", "reason"]
        # Normalize column names: backend may use camelCase
        normalized = []
        for row in rows:
            normalized.append({
                "timestamp": row.get("timestamp", row.get("date", "")),
                "type": row.get("type", ""),
                "amount": row.get("amount", ""),
                "reason": row.get("reason", ""),
            })
        render(normalized, columns, ctx.obj)
    except CliApiError as e:
        handle_error(e)
