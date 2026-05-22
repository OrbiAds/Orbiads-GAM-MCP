"""Story 73.4 CLI wrappers for inventory mutations and job bulk updates."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    client = MagicMock()
    for method in ("get", "post", "put", "patch", "delete"):
        getattr(client, method).return_value = ret.get(method, {"ok": True})
    return client


def _write_json(tmp_path, payload):
    path = tmp_path / "payload.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


@pytest.mark.parametrize(
    ("command_args", "patch_target", "expected_path", "expected_body", "payload"),
    [
        (
            ["line-items", "update-all", "job-42", "--file", "{file}", "--yes"],
            "orbiads_cli.commands.line_items.get_client",
            "/api/gam/jobs/job-42/line-items/update-all",
            {"costPerUnit": {"micros": "1000000", "currencyCode": "EUR"}},
            {"costPerUnit": {"micros": "1000000", "currencyCode": "EUR"}},
        ),
        (
            ["inventory", "create-ad-units", "--file", "{file}"],
            "orbiads_cli.commands.inventory.get_client",
            "/api/gam/ad-units",
            {"name": "Top", "code": "top"},
            {"name": "Top", "code": "top"},
        ),
        (
            ["inventory", "import-ad-units", "--file", "{file}", "--dry-run"],
            "orbiads_cli.commands.inventory.get_client",
            "/api/gam/ad-units/import",
            {"units": [{"name": "Top", "code": "top"}], "dryRun": True},
            {"units": [{"name": "Top", "code": "top"}], "dryRun": False},
        ),
        (
            ["inventory", "validate-fluid-batch", "--file", "{file}"],
            "orbiads_cli.commands.inventory.get_client",
            "/api/gam/ad-units/validate-fluid-batch",
            {"adUnitIds": ["12345", "67890"]},
            {"adUnitIds": ["12345", "67890"]},
        ),
    ],
)
def test_story_73_4_mutation_wrappers_call_expected_routes(
    authenticated_config,
    tmp_path,
    command_args,
    patch_target,
    expected_path,
    expected_body,
    payload,
):
    client = _mock_client()
    file_path = _write_json(tmp_path, payload)
    command_args = [file_path if arg == "{file}" else arg for arg in command_args]

    with patch(patch_target, return_value=client):
        result = runner.invoke(app, ["--json", *command_args])

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(expected_path, json=expected_body)


def test_update_all_yes_passes_effective_confirmation_context(authenticated_config, tmp_path):
    client = _mock_client()
    payload_file = _write_json(tmp_path, {"priority": 8})

    with (
        patch("orbiads_cli.commands.line_items.get_client", return_value=client),
        patch("orbiads_cli.commands.line_items.confirm", return_value=True) as confirm_mock,
    ):
        result = runner.invoke(
            app,
            ["line-items", "update-all", "job-42", "--file", payload_file, "--yes"],
        )

    assert result.exit_code == 0, result.output
    confirm_mock.assert_called_once()
    _, effective_ctx = confirm_mock.call_args.args
    assert effective_ctx.yes is True


def test_import_ad_units_without_flag_forwards_body_dry_run(authenticated_config, tmp_path):
    client = _mock_client()
    payload_file = _write_json(
        tmp_path, {"units": [{"name": "Top", "code": "top"}], "dryRun": False}
    )

    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(
            app, ["inventory", "import-ad-units", "--file", payload_file]
        )

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/ad-units/import",
        json={"units": [{"name": "Top", "code": "top"}], "dryRun": False},
    )


def test_story_73_4_invalid_json_exits_2(authenticated_config, tmp_path):
    payload_file = tmp_path / "bad.json"
    payload_file.write_text("{not json", encoding="utf-8")

    result = runner.invoke(
        app, ["inventory", "validate-fluid-batch", "--file", str(payload_file)]
    )

    assert result.exit_code == 2
    assert "invalid JSON" in result.output
