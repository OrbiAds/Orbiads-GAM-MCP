"""Story 117-7 - `orbiads reporting forecast-availability <line_item_id>`.

Calls OrbiAds' REST API GET /api/gam/reports/forecast/availability/{line_item_id}
(SOAP ForecastService.getAvailabilityForecastById server side). Options are sent
only when enabled, mirroring AvailabilityForecastOptions (both minOccurs=0).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _run(*args):
    client = MagicMock()
    client.get.return_value = {"availableUnits": 40000, "matchedUnits": 100000}
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["--json", "reporting", "forecast-availability", *args])
    return result, client


def test_default_sends_no_options(authenticated_config):
    result, client = _run("555")
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/reports/forecast/availability/555", params=None
    )
    assert "40000" in result.output


def test_flags_map_to_query_params(authenticated_config):
    result, client = _run("555", "--include-contending", "--include-breakdown")
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/reports/forecast/availability/555",
        params={
            "includeContendingLineItems": "true",
            "includeTargetingCriteriaBreakdown": "true",
        },
    )


def test_line_item_id_is_url_encoded(authenticated_config):
    """A malformed id never alters the path; the server answers 422."""
    result, client = _run("12/../34")
    assert result.exit_code == 0, result.output
    assert client.get.call_args.args[0] == "/api/gam/reports/forecast/availability/12%2F..%2F34"
