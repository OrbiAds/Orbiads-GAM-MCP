"""Story 117-6 - `orbiads reporting run --comparison / --comparison-from / --comparison-to`.

The CLI posts to OrbiAds' REST API (POST /api/gam/reports/custom); the comparison
period is validated server side (422 VALIDATION_ERROR) and forwarded to GAM as
``ReportDefinition.comparisonDateRange``. `--start/--end` are now sent as a FIXED
range (they were silently ignored - the backend defaulted to LAST_MONTH).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()

BASE = {
    "dimensions": ["DATE"],
    "metrics": ["AD_SERVER_IMPRESSIONS"],
    "dateRangeType": "FIXED",
    "startDate": "2026-11-01",
    "endDate": "2026-11-07",
}


def _run(*extra):
    client = MagicMock()
    client.post.return_value = {"rows": [], "comparisonDateRanges": []}
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "--json",
                "reporting",
                "run",
                "--dimensions",
                "DATE",
                "--metrics",
                "AD_SERVER_IMPRESSIONS",
                "--start",
                "2026-11-01",
                "--end",
                "2026-11-07",
                *extra,
            ],
        )
    return result, client


def test_without_comparison_payload_has_no_comparison_keys(authenticated_config):
    result, client = _run()
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/reports/custom", json=BASE)


def test_relative_comparison(authenticated_config):
    result, client = _run("--comparison", "previous_period")
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/reports/custom",
        json={**BASE, "comparisonDateRangeType": "PREVIOUS_PERIOD"},
    )


def test_fixed_comparison_implied_by_dates(authenticated_config):
    result, client = _run("--comparison-from", "2026-10-01", "--comparison-to", "2026-10-07")
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/reports/custom",
        json={
            **BASE,
            "comparisonDateRangeType": "FIXED",
            "comparisonStartDate": "2026-10-01",
            "comparisonEndDate": "2026-10-07",
        },
    )


def test_incomplete_fixed_comparison_is_forwarded_for_server_validation(authenticated_config):
    """Only one bound: the CLI does not guess - the server answers 422 explicitly."""
    result, client = _run("--comparison-from", "2026-10-01")
    assert result.exit_code == 0, result.output
    sent = client.post.call_args.kwargs["json"]
    assert sent["comparisonDateRangeType"] == "FIXED"
    assert sent["comparisonStartDate"] == "2026-10-01"
    assert sent["comparisonEndDate"] is None
