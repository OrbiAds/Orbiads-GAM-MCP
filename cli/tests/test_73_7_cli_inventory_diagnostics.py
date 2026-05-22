"""Story 73.7 CLI wrappers for inventory diagnostics and size mappings."""

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


SIZE_MAPPING_PAYLOAD = {
    "adUnitId": "12345",
    "mappings": [
        {
            "viewportWidth": 1024,
            "viewportHeight": 768,
            "sizes": [{"width": 728, "height": 90}],
        }
    ],
}


@pytest.mark.parametrize(
    ("command_args", "method", "expected_path", "expected_kwargs", "payload"),
    [
        (
            ["inventory", "understanding", "analyze"],
            "post",
            "/api/gam/inventory/understanding/analyze",
            {"json": {"reuseLatest": False}},
            None,
        ),
        (
            ["inventory", "understanding", "get", "analysis-1"],
            "get",
            "/api/gam/inventory/understanding/analyses/analysis-1",
            {},
            None,
        ),
        (
            ["inventory", "size-mappings", "create", "--file", "{file}"],
            "post",
            "/api/gam/inventory/size-mappings",
            {"json": SIZE_MAPPING_PAYLOAD},
            SIZE_MAPPING_PAYLOAD,
        ),
        (
            ["inventory", "size-mappings", "get", "12345"],
            "get",
            "/api/gam/inventory/size-mappings/12345",
            {},
            None,
        ),
        (
            ["inventory", "size-mappings", "update", "12345", "--file", "{file}"],
            "put",
            "/api/gam/inventory/size-mappings/12345",
            {"json": SIZE_MAPPING_PAYLOAD},
            {**SIZE_MAPPING_PAYLOAD, "adUnitId": "from-file"},
        ),
        (
            ["inventory", "size-mappings", "delete", "12345", "--yes"],
            "delete",
            "/api/gam/inventory/size-mappings/12345",
            {},
            None,
        ),
        (
            ["inventory", "health"],
            "get",
            "/api/gam/inventory/health",
            {"params": {"period": "30d"}},
            None,
        ),
    ],
)
def test_story_73_7_inventory_diagnostics_call_expected_routes(
    authenticated_config,
    tmp_path,
    command_args,
    method,
    expected_path,
    expected_kwargs,
    payload,
):
    client = _mock_client(
        get={"ok": True, "analysisId": "analysis-1"},
        post={"ok": True, "analysisId": "analysis-1"},
        put={"ok": True},
        delete=None,
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


def test_understanding_analyze_reuse_latest_true(authenticated_config):
    client = _mock_client(post={"analysisId": "analysis-1"})

    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(
            app, ["inventory", "understanding", "analyze", "--reuse-latest"]
        )

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/inventory/understanding/analyze", json={"reuseLatest": True}
    )


def test_understanding_analyze_help_documents_synchronous_risk(authenticated_config):
    result = runner.invoke(app, ["inventory", "understanding", "analyze", "--help"])

    assert result.exit_code == 0, result.output
    assert "runs synchronously" in result.output
    assert "several minutes" in result.output
    assert "--reuse-latest" in result.output


def test_size_mappings_delete_yes_passes_effective_confirmation_context(
    authenticated_config,
):
    client = _mock_client(delete=None)

    with (
        patch("orbiads_cli.commands.inventory.get_client", return_value=client),
        patch("orbiads_cli.commands.inventory.confirm", return_value=True) as confirm_mock,
    ):
        result = runner.invoke(
            app, ["inventory", "size-mappings", "delete", "12345", "--yes"]
        )

    assert result.exit_code == 0, result.output
    confirm_mock.assert_called_once()
    message, effective_ctx = confirm_mock.call_args.args
    assert message == "Delete size mapping for 12345?"
    assert effective_ctx.yes is True
    client.delete.assert_called_once_with("/api/gam/inventory/size-mappings/12345")


def test_health_custom_period_passes_through(authenticated_config):
    client = _mock_client(get={"healthy": True})

    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "health", "--period", "7d"])

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/inventory/health", params={"period": "7d"}
    )


def test_size_mappings_create_missing_file_exits_2(authenticated_config, tmp_path):
    missing_path = tmp_path / "missing.json"

    result = runner.invoke(
        app,
        ["inventory", "size-mappings", "create", "--file", str(missing_path)],
    )

    assert result.exit_code == 2
    assert "file not found" in result.output
