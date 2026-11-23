"""Story 117-2 - `orbiads orders list` typed filters and `orbiads line-items list`.

The CLI calls OrbiAds' REST API (GET /api/gam/orders and /api/gam/line-items) with typed query
parameters; it never builds PQL. Validation of fields/values is server side (INVALID_PARAMETERS).
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _client(data):
    client = MagicMock()
    client.get.return_value = data
    return client


def _run(module, client, *args):
    with patch(f"orbiads_cli.commands.{module}.get_client", return_value=client):
        return runner.invoke(app, ["--json", *args])


ORDERS_PAGE = {
    "orders": [{"id": "1", "name": "LT-117-2-A", "advertiserId": "9", "status": "DRAFT"}],
    "count": 1,
    "hasMore": True,
    "nextPageToken": "tok",
    "offset": 0,
    "limit": 1,
}
LI_PAGE = {
    "lineItems": [{"id": "5", "name": "LT-117-2-LI", "status": "READY", "type": "STANDARD"}],
    "count": 1,
    "hasMore": False,
    "nextPageToken": None,
    "offset": 0,
    "limit": 50,
}


def test_orders_list_without_new_options_keeps_the_legacy_call():
    client = _client({"orders": []})

    result = _run("orders", client, "orders", "list", "-q", "acme", "--limit", "20")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/orders", params={"limit": 20, "offset": 0, "q": "acme"})


def test_orders_list_advertiser_only_keeps_the_legacy_call():
    client = _client({"orders": []})

    result = _run("orders", client, "orders", "list", "--advertiser-id", "42")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/orders", params={"advertiser_id": "42"})


def test_orders_list_maps_every_new_option_to_its_query_param():
    client = _client(ORDERS_PAGE)

    result = _run(
        "orders",
        client,
        "orders",
        "list",
        "--status",
        "DRAFT",
        "--advertiser-id",
        "9",
        "--start-after",
        "2026-11-01",
        "--end-before",
        "2026-12-01",
        "--order-by",
        "startDateTime desc",
        "--page-token",
        "abc",
        "--limit",
        "300",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/orders",
        params={
            "limit": 300,
            "offset": 0,
            "advertiser_id": "9",
            "status": "DRAFT",
            "start_after": "2026-11-01",
            "end_before": "2026-12-01",
            "order_by": "startDateTime desc",
            "page_token": "abc",
        },
    )
    assert json.loads(result.stdout)[0]["id"] == "1"


def test_orders_list_prints_the_next_page_hint_on_stderr_only_in_non_json_mode():
    client = _client(ORDERS_PAGE)
    with patch("orbiads_cli.commands.orders.get_client", return_value=client):
        table = runner.invoke(app, ["--output", "csv", "orders", "list", "--status", "DRAFT"])
    assert table.exit_code == 0, table.output
    assert "--page-token tok" in table.output
    json_run = _run("orders", client, "orders", "list", "--status", "DRAFT")
    assert "--page-token" not in json_run.stdout


def test_orders_list_rejects_a_limit_above_500():
    result = _run("orders", _client(ORDERS_PAGE), "orders", "list", "--status", "DRAFT", "--limit", "501")
    assert result.exit_code != 0


def test_line_items_list_without_option_sends_only_the_limit():
    client = _client(LI_PAGE)

    result = _run("line_items", client, "line-items", "list")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/line-items", params={"limit": 50})
    assert json.loads(result.stdout)[0]["id"] == "5"


def test_line_items_list_shows_line_item_type_in_the_type_column():
    """Audit 117-2 avert. 5: the API returns ``lineItemType``; the ``type`` column was empty."""
    page = {**LI_PAGE, "lineItems": [{"id": "5", "name": "x", "status": "READY",
                                       "lineItemType": "SPONSORSHIP"}]}
    client = _client(page)

    result = _run("line_items", client, "line-items", "list")

    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)[0]["type"] == "SPONSORSHIP"


def test_line_items_list_maps_every_option_to_its_query_param():
    client = _client(LI_PAGE)

    result = _run(
        "line_items",
        client,
        "line-items",
        "list",
        "--order-id",
        "77",
        "--status",
        "READY",
        "--type",
        "STANDARD",
        "--start-after",
        "2026-11-01",
        "--end-before",
        "2026-12-01",
        "--order-by",
        "name",
        "--page-token",
        "abc",
        "--limit",
        "500",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/line-items",
        params={
            "limit": 500,
            "order_id": "77",
            "status": "READY",
            "type": "STANDARD",
            "start_after": "2026-11-01",
            "end_before": "2026-12-01",
            "order_by": "name",
            "page_token": "abc",
        },
    )


def test_line_items_list_shows_the_next_page_hint():
    client = _client({**LI_PAGE, "hasMore": True, "nextPageToken": "next-tok"})
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(app, ["--output", "csv", "line-items", "list", "--limit", "1"])
    assert result.exit_code == 0, result.output
    assert "--page-token next-tok" in result.output


def test_line_items_list_server_validation_error_is_reported():
    from orbiads_cli.client import CliApiError

    client = MagicMock()
    client.get.side_effect = CliApiError(2, "field 'foo' is not filterable", "INVALID_PARAMETERS")
    result = _run("line_items", client, "line-items", "list", "--status", "NOPE")
    assert result.exit_code != 0
