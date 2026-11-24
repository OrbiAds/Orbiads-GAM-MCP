"""Story 118-4 - `orbiads advertisers partners list|get|update` (companies of type PARTNER)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _run(args, client):
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        return runner.invoke(app, args)


def test_list_sends_the_filters(authenticated_config):
    client = MagicMock()
    client.get.return_value = {
        "items": [
            {
                "id": "5",
                "name": "Partner A",
                "type": "PARTNER",
                "creditStatus": "ACTIVE",
            }
        ],
        "hasMore": False,
    }

    result = _run(
        ["advertisers", "partners", "list", "--name-contains", "Part", "--limit", "10"],
        client,
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/partners", params={"limit": 10, "name_contains": "Part"}
    )
    assert "Partner A" in result.output


def test_get_reads_one_partner(authenticated_config):
    client = MagicMock()
    client.get.return_value = {"id": "5", "type": "PARTNER"}

    result = _run(["advertisers", "partners", "get", "5"], client)

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/partners/5")


def test_update_patches_the_fields_of_the_file(authenticated_config, tmp_path):
    body = tmp_path / "p.json"
    body.write_text(json.dumps({"name": "Partner B", "comment": "c"}), encoding="utf-8")
    client = MagicMock()
    client.patch.return_value = {"id": "5", "name": "Partner B"}

    result = _run(
        ["advertisers", "partners", "update", "5", "--file", str(body)], client
    )

    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/partners/5", json={"updates": {"name": "Partner B", "comment": "c"}}
    )


def test_update_accepts_a_wrapped_body_and_dry_run(authenticated_config, tmp_path):
    body = tmp_path / "p.json"
    body.write_text(
        json.dumps({"updates": {"creditStatus": "ON_HOLD"}}), encoding="utf-8"
    )
    client = MagicMock()
    client.patch.return_value = {"preview": [], "changes": {}}

    result = _run(
        ["advertisers", "partners", "update", "5", "--file", str(body), "--dry-run"],
        client,
    )

    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/partners/5",
        json={"updates": {"creditStatus": "ON_HOLD"}, "dryRun": True},
    )


def test_update_replays_the_preview_token(authenticated_config, tmp_path):
    """Audit 118-4 AVERT-4: execute exactly the previewed change."""
    body = tmp_path / "p.json"
    body.write_text(json.dumps({"comment": "c"}), encoding="utf-8")
    client = MagicMock()
    client.patch.return_value = {"id": "5"}

    result = _run(
        [
            "advertisers",
            "partners",
            "update",
            "5",
            "--file",
            str(body),
            "--confirmation-token",
            "tok-1",
        ],
        client,
    )

    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/partners/5",
        json={"updates": {"comment": "c"}, "confirmationToken": "tok-1"},
    )
    both = _run(
        [
            "advertisers",
            "partners",
            "update",
            "5",
            "--file",
            str(body),
            "--dry-run",
            "--confirmation-token",
            "t",
        ],
        client,
    )
    assert both.exit_code == 2
