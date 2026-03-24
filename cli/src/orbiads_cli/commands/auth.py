"""Authentication commands: login, logout, status."""

import time
import webbrowser

import httpx
import typer
from rich.console import Console

from orbiads_cli import config
from orbiads_cli.config import DEFAULT_API_URL

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
                    # Save tokens
                    config.set_token(
                        poll_data["accessToken"],
                        poll_data["refreshToken"],
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
def status() -> None:
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
        err_console.print("[red]Token invalid. Run `orbiads auth login` to re-authenticate.[/red]")
        raise typer.Exit(code=4)

    if resp.status_code != 200:
        err_console.print(f"[red]Unexpected response (HTTP {resp.status_code}).[/red]")
        raise typer.Exit(code=1)

    body = resp.json()
    if body.get("error"):
        err_console.print(f"[red]Server error: {body['error'].get('message', 'Unknown')}[/red]")
        raise typer.Exit(code=1)

    data = body.get("data", {})
    email = data.get("email", "unknown")
    network = data.get("networkCode", "not set")

    err_console.print(f"  Authenticated as: [bold]{email}[/bold]")
    err_console.print(f"  GAM Network:      [bold]{network}[/bold]")
    raise typer.Exit(code=0)
