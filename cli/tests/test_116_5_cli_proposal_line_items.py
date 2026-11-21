"""Story 116-5 — `orbiads programmatic proposal-line-items <verb>` (PLI lifecycle).

Each write verb posts the batch body ``{"pliIds": [...]}`` to its
``/api/gam/proposal-line-items/<verb>`` route; ``get`` reads ``/{id}`` (the CLI calls
OrbiAds' REST API, not GAM).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(ret=None):
    client = MagicMock()
    client.post.return_value = ret or {"numChanges": 2, "targetCount": 2}
    client.get.return_value = ret or {"id": "10", "reservationStatus": "RESERVED"}
    return client


def _run(client, *args):
    with patch("orbiads_cli.commands.programmatic.get_client", return_value=client):
        return runner.invoke(app, ["programmatic", "proposal-line-items", *args])


@pytest.mark.parametrize("verb", ["resume", "release", "unarchive"])
def test_verb_posts_the_pli_ids_to_its_route(verb):
    client = _mock_client()

    result = _run(client, verb, "10", "11", "--yes")

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        f"/api/gam/proposal-line-items/{verb}", json={"pliIds": ["10", "11"]}
    )


def test_pause_sends_the_reason():
    client = _mock_client()

    result = _run(client, "pause", "10", "--reason", "creative review", "--yes")

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/proposal-line-items/pause",
        json={"pliIds": ["10"], "reason": "creative review"},
    )


def test_pause_without_reason_is_a_usage_error_and_calls_nothing():
    client = _mock_client()

    result = _run(client, "pause", "10", "--yes")

    assert result.exit_code != 0
    client.post.assert_not_called()


def test_reserve_defaults_to_no_overbook_flag():
    client = _mock_client()

    result = _run(client, "reserve", "10", "--yes")

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/proposal-line-items/reserve", json={"pliIds": ["10"]}
    )


def test_reserve_allow_overbook_is_sent_explicitly():
    client = _mock_client()

    result = _run(client, "reserve", "10", "--allow-overbook", "--yes")

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/proposal-line-items/reserve",
        json={"pliIds": ["10"], "allowOverbook": True},
    )


def test_get_reads_the_line_item():
    client = _mock_client()

    result = _run(client, "get", "10")

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/proposal-line-items/10")
    assert "RESERVED" in result.output
