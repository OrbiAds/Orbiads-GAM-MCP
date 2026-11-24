"""Repair ``repair-cli-403-server-message`` (live R118b, v2.0.75): every 403 was printed as
"Permission denied. Run `orbiads auth login`." — hiding MCM_NOT_ENABLED and the backend
business 403s whose message says what to do (``backend/src/core/auth.py``: GAM_NOT_CONNECTED,
GAM_PERMISSIONS_DESYNC, WRITE_FORBIDDEN). Only a token problem keeps the login hint.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.client import CliApiError
from orbiads_cli.errors import _format_message
from orbiads_cli.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    ("code", "message"),
    [
        (
            "GAM_NOT_CONNECTED",
            "Connect your GAM account before performing this action.",
        ),
        (
            "GAM_PERMISSIONS_DESYNC",
            "Reconnect your GAM account to refresh permissions.",
        ),
        ("WRITE_FORBIDDEN", "Your GAM role does not allow write operations"),
        (
            "MCM_NOT_ENABLED",
            "Multiple Customer Management (MCM) is not enabled on this GAM network.",
        ),
    ],
)
def test_business_403_shows_the_server_code_and_message(code, message):
    text = _format_message(CliApiError(4, message, code))
    assert text == f"Permission denied ({code}): {message}"
    assert "auth login" not in text


@pytest.mark.parametrize(
    "code", ["AUTH_REQUIRED", "TOKEN_EXPIRED", "TOKEN_REVOKED", "", "HTTP_ERROR"]
)
def test_token_problems_keep_the_login_hint(code):
    text = _format_message(CliApiError(4, "whatever", code))
    assert text == "Permission denied. Run `orbiads auth login`."


def test_live_r118b_case_end_to_end(authenticated_config):
    """`orbiads mcm earnings` on a network without MCM (adclick, v2.0.75)."""
    client = MagicMock()
    client.get.side_effect = CliApiError(
        4,
        "Multiple Customer Management (MCM) is not enabled on this GAM network: it is not an "
        "MCM parent, so it has no MCM earnings.",
        "MCM_NOT_ENABLED",
    )
    with patch("orbiads_cli.commands.mcm.get_client", return_value=client):
        result = runner.invoke(
            app, ["mcm", "earnings", "--month", "10", "--year", "2026"]
        )
    assert result.exit_code == 4  # exit code semantics unchanged
    assert (
        "Permission denied (MCM_NOT_ENABLED): Multiple Customer Management"
        in result.output
    )
    assert "auth login" not in result.output
