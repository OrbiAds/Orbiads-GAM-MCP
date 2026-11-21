"""Story 116-4 — `orbiads programmatic proposals <verb>` (proposal lifecycle).

Each verb posts the batch body ``{"proposalIds": [...]}`` to its
``/api/gam/proposals/<verb>`` route (the CLI calls OrbiAds' REST API, not GAM).
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
    return client


@pytest.mark.parametrize(
    ("verb", "path"),
    [
        ("resume", "/api/gam/proposals/resume"),
        ("unarchive", "/api/gam/proposals/unarchive"),
        ("discard-drafts", "/api/gam/proposals/discard-drafts"),
        ("request-buyer-review", "/api/gam/proposals/request-buyer-review"),
        ("push-to-order", "/api/gam/proposals/push-to-order"),
    ],
)
def test_verb_posts_the_proposal_ids_to_its_route(verb, path):
    client = _mock_client()
    with patch("orbiads_cli.commands.programmatic.get_client", return_value=client):
        result = runner.invoke(app, ["programmatic", "proposals", verb, "10", "11", "--yes"])

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(path, json={"proposalIds": ["10", "11"]})


def test_pause_sends_the_reason():
    client = _mock_client()
    with patch("orbiads_cli.commands.programmatic.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["programmatic", "proposals", "pause", "10", "--reason", "creative review", "--yes"],
        )

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/proposals/pause", json={"proposalIds": ["10"], "reason": "creative review"}
    )


def test_pause_without_reason_is_a_usage_error_and_calls_nothing():
    client = _mock_client()
    with patch("orbiads_cli.commands.programmatic.get_client", return_value=client):
        result = runner.invoke(app, ["programmatic", "proposals", "pause", "10", "--yes"])

    assert result.exit_code != 0
    client.post.assert_not_called()


def test_declining_the_confirmation_prompt_calls_nothing():
    client = _mock_client()
    with (
        patch("orbiads_cli.commands.programmatic.get_client", return_value=client),
        patch("orbiads_cli.commands.programmatic.confirm", return_value=False),
    ):
        result = runner.invoke(app, ["programmatic", "proposals", "resume", "10"])

    assert result.exit_code == 0
    client.post.assert_not_called()


def test_verb_requires_at_least_one_id():
    client = _mock_client()
    with patch("orbiads_cli.commands.programmatic.get_client", return_value=client):
        result = runner.invoke(app, ["programmatic", "proposals", "resume", "--yes"])

    assert result.exit_code != 0
    client.post.assert_not_called()
