"""Tests for CLI exit codes — Story 55.9 Task 3.

For each semantic exit code (0-6), mock the corresponding HTTP status
and verify the CLI exit code AND stderr message.
"""

from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from orbiads_cli.client import CliApiError
from orbiads_cli.main import app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_client_raising(exit_code, message, error_code="", details=None):
    """Return a mock client whose get() raises CliApiError."""
    client = MagicMock()
    client.get.side_effect = CliApiError(exit_code, message, error_code, details)
    return client


def _mock_client_ok(data):
    """Return a mock client whose get() returns data."""
    client = MagicMock()
    client.get.return_value = data
    return client


# ===========================================================================
# Exit code 0: 200 → success
# ===========================================================================


class TestExitCode0:

    def test_success_returns_0(self, authenticated_config):
        client = _mock_client_ok({
            "balance": 50,
            "plan": "starter",
            "cycleStart": "2026-04-01",
            "overdue": False,
        })
        with patch("orbiads_cli.commands.billing.get_client", return_value=client):
            result = runner.invoke(app, ["billing", "balance"])
        assert result.exit_code == 0


# ===========================================================================
# Exit code 1: 500 → general error
# ===========================================================================


class TestExitCode1:

    def test_500_returns_exit_1(self, authenticated_config):
        client = _mock_client_raising(1, "Internal server error")
        with patch("orbiads_cli.commands.billing.get_client", return_value=client):
            result = runner.invoke(app, ["billing", "balance"])
        assert result.exit_code == 1
        assert "Error: Internal server error" in result.output


# ===========================================================================
# Exit code 2: invalid args (Typer handles natively)
# ===========================================================================


class TestExitCode2:

    def test_invalid_args_returns_exit_2(self, authenticated_config):
        """Missing required option triggers Typer's usage error (exit 2)."""
        result = runner.invoke(app, ["network", "switch"])
        assert result.exit_code == 2


# ===========================================================================
# Exit code 3: 404 → not found
# ===========================================================================


class TestExitCode3:

    def test_404_returns_exit_3(self, authenticated_config):
        client = _mock_client_raising(
            3, "Not found", details={"resource": "/api/campaigns/x"}
        )
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, ["campaigns", "get", "x"])
        assert result.exit_code == 3
        assert "Not found" in result.output


# ===========================================================================
# Exit code 4: 401 → permission denied
# ===========================================================================


class TestExitCode4:

    def test_401_returns_exit_4(self, authenticated_config):
        client = _mock_client_raising(4, "Unauthorized")
        with patch("orbiads_cli.commands.billing.get_client", return_value=client):
            result = runner.invoke(app, ["billing", "balance"])
        assert result.exit_code == 4
        assert "Permission denied" in result.output
        assert "orbiads auth login" in result.output


# ===========================================================================
# Exit code 5: 409 → conflict
# ===========================================================================


class TestExitCode5:

    def test_409_returns_exit_5(self, authenticated_config):
        client = MagicMock()
        client.post.side_effect = CliApiError(5, "Campaign already deployed")
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, ["campaigns", "deploy", "c1", "--yes"])
        assert result.exit_code == 5
        assert "Conflict: Campaign already deployed" in result.output


# ===========================================================================
# Exit code 6: 412 INSUFFICIENT_CREDITS → credits error
# ===========================================================================


class TestExitCode6:

    def test_412_insufficient_credits_returns_exit_6(self, authenticated_config):
        client = MagicMock()
        client.post.side_effect = CliApiError(
            6,
            "Insufficient credits",
            "INSUFFICIENT_CREDITS",
            {"balance": 2, "required": 5},
        )
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, ["campaigns", "deploy", "c1", "--yes"])
        assert result.exit_code == 6
        assert "Insufficient credits" in result.output
        assert "Balance: 2" in result.output
        assert "required: 5" in result.output
