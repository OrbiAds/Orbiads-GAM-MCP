from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def test_mcm_earnings_gets_rest_endpoint(authenticated_config) -> None:
    client = MagicMock()
    client.get.return_value = {
        "month": 5,
        "year": 2026,
        "totalEarnings": {"currencyCode": "EUR", "microAmount": 0},
        "earningsByChildNetwork": [],
    }

    with patch("orbiads_cli.commands.mcm.get_client", return_value=client):
        result = runner.invoke(app, ["mcm", "earnings", "--month", "5", "--year", "2026"])

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/mcm/earnings",
        params={"month": 5, "year": 2026},
    )
