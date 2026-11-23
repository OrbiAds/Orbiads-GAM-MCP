"""Story 117-19 - REST/CLI billing parity: insufficient credits on a now-billed command.

The backend answers 402 with the MCP error ``INSUFFICIENT_CREDITS`` and the MCP message
"Insufficient credits (available: 0.2, required: 0.5). Top up your balance." (fractional
credits). The CLI must show balance + required, never a trace, and exit with code 6.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest
from orbiads_cli.client import CliApiError, OrbiAdsClient
from orbiads_cli.main import app
from typer.testing import CliRunner

runner = CliRunner()

MESSAGE = "Insufficient credits (available: 0.2, required: 0.5). Top up your balance."


def _backend_402() -> httpx.Response:
    return httpx.Response(
        402, json={"data": None, "error": {"code": "INSUFFICIENT_CREDITS", "message": MESSAGE}}
    )


def test_parse_response_extracts_fractional_balance_and_required():
    try:
        OrbiAdsClient._parse_response(_backend_402())
    except CliApiError as exc:
        assert exc.exit_code == 6
        assert exc.error_code == "INSUFFICIENT_CREDITS"
        assert exc.details == {"balance": 0.2, "required": 0.5}
    else:  # pragma: no cover - must raise
        raise AssertionError("a 402 INSUFFICIENT_CREDITS must raise CliApiError")


def test_legacy_balance_wording_still_parses_as_integers():
    with pytest.raises(CliApiError) as exc_info:
        OrbiAdsClient._parse_response(
            httpx.Response(
                402,
                json={
                    "data": None,
                    "error": {"code": "INSUFFICIENT_CREDITS", "message": "balance: 2, required: 5"},
                },
            )
        )
    assert exc_info.value.details == {"balance": 2, "required": 5}


def test_billed_command_shows_balance_required_and_exits_6(authenticated_config):
    client = MagicMock()
    client.post.side_effect = lambda path, **kw: OrbiAdsClient._parse_response(_backend_402())
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(app, ["line-items", "duplicate", "7334823028"])
    assert result.exit_code == 6
    output = result.output + (result.stderr if result.stderr_bytes else "")
    assert "Insufficient credits. Balance: 0.2, required: 0.5" in output
    assert "Traceback" not in output
