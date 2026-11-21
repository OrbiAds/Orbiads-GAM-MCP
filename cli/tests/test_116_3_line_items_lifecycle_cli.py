"""Story 116-3 — `orbiads line-items lifecycle` forwards overbook ack, delete and batches.

The CLI calls the OrbiAds REST route `POST /api/gam/line-items/lifecycle` (never GAM).
WSDL anchors (LineItemService.wsdl, v202605): :6147 ReserveAndOverbookLineItems,
:6207 ResumeAndOverbookLineItems, :2186 DeleteLineItems.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()

def _two_step_client(result):
    """MagicMock client: dryRun -> preview + token, confirmationToken -> ``result``."""
    client = MagicMock()

    def _post(path, json=None, **_):
        if json.get("dryRun"):
            return {"preview": [{"operation": "x", "irreversible": True}], "confirmationToken": "tok-1"}
        return result

    client.post.side_effect = _post
    return client


def _invoke(args: list[str], client: MagicMock):
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        return runner.invoke(app, ["line-items", "lifecycle", *args])


def test_lifecycle_sends_every_id_in_one_batch_call(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"numChanges": 3, "requested": 3}

    result = _invoke(["pause", "--ids", "11, 12,13", "--yes"], client)

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/line-items/lifecycle",
        json={"line_item_ids": ["11", "12", "13"], "action": "pause"},
    )


@pytest.mark.parametrize("action", ["reserve_and_overbook", "resume_and_overbook", "delete"])
def test_lifecycle_forwards_the_new_actions_verbatim(authenticated_config, action):
    client = _two_step_client({"numChanges": 1})

    result = _invoke([action, "--ids", "5", "--acknowledge-overbook", "--yes"], client)

    assert result.exit_code == 0, result.output
    # Story 116-10: preview first (dryRun), then the token round trip, --yes or not.
    first, last = client.post.call_args_list[0].kwargs["json"], client.post.call_args.kwargs["json"]
    assert first["dryRun"] is True and "confirmationToken" not in first
    assert last["confirmationToken"] == "tok-1" and "dryRun" not in last
    assert last["action"] == action
    assert last["acknowledge_overbook"] is True


def test_lifecycle_omits_the_ack_unless_asked(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"numChanges": 1}

    _invoke(["reserve", "--ids", "5", "--yes"], client)

    assert "acknowledge_overbook" not in client.post.call_args.kwargs["json"]


def test_lifecycle_declined_confirmation_sends_nothing(authenticated_config):
    client = _two_step_client({})

    with patch("orbiads_cli.commands.line_items.confirm", return_value=False):
        result = _invoke(["delete", "--ids", "5"], client)

    assert result.exit_code == 0
    # Only the preview was sent: nothing executed, no token consumed.
    client.post.assert_called_once()
    assert client.post.call_args.kwargs["json"]["dryRun"] is True


def test_lifecycle_rejects_an_empty_id_list(authenticated_config):
    client = MagicMock()

    result = _invoke(["pause", "--ids", " , ", "--yes"], client)

    assert result.exit_code == 2
    client.post.assert_not_called()
