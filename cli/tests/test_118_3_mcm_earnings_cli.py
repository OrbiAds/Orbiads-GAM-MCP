"""Story 118-3 - `orbiads mcm earnings` filters, sort and pagination."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _run(args, data):
    client = MagicMock()
    client.get.return_value = data
    with patch("orbiads_cli.commands.mcm.get_client", return_value=client):
        result = runner.invoke(app, args)
    return result, client


def test_default_call_is_unchanged(authenticated_config):
    result, client = _run(["mcm", "earnings", "--month", "10", "--year", "2026"], {})
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/mcm/earnings", params={"month": 10, "year": 2026}
    )


def test_options_are_sent_and_next_page_is_announced(authenticated_config):
    result, client = _run(
        [
            "mcm", "earnings", "--month", "10", "--year", "2026",
            "--child-network-code", "123", "--child-network-code", "456",
            "--delegation-type", "manage_account", "--order-by", "totalEarnings desc",
            "--limit", "100", "--page-token", "tok", "--skip", "5",
        ],
        {"mcmEarnings": [], "nextPageToken": "next"},
    )
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/mcm/earnings",
        params={
            "month": 10,
            "year": 2026,
            "child_network_code": ["123", "456"],
            "delegation_type": "MANAGE_ACCOUNT",
            "order_by": "totalEarnings desc",
            "page_size": 100,
            "page_token": "tok",
            "skip": 5,
        },
    )
    assert "--page-token next" in result.output
