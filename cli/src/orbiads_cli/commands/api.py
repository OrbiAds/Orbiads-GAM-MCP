"""Generic API passthrough commands.

This is a migration bridge: every authenticated backend endpoint remains
callable from the CLI even before it gets a dedicated, ergonomic command.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render, render_detail

app = typer.Typer(help="Call authenticated OrbiAds API endpoints", no_args_is_help=True)

_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def _load_json_payload(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    file_path = Path(path)
    if not file_path.is_file():
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"Error: invalid JSON in {path}: {exc}", err=True)
        raise typer.Exit(code=2)
    if not isinstance(payload, dict):
        typer.echo("Error: JSON payload must be an object.", err=True)
        raise typer.Exit(code=2)
    return payload


def _parse_query(values: list[str] | None) -> dict[str, str]:
    params: dict[str, str] = {}
    for value in values or []:
        if "=" not in value:
            typer.echo(f"Error: query param must be key=value: {value}", err=True)
            raise typer.Exit(code=2)
        key, raw = value.split("=", 1)
        if not key:
            typer.echo(f"Error: query param key is empty: {value}", err=True)
            raise typer.Exit(code=2)
        params[key] = raw
    return params


def _render_any(data: Any, ctx: OutputContext) -> None:
    if isinstance(data, dict):
        render_detail(data, ctx)
        return
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        columns: list[str] = []
        for item in data:
            for key in item:
                if key not in columns:
                    columns.append(key)
        render(data, columns, ctx)
        return
    print(json.dumps(data, indent=2, default=str))


@app.command("request")
def request(
    ctx: typer.Context,
    method: str = typer.Argument(..., help="HTTP method: GET, POST, PUT, PATCH, DELETE"),
    path: str = typer.Argument(..., help="Backend path, e.g. /api/gam/features"),
    file: str | None = typer.Option(None, "--file", "-f", help="JSON object payload file"),
    query: list[str] | None = typer.Option(None, "--query", "-q", help="Query param key=value"),
):
    """Call an authenticated backend endpoint and print its JSend data."""
    method_name = method.upper()
    if method_name not in _METHODS:
        typer.echo(f"Error: unsupported method: {method}", err=True)
        raise typer.Exit(code=2)
    if not path.startswith("/api/"):
        typer.echo("Error: path must start with /api/.", err=True)
        raise typer.Exit(code=2)

    payload = _load_json_payload(file)
    params = _parse_query(query)
    kwargs: dict[str, Any] = {}
    if params:
        kwargs["params"] = params
    if payload is not None:
        kwargs["json"] = payload

    try:
        client = get_client()
        if method_name == "GET":
            data = client.get(path, **kwargs)
        elif method_name == "POST":
            data = client.post(path, **kwargs)
        elif method_name == "PUT":
            data = client.put(path, **kwargs)
        elif method_name == "PATCH":
            data = client.patch(path, **kwargs)
        else:
            data = client.delete(path, **kwargs)
        _render_any(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)
