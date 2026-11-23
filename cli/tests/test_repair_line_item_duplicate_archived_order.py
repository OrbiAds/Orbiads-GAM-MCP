"""Repair line-item-duplicate-archived-order - `orbiads line-items duplicate`.

The backend now answers a duplicate into an archived order with a structured
422 (``GAM_ORDER_ARCHIVED`` + actionable message) instead of a bare 500
("An internal error occurred"). The CLI must surface that message and fail
with a non-zero exit code.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
from typer.testing import CliRunner

from orbiads_cli.client import CliApiError, OrbiAdsClient
from orbiads_cli.main import app

runner = CliRunner()

MESSAGE = (
    "GAM refused the change: the target order is archived (a GAM rule, retrying will "
    "not help). Unarchive the order first (order lifecycle 'unarchive'), or target "
    "another order - e.g. a line item duplicate accepts an orderId override."
)


def _backend_422() -> httpx.Response:
    return httpx.Response(
        422,
        json={"data": None, "error": {"code": "GAM_ORDER_ARCHIVED", "message": MESSAGE}},
    )


def test_parse_response_keeps_structured_code_and_message():
    try:
        OrbiAdsClient._parse_response(_backend_422())
    except CliApiError as exc:
        assert exc.error_code == "GAM_ORDER_ARCHIVED"
        assert exc.message == MESSAGE
        assert exc.exit_code != 0
    else:  # pragma: no cover - must raise
        raise AssertionError("a 422 must raise CliApiError")


def test_duplicate_command_shows_actionable_message(authenticated_config):
    client = MagicMock()

    def _post(path, **kwargs):
        assert path == "/api/gam/line-items/7334823028/duplicate"
        return OrbiAdsClient._parse_response(_backend_422())

    client.post.side_effect = _post
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(app, ["line-items", "duplicate", "7334823028"])
    assert result.exit_code != 0
    output = result.output + (result.stderr if result.stderr_bytes else "")
    assert "target order is archived" in output
    assert "internal error" not in output.lower()
