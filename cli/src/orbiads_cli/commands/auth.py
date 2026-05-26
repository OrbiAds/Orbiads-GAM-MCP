"""Authentication commands: login, logout, status."""

import time
import webbrowser

import httpx
import typer
from rich.console import Console

from orbiads_cli import config
from orbiads_cli.config import (
    DEFAULT_API_URL,
    DEFAULT_FIREBASE_API_KEY,
    DEFAULT_FIREBASE_REFERER,
)
from orbiads_cli.output import OutputContext, render_detail

app = typer.Typer(help="Authentication (login, logout, status)", no_args_is_help=True)

# stderr console for all auth output (stdout reserved for JSON data)
err_console = Console(stderr=True)

# Maximum polling duration in seconds (match server device code TTL)
_MAX_POLL_DURATION = 900

# HTTP timeout for individual requests
_HTTP_TIMEOUT = 30.0


def _get_api_url() -> str:
    """Return the configured API URL or the default."""
    cfg = config.load()
    return cfg.get("apiUrl", DEFAULT_API_URL) if cfg else DEFAULT_API_URL


def _exchange_custom_token(custom_token: str) -> tuple[str, str]:
    """Exchange a Firebase custom token for CLI session tokens."""
    import os

    firebase_key = os.environ.get("ORBIADS_FIREBASE_KEY") or DEFAULT_FIREBASE_API_KEY
    try:
        resp = httpx.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={firebase_key}",
            headers={"Referer": DEFAULT_FIREBASE_REFERER},
            json={"token": custom_token, "returnSecureToken": True},
            timeout=_HTTP_TIMEOUT,
        )
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        err_console.print(f"[red]Failed to finalize login: {exc}[/red]")
        raise typer.Exit(code=1) from None

    data = resp.json()
    id_token = data.get("idToken")
    refresh_token = data.get("refreshToken")
    if not id_token or not refresh_token:
        err_console.print("[red]Failed to finalize login: invalid Firebase response.[/red]")
        raise typer.Exit(code=1)
    return id_token, refresh_token


def _refresh_stored_token() -> str | None:
    """Refresh the stored Firebase ID token, mirroring the main CLI client."""
    import os

    cfg = config.load() or {}
    refresh_token = cfg.get("refreshToken")
    if not refresh_token:
        return None

    firebase_key = os.environ.get("ORBIADS_FIREBASE_KEY") or DEFAULT_FIREBASE_API_KEY
    try:
        resp = httpx.post(
            f"https://securetoken.googleapis.com/v1/token?key={firebase_key}",
            headers={"Referer": DEFAULT_FIREBASE_REFERER},
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            timeout=15.0,
        )
    except httpx.HTTPError:
        return None

    if resp.status_code != 200:
        return None

    data = resp.json()
    new_token = data.get("id_token")
    new_refresh = data.get("refresh_token") or refresh_token
    if not new_token:
        return None

    config.set_token(new_token, new_refresh)
    return str(new_token)


@app.command()
def login() -> None:
    """Authenticate with OrbiAds via browser device flow."""
    api_url = _get_api_url()

    # Step 1: Request a device code
    try:
        resp = httpx.post(
            f"{api_url}/api/auth/gam/device-code",
            timeout=_HTTP_TIMEOUT,
        )
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        err_console.print(f"[red]Failed to initiate login: {exc}[/red]")
        raise typer.Exit(code=1) from None

    body = resp.json()
    if body.get("error"):
        err_console.print(f"[red]Server error: {body['error'].get('message', 'Unknown error')}[/red]")
        raise typer.Exit(code=1)

    data = body["data"]
    device_code = data["deviceCode"]
    user_code = data["userCode"]
    verification_url = data["verificationUrl"]
    poll_interval = data.get("pollInterval", 5)

    # Step 2: Display instructions and open browser
    err_console.print()
    err_console.print(f"  To authorize, visit: [bold cyan]{verification_url}[/bold cyan]")
    err_console.print(f"  Your code: [bold yellow]{user_code}[/bold yellow]")
    err_console.print()
    err_console.print("  Waiting for authorization...", style="dim")

    webbrowser.open(verification_url)

    # Step 3: Poll for authorization
    start_time = time.monotonic()
    try:
        with err_console.status("[bold green]Waiting for browser authorization...") as spinner:
            while True:
                elapsed = time.monotonic() - start_time
                if elapsed >= _MAX_POLL_DURATION:
                    err_console.print(
                        "[red]Authorization timed out (max 15 min). Please try again.[/red]"
                    )
                    raise typer.Exit(code=4)

                time.sleep(poll_interval)

                try:
                    poll_resp = httpx.get(
                        f"{api_url}/api/auth/gam/device-token-status",
                        params={"deviceCode": device_code},
                        timeout=_HTTP_TIMEOUT,
                    )
                    poll_resp.raise_for_status()
                except httpx.HTTPError as exc:
                    err_console.print(f"[red]Polling error: {exc}[/red]")
                    raise typer.Exit(code=1) from None

                poll_body = poll_resp.json()
                if poll_body.get("error"):
                    err_console.print(
                        f"[red]Server error: {poll_body['error'].get('message', 'Unknown error')}[/red]"
                    )
                    raise typer.Exit(code=1)

                poll_data = poll_body["data"]
                status_value = poll_data["status"]

                if status_value == "authorized":
                    if poll_data.get("customToken"):
                        access_token, refresh_token = _exchange_custom_token(
                            poll_data["customToken"]
                        )
                    else:
                        # Backward compatibility for legacy servers that returned
                        # Firebase tokens directly.
                        access_token = poll_data["accessToken"]
                        refresh_token = poll_data["refreshToken"]

                    config.set_token(
                        access_token,
                        refresh_token,
                    )
                    spinner.stop()
                    err_console.print("[bold green]Authenticated successfully![/bold green]")
                    raise typer.Exit(code=0)

                elif status_value == "expired":
                    spinner.stop()
                    err_console.print(
                        "[red]Authorization expired. Please try again.[/red]"
                    )
                    raise typer.Exit(code=4)

                # status == "pending" — continue polling

    except KeyboardInterrupt:
        err_console.print("\n[yellow]Authorization cancelled.[/yellow]")
        raise typer.Exit(code=1) from None


