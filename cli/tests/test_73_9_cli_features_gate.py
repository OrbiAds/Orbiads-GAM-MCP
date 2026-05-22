"""Story 73.9 CLI wrappers for GAM features."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    client = MagicMock()
    for method in ("get", "post", "put", "patch", "delete"):
        getattr(client, method).return_value = ret.get(method, {"ok": True})
    return client


def test_features_list_calls_cached_probe_route(authenticated_config):
    client = _mock_client(get={"features": None})

    with patch("orbiads_cli.commands.features.get_client", return_value=client):
        result = runner.invoke(app, ["--json", "features", "list"])

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/features")
    client.post.assert_not_called()


def test_features_probe_calls_literal_custom_verb_route(authenticated_config):
    client = _mock_client(post={"features": {"supportsPmp": True}})

    with patch("orbiads_cli.commands.features.get_client", return_value=client):
        result = runner.invoke(app, ["--json", "features", "probe"])

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/features:probe")
    client.get.assert_not_called()


def test_features_group_is_registered(authenticated_config):
    result = runner.invoke(app, ["features", "--help"])

    assert result.exit_code == 0, result.output
    assert "list" in result.output
    assert "probe" in result.output
