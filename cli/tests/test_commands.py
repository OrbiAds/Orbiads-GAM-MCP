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
    # Audit F0-3: `creatives list` now requires --advertiser-id and hits the
    # real advertiser-scoped endpoint. The old `/api/gam/creatives` collection
    # route never existed (always 404'd).

    def test_creatives_list_for_advertiser(self, authenticated_config):
        client = _mock_client(get_return=[
            {"id": "cr1", "name": "Banner", "type": "image", "size": "300x250", "status": "active"},
        ])
        with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
            result = runner.invoke(app, ["creatives", "list", "--advertiser-id", "555"])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/gam/advertisers/555/creatives", params={"limit": 50}
        )
        assert "Banner" in result.output

    def test_creatives_list_requires_advertiser_id(self, authenticated_config):
        client = _mock_client(get_return=[])
        with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
            result = runner.invoke(app, ["creatives", "list"])
        # Typer auto-generates a usage error (exit code 2) for the missing
        # required option — no broken API call is issued.
        assert result.exit_code == 2
        client.get.assert_not_called()

    def test_creatives_upload_missing_file_argument(self, authenticated_config):
        """Story 61.3 — the previous "not supported" stub became a working
        multipart upload. Without the required <file> argument, Typer raises a
        usage error (exit 2); no HTTP call. See TestCreativesUpload_61_3 for
        the success path."""
        client = _mock_client(get_return=None)
        with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
            result = runner.invoke(app, ["creatives", "upload"])
        assert result.exit_code == 2
        client.post_multipart.assert_not_called()


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


# ===========================================================================
# Story 61.2 — inventory keys path fix + graceful --values handling
# ===========================================================================


class TestInventoryKeys_61_2:
    """Regression tests for Story 61.2 (defect #1)."""

    def test_keys_uses_correct_custom_targeting_keys_path(self, authenticated_config):
        """Was calling /api/gam/targeting-keys (404). Must hit
        /api/gam/custom-targeting-keys (network.py:268)."""
        client = _mock_client(get_return={"keys": [
            {"id": "k1", "name": "geo", "keyType": "PREDEFINED", "values": []}
        ]})
        with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
            result = runner.invoke(app, ["inventory", "keys"])
        assert result.exit_code == 0, result.output
        client.get.assert_called_once_with(
            "/api/gam/custom-targeting-keys", params={"limit": 50}
        )
        assert "geo" in result.output

    def test_keys_values_branch_fails_gracefully_until_epic_62(self, authenticated_config):
        """--values has no REST route (get_custom_targeting_values is MCP-ONLY,
        pending Epic 62). Must exit 1 with a clear message, NOT crash or 404."""
        client = _mock_client()
        with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
            result = runner.invoke(app, ["inventory", "keys", "--key-id", "42", "--values"])
        assert result.exit_code == 1
        client.get.assert_not_called()  # never reach the dead path
        assert "not yet supported" in result.output
        assert "Epic 62" in result.output


# ===========================================================================
# Story 61.3 — creatives upload real multipart (was a stub)
# ===========================================================================


class TestCreativesUpload_61_3:
    """Regression tests for Story 61.3 (defect #2 — `creatives upload`)."""

    def test_upload_posts_multipart_to_upload_single(self, authenticated_config, tmp_path):
        """`orbiads creatives upload <file>` must POST multipart to
        /api/creatives/upload-single, not error out pointing at MCP."""
        f = tmp_path / "banner.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\nfake-image-bytes")
        client = MagicMock()
        client.post_multipart.return_value = {
            "creativeId": "cr-123", "status": "uploaded", "name": "banner.png"
        }
        with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
            result = runner.invoke(app, ["creatives", "upload", str(f)])
        assert result.exit_code == 0, result.output
        client.post_multipart.assert_called_once_with(
            "/api/creatives/upload-single", str(f)
        )
        assert "cr-123" in result.output

    def test_upload_missing_file_exits_2(self, authenticated_config, tmp_path):
        """Missing file → exit 2 (bad args), no HTTP call."""
        client = MagicMock()
        with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
            result = runner.invoke(app, ["creatives", "upload", str(tmp_path / "nope.png")])
        assert result.exit_code == 2
        client.post_multipart.assert_not_called()
        assert "not found" in result.output

    def test_client_post_multipart_helper_builds_files_kwarg(self, tmp_path):
        """Unit test for the new client.post_multipart helper.

        Verifies it calls _request("POST", path, files={"file": (name, fh, ctype)})
        with the correct mimetype inferred from extension.
        """
        from orbiads_cli.client import OrbiAdsClient

        f = tmp_path / "logo.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\nbytes")

        # Build a real client but stub _request to capture the call.
        # OrbiAdsClient.__init__ takes a plain dict (see client.py:97).
        c = OrbiAdsClient({"token": "t", "refreshToken": "r", "apiUrl": "http://x"})

        # Capture the multipart payload INSIDE the call (the file handle is
        # closed by post_multipart's `with open(...)` once _request returns —
        # which is correct production behavior: httpx streams it then we close).
        captured = {}

        def fake_request(method, path, **kw):
            files = kw["files"]
            name, fh, ctype = files["file"]
            captured.update(method=method, path=path, name=name, ctype=ctype,
                            head=fh.read(4))
            return {"ok": True}

        c._request = fake_request
        c.post_multipart("/api/creatives/upload-single", str(f))

        assert captured["method"] == "POST"
        assert captured["path"] == "/api/creatives/upload-single"
        assert captured["name"] == "logo.png"
        assert captured["ctype"] == "image/png"
        assert captured["head"] == b"\x89PNG"
