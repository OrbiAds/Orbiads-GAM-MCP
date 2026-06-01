from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def test_live_stream_cli_five_verbs(authenticated_config) -> None:
    client = MagicMock()
    client.get.return_value = {"data": {"adBreaks": []}, "error": None}
    client.post.return_value = {"data": {"id": "ab-1"}, "error": None}
    client.patch.return_value = {"data": {"id": "ab-1"}, "error": None}
    client.delete.return_value = {"data": {"deleted": True}, "error": None}

    with patch("orbiads_cli.commands.live_stream.get_client", return_value=client):
        assert runner.invoke(
            app,
            ["live-stream", "list", "--area", "event_id", "--identifier", "game-1"],
        ).exit_code == 0
        assert runner.invoke(
            app,
            ["live-stream", "get", "ab-1", "--area", "event_id", "--identifier", "game-1"],
        ).exit_code == 0
        assert runner.invoke(
            app,
            [
                "live-stream",
                "create",
                "--area",
                "event_id",
                "--identifier",
                "game-1",
                "--start-time",
                "2026-06-15T20:30:00Z",
                "--duration",
                "60s",
            ],
        ).exit_code == 0
        assert runner.invoke(
            app,
            ["live-stream", "patch", "ab-1", "--asset-key", "asset-1", "--duration", "45s"],
        ).exit_code == 0
        assert runner.invoke(
            app,
            ["live-stream", "delete", "ab-1", "--asset-key", "asset-1"],
        ).exit_code == 0

    assert client.get.call_count == 2
    client.post.assert_called_once()
    client.patch.assert_called_once()
    client.delete.assert_called_once()
