"""Story 75.3 - unified streaming creative upload CLI command."""

from __future__ import annotations

import json
import zipfile
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.client import CliApiError
from orbiads_cli.main import app

runner = CliRunner()


def _mk_png(tmp_path) -> str:
    path = tmp_path / "banner.png"
    path.write_bytes(b"\x89PNG\r\n\x1a\nfake-image-bytes")
    return str(path)


def _mk_zip(tmp_path) -> str:
    path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("index.html", "<html></html>")
    return str(path)


def _success_client() -> MagicMock:
    client = MagicMock()
    client.post.return_value = {
        "creativeId": "2001",
        "type": "IMAGE",
        "name": "Summer Banner",
        "size": {"width": 300, "height": 250},
        "status": "ACTIVE",
    }
    return client


def test_upload_image_posts_multipart(authenticated_config, tmp_path):
    """AC1 - IMAGE upload streams multipart to the GAM upload route."""
    png = _mk_png(tmp_path)
    client = _success_client()

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                png,
                "--name",
                "Summer Banner",
                "--advertiser-id",
                "456",
                "--size",
                "300x250",
            ],
        )

    assert result.exit_code == 0, result.output
    call = client.post.call_args
    assert call.args[0] == "/api/gam/creatives/upload"
    file_name, _handle, content_type = call.kwargs["files"]["file"]
    assert file_name == "banner.png"
    assert content_type == "image/png"
    fields = call.kwargs["data"]
    assert fields["advertiser_id"] == "456"
    assert fields["name"] == "Summer Banner"
    assert fields["type"] == "IMAGE"
    assert json.loads(fields["size"]) == {"width": 300, "height": 250}


def test_upload_html5_zip_auto_detects_type(authenticated_config, tmp_path):
    """AC2 - .zip uploads are sent as HTML5 creatives."""
    bundle = _mk_zip(tmp_path)
    client = _success_client()
    client.post.return_value = {
        "creativeId": "2002",
        "type": "HTML5",
        "name": "HTML5 300x250",
        "size": {"width": 300, "height": 250},
        "status": "ACTIVE",
    }

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                bundle,
                "--name",
                "HTML5 300x250",
                "--advertiser-id",
                "456",
                "--size",
                "300x250",
            ],
        )

    assert result.exit_code == 0, result.output
    assert client.post.call_args.kwargs["data"]["type"] == "HTML5"


def test_upload_native_with_metadata(authenticated_config, tmp_path):
    """AC3 - NATIVE upload sends raw metadata JSON as a multipart field."""
    png = _mk_png(tmp_path)
    metadata = (
        '{"template_id": 789, "headline": "Buy Now", '
        '"body": "Best offer", "click_url": "https://example.com"}'
    )
    client = _success_client()
    client.post.return_value = {
        "creativeId": "2003",
        "type": "NATIVE",
        "name": "Native Ad",
        "status": "ACTIVE",
    }

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                png,
                "--type",
                "native",
                "--name",
                "Native Ad",
                "--advertiser-id",
                "456",
                "--metadata",
                metadata,
            ],
        )

    assert result.exit_code == 0, result.output
    fields = client.post.call_args.kwargs["data"]
    assert fields["type"] == "NATIVE"
    assert fields["metadata"] == metadata


def test_upload_missing_file_exits_2_before_network(authenticated_config):
    """AC8 - missing files fail locally before get_client()."""
    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                "./does-not-exist.png",
                "--name",
                "N",
                "--advertiser-id",
                "1",
                "--size",
                "1x1",
            ],
        )

    assert result.exit_code == 2
    assert "file not found: ./does-not-exist.png" in result.output
    get_client_mock.assert_not_called()


def test_upload_image_requires_size(authenticated_config, tmp_path):
    """AC1/AC5 - IMAGE uploads require an explicit size."""
    png = _mk_png(tmp_path)

    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            ["creatives", "upload", png, "--name", "N", "--advertiser-id", "1"],
        )

    assert result.exit_code == 2
    assert "--size is required" in result.output
    get_client_mock.assert_not_called()


def test_upload_unknown_extension_requires_type(authenticated_config, tmp_path):
    """AC5 - unknown extensions are not guessed."""
    path = tmp_path / "creative.bin"
    path.write_bytes(b"abc")

    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            ["creatives", "upload", str(path), "--name", "N", "--advertiser-id", "1"],
        )

    assert result.exit_code == 2
    assert "cannot auto-detect creative type" in result.output
    get_client_mock.assert_not_called()


def test_upload_rejects_video_audio_types(authenticated_config, tmp_path):
    """AC5 - VIDEO/AUDIO are registered by URL, not uploaded as multipart."""
    png = _mk_png(tmp_path)

    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                png,
                "--type",
                "video",
                "--name",
                "V",
                "--advertiser-id",
                "1",
            ],
        )

    assert result.exit_code == 2
    assert "Use `creatives register" in result.output
    get_client_mock.assert_not_called()


