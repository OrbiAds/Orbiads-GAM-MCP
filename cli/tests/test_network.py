"""Tests for CLI network commands (info, list, switch) — Story 55.3.

Uses typer.testing.CliRunner with mocked OrbiAdsClient to avoid real API traffic.
"""

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli import config as config_mod
from orbiads_cli.client import CliApiError
from orbiads_cli.main import app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _setup_auth(tmp_config):
    """Write a valid config so the auth guard and get_client() pass."""
    config_mod.save({
        "apiUrl": "https://test.example.com",
        "token": "test-token",
        "refreshToken": "test-refresh",
    })


def _mock_client(get_return=None, post_return=None, side_effect=None):
    """Return a patched get_client that returns a mock OrbiAdsClient."""
    client = MagicMock()
    if side_effect:
        client.get.side_effect = side_effect
        client.post.side_effect = side_effect
    else:
        client.get.return_value = get_return
        client.post.return_value = post_return
    return client


# ===========================================================================
# orbiads network info
# ===========================================================================


class TestNetworkInfo:

    def test_info_connected(self, tmp_config):
        """Display connection state in table format."""
        _setup_auth(tmp_config)
        client = _mock_client(get_return={
            "state": "CONNECTED_READY",
            "networkCode": "12345",
        })

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "info"])

        assert result.exit_code == 0
        assert "CONNECTED_READY" in result.output
        assert "12345" in result.output

    def test_info_json_output(self, tmp_config):
        """--json flag outputs JSON to stdout."""
        _setup_auth(tmp_config)
        client = _mock_client(get_return={
            "state": "NOT_CONNECTED",
            "networkCode": None,
        })

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["--json", "network", "info"])

        assert result.exit_code == 0
        assert '"state"' in result.output
        assert "NOT_CONNECTED" in result.output

    def test_info_api_error(self, tmp_config):
        """API error yields correct exit code."""
        _setup_auth(tmp_config)
        client = _mock_client(side_effect=CliApiError(4, "Unauthorized"))

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "info"])

        assert result.exit_code == 4


# ===========================================================================
# orbiads network list
# ===========================================================================


class TestNetworkList:

    def test_list_networks(self, tmp_config):
        """Display networks in table format."""
        _setup_auth(tmp_config)
        client = _mock_client(get_return={
            "networks": [
                {"networkCode": "11111", "displayName": "Network A"},
                {"networkCode": "22222", "displayName": "Network B"},
            ],
        })

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "list"])

        assert result.exit_code == 0
        assert "11111" in result.output
        assert "22222" in result.output
        assert "Network A" in result.output

    def test_list_json_output(self, tmp_config):
        """--json flag outputs JSON array."""
        _setup_auth(tmp_config)
        client = _mock_client(get_return={
            "networks": [
                {"networkCode": "11111", "displayName": "Network A"},
            ],
        })

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["--json", "network", "list"])

        assert result.exit_code == 0
        assert '"networkCode"' in result.output
        assert "11111" in result.output

    def test_list_empty(self, tmp_config):
        """Empty networks list renders without error."""
        _setup_auth(tmp_config)
        client = _mock_client(get_return={"networks": []})

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "list"])

        assert result.exit_code == 0

    def test_list_api_error(self, tmp_config):
        """API 404 yields exit code 3."""
        _setup_auth(tmp_config)
        client = _mock_client(side_effect=CliApiError(3, "Not found", "GAM_NO_PENDING_OAUTH"))

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "list"])

        assert result.exit_code == 3


# ===========================================================================
# orbiads network switch
# ===========================================================================


class TestNetworkSwitch:

    def test_switch_success(self, tmp_config):
        """Switch updates server and local config."""
        _setup_auth(tmp_config)
        client = _mock_client(post_return={"networkCode": "99999"})

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "switch", "--network-code", "99999"])

        assert result.exit_code == 0
        # Verify local config updated
        cfg = config_mod.load()
        assert cfg["networkCode"] == "99999"
        # Confirmation message goes to stderr (captured in output by CliRunner)
        assert "Switched to network 99999" in result.output

    def test_switch_api_error(self, tmp_config):
        """API error during switch yields correct exit code."""
        _setup_auth(tmp_config)
        client = _mock_client(side_effect=CliApiError(1, "Invalid network code"))

        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "switch", "--network-code", "bad"])

        assert result.exit_code == 1
        # Config should NOT be updated on error
        cfg = config_mod.load()
        assert cfg.get("networkCode") is None

    def test_switch_missing_option(self, tmp_config):
        """Missing --network-code option shows usage error."""
        _setup_auth(tmp_config)

        result = runner.invoke(app, ["network", "switch"])

        assert result.exit_code == 2  # typer usage error
