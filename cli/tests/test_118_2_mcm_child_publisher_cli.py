"""Story 118-2 - `orbiads mcm child-publishers invite|update`, `orbiads advertisers companies create`.

HTTP is mocked at the client boundary (``get_client``). ``invite`` is two-step (GAM emails a
third party): dryRun -> {preview, confirmationToken} -> confirmation -> same body + token.
``update`` and ``companies create`` are one call, or --dry-run / --confirmation-token.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()

INVITE = {
    "name": "LT Child",
    "email": "child@example.com",
    "delegationType": "MANAGE_ACCOUNT",
    "proposedRevenueShareMillipercent": 15000,
}
PREVIEW = {
    "dryRun": True,
    "preview": [{"operation": "mcm.invite_child_publisher"}],
    "confirmationToken": "tok-1",
    "externalEffect": "GAM sends an MCM invitation email to child@example.com",
}


def _write(tmp_path, data, name="body.json"):
    path = tmp_path / name
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def _mcm_client():
    client = MagicMock()

    def _post(path, json=None, **_):
        return PREVIEW if json.get("dryRun") else {"invitationStatus": "PENDING"}

    client.post.side_effect = _post
    client.patch.return_value = {"childPublisher": {"id": "9"}, "changes": {}}
    return client


def _run_mcm(args, client):
    with patch("orbiads_cli.commands.mcm.get_client", return_value=client):
        return runner.invoke(app, args)


def test_invite_previews_then_sends_with_the_token(authenticated_config, tmp_path):
    client = _mcm_client()
    path = _write(tmp_path, INVITE)

    result = _run_mcm(["mcm", "child-publishers", "invite", "--file", path, "--yes"], client)

    assert result.exit_code == 0, result.output
    calls = [(c.args[0], c.kwargs["json"]) for c in client.post.call_args_list]
    assert calls == [
        ("/api/gam/mcm/child-publishers", {**INVITE, "dryRun": True}),
        ("/api/gam/mcm/child-publishers", {**INVITE, "confirmationToken": "tok-1"}),
    ]


def test_invite_declined_prompt_sends_nothing(authenticated_config, tmp_path):
    client = _mcm_client()
    path = _write(tmp_path, INVITE)

    prompts: list[str] = []

    def _decline(message, ctx):
        prompts.append(message)
        return False

    with patch("orbiads_cli.commands.mcm.confirm", side_effect=_decline):
        _run_mcm(["mcm", "child-publishers", "invite", "--file", path], client)

    assert client.post.call_count == 1  # the preview only
    assert client.post.call_args.kwargs["json"]["dryRun"] is True
    assert prompts and "child@example.com" in prompts[0]


def test_invite_rejects_a_non_object_file(authenticated_config, tmp_path):
    client = _mcm_client()
    path = _write(tmp_path, [INVITE])

    result = _run_mcm(["mcm", "child-publishers", "invite", "--file", path, "--yes"], client)

    assert result.exit_code == 2
    client.post.assert_not_called()


def test_update_is_one_call_with_dry_run_and_token_options(authenticated_config, tmp_path):
    client = _mcm_client()
    path = _write(tmp_path, {"updates": {"comment": "c"}})

    for extra, expected in (
        ([], {"updates": {"comment": "c"}}),
        (["--dry-run"], {"updates": {"comment": "c"}, "dryRun": True}),
        (["--confirmation-token", "t1"], {"updates": {"comment": "c"}, "confirmationToken": "t1"}),
    ):
        client.patch.reset_mock()
        result = _run_mcm(
            ["mcm", "child-publishers", "update", "9", "--file", path, *extra], client
        )
        assert result.exit_code == 0, result.output
        client.patch.assert_called_once_with("/api/gam/mcm/child-publishers/9", json=expected)

    both = _run_mcm(
        ["mcm", "child-publishers", "update", "9", "--file", path, "--dry-run",
         "--confirmation-token", "t"],
        client,
    )
    assert both.exit_code == 2


def test_companies_create_posts_the_type_and_fields(authenticated_config, tmp_path):
    client = MagicMock()
    client.post.return_value = {"company": {"id": "31"}, "created": True}
    path = _write(tmp_path, {"name": "LT-118-2-P", "comment": "lt"})

    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["advertisers", "companies", "create", "--type", "partner", "--file", path,
             "--dry-run"],
        )

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/companies",
        json={"name": "LT-118-2-P", "comment": "lt", "type": "PARTNER", "dryRun": True},
    )
