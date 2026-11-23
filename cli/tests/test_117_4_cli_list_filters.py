"""Story 117-4 - `orbiads inventory ad-units|placements` filters, `orbiads advertisers companies`.

The CLI calls OrbiAds' REST API with typed query parameters; it never builds PQL. Validation of
fields/values is server side (INVALID_PARAMETERS).
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.client import CliApiError
from orbiads_cli.main import app

runner = CliRunner()


def _client(data):
    client = MagicMock()
    client.get.return_value = data
    return client


def _run(module, client, *args, json_output=True):
    flags = ["--json"] if json_output else ["--output", "csv"]
    with patch(f"orbiads_cli.commands.{module}.get_client", return_value=client):
        return runner.invoke(app, [*flags, *args])


AD_UNIT_PAGE = {
    "items": [
        {
            "id": "11",
            "name": "LT-117-4-home",
            "adUnitCode": "home",
            "parentId": "1",
            "status": "ARCHIVED",
            "adUnitSizes": [{"width": 300, "height": 250}, {"width": 728, "height": 90}],
        }
    ],
    "count": 1,
    "rawCount": 1,
    "hasMore": True,
    "nextPageToken": "tok",
    "offset": 0,
    "limit": 50,
    "clientSideFilters": ["size"],
}
PLACEMENT_PAGE = {
    "items": [{"id": "5", "name": "LT-117-4-p", "status": "ACTIVE", "adUnitIds": ["11"]}],
    "count": 1,
    "rawCount": 1,
    "hasMore": False,
    "nextPageToken": None,
    "offset": 0,
    "limit": 50,
    "clientSideFilters": [],
}
COMPANY_PAGE = {
    "items": [{"id": "9", "name": "Net", "type": "AD_NETWORK", "creditStatus": "ACTIVE"}],
    "count": 1,
    "rawCount": 1,
    "hasMore": True,
    "nextPageToken": "ctok",
    "offset": 0,
    "limit": 50,
    "clientSideFilters": ["creditStatus"],
}


def test_ad_units_without_filter_options_keeps_the_legacy_call():
    client = _client({"adUnits": []})

    result = _run("inventory", client, "inventory", "ad-units", "--search", "x", "--limit", "7")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/ad-units", params={"limit": 7, "q": "x"})


def test_ad_units_maps_every_option_to_its_query_param():
    client = _client(AD_UNIT_PAGE)

    result = _run(
        "inventory",
        client,
        "inventory",
        "ad-units",
        "--parent-id",
        "1",
        "--status",
        "ARCHIVED",
        "--code",
        "home",
        "--name-contains",
        "LT-117-4",
        "--size",
        "300x250",
        "--since",
        "2026-11-01",
        "--order-by",
        "name desc",
        "--page-token",
        "abc",
        "--limit",
        "10",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/ad-units",
        params={
            "limit": 10,
            "parent_id": "1",
            "status": "ARCHIVED",
            "code": "home",
            "name_contains": "LT-117-4",
            "size": "300x250",
            "since": "2026-11-01",
            "order_by": "name desc",
            "page_token": "abc",
        },
    )
    assert json.loads(result.stdout)[0]["status"] == "ARCHIVED"


def test_ad_units_search_cannot_be_combined_with_filters():
    client = _client({})

    result = _run("inventory", client, "inventory", "ad-units", "--search", "x", "--status", "ACTIVE")

    assert result.exit_code == 2
    client.get.assert_not_called()


def test_ad_units_table_flattens_sizes_and_prints_footer_notes():
    client = _client(AD_UNIT_PAGE)

    result = _run(
        "inventory",
        client,
        "inventory",
        "ad-units",
        "--status",
        "ARCHIVED",
        "--size",
        "300x250",
        json_output=False,
    )

    assert result.exit_code == 0, result.output
    assert "300x250, 728x90" in result.output
    assert "--size is applied to each page" in result.output
    assert "--page-token tok" in result.output


def test_placements_without_filter_options_keeps_the_legacy_call():
    client = _client({"placements": []})

    result = _run("inventory", client, "inventory", "placements", "--limit", "9")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/placements", params={"limit": 9})


def test_placements_maps_every_option_to_its_query_param():
    client = _client(PLACEMENT_PAGE)

    result = _run(
        "inventory",
        client,
        "inventory",
        "placements",
        "--status",
        "ACTIVE",
        "--name-contains",
        "LT-117-4",
        "--code",
        "pc1",
        "--ad-unit-id",
        "11",
        "--since",
        "2026-11-01",
        "--order-by",
        "id desc",
        "--page-token",
        "abc",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/placements",
        params={
            "limit": 50,
            "status": "ACTIVE",
            "name_contains": "LT-117-4",
            "code": "pc1",
            "ad_unit_id": "11",
            "since": "2026-11-01",
            "order_by": "id desc",
            "page_token": "abc",
        },
    )


def test_companies_list_maps_every_option_and_prints_footer_notes():
    client = _client(COMPANY_PAGE)

    result = _run(
        "advertisers",
        client,
        "advertisers",
        "companies",
        "list",
        "--type",
        "AD_NETWORK",
        "--name-contains",
        "net",
        "--credit-status",
        "ACTIVE",
        "--since",
        "2026-11-01",
        "--order-by",
        "name desc",
        "--page-token",
        "abc",
        "--limit",
        "20",
        json_output=False,
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/companies",
        params={
            "limit": 20,
            "type": "AD_NETWORK",
            "name_contains": "net",
            "credit_status": "ACTIVE",
            "since": "2026-11-01",
            "order_by": "name desc",
            "page_token": "abc",
        },
    )
    assert "AD_NETWORK" in result.output
    assert "--credit-status is applied to each page" in result.output
    assert "--page-token ctok" in result.output


def test_companies_list_without_options_lists_the_first_page():
    client = _client(COMPANY_PAGE)

    result = _run("advertisers", client, "advertisers", "companies", "list")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/companies", params={"limit": 50})


def test_companies_get_calls_the_company_route():
    client = _client({"id": "5", "type": "PARTNER", "name": "P"})

    result = _run("advertisers", client, "advertisers", "companies", "get", "5")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/companies/5")
    assert json.loads(result.stdout)["type"] == "PARTNER"


def test_legacy_advertisers_list_is_untouched():
    client = _client({"advertisers": [{"id": "1", "name": "A", "type": "ADVERTISER"}]})

    result = _run("advertisers", client, "advertisers", "list")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/advertisers")


def test_api_error_is_reported_not_traced():
    client = MagicMock()
    client.get.side_effect = CliApiError(422, "INVALID_PARAMETERS", "status 'DELETED' is invalid")

    result = _run("inventory", client, "inventory", "ad-units", "--status", "DELETED")

    assert result.exit_code != 0
    assert "Traceback" not in result.output
