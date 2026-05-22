"""Tests for the generic API passthrough command."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _client() -> MagicMock:
    client = MagicMock()
    client.get.return_value = {"ok": True}
    client.post.return_value = {"created": True}
    client.patch.return_value = {"updated": True}
    return client


def test_api_request_get_with_query(authenticated_config):
    client = _client()
    with patch("orbiads_cli.commands.api.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["--json", "api", "request", "GET", "/api/gam/features", "-q", "probe=true"],
        )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/features",
        params={"probe": "true"},
    )


def test_api_request_post_with_file(authenticated_config, tmp_path):
    client = _client()
    payload = {"networkCode": "66235823"}
    file_path = tmp_path / "payload.json"
    file_path.write_text(json.dumps(payload), encoding="utf-8")

    with patch("orbiads_cli.commands.api.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["--json", "api", "request", "POST", "/api/gam/switch-network", "-f", str(file_path)],
        )

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/switch-network",
        json=payload,
    )


def test_api_request_rejects_non_api_path(authenticated_config):
    result = runner.invoke(app, ["api", "request", "GET", "/health"])

    assert result.exit_code == 2
    assert "path must start with /api/" in result.output


def test_api_request_rejects_bad_query(authenticated_config):
    result = runner.invoke(app, ["api", "request", "GET", "/api/gam/features", "-q", "bad"])

    assert result.exit_code == 2
    assert "key=value" in result.output
