"""Two-step confirmation for irreversible / overbooking writes (story 116-10).

The OrbiAds backend refuses an irreversible REST write (order / line item ``delete``,
``*_and_overbook``, permanent LICA deletion) that does not carry the confirmation token of a
preview: ``dryRun=true`` returns ``{preview, confirmationToken}`` and executes nothing, the
same request with ``confirmationToken`` executes (single use, 5 minutes, bound to the active
GAM network). This helper drives the two calls so the commands stay one-liners:

1. send the payload with ``dryRun=true``;
2. show the preview (irreversibility / overbook warnings, targets, advisories, cost) on
   stderr and ask the human (``confirm``);
3. send the payload again with the ``confirmationToken``.

``--yes`` (and a non-TTY) only skips step 2's HUMAN prompt: the preview and the token round
trip always happen, so a script can no longer fire an irreversible write in one blind call.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import typer

from orbiads_cli.client import CliApiError
from orbiads_cli.output import OutputContext

_PREVIEW_ADVISORY_KEYS = (
    "targets",
    "missingAssociations",
    "missingIds",
    "uncheckedIds",
    "partiallyCheckedIds",
)


def _echo(message: str) -> None:
    typer.echo(message, err=True)


def show_preview(preview: dict[str, Any]) -> None:
    """Print what is about to be confirmed (stderr; stdout stays the final result)."""
    items = preview.get("preview")
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        label = "IRREVERSIBLE" if item.get("irreversible") else "Preview"
        if item.get("overbook"):
            label = "OVERBOOK"
        _echo(f"{label}: {item.get('operation', '')} {_summary(item)}".rstrip())
        if item.get("warning"):
            _echo(f"  Warning: {item['warning']}")
    if preview.get("preflightSkipped"):
        _echo("  The pre-delete check was skipped (GAM could not be read).")
    if preview.get("warning"):
        _echo(f"  Warning: {preview['warning']}")
    for key in _PREVIEW_ADVISORY_KEYS:
        if preview.get(key):
            _echo(f"  {key}: {preview[key]}")
    if "estimatedCost" in preview:
        _echo(f"  Estimated cost: {preview['estimatedCost']} credit(s)")


def _summary(item: dict[str, Any]) -> str:
    parts = []
    for key in ("action", "order_ids", "line_item_ids", "line_item_id", "creative_ids"):
        if key in item:
            parts.append(f"{key}={item[key]}")
    return " ".join(parts)


def _rejects_two_step_fields(err: CliApiError) -> bool:
    """True when a 422 ``extra=forbid`` error names ``dryRun`` / ``confirmationToken``.

    A backend that predates story 116-10 declares the route's body ``extra=forbid`` and
    answers a dry-run with ``VALIDATION_ERROR`` + ``fields: [{field: dryRun, type:
    extra_forbidden}]``; the generic "Request validation failed" hides the real cause.
    """
    if err.error_code != "VALIDATION_ERROR":
        return False
    fields = err.details.get("fields")
    return any(
        isinstance(f, dict)
        and f.get("type") == "extra_forbidden"
        and f.get("field") in ("dryRun", "confirmationToken")
        for f in (fields if isinstance(fields, list) else [])
    )


def run_guarded_post(
    post: Callable[[dict[str, Any]], Any],
    payload: dict[str, Any],
    *,
    ctx: OutputContext,
    prompt: str,
    confirm_fn: Callable[[str, OutputContext], bool],
    two_step: bool,
) -> Any:
    """POST ``payload`` through the dry-run -> token flow when required.

    ``post(body)`` sends one request to the route (the command passes
    ``lambda body: client.post("/api/gam/...", json=body)``).

    ``two_step=False`` is for actions the CLI knows to be reversible: they stay one call, but
    if the server answers ``CONFIRMATION_REQUIRED`` anyway (server stricter than the CLI's
    own table) the two-step flow is used instead of failing.
    """
    if not two_step:
        try:
            return post(payload)
        except CliApiError as err:
            if err.error_code != "CONFIRMATION_REQUIRED":
                raise

    try:
        preview = post({**payload, "dryRun": True})
    except CliApiError as err:
        if _rejects_two_step_fields(err):
            raise CliApiError(
                1,
                "The OrbiAds server is older than this CLI: it does not know the "
                "two-step confirmation fields (dryRun / confirmationToken), so nothing was "
                "executed. Redeploy / upgrade the backend before using this command.",
                "SERVER_OLDER_THAN_CLI",
            ) from err
        raise
    token = preview.get("confirmationToken") if isinstance(preview, dict) else None
    if not token:
        raise CliApiError(
            1,
            "The server did not return a confirmation token for the preview; nothing was "
            "executed. Upgrade the OrbiAds CLI and retry.",
            "NO_CONFIRMATION_TOKEN",
        )
    show_preview(preview)
    if not confirm_fn(prompt, ctx):
        raise typer.Exit(code=0)
    return post({**payload, "confirmationToken": token})
