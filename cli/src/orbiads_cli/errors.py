"""Global error handler for OrbiAds CLI commands.

Every command should catch :class:`CliApiError` and delegate to
:func:`handle_error` for consistent stderr formatting and exit codes.

Usage pattern (applied in stories 55-3 through 55-8)::

    from orbiads_cli.client import CliApiError, get_client
    from orbiads_cli.errors import handle_error

    @app.command()
    def list(ctx: typer.Context):
        try:
            client = get_client()
            data = client.get("/api/campaigns")
            render(data, [...], ctx.obj)
        except CliApiError as e:
            handle_error(e)

Exit code semantics
-------------------
=====  =============  ==========================================
Code   HTTP origin    stderr message
=====  =============  ==========================================
0      2xx            *(none -- data goes to stdout)*
1      400/500/other  ``Error: {message}``
2      *(client)*     *(Typer auto-generates usage)*
3      404            ``Not found: {resource}``
4      401/403        ``Permission denied. Run `orbiads auth login`.``
5      409            ``Conflict: {message}``
6      412 (credits)  ``Insufficient credits. Balance: X, required: Y``
=====  =============  ==========================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import typer

if TYPE_CHECKING:
    from orbiads_cli.client import CliApiError


def handle_error(err: CliApiError) -> None:  # noqa: C901
    """Print a formatted error to *stderr* and raise ``typer.Exit``.

    The exit code on the raised :class:`typer.Exit` matches the semantic
    code stored on *err* so that callers (scripts, AI agents) can react
    programmatically without parsing text.
    """
    msg = _format_message(err)
    typer.echo(msg, err=True)
    raise typer.Exit(code=err.exit_code)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _format_message(err: CliApiError) -> str:
    """Return a human-readable single-line error string."""
    code = err.exit_code
    details = err.details

    if code == 3:
        resource = details.get("resource", err.message)
        return f"Not found: {resource}"

    if code == 4:
        return "Permission denied. Run `orbiads auth login`."

    if code == 5:
        return f"Conflict: {err.message}"

    if code == 6:
        balance = details.get("balance", "?")
        required = details.get("required", "?")
        return (
            f"Insufficient credits. Balance: {balance}, required: {required}"
        )

    # Generic fallback (exit code 1 and anything else).
    return f"Error: {err.message}"
