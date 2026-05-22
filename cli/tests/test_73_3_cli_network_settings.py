"""Story 73.3 CLI wrappers for network, settings, preview, and reference data."""

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
    ("command_args", "patch_target", "method", "path", "expected_kwargs", "payload"),
    [
        (
            ["network", "list-gam"],
            "orbiads_cli.commands.network.get_client",
            "get",
            "/api/gam/networks",
            {},
            None,
        ),
        (
            ["network", "config"],
            "orbiads_cli.commands.network.get_client",
            "get",
            "/api/gam/network-config",
            {},
            None,
        ),
        (
            ["network", "init"],
            "orbiads_cli.commands.network.get_client",
            "post",
            "/api/gam/network-init",
            {},
            None,
        ),
        (
            ["network", "gam-info"],
            "orbiads_cli.commands.network.get_client",
            "get",
            "/api/gam/network-info",
            {},
            None,
        ),
        (
            ["network", "test-connection"],
            "orbiads_cli.commands.network.get_client",
            "post",
            "/api/gam/test-connection",
            {},
            None,
        ),
        (
            ["network", "parse-ad-tag", "--file", "{file}"],
            "orbiads_cli.commands.network.get_client",
            "post",
            "/api/gam/parse-ad-tag",
            {"json": {"pastedText": "<script></script>"}},
            {"pastedText": "<script></script>"},
        ),
        (
            ["settings", "gam-preferences", "get"],
            "orbiads_cli.commands.settings_cmd.get_client",
            "get",
            "/api/gam/preferences",
            {},
            None,
        ),
        (
            ["settings", "gam-preferences", "set", "--file", "{file}"],
            "orbiads_cli.commands.settings_cmd.get_client",
            "put",
            "/api/gam/preferences",
            {"json": {"advertiserId": "123", "adUnitIds": ["au1"]}},
            {"advertiserId": "123", "adUnitIds": ["au1"]},
        ),
        (
            ["settings", "segmentation", "get"],
            "orbiads_cli.commands.settings_cmd.get_client",
            "get",
            "/api/gam/segmentation-preferences",
            {},
            None,
        ),
        (
            ["settings", "segmentation", "set", "--file", "{file}"],
            "orbiads_cli.commands.settings_cmd.get_client",
            "put",
            "/api/gam/segmentation-preferences",
            {"json": {"countries": ["FR"], "device": "desktop"}},
            {"countries": ["FR"], "device": "desktop"},
        ),
        (
            ["settings", "format-keys", "get"],
            "orbiads_cli.commands.settings_cmd.get_client",
            "get",
            "/api/gam/format-keys-config",
            {},
            None,
        ),
        (
            ["settings", "format-keys", "set", "--file", "{file}"],
            "orbiads_cli.commands.settings_cmd.get_client",
            "put",
            "/api/gam/format-keys-config",
            {"json": {"key1Id": "12345", "key1Name": "format"}},
            {"key1Id": "12345", "key1Name": "format"},
        ),
        (
            ["preview", "urls", "get"],
            "orbiads_cli.commands.preview.get_client",
            "get",
            "/api/gam/preview-urls",
            {},
            None,
        ),
        (
            ["preview", "urls", "set", "--file", "{file}"],
            "orbiads_cli.commands.preview.get_client",
            "put",
            "/api/gam/preview-urls",
            {"json": {"previewUrls": [{"name": "Home", "url": "https://example.com"}]}},
            {"previewUrls": [{"name": "Home", "url": "https://example.com"}]},
        ),
        (
            ["inventory", "technology-targets", "--type", "device"],
            "orbiads_cli.commands.inventory.get_client",
            "get",
            "/api/gam/technology-targets",
            {"params": {"type": "device"}},
            None,
        ),
    ],
)
def test_story_73_3_wrappers_call_expected_routes(
    authenticated_config,
    tmp_path,
    command_args,
    patch_target,
    method,
    path,
    expected_kwargs,
    payload,
):
    client = _mock_client()
    if payload is not None:
        file_path = _write_json(tmp_path, payload)
        command_args = [file_path if arg == "{file}" else arg for arg in command_args]

    with patch(patch_target, return_value=client):
        result = runner.invoke(app, ["--json", *command_args])

    assert result.exit_code == 0, result.output
    mocked_method = getattr(client, method)
    mocked_method.assert_called_once()
    call_args, call_kwargs = mocked_method.call_args
    assert call_args == (path,)
    assert call_kwargs == expected_kwargs


def test_network_parse_ad_tag_invalid_json_exits_2(authenticated_config, tmp_path):
    payload_path = tmp_path / "bad.json"
    payload_path.write_text("{not json", encoding="utf-8")

    result = runner.invoke(
        app,
        ["network", "parse-ad-tag", "--file", str(payload_path)],
    )

    assert result.exit_code == 2
    assert "invalid JSON" in result.output


def test_preview_urls_set_missing_file_exits_2(authenticated_config, tmp_path):
    missing_path = tmp_path / "missing.json"

    result = runner.invoke(
        app,
        ["preview", "urls", "set", "--file", str(missing_path)],
    )

    assert result.exit_code == 2
    assert "file not found" in result.output
