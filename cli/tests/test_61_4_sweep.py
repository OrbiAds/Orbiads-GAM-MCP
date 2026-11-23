"""Story 61.4 — REST-ONLY sweep tests: campaigns / line-items / jobs.

One test per new CLI command: assert correct HTTP method + path + (where
applicable) JSON body forwarded from the --file payload. All HTTP traffic is
mocked through ``get_client`` patches per the established CLI test pattern.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(get_return=None, post_return=None, patch_return=None):
    client = MagicMock()
    client.get.return_value = get_return
    client.post.return_value = post_return
    client.patch.return_value = patch_return
    return client


def _write_json(tmp_path, payload):
    f = tmp_path / "payload.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


# ─── campaigns extensions (4 verbs) ────────────────────────────────────────


class TestCampaignsExtensions_61_4:


    def test_read_by_campaign_id_calls_live_recap(self, authenticated_config):
        client = _mock_client(get_return={"orderId": 456, "source": "gam_live"})
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, ["--json", "campaigns", "read", "--campaign-id", "c1"])
        assert result.exit_code == 0, result.output
        client.get.assert_called_once_with(
            "/api/campaigns/live-recap",
            params={"campaignId": "c1"},
        )

    def test_read_by_order_id_calls_live_recap(self, authenticated_config):
        client = _mock_client(get_return={"orderId": 456, "source": "gam_live"})
        with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
            result = runner.invoke(app, ["--json", "campaigns", "read", "--order-id", "456"])
        assert result.exit_code == 0, result.output
        client.get.assert_called_once_with(
            "/api/campaigns/live-recap",
            params={"orderId": 456},
        )

    def test_read_requires_campaign_or_order_id(self, authenticated_config):
        result = runner.invoke(app, ["campaigns", "read"])
        assert result.exit_code == 2
        assert "provide --campaign-id or --order-id" in result.output







# ─── line-items (7 verbs) ──────────────────────────────────────────────────


class TestLineItems_61_4:

    def test_activate(self, authenticated_config):
        client = _mock_client(post_return={"activated": 5})
        with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
            result = runner.invoke(app, ["line-items", "activate", "j1", "--yes"])
        assert result.exit_code == 0
        client.post.assert_called_once_with("/api/gam/jobs/j1/line-items/activate")

    def test_pause(self, authenticated_config):
        client = _mock_client(post_return={"paused": 5})
        with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
            result = runner.invoke(app, ["line-items", "pause", "j1", "--yes"])
        assert result.exit_code == 0
        client.post.assert_called_once_with("/api/gam/jobs/j1/line-items/pause")

    def test_archive(self, authenticated_config):
        client = _mock_client(post_return={"archived": 5})
        with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
            result = runner.invoke(app, ["line-items", "archive", "j1", "--yes"])
        assert result.exit_code == 0
        client.post.assert_called_once_with("/api/gam/jobs/j1/line-items/archive")

    def test_update(self, authenticated_config, tmp_path):
        client = _mock_client(post_return={"id": "li1", "updated": True})
        f = _write_json(tmp_path, {"goal": {"impressions": 100000}})
        with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
            result = runner.invoke(
                app, ["line-items", "update", "j1", "li1", "--file", f]
            )
        assert result.exit_code == 0
        client.post.assert_called_once_with(
            "/api/gam/jobs/j1/line-items/li1/update",
            json={"goal": {"impressions": 100000}},
        )

    def test_duplicate(self, authenticated_config):
        client = _mock_client(post_return={"id": "li2"})
        with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
            result = runner.invoke(app, ["line-items", "duplicate", "li1"])
        assert result.exit_code == 0
        client.post.assert_called_once_with("/api/gam/line-items/li1/duplicate")

    def test_verify_is_get(self, authenticated_config):
        client = _mock_client(get_return={"status": "ok"})
        with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
            result = runner.invoke(app, ["line-items", "verify", "j1"])
        assert result.exit_code == 0
        client.get.assert_called_once_with("/api/gam/jobs/j1/verify")

    def test_update_targeting_patches(self, authenticated_config, tmp_path):
        client = _mock_client(patch_return={"updated": True})
        f = _write_json(tmp_path, {"geo": ["FR"]})
        with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
            result = runner.invoke(
                app, ["line-items", "update-targeting", "c1", "li1", "--file", f]
            )
        assert result.exit_code == 0
        client.patch.assert_called_once_with(
            "/api/campaigns/c1/line-items/li1/targeting", json={"geo": ["FR"]}
        )


# ─── jobs (3 verbs) ────────────────────────────────────────────────────────


class TestJobs_61_4:

    def test_list(self, authenticated_config):
        client = _mock_client(get_return={"jobs": [{"id": "j1", "status": "deployed"}]})
        with patch("orbiads_cli.commands.jobs.get_client", return_value=client):
            result = runner.invoke(app, ["jobs", "list"])
        assert result.exit_code == 0
        client.get.assert_called_once_with("/api/jobs/", params={"limit": 50})
        assert "j1" in result.output

    def test_list_with_status_filter(self, authenticated_config):
        client = _mock_client(get_return={"jobs": []})
        with patch("orbiads_cli.commands.jobs.get_client", return_value=client):
            result = runner.invoke(app, ["jobs", "list", "--status", "running"])
        assert result.exit_code == 0
        client.get.assert_called_once_with(
            "/api/jobs/", params={"limit": 50, "status": "running"}
        )

    def test_get(self, authenticated_config):
        client = _mock_client(get_return={"id": "j1", "status": "draft"})
        with patch("orbiads_cli.commands.jobs.get_client", return_value=client):
            result = runner.invoke(app, ["jobs", "get", "j1"])
        assert result.exit_code == 0
        client.get.assert_called_once_with("/api/jobs/j1")

    def test_duplicate(self, authenticated_config):
        client = _mock_client(post_return={"id": "j2"})
        with patch("orbiads_cli.commands.jobs.get_client", return_value=client):
            result = runner.invoke(app, ["jobs", "duplicate", "j1"])
        assert result.exit_code == 0
        client.post.assert_called_once_with("/api/jobs/j1/duplicate")
