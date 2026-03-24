"""Tests for CLI commands — Story 55.9 Task 2.

One test per command group minimum, using CliRunner + mocked get_client().
All HTTP traffic mocked via MagicMock on OrbiAdsClient.
"""

import json
from unittest.mock import patch, MagicMock

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _setup_auth(tmp_config):
    """Write a valid config so the auth guard passes."""
    from orbiads_cli import config as config_mod
    config_mod.save({
        "apiUrl": "https://test.example.com",
        "token": "test-token",
        "refreshToken": "test-refresh",
    })


def _mock_client(get_return=None, post_return=None):
    """Create a mock OrbiAdsClient with preset return values."""
    client = MagicMock()
    client.get.return_value = get_return
    client.post.return_value = post_return
    return client


# ===========================================================================
# network info
# ===========================================================================


class TestNetworkInfoCommand:

    def test_network_info_calls_connection_state(self, authenticated_config):
        client = _mock_client(get_return={
            "state": "CONNECTED_READY",
            "networkCode": "12345",
        })
        with patch("orbiads_cli.commands.network.get_client", return_value=client):
            result = runner.invoke(app, ["network", "info"])
        assert result.exit_code == 0
        client.get.assert_called_once_with("/api/auth/gam/connection-state")
        assert "CONNECTED_READY" in result.output


# ===========================================================================
# campaigns list
# ===========================================================================


class TestCampaignsListCommand:

    def test_campaigns_list(self, authenticated_config):
        client = _mock_client(get_return=[
            {"id": "c1", "name": "Test", "status": "draft", "createdAt": "2026-03-23"},
        ])
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, ["campaigns", "list"])
        assert result.exit_code == 0
        client.get.assert_called_once_with("/api/campaigns", params={})
        assert "Test" in result.output

    def test_campaigns_list_with_params(self, authenticated_config):
        client = _mock_client(get_return=[])
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, [
                "campaigns", "list", "--status", "deployed", "--limit", "10",
            ])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/campaigns", params={"status": "deployed", "limit": 10}
        )

    def test_campaigns_list_json(self, authenticated_config):
        client = _mock_client(get_return=[
            {"id": "c1", "name": "Test", "status": "draft", "createdAt": "2026-03-23"},
        ])
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, ["--json", "campaigns", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "Test"


# ===========================================================================
# orders list
# ===========================================================================


class TestOrdersListCommand:

    def test_orders_list(self, authenticated_config):
        client = _mock_client(get_return={
            "orders": [
                {"id": "o1", "name": "Order 1", "advertiserName": "Acme", "status": "active"},
            ]
        })
        with patch("orbiads_cli.commands.orders.get_client", return_value=client):
            result = runner.invoke(app, ["orders", "list"])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/gam/orders", params={"limit": 50, "offset": 0}
        )
        assert "Order 1" in result.output

    def test_orders_list_with_advertiser_id(self, authenticated_config):
        client = _mock_client(get_return={
            "orders": [
                {"id": "o2", "name": "Filtered", "advertiserName": "X", "status": "active"},
            ]
        })
        with patch("orbiads_cli.commands.orders.get_client", return_value=client):
            result = runner.invoke(app, [
                "orders", "list", "--advertiser-id", "adv-123",
            ])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/gam/orders", params={"advertiser_id": "adv-123"}
        )


# ===========================================================================
# creatives list
# ===========================================================================


class TestCreativesListCommand:

    def test_creatives_list_with_type_filter(self, authenticated_config):
        client = _mock_client(get_return=[
            {"id": "cr1", "name": "Banner", "type": "image", "size": "300x250", "status": "active"},
        ])
        with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
            result = runner.invoke(app, ["creatives", "list", "--type", "image"])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/gam/creatives", params={"limit": 50, "type": "image"}
        )
        assert "Banner" in result.output

    def test_creatives_list_default(self, authenticated_config):
        client = _mock_client(get_return=[])
        with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
            result = runner.invoke(app, ["creatives", "list"])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/gam/creatives", params={"limit": 50}
        )


# ===========================================================================
# inventory ad-units
# ===========================================================================


class TestInventoryAdUnitsCommand:

    def test_ad_units_with_search(self, authenticated_config):
        client = _mock_client(get_return=[
            {"id": "au1", "name": "homepage_top", "sizes": "728x90", "parentPath": "/"},
        ])
        with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
            result = runner.invoke(app, ["inventory", "ad-units", "--search", "homepage"])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/gam/ad-units", params={"limit": 50, "search": "homepage"}
        )
        assert "homepage_top" in result.output

    def test_ad_units_default(self, authenticated_config):
        client = _mock_client(get_return=[])
        with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
            result = runner.invoke(app, ["inventory", "ad-units"])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/gam/ad-units", params={"limit": 50}
        )


# ===========================================================================
# reporting run
# ===========================================================================


class TestReportingRunCommand:

    def test_reporting_run(self, authenticated_config):
        client = _mock_client(post_return={
            "headers": ["DATE", "IMPRESSIONS"],
            "rows": [
                {"DATE": "2026-03-01", "IMPRESSIONS": "1000"},
            ],
        })
        with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
            result = runner.invoke(app, [
                "reporting", "run",
                "--dimensions", "DATE",
                "--metrics", "IMPRESSIONS",
                "--start", "2026-03-01",
                "--end", "2026-03-31",
            ])
        assert result.exit_code == 0
        client.post.assert_called_once_with(
            "/api/gam/reports/custom",
            json={
                "dimensions": ["DATE"],
                "metrics": ["IMPRESSIONS"],
                "startDate": "2026-03-01",
                "endDate": "2026-03-31",
            },
        )


# ===========================================================================
# billing balance
# ===========================================================================


class TestBillingBalanceCommand:

    def test_billing_balance(self, authenticated_config):
        client = _mock_client(get_return={
            "balance": 42,
            "plan": "starter",
            "cycleStart": "2026-04-01",
            "overdue": False,
        })
        with patch("orbiads_cli.commands.billing.get_client", return_value=client):
            result = runner.invoke(app, ["billing", "balance"])
        assert result.exit_code == 0
        client.get.assert_called_once_with("/api/billing")
        assert "42" in result.output
        assert "starter" in result.output

    def test_billing_balance_json(self, authenticated_config):
        client = _mock_client(get_return={
            "balance": 42,
            "plan": "starter",
            "cycleStart": "2026-04-01",
            "overdue": False,
        })
        with patch("orbiads_cli.commands.billing.get_client", return_value=client):
            result = runner.invoke(app, ["--json", "billing", "balance"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["credits"] == 42
        assert data["plan"] == "starter"
