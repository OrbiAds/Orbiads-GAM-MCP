"""Story 100.8 - campaign media plan/deploy CLI passthrough."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def test_campaigns_plan_deployment_posts_mcp_payload(tmp_path: Path):
    payload_file = tmp_path / "media.json"
    payload_file.write_text(
        json.dumps(
            {
                "orderId": 1,
                "advertiserId": 2,
                "adUnitIds": ["10"],
                "vastRedirectUrl": "https://ads.example/vast.xml",
                "startDateTime": "2026-01-01T00:00:00",
                "endDateTime": "2026-01-31T23:59:59",
                "goal": 100,
            }
        ),
        encoding="utf-8",
    )
    client = MagicMock()
    client.post_raw.return_value = {"ok": True}

    with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["--json", "campaigns", "plan-deployment", "--preset", "video_vast", "--file", str(payload_file)],
        )

    assert result.exit_code == 0
    posted = client.post_raw.call_args
    assert posted.args[0] == "/mcp"
    body = posted.kwargs["json"]
    assert body["method"] == "tools/call"
    assert body["params"]["name"] == "campaign"
    assert body["params"]["arguments"]["action"] == "plan_deployment"
    assert body["params"]["arguments"]["params"]["preset"] == "video_vast"


def test_campaigns_deploy_media_posts_mcp_payload(tmp_path: Path):
    payload_file = tmp_path / "media.json"
    payload_file.write_text(
        json.dumps(
            {
                "orderId": 1,
                "advertiserId": 2,
                "adUnitIds": ["10"],
                "mediaSourceUrl": "https://cdn.example/video.mp4",
                "startDateTime": "2026-01-01T00:00:00",
                "endDateTime": "2026-01-31T23:59:59",
                "goal": 100,
            }
        ),
        encoding="utf-8",
    )
    client = MagicMock()
    client.post_raw.return_value = {"ok": True}

    with patch("orbiads_cli.commands.campaigns.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "--json",
                "--yes",
                "campaigns",
                "deploy-media",
                "--preset",
                "video_hosted",
                "--file",
                str(payload_file),
                "--confirmation-token",
                "token-123",
            ],
        )

    assert result.exit_code == 0
    posted = client.post_raw.call_args
    assert posted.args[0] == "/mcp"
    body = posted.kwargs["json"]
    args = body["params"]["arguments"]
    assert args["action"] == "deploy_media"
    assert args["params"]["preset"] == "video_hosted"
    assert args["params"]["confirmationToken"] == "token-123"
