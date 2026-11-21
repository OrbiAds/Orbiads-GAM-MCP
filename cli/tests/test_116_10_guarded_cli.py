"""Story 116-10a - the CLI drives the two-step confirmation of irreversible REST writes.

HTTP is mocked at the client boundary: the CLI never reaches GAM nor the backend here.
Contract: dryRun -> {preview, confirmationToken} -> same payload + confirmationToken.
``--yes`` skips only the human prompt, never the token round trip.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.client import CliApiError
from orbiads_cli.main import app

runner = CliRunner()

PREVIEW = {
    "dryRun": True,
    "preview": [
        {
            "operation": "order_lifecycle",
            "action": "delete",
            "order_ids": ["5"],
            "irreversible": True,
            "warning": "IRREVERSIBLE: deletes the order",
        }
    ],
    "confirmationToken": "tok-1",
    "preflightSkipped": True,
    "warning": "The pre-delete check could not read the targets",
    "estimatedCost": 0.0,
}


def _client(result=None):
    client = MagicMock()

    def _post(path, json=None, **_):
        return PREVIEW if json.get("dryRun") else (result or {"numChanges": 1})

    client.post.side_effect = _post
    return client


def _run(cmd_module, args, client, **patches):
    with patch(f"orbiads_cli.commands.{cmd_module}.get_client", return_value=client):
        return runner.invoke(app, args)


def _bodies(client):
    return [c.kwargs["json"] for c in client.post.call_args_list]


@pytest.mark.parametrize(
    ("module", "args", "path"),
    [
        ("orders", ["orders", "lifecycle", "delete", "5"], "/api/gam/orders/lifecycle"),
        (
            "line_items",
            ["line-items", "lifecycle", "delete", "--ids", "5"],
            "/api/gam/line-items/lifecycle",
        ),
    ],
)
def test_yes_still_does_the_preview_and_token_round_trip(authenticated_config, module, args, path):
    client = _client()

    result = _run(module, [*args, "--yes"], client)

    assert result.exit_code == 0, result.output
    bodies = _bodies(client)
    assert len(bodies) == 2
    assert bodies[0]["dryRun"] is True and "confirmationToken" not in bodies[0]
    assert bodies[1] == {**{k: v for k, v in bodies[0].items() if k != "dryRun"}, "confirmationToken": "tok-1"}
    assert all(c.args[0] == path for c in client.post.call_args_list)


def test_preview_is_shown_on_stderr_before_the_prompt(authenticated_config):
    client = _client()
    seen = {}

    def _confirm(msg, ctx):
        seen["asked"] = True
        return True

    with (
        patch("orbiads_cli.commands.orders.get_client", return_value=client),
        patch("orbiads_cli.commands.orders.confirm", side_effect=_confirm),
    ):
        result = runner.invoke(app, ["orders", "lifecycle", "delete", "5"])

    assert result.exit_code == 0, result.output
    assert seen["asked"] is True
    assert "IRREVERSIBLE" in result.output
    assert "pre-delete check was skipped" in result.output
    assert len(_bodies(client)) == 2


def test_declining_after_the_preview_never_sends_the_token(authenticated_config):
    client = _client()
    with (
        patch("orbiads_cli.commands.orders.get_client", return_value=client),
        patch("orbiads_cli.commands.orders.confirm", return_value=False),
    ):
        result = runner.invoke(app, ["orders", "lifecycle", "delete", "5"])

    assert result.exit_code == 0
    assert len(_bodies(client)) == 1 and _bodies(client)[0]["dryRun"] is True


def test_reversible_action_stays_one_call(authenticated_config):
    client = _client()
    result = _run("orders", ["orders", "lifecycle", "pause", "5", "--yes"], client)
    assert result.exit_code == 0, result.output
    assert _bodies(client) == [{"order_ids": ["5"], "action": "pause"}]


def test_server_stricter_than_the_cli_table_falls_back_to_two_step(authenticated_config):
    client = MagicMock()

    def _post(path, json=None, **_):
        if json.get("dryRun"):
            return PREVIEW
        if "confirmationToken" in json:
            return {"numChanges": 1}
        raise CliApiError(1, "needs confirmation", "CONFIRMATION_REQUIRED")

    client.post.side_effect = _post
    result = _run("orders", ["orders", "lifecycle", "pause", "5", "--yes"], client)

    assert result.exit_code == 0, result.output
    assert [("dryRun" in b, "confirmationToken" in b) for b in _bodies(client)] == [
        (False, False),
        (True, False),
        (False, True),
    ]


def test_missing_token_in_the_preview_fails_without_executing(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"preview": []}  # old/odd server: no token

    result = _run("orders", ["orders", "lifecycle", "delete", "5", "--yes"], client)

    assert result.exit_code == 1
    assert "nothing was executed" in result.output
    assert client.post.call_count == 1


def test_api_refusal_on_execute_is_reported(authenticated_config):
    client = MagicMock()

    def _post(path, json=None, **_):
        if json.get("dryRun"):
            return PREVIEW
        raise CliApiError(5, "network changed", "NETWORK_CHANGED")

    client.post.side_effect = _post
    result = _run("orders", ["orders", "lifecycle", "delete", "5", "--yes"], client)
    assert result.exit_code == 5
    assert "network changed" in result.output
