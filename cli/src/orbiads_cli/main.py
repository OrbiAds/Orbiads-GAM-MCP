"""OrbiAds CLI — Google Ad Manager from the command line."""

import typer

from orbiads_cli import __version__
from orbiads_cli.config import has_token
from orbiads_cli.output import OutputContext
from orbiads_cli.commands import (
    advertisers,
    auth,
    campaigns,
    config_cmd,
    orders,
    creatives,
    inventory,
    reporting,
    billing,
    network,
)

app = typer.Typer(
    name="orbiads",
    help="OrbiAds CLI — Google Ad Manager from the command line",
    no_args_is_help=True,
)


def version_callback(value: bool):
    if value:
        print(f"orbiads {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show version"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON to stdout"),
    output: str = typer.Option(None, "--output", help="Output format: table, json, csv"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmations"),
):
    """OrbiAds CLI — Google Ad Manager from the command line"""
    # Build OutputContext from global flags and store in context
    ctx.obj = OutputContext.from_flags(json_output, output, yes)

    # Auth guard: skip for auth group, help, and version
    if ctx.invoked_subcommand in ("auth", "config"):
        return
    if ctx.invoked_subcommand is None:
        return
    if not has_token():
        typer.echo("Not authenticated. Run `orbiads auth login` first.", err=True)
        raise typer.Exit(code=4)


# Register command groups
app.add_typer(auth.app, name="auth")
app.add_typer(config_cmd.app, name="config", help="Manage CLI configuration")
app.add_typer(advertisers.app, name="advertisers")
app.add_typer(campaigns.app, name="campaigns")
app.add_typer(orders.app, name="orders")
app.add_typer(creatives.app, name="creatives")
app.add_typer(inventory.app, name="inventory")
app.add_typer(reporting.app, name="reporting")
app.add_typer(billing.app, name="billing")
app.add_typer(network.app, name="network")
