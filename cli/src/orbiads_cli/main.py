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
    features,
    billing,
    network,
    line_items,    # Story 61.4
    jobs,          # Story 61.4
    settings_cmd,  # Story 61.7
    audiences,     # Story 61.7
    audit_log,     # Story 61.7
    preview,       # Story 61.7
    api,           # Generic API passthrough for migration coverage
    contacts,      # Story 62.4
    users,         # Story 62.4
    roles,         # Story 62.4
    licas,             # Story 62.1
    native_styles,     # Story 62.1
    creative_templates,# Story 62.1
    creative_qa,              # Story 62.6
    custom_targeting_values,  # Story 62.5
    pql,                      # Story 62.5
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
app.add_typer(features.app, name="features")
app.add_typer(billing.app, name="billing")
app.add_typer(network.app, name="network")
app.add_typer(line_items.app, name="line-items")  # Story 61.4
app.add_typer(jobs.app, name="jobs")              # Story 61.4
app.add_typer(settings_cmd.app, name="settings")  # Story 61.7 — server-side tenant settings (distinct from `config`)
app.add_typer(audiences.app, name="audiences")    # Story 61.7
app.add_typer(audit_log.app, name="audit")        # Story 61.7
app.add_typer(preview.app, name="preview")        # Story 61.7
app.add_typer(api.app, name="api")                # Generic API passthrough
app.add_typer(contacts.app, name="contacts")      # Story 62.4
app.add_typer(users.app, name="users")            # Story 62.4
app.add_typer(roles.app, name="roles")            # Story 62.4
app.add_typer(licas.app, name="licas")                                  # Story 62.1
app.add_typer(native_styles.app, name="native-styles")                  # Story 62.1
app.add_typer(creative_templates.app, name="creative-templates")        # Story 62.1
app.add_typer(creative_qa.app, name="creative-qa")                      # Story 62.6
app.add_typer(custom_targeting_values.app, name="custom-targeting-values")  # Story 62.5
app.add_typer(pql.app, name="pql")                                       # Story 62.5