def test_upload_invalid_metadata_json_exits_2(authenticated_config, tmp_path):
    """AC6 - metadata JSON is validated before network calls."""
    png = _mk_png(tmp_path)

    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                png,
                "--type",
                "native",
                "--name",
                "N",
                "--advertiser-id",
                "1",
                "--metadata",
                "{not-json}",
            ],
        )

    assert result.exit_code == 2
    assert "invalid --metadata JSON" in result.output
    get_client_mock.assert_not_called()


def test_upload_dry_run_prints_plan_without_network(authenticated_config, tmp_path):
    """AC6 - --dry-run validates locally and never instantiates the HTTP client."""
    png = _mk_png(tmp_path)

    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                png,
                "--name",
                "B",
                "--advertiser-id",
                "456",
                "--size",
                "300x250",
                "--dry-run",
            ],
        )

    assert result.exit_code == 0, result.output
    assert "[dry-run] POST /api/gam/creatives/upload" in result.output
    get_client_mock.assert_not_called()


def test_upload_json_output(authenticated_config, tmp_path):
    """AC7 - --json emits parseable detail JSON."""
    png = _mk_png(tmp_path)
    client = _success_client()

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "--json",
                "creatives",
                "upload",
                png,
                "--name",
                "Summer Banner",
                "--advertiser-id",
                "456",
                "--size",
                "300x250",
            ],
        )

    assert result.exit_code == 0, result.output
    parsed = json.loads(result.stdout)
    assert parsed["creativeId"] == "2001"
    assert parsed["type"] == "IMAGE"


def test_upload_backend_error_uses_semantic_exit_code(authenticated_config, tmp_path):
    """AC9 - backend CliApiError is surfaced by the shared handler."""
    png = _mk_png(tmp_path)
    client = MagicMock()
    client.post.side_effect = CliApiError(1, "GAM API error: bad SOAP", "GAM_API_ERROR")

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "upload",
                png,
                "--name",
                "B",
                "--advertiser-id",
                "456",
                "--size",
                "300x250",
            ],
        )

    assert result.exit_code == 1
    assert "Error: GAM API error: bad SOAP" in result.output


def test_register_video_posts_json(authenticated_config):
    """AC4 - VIDEO registration posts camelCase JSON to the register route."""
    client = MagicMock()
    client.post.return_value = {
        "creativeId": "3001",
        "type": "VIDEO",
        "name": "Pre-roll",
        "size": {"width": 640, "height": 360},
        "status": "ACTIVE",
    }

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "register",
                "--type",
                "VIDEO",
                "--advertiser-id",
                "456",
                "--name",
                "Pre-roll",
                "--vast-url",
                "https://ad.server.com/vast.xml",
                "--size",
                "640x360",
                "--duration-ms",
                "30000",
            ],
        )

    assert result.exit_code == 0, result.output
    call = client.post.call_args
    assert call.args[0] == "/api/gam/creatives/upload/register"
    assert call.kwargs["json"] == {
        "type": "VIDEO",
        "advertiserId": 456,
        "name": "Pre-roll",
        "vastRedirectUrl": "https://ad.server.com/vast.xml",
        "durationMs": 30000,
        "size": {"width": 640, "height": 360},
    }


def test_register_audio_posts_json_without_size(authenticated_config):
    """AC4 - AUDIO registration uses the same endpoint and omits absent size."""
    client = MagicMock()
    client.post.return_value = {
        "creativeId": "3002",
        "type": "AUDIO",
        "name": "Audio",
        "status": "ACTIVE",
    }

    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "creatives",
                "register",
                "--type",
                "AUDIO",
                "--advertiser-id",
                "456",
                "--name",
                "Audio",
                "--vast-url",
                "https://ad.server.com/audio.xml",
            ],
        )

    assert result.exit_code == 0, result.output
    body = client.post.call_args.kwargs["json"]
    assert body["type"] == "AUDIO"
    assert "size" not in body


def test_register_dry_run_prints_body_without_network(authenticated_config):
    """AC6 - register --dry-run avoids auth/client/network work."""
    with patch("orbiads_cli.commands.creatives.get_client") as get_client_mock:
        result = runner.invoke(
            app,
            [
                "creatives",
                "register",
                "--type",
                "VIDEO",
                "--advertiser-id",
                "1",
                "--name",
                "X",
                "--vast-url",
                "https://x.test/vast.xml",
                "--dry-run",
            ],
        )

    assert result.exit_code == 0, result.output
    assert "[dry-run] POST /api/gam/creatives/upload/register" in result.output
    get_client_mock.assert_not_called()
