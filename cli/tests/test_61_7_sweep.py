"""Story 61.7 — final REST-ONLY sweep (advertisers/orders/settings/audiences/audit/preview/creatives uploads)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    c = MagicMock()
    for k in ("get", "post", "put", "patch", "delete"):
        getattr(c, k).return_value = ret.get(k)
    return c


def _write_json(tmp_path, payload):
    f = tmp_path / "p.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


# ─── advertisers / orders extensions ───────────────────────────────────────


def test_advertisers_find_or_create(authenticated_config):
    client = _mock_client(post={"id": "adv-1", "created": True})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(
            app, ["advertisers", "find-or-create", "--name", "Acme", "--type", "ADVERTISER"]
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/advertisers/find-or-create", json={"name": "Acme", "type": "ADVERTISER"}
    )


def test_orders_approve(authenticated_config):
    client = _mock_client(post={"approved": True})
    with patch("orbiads_cli.commands.orders.get_client", return_value=client):
        result = runner.invoke(app, ["orders", "approve", "o1", "--yes"])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/gam/orders/o1/approve")


def test_orders_list_delivering(authenticated_config):
    client = _mock_client(get={"orders": [{"id": "o1", "status": "delivering"}]})
    with patch("orbiads_cli.commands.orders.get_client", return_value=client):
        result = runner.invoke(app, ["orders", "list-delivering"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/orders", params={"limit": 50, "status": "delivering"}
    )


# ─── settings (9 verbs across 4 sub-groups) ────────────────────────────────


def test_settings_presets_list(authenticated_config):
    client = _mock_client(get={"presets": []})
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(app, ["settings", "presets", "list"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/settings/presets")


def test_settings_presets_create(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "p1"})
    f = _write_json(tmp_path, {"name": "morning"})
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(app, ["settings", "presets", "create", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/settings/presets", json={"name": "morning"})


def test_settings_presets_delete(authenticated_config):
    client = _mock_client(delete={"ok": True})
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(app, ["settings", "presets", "delete", "p1"])
    assert result.exit_code == 0
    client.delete.assert_called_once_with("/api/settings/presets/p1")


@pytest.mark.parametrize("noun,path", [
    ("general",            "/api/settings/general"),
    ("naming",             "/api/settings/naming"),
    ("delivery-defaults",  "/api/settings/delivery-defaults"),
])
def test_settings_get_set(authenticated_config, tmp_path, noun, path):
    # GET
    client = _mock_client(get={"setting": True})
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(app, ["settings", noun, "get"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(path)

    # PUT (set)
    client = _mock_client(put={"setting": True})
    f = _write_json(tmp_path, {"x": 1})
    with patch("orbiads_cli.commands.settings_cmd.get_client", return_value=client):
        result = runner.invoke(app, ["settings", noun, "set", "--file", f])
    assert result.exit_code == 0
    client.put.assert_called_once_with(path, json={"x": 1})


# ─── audiences / audit / preview ───────────────────────────────────────────


def test_audiences_list(authenticated_config):
    client = _mock_client(get={"audienceSegments": []})
    with patch("orbiads_cli.commands.audiences.get_client", return_value=client):
        result = runner.invoke(app, ["audiences", "list"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/audience-segments")


def test_audit_log(authenticated_config):
    client = _mock_client(get={"entries": []})
    with patch("orbiads_cli.commands.audit_log.get_client", return_value=client):
        result = runner.invoke(app, ["audit", "log"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/settings/audit/", params={"limit": 50})


def test_preview_share(authenticated_config, tmp_path):
    client = _mock_client(post={"url": "https://x"})
    f = _write_json(tmp_path, {"creativeId": "cr1"})
    with patch("orbiads_cli.commands.preview.get_client", return_value=client):
        result = runner.invoke(app, ["preview", "share", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/preview/share", json={"creativeId": "cr1"})


def test_preview_campaign(authenticated_config):
    client = _mock_client(post={"links": []})
    with patch("orbiads_cli.commands.preview.get_client", return_value=client):
        result = runner.invoke(app, ["preview", "campaign", "j1"])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/creatives/j1/gam-preview-link", json={})


# ─── creatives upload variants ────────────────────────────────────────────


@pytest.mark.parametrize("verb,path", [
    ("upload-third-party", "/api/creatives/upload-third-party"),
    ("upload-html5",       "/api/creatives/upload-html5"),
    ("upload-video",       "/api/creatives/upload-video"),
    ("upload-audio",       "/api/creatives/upload-audio"),
])
def test_creatives_upload_single_variants(authenticated_config, tmp_path, verb, path):
    f = tmp_path / "asset.bin"
    f.write_bytes(b"abc")
    client = MagicMock()
    client.post_multipart.return_value = {"id": "c1"}
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", verb, str(f)])
    assert result.exit_code == 0, result.output
    client.post_multipart.assert_called_once_with(path, str(f))


def test_creatives_upload_images_multi(authenticated_config, tmp_path):
    """upload-images uses _post_many_files (not post_multipart) — verifies it
    calls _request with a list of ("files", ...) tuples."""
    f1 = tmp_path / "a.png"; f1.write_bytes(b"\x89PNG")
    f2 = tmp_path / "b.png"; f2.write_bytes(b"\x89PNG")
    client = MagicMock()
    client._request.return_value = {"created": 2}
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "upload-images", str(f1), str(f2)])
    assert result.exit_code == 0, result.output
    args = client._request.call_args
    assert args.args[0] == "POST"
    assert args.args[1] == "/api/creatives/upload-images"
    files_arg = args.kwargs["files"]
    assert len(files_arg) == 2
    assert all(field == "files" for field, _ in files_arg)


def test_creatives_list_by_line_item(authenticated_config):
    client = _mock_client(get={"creatives": [{"id": "c1"}]})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "list-by-line-item", "li1"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/line-items/li1/creatives")
