"""Story 73.6 CLI wrappers for inventory blueprint utilities."""

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
    ("command_args", "method", "expected_path", "expected_kwargs", "payload"),
    [
        (
            ["inventory", "blueprint", "validate", "--file", "{file}"],
            "post",
            "/api/gam/inventory/blueprint/validate",
            {"json": {"name": "Blueprint", "preferences": {}}},
            {"name": "Blueprint", "preferences": {}},
        ),
        (
            ["inventory", "blueprint", "export", "--file", "{file}"],
            "post",
            "/api/gam/inventory/blueprint/export",
            {"json": {"blueprint": {"name": "Blueprint"}, "format": "csv"}},
            {"blueprint": {"name": "Blueprint"}, "format": "csv"},
        ),
        (
            ["inventory", "blueprint", "templates", "list"],
            "get",
            "/api/gam/inventory/blueprint/templates",
            {},
            None,
        ),
        (
            ["inventory", "blueprint", "templates", "get", "grid"],
            "get",
            "/api/gam/inventory/blueprint/templates/grid",
            {},
            None,
        ),
        (
            ["inventory", "blueprint", "size-bundles", "list"],
            "get",
            "/api/gam/inventory/blueprint/size-bundles",
            {},
            None,
        ),
        (
            ["inventory", "blueprint", "size-bundles", "create", "--file", "{file}"],
            "post",
            "/api/gam/inventory/blueprint/size-bundles",
            {"json": {"name": "Leaderboard", "sizes": [{"width": 728, "height": 90}]}},
            {"name": "Leaderboard", "sizes": [{"width": 728, "height": 90}]},
        ),
        (
            ["inventory", "blueprint", "size-bundles", "delete", "b-1", "--yes"],
            "delete",
            "/api/gam/inventory/blueprint/size-bundles/b-1",
            {},
            None,
        ),
        (
            ["inventory", "blueprint", "recalculate-sizes", "--file", "{file}"],
            "post",
            "/api/gam/inventory/blueprint/recalculate-sizes",
            {"json": {"blueprint": {"name": "Blueprint", "preferences": {}}}},
            {"blueprint": {"name": "Blueprint", "preferences": {}}},
        ),
        (
            ["inventory", "blueprint", "custom-positions", "list"],
            "get",
            "/api/gam/inventory/blueprint/custom-positions",
            {},
            None,
        ),
        (
            ["inventory", "blueprint", "custom-positions", "create", "--file", "{file}"],
            "post",
            "/api/gam/inventory/blueprint/custom-positions",
            {"json": {"name": "above_fold", "label": "Above fold"}},
            {"name": "above_fold", "label": "Above fold"},
        ),
    ],
)
def test_story_73_6_blueprint_wrappers_call_expected_routes(
    authenticated_config,
    tmp_path,
    command_args,
    method,
    expected_path,
    expected_kwargs,
    payload,
):
    client = _mock_client(
        get=[{"id": "grid", "name": "Grid"}],
        post={"ok": True, "format": "csv", "csv": "name,path\nTop,/top"},
        delete={"deleted": True},
    )
    if payload is not None:
        file_path = _write_json(tmp_path, payload)
        command_args = [file_path if arg == "{file}" else arg for arg in command_args]

    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["--json", *command_args])

    assert result.exit_code == 0, result.output
    mocked_method = getattr(client, method)
    mocked_method.assert_called_once()
    call_args, call_kwargs = mocked_method.call_args
    assert call_args == (expected_path,)
    assert call_kwargs == expected_kwargs


def test_blueprint_export_renders_full_data_object(authenticated_config, tmp_path):
    client = _mock_client(post={"format": "csv", "csv": "name,path\nTop,/top"})
    payload_file = _write_json(
        tmp_path, {"blueprint": {"name": "Blueprint"}, "format": "csv"}
    )

    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "--json",
                "inventory",
                "blueprint",
                "export",
                "--file",
                payload_file,
            ],
        )

    assert result.exit_code == 0, result.output
    assert '"format": "csv"' in result.output
    assert '"csv": "name,path\\nTop,/top"' in result.output


def test_size_bundles_delete_yes_passes_effective_confirmation_context(
    authenticated_config,
):
    client = _mock_client(delete={"deleted": True})

    with (
        patch("orbiads_cli.commands.inventory.get_client", return_value=client),
        patch("orbiads_cli.commands.inventory.confirm", return_value=True) as confirm_mock,
    ):
        result = runner.invoke(
            app,
            ["inventory", "blueprint", "size-bundles", "delete", "b-1", "--yes"],
        )

    assert result.exit_code == 0, result.output
    confirm_mock.assert_called_once()
    _, effective_ctx = confirm_mock.call_args.args
    assert effective_ctx.yes is True
    client.delete.assert_called_once_with("/api/gam/inventory/blueprint/size-bundles/b-1")


def test_blueprint_validate_missing_file_exits_2(authenticated_config, tmp_path):
    missing_path = tmp_path / "missing.json"

    result = runner.invoke(
        app,
        ["inventory", "blueprint", "validate", "--file", str(missing_path)],
    )

    assert result.exit_code == 2
    assert "file not found" in result.output
