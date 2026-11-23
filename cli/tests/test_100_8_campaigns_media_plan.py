"""Story 100.8 media plan/deploy CLI commands - repaired (no more dead /mcp passthrough).

The CLI cannot call `/mcp/`: the mount answers 307 (httpx does not follow it) and the
endpoint only accepts its own OAuth tokens, not the CLI Firebase ID token. The commands
therefore fail honestly and never touch the network.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    "argv",
    [
        ["campaigns", "plan-deployment", "--preset", "video_vast", "--file", "x.json"],
        [
            "--yes",
            "campaigns",
            "deploy-media",
            "--preset",
            "video_hosted",
            "--file",
            "x.json",
            "--confirmation-token",
            "token-123",
        ],
    ],
)
def test_media_commands_fail_honestly_without_network(argv):
    client = MagicMock()
    with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
        result = runner.invoke(app, argv)

    assert result.exit_code == 1
    assert "not available from the CLI" in result.output
    assert "campaign(action=" in result.output
    assert "success" not in result.output.lower()
    assert client.method_calls == []
