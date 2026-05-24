from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def test_creative_wrappers_list_calls_rest(authenticated_config):
    client = MagicMock()
    client.get.return_value = {"results": []}

    with patch("orbiads_cli.commands.creative_wrappers.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creative-wrappers",
                "list",
                "--label-id",
                "55",
                "--status",
                "ACTIVE",
                "--limit",
                "25",
            ],
        )

    assert result.exit_code == 0, result.output
    assert client.get.call_args.args[0] == "/api/gam/creative-wrappers"
    assert client.get.call_args.kwargs["params"]["labelId"] == 55


def test_creative_wrappers_get_calls_rest(authenticated_config):
    client = MagicMock()
    client.get.return_value = {"id": 2}

    with patch("orbiads_cli.commands.creative_wrappers.get_client", return_value=client):
        result = runner.invoke(app, ["creative-wrappers", "get", "2"])

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/creative-wrappers/2")


def test_creative_wrappers_create_posts_json_file(authenticated_config, tmp_path):
    client = MagicMock()
    client.post.return_value = {"id": 2}
    payload_path = tmp_path / "wrapper.json"
    payload = {"labelId": 55, "creativeWrapperType": "HTML", "htmlHeader": "<h></h>"}
    payload_path.write_text(json.dumps(payload), encoding="utf-8")

    with patch("orbiads_cli.commands.creative_wrappers.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["creative-wrappers", "create", "--file", str(payload_path)],
        )

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/creative-wrappers", json=payload)


def test_creative_wrappers_update_and_lifecycle_calls(authenticated_config, tmp_path):
    client = MagicMock()
    client.patch.return_value = {"id": 2}
    client.post.return_value = {"numChanges": 1}
    payload_path = tmp_path / "update.json"
    payload_path.write_text(json.dumps({"htmlFooter": "<f></f>"}), encoding="utf-8")

    with patch("orbiads_cli.commands.creative_wrappers.get_client", return_value=client):
        update = runner.invoke(
            app,
            ["creative-wrappers", "update", "2", "--file", str(payload_path)],
        )
        activate = runner.invoke(app, ["creative-wrappers", "activate", "2"])
        deactivate = runner.invoke(app, ["creative-wrappers", "deactivate", "2"])

    assert update.exit_code == 0, update.output
    assert activate.exit_code == 0, activate.output
    assert deactivate.exit_code == 0, deactivate.output
    client.patch.assert_called_once_with("/api/gam/creative-wrappers/2", json={"htmlFooter": "<f></f>"})
    assert client.post.call_args_list[0].args[0] == "/api/gam/creative-wrappers/2/activate"
    assert client.post.call_args_list[1].args[0] == "/api/gam/creative-wrappers/2/deactivate"


def test_creative_wrappers_set_data_declaration_calls_rest(authenticated_config):
    client = MagicMock()
    client.patch.return_value = {"id": 2}

    with patch("orbiads_cli.commands.creative_wrappers.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creative-wrappers",
                "set-data-declaration",
                "--wrapper-id",
                "2",
                "--declaration-type",
                "DECLARED",
                "--third-party-company-ids",
                "23",
                "--third-party-company-ids",
                "45",
            ],
        )

    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/creative-wrappers/2/data-declaration",
        json={"declarationType": "DECLARED", "thirdPartyCompanyIds": [23, 45]},
    )


def test_creative_wrappers_company_lookup_commands_call_rest(authenticated_config):
    client = MagicMock()
    client.get.return_value = {"results": []}

    with patch("orbiads_cli.commands.creative_wrappers.get_client", return_value=client):
        listed = runner.invoke(app, ["creative-wrappers", "list-companies", "--force-refresh"])
        found = runner.invoke(
            app,
            [
                "creative-wrappers",
                "find-company",
                "--name",
                "Integral Ad Science",
                "--min-score",
                "0.7",
            ],
        )

    assert listed.exit_code == 0, listed.output
    assert found.exit_code == 0, found.output
    assert client.get.call_args_list[0].args[0] == "/api/gam/rich-media-ads-companies"
    assert client.get.call_args_list[0].kwargs["params"] == {"forceRefresh": True}
    assert client.get.call_args_list[1].args[0] == "/api/gam/rich-media-ads-companies/search"
    assert client.get.call_args_list[1].kwargs["params"] == {
        "name": "Integral Ad Science",
        "minScore": 0.7,
    }