@app.command()
def logout() -> None:
    """Clear local credentials."""
    config.clear()
    err_console.print("Logged out.")
    raise typer.Exit(code=0)


@app.command()
def status(ctx: typer.Context) -> None:
    """Show current authentication status."""
    if not config.has_token():
        err_console.print("Not authenticated.")
        raise typer.Exit(code=4)

    api_url = _get_api_url()
    token = config.get_token()

    try:
        resp = httpx.get(
            f"{api_url}/api/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=_HTTP_TIMEOUT,
        )
    except httpx.HTTPError as exc:
        err_console.print(f"[red]Request failed: {exc}[/red]")
        raise typer.Exit(code=1) from None

    if resp.status_code == 401:
        refreshed_token = _refresh_stored_token()
        if refreshed_token:
            token = refreshed_token
            try:
                resp = httpx.get(
                    f"{api_url}/api/me",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=_HTTP_TIMEOUT,
                )
            except httpx.HTTPError as exc:
                err_console.print(f"[red]Request failed: {exc}[/red]")
                raise typer.Exit(code=1) from None

    if resp.status_code == 401:
        err_console.print("[red]Token invalid. Run `orbiads auth login` to re-authenticate.[/red]")
        raise typer.Exit(code=4)

    if resp.status_code != 200:
        err_console.print(f"[red]Unexpected response (HTTP {resp.status_code}).[/red]")
        raise typer.Exit(code=1)

    body = resp.json()
    if body.get("error"):
        err_console.print(f"[red]Server error: {body['error'].get('message', 'Unknown')}[/red]")
        raise typer.Exit(code=1)

    data = dict(body.get("data", {}))
    email = data.get("email", "unknown")
    network = _resolve_network_code(api_url, token, data)
    data["email"] = email
    data["networkCode"] = network

    output_ctx = ctx.obj if isinstance(ctx.obj, OutputContext) else OutputContext()
    if output_ctx.format == "json":
        render_detail(data, output_ctx)
        raise typer.Exit(code=0)

    err_console.print(f"  Authenticated as: [bold]{email}[/bold]")
    err_console.print(f"  GAM Network:      [bold]{network or 'not set'}[/bold]")
    raise typer.Exit(code=0)


def _resolve_network_code(api_url: str, token: str, data: dict) -> str | None:
    network = data.get("networkCode") or data.get("network_code")
    if network:
        return str(network)

    cfg = config.load() or {}
    if cfg.get("networkCode"):
        return str(cfg["networkCode"])

    try:
        resp = httpx.get(
            f"{api_url}/api/auth/gam/connection-state",
            headers={"Authorization": f"Bearer {token}"},
            timeout=_HTTP_TIMEOUT,
        )
    except httpx.HTTPError:
        return None

    if resp.status_code != 200:
        return None

    try:
        body = resp.json()
    except ValueError:
        return None

    state_data = body.get("data", {})
    network = state_data.get("networkCode") or state_data.get("network_code")
    return str(network) if network else None
