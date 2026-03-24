"""Config command group — orbiads config show / set."""

import typer

from orbiads_cli import config
from orbiads_cli.output import OutputContext, render_detail

app = typer.Typer(help="Manage CLI configuration")

VALID_OUTPUTS = ("table", "json", "csv")


def _mask_token(value: str | None) -> str:
    """Mask a token: show first 8 chars + '...' or 'not set'."""
    if not value:
        return "not set"
    if len(value) <= 8:
        return value
    return value[:8] + "..."


@app.command("show")
def show(ctx: typer.Context):
    """Display current configuration."""
    cfg = config.load()
    if cfg is None:
        typer.echo(
            "No configuration found. Run `orbiads auth login` first.",
            err=True,
        )
        raise typer.Exit(code=4)

    # Build display dict with masked tokens
    display = {
        "token": _mask_token(cfg.get("token")),
        "refreshToken": _mask_token(cfg.get("refreshToken")),
        "networkCode": cfg.get("networkCode", "not set"),
        "apiUrl": cfg.get("apiUrl", "not set"),
        "defaultOutput": cfg.get("defaultOutput", "not set"),
    }

    out_ctx: OutputContext = ctx.obj if isinstance(ctx.obj, OutputContext) else OutputContext()
    render_detail(display, out_ctx)


@app.command("set")
def set_config(
    ctx: typer.Context,
    network_code: str = typer.Option(None, "--network-code", help="GAM network code"),
    api_url: str = typer.Option(None, "--api-url", help="Backend API URL"),
    default_output: str = typer.Option(
        None,
        "--default-output",
        help=f"Default output format ({', '.join(VALID_OUTPUTS)})",
    ),
):
    """Update configuration fields."""
    cfg = config.load()
    if cfg is None:
        typer.echo(
            "No configuration found. Run `orbiads auth login` first.",
            err=True,
        )
        raise typer.Exit(code=4)

    if default_output is not None and default_output not in VALID_OUTPUTS:
        typer.echo(
            f"Invalid output format '{default_output}'. Must be one of: {', '.join(VALID_OUTPUTS)}",
            err=True,
        )
        raise typer.Exit(code=2)

    if network_code is not None:
        cfg["networkCode"] = network_code
    if api_url is not None:
        cfg["apiUrl"] = api_url
    if default_output is not None:
        cfg["defaultOutput"] = default_output

    config.save(cfg)
    typer.echo("Configuration updated.", err=True)
