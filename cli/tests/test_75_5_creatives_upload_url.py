"""Story 75.5 - creative upload from a public asset URL."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _success_client() -> MagicMock:
    client = MagicMock()
    client.post.return_value = {
        "creativeId": "2101",
        "type": "IMAGE",
        "name": "Banner",
        "size": {"width": 300, "height": 250},
        "status": "ACTIVE",
    }
    return client


def test_upload_url_image_posts_json(authenticated_config):
    client = _success_client()

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload-url",
                "https://cdn.example.com/banner.png",
                "--name",
                "Banner",
                "--advertiser-id",
                "456",
                "--size",
                "300x250",
            ],
        )

    assert result.exit_code == 0, result.output
    call = client.post.call_args
    assert call.args[0] == "/api/gam/creatives/upload/from-url"
    assert call.kwargs["json"] == {
        "assetUrl": "https://cdn.example.com/banner.png",
        "advertiserId": 456,
        "name": "Banner",
        "size": {"width": 300, "height": 250},
    }


def test_upload_url_html5_type(authenticated_config):
    client = _success_client()
    client.post.return_value["type"] = "HTML5"

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload-url",
                "https://cdn.example.com/bundle.zip",
                "--name",
                "H5",
                "--advertiser-id",
                "456",
                "--type",
                "html5",
                "--size",
                "300x250",
            ],
        )

    assert result.exit_code == 0, result.output
    assert client.post.call_args.kwargs["json"]["type"] == "HTML5"


def test_upload_url_native_metadata(authenticated_config):
    client = _success_client()
    metadata = '{"template_id": 789, "headline": "Buy Now"}'

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload-url",
                "https://cdn.example.com/main.png",
                "--name",
                "Native",
                "--advertiser-id",
                "456",
                "--type",
                "native",
                "--metadata",
                metadata,
            ],
        )

    assert result.exit_code == 0, result.output
    body = client.post.call_args.kwargs["json"]
    assert body["type"] == "NATIVE"
    assert body["metadata"] == {"template_id": 789, "headline": "Buy Now"}


def test_upload_url_rejects_non_http_url(authenticated_config):
    client = MagicMock()

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload-url",
                "file:///etc/passwd",
                "--name",
                "X",
                "--advertiser-id",
                "1",
            ],
        )

    assert result.exit_code == 2
    assert "--asset-url must be http(s)://" in result.output
    client.post.assert_not_called()


def test_upload_url_dry_run_no_network(authenticated_config):
    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload-url",
                "https://cdn.example.com/x.png",
                "--name",
                "X",
                "--advertiser-id",
                "1",
                "--size",
                "1x1",
                "--dry-run",
            ],
        )

    assert result.exit_code == 0, result.output
    assert "POST /api/gam/creatives/upload/from-url" in result.output
    get_client_mock.assert_not_called()


def test_upload_url_rejects_video_type(authenticated_config):
    client = MagicMock()

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload-url",
                "https://cdn.example.com/x.mp4",
                "--name",
                "X",
                "--advertiser-id",
                "1",
                "--type",
                "video",
            ],
        )

    assert result.exit_code == 2
    assert "creatives register" in result.output
    client.post.assert_not_called()


def test_upload_url_invalid_metadata_json(authenticated_config):
    client = MagicMock()

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload-url",
                "https://cdn.example.com/x.png",
                "--name",
                "X",
                "--advertiser-id",
                "1",
                "--type",
                "native",
                "--metadata",
                "{not json}",
            ],
        )

    assert result.exit_code == 2
    assert "invalid --metadata JSON" in result.output
    client.post.assert_not_called()


def test_upload_url_json_output(authenticated_config):
    client = _success_client()

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "--json",
                "creatives",
                "upload-url",
                "https://cdn.example.com/x.png",
                "--name",
                "B",
                "--advertiser-id",
                "1",
                "--size",
                "1x1",
            ],
        )

    assert result.exit_code == 0, result.output
    parsed = json.loads(result.stdout)
    assert parsed["creativeId"] == "2101"
