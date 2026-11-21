"""Story 116-6 - `orbiads programmatic proposals list` / `proposal-line-items list`.

The CLI calls OrbiAds' REST API (GET /api/gam/proposals and /api/gam/proposal-line-items) with
typed query parameters; it never builds PQL.
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


def _run(client, *args):
    with patch("orbiads_cli.commands.programmatic.get_client", return_value=client):
        return runner.invoke(app, ["--json", "programmatic", *args])


PAGE = {
    "proposals": [{"id": "1", "name": "P1", "status": "DRAFT", "isProgrammatic": False}],
    "hasMore": False,
    "offset": 0,
    "limit": 200,
    "clientSideFilters": [],
}


def test_proposals_list_without_filter_sends_only_the_paging_params():
    client = _client(PAGE)

    result = _run(client, "proposals", "list")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/proposals", params={"limit": 200, "offset": 0})
    assert json.loads(result.stdout)[0]["id"] == "1"


def test_proposals_list_maps_every_flag_to_its_camel_case_query_param():
    client = _client(PAGE)

    result = _run(
        client,
        "proposals",
        "list",
        "--status",
        "DRAFT",
        "--negotiation-status",
        "FINALIZED",
        "--buyer",
        "42",
        "--non-programmatic",
        "--not-archived",
        "--since",
        "2026-11-01T00:00:00Z",
        "--limit",
        "25",
        "--offset",
        "50",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/proposals",
        params={
            "limit": 25,
            "offset": 50,
            "status": "DRAFT",
            "negotiationStatus": "FINALIZED",
            "buyerId": "42",
            "isProgrammatic": "false",
            "isArchived": "false",
            "lastModifiedAfter": "2026-11-01T00:00:00Z",
        },
    )


def test_proposals_list_programmatic_flag_sends_true():
    client = _client(PAGE)

    _run(client, "proposals", "list", "--programmatic")

    assert client.get.call_args.kwargs["params"]["isProgrammatic"] == "true"


def test_proposals_list_hints_the_next_offset_when_more_results_exist():
    client = _client({**PAGE, "hasMore": True, "offset": 200, "limit": 200})

    result = _run(client, "proposals", "list")

    assert "--offset 400" in result.output


def test_proposals_list_reports_page_level_filters():
    client = _client({**PAGE, "clientSideFilters": ["buyerId"]})

    result = _run(client, "proposals", "list", "--buyer", "42")

    assert "buyerId filtered on the returned page only" in result.output


def test_proposals_list_rejects_a_limit_above_500_without_calling_the_api():
    client = _client(PAGE)

    result = _run(client, "proposals", "list", "--limit", "501")

    assert result.exit_code != 0
    client.get.assert_not_called()


def test_pli_list_is_network_wide_by_default():
    client = _client({"lineItems": [{"id": "10"}], "hasMore": False})

    result = _run(client, "proposal-line-items", "list")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/proposal-line-items", params={"limit": 200, "offset": 0}
    )
    assert json.loads(result.stdout) == [{"id": "10"}]


def test_pli_list_maps_the_filters():
    client = _client({"lineItems": [], "hasMore": False})

    result = _run(
        client,
        "proposal-line-items",
        "list",
        "--proposal-id",
        "500",
        "--status",
        "RESERVED",
        "--programmatic",
        "--include-archived",
        "--since",
        "2026-11-01T00:00:00Z",
        "--limit",
        "10",
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/proposal-line-items",
        params={
            "limit": 10,
            "offset": 0,
            "includeArchived": "true",
            "proposalId": "500",
            "reservationStatus": "RESERVED",
            "isProgrammatic": "true",
            "lastModifiedAfter": "2026-11-01T00:00:00Z",
        },
    )
