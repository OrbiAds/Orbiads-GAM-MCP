"""Story 117-5 - `orbiads audit changes list|get` (GAM change history).

The CLI calls OrbiAds' REST API (GET /api/gam/change-events[/{id}]) with typed query parameters;
it never talks to GAM and never builds a REST ``filter`` itself (validation is server side,
INVALID_PARAMETERS). The legacy `orbiads audit log` call is unchanged.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()

PAGE = {
    "source": "gam",
    "events": [
        {
            "id": "1001",
            "name": "networks/123/changeEvents/1001",
            "changeTime": "2026-11-20T10:00:00Z",
            "user": {"id": "77", "name": "networks/123/users/77"},
            "entityType": "LINE_ITEM",
            "entityId": "555",
            "operation": "UPDATE",
            "source": "gam",
        }
    ],
    "count": 1,
    "nextPageToken": "NEXT",
    "hasMore": True,
}


def _client(data):
    client = MagicMock()
    client.get.return_value = data
    return client


def _run(client, *args):
    with patch("orbiads_cli.commands.audit_log.get_client", return_value=client):
        return runner.invoke(app, ["--json", *args])


def test_changes_list_maps_every_option_to_its_query_param():
    client = _client(PAGE)

    result = _run(
        client,
        "audit",
        "changes",
        "list",
        "--entity-type",
        "LINE_ITEM",
        "--entity-id",
        "555",
        "--user",
        "77",
        "--since",
        "2026-11-01",
        "--until",
        "2026-11-30",
        "--operation",
        "UPDATE",
        "--page-token",
        "TOK",
        "--limit",
        "10",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/change-events",
        params={
            "limit": 10,
            "entity_type": "LINE_ITEM",
            "entity_id": "555",
            "user": "77",
            "since": "2026-11-01",
            "until": "2026-11-30",
            "operation": "UPDATE",
            "page_token": "TOK",
        },
    )
    rows = json.loads(result.stdout)
    assert (
        rows[0]["id"] == "1001"
        and rows[0]["userId"] == "77"
        and rows[0]["source"] == "gam"
    )


def test_changes_list_without_options_sends_only_the_default_limit():
    client = _client({"events": []})

    result = _run(client, "audit", "changes", "list")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/change-events", params={"limit": 50})


def test_changes_list_limit_is_bounded_to_100():
    client = _client(PAGE)
    assert _run(client, "audit", "changes", "list", "--limit", "101").exit_code != 0
    assert _run(client, "audit", "changes", "list", "--limit", "0").exit_code != 0
    client.get.assert_not_called()


def test_changes_list_prints_the_next_page_token_hint_in_non_json_mode():
    client = _client(PAGE)
    with patch("orbiads_cli.commands.audit_log.get_client", return_value=client):
        result = runner.invoke(app, ["--output", "csv", "audit", "changes", "list"])
    assert result.exit_code == 0, result.output
    assert "--page-token NEXT" in result.output


def test_changes_get_calls_the_item_route_and_url_encodes_the_id():
    client = _client(PAGE["events"][0])

    result = _run(client, "audit", "changes", "get", "1001")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/change-events/1001")
    assert json.loads(result.stdout)["entityId"] == "555"

    client2 = _client(PAGE["events"][0])
    _run(client2, "audit", "changes", "get", "../orders/1")
    client2.get.assert_called_once_with("/api/gam/change-events/..%2Forders%2F1")


def test_changes_list_surfaces_a_server_validation_error():
    from orbiads_cli.client import CliApiError

    client = MagicMock()
    client.get.side_effect = CliApiError(
        1, "entity_type FOO is invalid", "INVALID_PARAMETERS"
    )

    result = _run(client, "audit", "changes", "list", "--entity-type", "FOO")

    assert result.exit_code != 0
    assert "INVALID_PARAMETERS" in result.output or "FOO" in result.output


def test_legacy_audit_log_command_is_unchanged():
    client = _client(
        {"entries": [{"timestamp": "t", "actor": "a", "action": "x", "target": "y"}]}
    )

    result = _run(client, "audit", "log", "--limit", "5")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/settings/audit/", params={"limit": 5})


# Story 117-17 - optional lower bound of the fallback lookup window of `get`.


def test_changes_get_since_is_forwarded_as_a_query_param():
    client = _client(PAGE["events"][0])

    result = _run(client, "audit", "changes", "get", "1001", "--since", "2026-01-01")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/change-events/1001", params={"since": "2026-01-01"}
    )


def test_changes_list_uses_the_server_cursor_and_does_not_invent_a_window():
    client = _client(PAGE)

    result = _run(client, "audit", "changes", "list", "--page-token", "CURSOR")

    assert result.exit_code == 0, result.output
    # the window (default: last 30 days) is completed server side, never by the CLI
    client.get.assert_called_once_with(
        "/api/gam/change-events", params={"limit": 50, "page_token": "CURSOR"}
    )
