"""Story 117-3 - `orbiads creatives list` typed filters, `orbiads licas list` / `list-by-creative`.

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


def _run(module, client, *args):
    with patch(f"orbiads_cli.commands.{module}.get_client", return_value=client):
        return runner.invoke(app, ["--json", *args])


CREATIVES_PAGE = {
    "items": [
        {
            "id": "11",
            "name": "LT-117-3-a",
            "creativeType": "ImageCreative",
            "size": {"width": 300, "height": 250},
            "status": "ACTIVE",
        }
    ],
    "count": 1,
    "rawCount": 1,
    "hasMore": True,
    "nextPageToken": "tok",
    "offset": 0,
    "limit": 50,
    "clientSideFilters": ["creativeType"],
}
LICA_PAGE = {
    "licas": [{"lineItemId": "7", "creativeId": "5", "status": "ACTIVE", "sizes": []}],
    "count": 1,
    "hasMore": False,
    "nextPageToken": None,
    "offset": 0,
    "limit": 50,
}


def test_creatives_list_advertiser_only_keeps_the_legacy_call():
    client = _client({"creatives": []})

    result = _run("creatives", client, "creatives", "list", "--advertiser-id", "555")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/advertisers/555/creatives", params={"limit": 50})


def test_creatives_list_without_any_option_is_still_a_usage_error():
    client = _client({})

    result = _run("creatives", client, "creatives", "list")

    assert result.exit_code == 2
    client.get.assert_not_called()


def test_creatives_list_maps_every_option_to_its_query_param():
    client = _client(CREATIVES_PAGE)

    result = _run(
        "creatives",
        client,
        "creatives",
        "list",
        "--advertiser-id",
        "9",
        "--type",
        "ImageCreative",
        "--name-contains",
        "LT-117-3",
        "--since",
        "2026-11-01",
        "--order-by",
        "lastModifiedDateTime desc",
        "--page-token",
        "abc",
        "--limit",
        "5",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/creatives",
        params={
            "limit": 5,
            "advertiser_id": "9",
            "type": "ImageCreative",
            "name_contains": "LT-117-3",
            "since": "2026-11-01",
            "order_by": "lastModifiedDateTime desc",
            "page_token": "abc",
        },
    )
    assert json.loads(result.stdout)[0]["type"] == "ImageCreative"
    assert json.loads(result.stdout)[0]["size"] == "300x250"


def test_creatives_list_a_single_new_option_switches_to_the_typed_route():
    client = _client(CREATIVES_PAGE)

    result = _run("creatives", client, "creatives", "list", "--name-contains", "x")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/creatives", params={"limit": 50, "name_contains": "x"}
    )


def test_creatives_list_prints_the_next_page_token_and_the_client_side_note(monkeypatch):
    client = _client(CREATIVES_PAGE)
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["--output", "csv", "creatives", "list", "--type", "ImageCreative"])
    assert result.exit_code == 0, result.output
    assert "--page-token tok" in result.output
    assert "applied to each page" in result.output


def test_licas_list_by_creative_calls_the_creative_route():
    client = _client(LICA_PAGE)

    result = _run(
        "licas",
        client,
        "licas",
        "list-by-creative",
        "5",
        "--status",
        "ACTIVE",
        "--page-token",
        "t",
        "--limit",
        "20",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/creatives/5/licas", params={"limit": 20, "status": "ACTIVE", "page_token": "t"}
    )
    assert json.loads(result.stdout) == LICA_PAGE["licas"]


def test_licas_list_maps_every_option_to_its_query_param():
    client = _client(LICA_PAGE)

    result = _run(
        "licas",
        client,
        "licas",
        "list",
        "--line-item-id",
        "7",
        "--creative-id",
        "5",
        "--status",
        "INACTIVE",
        "--since",
        "2026-11-01",
        "--page-token",
        "t",
        "--limit",
        "10",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/licas",
        params={
            "limit": 10,
            "line_item_id": "7",
            "creative_id": "5",
            "status": "INACTIVE",
            "since": "2026-11-01",
            "page_token": "t",
        },
    )


def test_licas_list_surfaces_the_server_refusal_of_an_unbounded_scan():
    client = MagicMock()
    client.get.side_effect = CliApiError(
        2, "licas listing is refused without a bounding filter", error_code="INVALID_PARAMETERS"
    )

    result = _run("licas", client, "licas", "list")

    assert result.exit_code != 0
    assert "bounding filter" in result.output


def test_licas_list_by_line_item_is_unchanged():
    client = _client([{"id": "", "lineItemId": "7", "creativeId": "5", "status": "ACTIVE"}])

    result = _run("licas", client, "licas", "list-by-line-item", "7")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/line-items/7/licas")
