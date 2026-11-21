"""Story 116-2 — `orbiads orders lifecycle` accepts several order IDs and overbook ack.

The CLI calls the OrbiAds REST route `POST /api/gam/orders/lifecycle` (never GAM).
WSDL anchors: OrderService.wsdl:249 / :3119 / :3645 (overbook), :1046 (DeleteOrders),
:1096 / :3204 / :3668 (without reservation changes).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _invoke(args: list[str], client: MagicMock):
    with patch("orbiads_cli.commands.orders.get_client", return_value=client):
        return runner.invoke(app, ["orders", "lifecycle", *args])


def test_lifecycle_sends_every_order_id_in_one_batch_call(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"numChanges": 3, "requested": 3}

    result = _invoke(["pause", "11", "12", "13", "--yes"], client)

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/orders/lifecycle",
        json={"order_ids": ["11", "12", "13"], "action": "pause"},
    )


def test_lifecycle_single_id_still_works(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"numChanges": 1}

    result = _invoke(["resume", "888", "--yes"], client)

    assert result.exit_code == 0, result.output
    assert client.post.call_args.kwargs["json"] == {"order_ids": ["888"], "action": "resume"}


@pytest.mark.parametrize(
    "action",
    [
        "approve_and_overbook",
        "resume_and_overbook",
        "submit_for_approval_and_overbook",
        "disapprove_without_reservation_changes",
        "retire_without_reservation_changes",
        "submit_for_approval_without_reservation_changes",
        "delete",
    ],
)
def test_lifecycle_forwards_the_new_actions_verbatim(authenticated_config, action):
    client = MagicMock()
    client.post.return_value = {"numChanges": 1}

    result = _invoke([action, "5", "--acknowledge-overbook", "--yes"], client)

    assert result.exit_code == 0, result.output
    body = client.post.call_args.kwargs["json"]
    assert body["action"] == action
    assert body["acknowledge_overbook"] is True


def test_lifecycle_omits_the_ack_unless_asked(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"numChanges": 1}

    _invoke(["approve", "5", "--yes"], client)

    assert "acknowledge_overbook" not in client.post.call_args.kwargs["json"]


def test_lifecycle_declined_confirmation_sends_nothing(authenticated_config):
    client = MagicMock()

    with patch("orbiads_cli.commands.orders.confirm", return_value=False):
        result = _invoke(["delete", "5"], client)

    assert result.exit_code == 0
    client.post.assert_not_called()


def test_lifecycle_requires_at_least_one_order_id(authenticated_config):
    client = MagicMock()

    result = _invoke(["pause", "--yes"], client)

    assert result.exit_code == 2
    client.post.assert_not_called()
