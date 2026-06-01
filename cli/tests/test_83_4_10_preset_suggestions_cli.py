from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def test_settings_presets_suggestions_list(authenticated_config):
    client = MagicMock()
    client.get.return_value = [{"signatureHash": "abc123456789abcd"}]
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(app, ["settings", "presets", "suggestions", "list"])

    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/settings/presets/suggestions", params={"limit": 5})


def test_settings_presets_suggestions_accept(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"id": "preset-1"}
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "settings",
                "presets",
                "suggestions",
                "accept",
                "abc123456789abcd",
                "--name",
                "Homepage",
            ],
        )

    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/settings/presets/suggestions/abc123456789abcd:accept",
        json={"name": "Homepage"},
    )


def test_settings_presets_suggestions_dismiss(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"signatureHash": "abc123456789abcd"}
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["settings", "presets", "suggestions", "dismiss", "abc123456789abcd"],
        )

    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/settings/presets/suggestions/abc123456789abcd:dismiss"
    )


def test_settings_presets_suggestions_recompute(authenticated_config):
    client = MagicMock()
    client.post.return_value = {"jobId": "job-1"}
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(app, ["settings", "presets", "suggestions", "recompute"])

    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/settings/presets/suggestions:recompute")
