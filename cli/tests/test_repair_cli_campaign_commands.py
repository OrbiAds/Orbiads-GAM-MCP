"""Repair story - CLI campaign write commands vs the read-only campaigns REST router.

Routes asserted here exist in the backend (checked against backend/main.py mounts and
backend/src/api/routes/**): GET /api/campaigns/live-recap, POST /api/campaigns/{id}/dry-run,
POST /api/jobs/{id}/deployment-plan,
POST /api/jobs/{id}/deploy (via `campaigns deploy --job-id`), GET /api/gam/ad-units, GET /api/gam/orders.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.client import CliApiError
from orbiads_cli.main import app

runner = CliRunner()


def _patch_campaigns(client):
    return patch("orbiads_cli.commands.campaigns.get_client", return_value=client)


# --- dead write commands: honest failure, no network ------------------------------------

@pytest.mark.parametrize(
    "argv,needle",
    [
        (["campaigns", "deploy", "c1", "--yes"], 'campaign(action="deploy"'),
        (["campaigns", "deploy", "c1", "--yes", "--confirmation-token", "t"], "--job-id"),
        (["campaigns", "update", "c1", "--file", "x.json"], 'action="update"'),
        (["campaigns", "add-line-items", "c1", "--file", "x.json"], "create_line_items_batch"),
        (["campaigns", "attach-creatives", "c1", "li1", "--file", "x.json"], "create_licas"),
        (["campaigns", "recover", "c1", "--yes"], 'action="rollback"'),
    ],
)
def test_dead_writes_exit_nonzero_without_success_or_http(argv, needle):
    client = MagicMock()
    with _patch_campaigns(client):
        result = runner.invoke(app, argv)
    assert result.exit_code == 1
    assert needle in result.output
    assert "successfully" not in result.output
    assert client.method_calls == []


def test_deploy_dry_run_still_uses_dry_run_read_route():
    client = MagicMock()
    client.post.return_value = {"plan": "p"}
    with _patch_campaigns(client):
        result = runner.invoke(app, ["--json", "campaigns", "deploy", "c1", "--dry-run"])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/campaigns/c1/dry-run")


# --- pause / archive: honest failure (no REST read exposes the campaign's own line items) ---

@pytest.mark.parametrize("cmd", ["pause", "archive"])
def test_pause_archive_fail_honestly_and_never_touch_foreign_line_items(cmd):
    client = MagicMock()
    with _patch_campaigns(client):
        result = runner.invoke(app, ["campaigns", cmd, "c1", "--yes"])
    assert result.exit_code == 1
    assert f'campaign(action="{cmd}"' in result.output
    assert "line-items lifecycle" in result.output
    assert "successfully" not in result.output
    # no recap read, no lifecycle write: nothing can hit the order's foreign line items
    assert client.method_calls == []


# --- campaigns deploy --job-id: jobs web deploy (two-step) ---------------------------------

def test_deploy_job_plan_step_posts_plan_route_and_deploys_nothing():
    client = MagicMock()
    client.post.return_value = {"confirmationToken": "tok"}
    with _patch_campaigns(client):
        result = runner.invoke(app, ["--json", "campaigns", "deploy", "c1", "--job-id", "j1"])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/jobs/j1/deployment-plan")
    assert "queued" not in result.output


def test_deploy_job_with_token_posts_deploy_and_reports_queued():
    client = MagicMock()
    client.post.return_value = {"jobId": "j1", "status": "queued"}
    with _patch_campaigns(client):
        result = runner.invoke(
            app,
            ["campaigns", "deploy", "c1", "--job-id", "j1", "--confirmation-token", "tok", "--yes"],
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/jobs/j1/deploy", json={"confirmationToken": "tok"})
    assert "queued for deployment" in result.output


def test_deploy_job_unconfirmed_response_is_not_success():
    client = MagicMock()
    client.post.return_value = None
    with _patch_campaigns(client):
        result = runner.invoke(
            app,
            ["campaigns", "deploy", "c1", "--job-id", "j1", "--confirmation-token", "tok", "--yes"],
        )
    assert result.exit_code == 1
    assert "queued for deployment" not in result.output


def test_deploy_job_http_error_exits_nonzero():
    client = MagicMock()
    client.post.side_effect = CliApiError(
        1, "Confirmation token not found or already consumed", "INVALID_TOKEN"
    )
    with _patch_campaigns(client):
        result = runner.invoke(
            app,
            ["campaigns", "deploy", "c1", "--job-id", "j1", "--confirmation-token", "bad", "--yes"],
        )
    assert result.exit_code == 1
    assert "queued for deployment" not in result.output


# --- B5: list response shapes ----------------------------------------------------------------

def test_inventory_ad_units_reads_items_key_and_sends_q():
    client = MagicMock()
    client.get.return_value = {
        "items": [{"id": "1", "name": "Home", "adUnitCode": "home", "sizes": [{"width": 300, "height": 250}]}],
        "total": 1,
    }
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["--json", "inventory", "ad-units", "--search", "ho", "--limit", "5"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/ad-units", params={"limit": 5, "q": "ho"})
    assert '"Home"' in result.output
    assert result.output.strip() != "[]"


def test_orders_list_reads_items_key():
    client = MagicMock()
    client.get.return_value = {"items": [{"id": "5", "name": "Order A", "status": "APPROVED"}], "total": 1}
    with patch("orbiads_cli.commands.orders.get_client", return_value=client):
        result = runner.invoke(app, ["--json", "orders", "list"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/orders", params={"limit": 50, "offset": 0})
    assert "Order A" in result.output
