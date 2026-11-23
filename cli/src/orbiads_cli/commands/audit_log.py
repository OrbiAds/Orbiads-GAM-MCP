"""Tenant audit log — Story 61.7 — and GAM change history — Story 117-5.

Maps `query_audit_log` -> GET /api/settings/audit/ (OrbiAds journal) and
`list_change_events` / `get_change_event` -> GET /api/gam/change-events[/{id}] (GAM change
history, including changes made in the GAM UI; read-only, active network only).

Story 117-17: GAM needs a time window, so the list completes a missing ``--since`` / ``--until``
(default: last 30 days) and pages with an OrbiAds time cursor. Story 117-17b: ``get`` searches
the event in a window (``--since`` / ``--until``, default: last 30 days).
"""

from __future__ import annotations

from urllib.parse import quote

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail

app = typer.Typer(help="Query the tenant audit log (Story 61.7)", no_args_is_help=True)

_COLUMNS = ["timestamp", "actor", "action", "target"]


@app.command("log")
def audit_log(
    ctx: typer.Context,
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500),
):
    """Query the audit log."""
    try:
        data = get_client().get("/api/settings/audit/", params={"limit": limit})
        if isinstance(data, dict):
            items = data.get("entries", data.get("results", data.get("logs", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


changes_app = typer.Typer(
    help="GAM change history (who changed what in GAM, incl. UI changes) — Story 117-5",
    no_args_is_help=True,
)
app.add_typer(changes_app, name="changes")

_CHANGE_COLUMNS = ["changeTime", "entityType", "entityId", "operation", "userId", "id"]


def _flat_change(event: dict) -> dict:
    """Flatten the nested ``user`` object so table/CSV output has a ``userId`` column."""
    flat = dict(event)
    user = event.get("user")
    flat["userId"] = user.get("id", "") if isinstance(user, dict) else ""
    return flat


@changes_app.command("list")
def list_changes(
    ctx: typer.Context,
    entity_type: str | None = typer.Option(
        None,
        "--entity-type",
        help="GAM resource type: LINE_ITEM, ORDER, CREATIVE, AD_UNIT, ...",
    ),
    entity_id: str | None = typer.Option(
        None, "--entity-id", help="Numeric id of the entity"
    ),
    user: str | None = typer.Option(None, "--user", help="Numeric id of the GAM user"),
    since: str | None = typer.Option(
        None,
        "--since",
        help=(
            "Changed on/after this ISO 8601 date or date-time. GAM needs a window: a missing "
            "bound is completed (default: last 30 days)"
        ),
    ),
    until: str | None = typer.Option(
        None, "--until", help="Changed on/before this ISO 8601 date or date-time"
    ),
    operation: str | None = typer.Option(
        None, "--operation", help="CREATE, UPDATE or DELETE"
    ),
    page_token: str | None = typer.Option(
        None,
        "--page-token",
        help="nextPageToken of the previous page (repeat the same filters)",
    ),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=100),
):
    """List GAM change events (read-only, active network only)."""
    params: dict = {"limit": limit}
    for key, value in (
        ("entity_type", entity_type),
        ("entity_id", entity_id),
        ("user", user),
        ("since", since),
        ("until", until),
        ("operation", operation),
        ("page_token", page_token),
    ):
        if value is not None:
            params[key] = value
    try:
        data = get_client().get("/api/gam/change-events", params=params)
        events = data.get("events", []) if isinstance(data, dict) else data
        render([_flat_change(e) for e in events], _CHANGE_COLUMNS, ctx.obj)
        if isinstance(data, dict) and data.get("hasMore") and ctx.obj.format != "json":
            typer.echo(
                f"More results: --page-token {data.get('nextPageToken')}", err=True
            )
    except CliApiError as e:
        handle_error(e)


@changes_app.command("get")
def get_change(
    ctx: typer.Context,
    change_event_id: str = typer.Argument(..., help="Change event id"),
    since: str | None = typer.Option(
        None,
        "--since",
        help="Start (ISO 8601) of the window searched for the event (default: last 30 days)",
    ),
    until: str | None = typer.Option(
        None, "--until", help="End (ISO 8601) of the window searched for the event"
    ),
):
    """Show one GAM change event."""
    try:
        params = {k: v for k, v in (("since", since), ("until", until)) if v}
        kwargs = {"params": params} if params else {}
        data = get_client().get(
            f"/api/gam/change-events/{quote(change_event_id, safe='')}", **kwargs
        )
        render_detail(_flat_change(data) if isinstance(data, dict) else {}, ctx.obj)
    except CliApiError as e:
        handle_error(e)
