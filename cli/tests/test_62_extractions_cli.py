"""Tests for the 6 CLI commands unlocked by service extractions:
   - Story 62.2a — `reporting billing-report` (BillingReportService)
   - Story 62.3a — `line-items create-adexchange/open-bidding/preferred-deal`
   - Story 62.5a — `inventory list-inactive`, `inventory archive-inactive`
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    c = MagicMock()
    for k in ("get", "post", "put", "patch", "delete"):
        getattr(c, k).return_value = ret.get(k)
    return c


def _write_json(tmp_path, payload):
    f = tmp_path / "p.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


# ── 62.2a billing-report ───────────────────────────────────────────────────


def test_billing_report_json(authenticated_config, tmp_path):
    client = _mock_client(post={"period": {}, "rows": []})
    f = _write_json(tmp_path, {"startDate": "2026-04-01", "endDate": "2026-04-30"})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "billing-report", "--file", f])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/reports/billing",
        json={"startDate": "2026-04-01", "endDate": "2026-04-30"},
    )


def test_billing_report_csv(authenticated_config, tmp_path):
    client = _mock_client(post="orderId,revenue\nO1,42\n")  # CSV streamed body
    f = _write_json(tmp_path, {
        "startDate": "2026-04-01", "endDate": "2026-04-30", "exportFormat": "csv"
    })
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "billing-report", "--file", f])
    assert result.exit_code == 0, result.output
    assert "orderId,revenue" in result.output


# ── 62.3a advanced line-item creation ─────────────────────────────────────


def test_line_items_create_adexchange(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "li-adx-1", "type": "ADEXCHANGE"})
    f = _write_json(tmp_path, {"orderId": "1", "adUnitIds": ["2"], "name": "AdX"})
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(
            app, ["line-items", "create-adexchange", "--file", f]
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/line-items/adexchange",
        json={"orderId": "1", "adUnitIds": ["2"], "name": "AdX"},
    )


def test_line_items_create_open_bidding(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "li-ob-1", "type": "OPEN_BIDDING"})
    f = _write_json(tmp_path, {"orderId": "1", "adUnitIds": ["2"], "name": "OB"})
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(
            app, ["line-items", "create-open-bidding", "--file", f]
        )
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/line-items/open-bidding",
        json={"orderId": "1", "adUnitIds": ["2"], "name": "OB"},
    )


def test_line_items_create_preferred_deal(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "li-pd-1", "type": "PREFERRED_DEAL"})
    f = _write_json(tmp_path, {
        "orderId": "1", "adUnitIds": ["2"], "name": "PD", "dealId": "deal-99"
    })
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(
            app, ["line-items", "create-preferred-deal", "--file", f]
        )
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/line-items/preferred-deal",
        json={"orderId": "1", "adUnitIds": ["2"], "name": "PD", "dealId": "deal-99"},
    )


# ── 62.5a inactive ad-units ───────────────────────────────────────────────


def test_inventory_list_inactive(authenticated_config):
    client = _mock_client(get={"inactiveAdUnits": [], "total": 0, "days": 90})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "list-inactive"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/ad-units/inactive", params={"days": 90}
    )


def test_inventory_list_inactive_custom_days(authenticated_config):
    client = _mock_client(get={"inactiveAdUnits": [], "total": 0, "days": 30})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "list-inactive", "--days", "30"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/ad-units/inactive", params={"days": 30}
    )


def test_inventory_archive_inactive(authenticated_config, tmp_path):
    client = _mock_client(post={"archivedCount": 3, "failedCount": 0})
    f = _write_json(tmp_path, {"adUnitIds": ["a1", "a2", "a3"]})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "archive-inactive", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/ad-units/archive-inactive",
        json={"adUnitIds": ["a1", "a2", "a3"]},
    )
