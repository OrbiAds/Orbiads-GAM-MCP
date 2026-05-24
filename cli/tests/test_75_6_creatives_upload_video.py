"""Story 75.6 - VIDEO/AUDIO multipart upload via GCS staging."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def test_upload_video_happy_path(authenticated_config, tmp_path):
    file = tmp_path / "spot.mp4"
    file.write_bytes(b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 1000)
    client = MagicMock()
    client.post.return_value = {
        "creativeId": "123",
        "type": "VIDEO",
        "name": "Promo",
        "status": "PENDING_TRANSCODE",
    }

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                str(file),
                "--name",
                "Promo",
                "--advertiser-id",
                "456",
                "--duration-ms",
                "30000",
                "--size",
                "1280x720",
            ],
        )

    assert result.exit_code == 0, result.output
    fields = client.post.call_args.kwargs["data"]
    assert fields["type"] == "VIDEO"
    assert fields["duration_ms"] == "30000"
    assert client.post.call_args.kwargs["timeout"] == 300.0
    assert "transcode-status" in result.output


def test_upload_video_missing_duration_exits_2(authenticated_config, tmp_path):
    file = tmp_path / "spot.mp4"
    file.write_bytes(b"\x00\x00\x00\x18ftypmp42")

    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                str(file),
                "--name",
                "Promo",
                "--advertiser-id",
                "456",
                "--size",
                "640x360",
            ],
        )

    assert result.exit_code == 2
    assert "--duration-ms is required" in result.output
    get_client_mock.assert_not_called()


def test_upload_audio_auto_detected_from_extension(authenticated_config, tmp_path):
    file = tmp_path / "jingle.mp3"
    file.write_bytes(b"ID3\x03" + b"\x00" * 1000)
    client = MagicMock()
    client.post.return_value = {
        "creativeId": "456",
        "type": "AUDIO",
        "name": "Jingle",
        "status": "PENDING_TRANSCODE",
    }

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                str(file),
                "--name",
                "Jingle",
                "--advertiser-id",
                "456",
                "--duration-ms",
                "30000",
            ],
        )

    assert result.exit_code == 0, result.output
    assert client.post.call_args.kwargs["data"]["type"] == "AUDIO"


def test_transcode_status_processing(authenticated_config):
    client = MagicMock()
    client.get.return_value = {
        "creativeType": "VideoCreative",
        "status": "ACTIVE",
        "vastPreviewUrl": None,
    }

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "transcode-status", "123"])

    assert result.exit_code == 0, result.output
    assert "PROCESSING" in result.output
    assert client.get.call_args.args[0] == "/api/gam/creatives/123"


def test_dry_run_video_does_not_hit_network(authenticated_config, tmp_path):
    file = tmp_path / "spot.mp4"
    file.write_bytes(b"\x00\x00\x00\x18ftypmp42")

    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                str(file),
                "--name",
                "Promo",
                "--advertiser-id",
                "456",
                "--duration-ms",
                "30000",
                "--size",
                "1280x720",
                "--dry-run",
            ],
        )

    assert result.exit_code == 0, result.output
    assert "[dry-run] POST /api/gam/creatives/upload" in result.output
    assert "duration_ms=30000" in result.output
    get_client_mock.assert_not_called()
