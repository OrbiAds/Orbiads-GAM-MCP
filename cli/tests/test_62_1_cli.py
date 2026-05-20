"""Story 62.1 — CLI wrappers for creatives / LICA / NativeStyle /
CreativeTemplate Tier B routes."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    c = MagicMock()
    for k in ("get", "post", "put", "patch", "delete"):
        getattr(c, k).return_value = ret.get(k)
    c.post_multipart.return_value = ret.get("post_multipart")
    return c


def _write_json(tmp_path, payload):
    f = tmp_path / "p.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


# === creatives (Story 62.1 extension — 9 verbs) ===========================


def test_creatives_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"creativeId": "cr-1"})
    f = _write_json(tmp_path, {"updateFields": {"name": "Renamed"}})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "update", "cr-1", "--file", f])
    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/creatives/cr-1", json={"updateFields": {"name": "Renamed"}}
    )


def test_creatives_archive(authenticated_config):
    client = _mock_client(post={"archived": True})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "archive", "cr-1", "--yes"])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/creatives/cr-1/archive")


def test_creatives_duplicate(authenticated_config):
    client = _mock_client(post={"id": "cr-2"})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "duplicate", "cr-1", "--yes"])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/creatives/cr-1/duplicate")


def test_creatives_preview_url(authenticated_config):
    client = _mock_client(get={"url": "https://preview/x"})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "preview-url", "cr-1"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/creatives/cr-1/preview-url")


def test_creatives_native_style_previews(authenticated_config):
    client = _mock_client(get={"previews": []})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app, ["creatives", "native-style-previews", "cr-1"]
        )
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/creatives/cr-1/native-style-previews"
    )


def test_creatives_list_by_network(authenticated_config):
    client = _mock_client(get={"items": [{"id": "cr-1", "name": "X"}], "total": 1})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "list-by-network"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/creatives", params={"limit": 100, "offset": 0}
    )


def test_creatives_list_by_network_with_query(authenticated_config):
    client = _mock_client(get={"items": []})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["creatives", "list-by-network", "--query", "promo", "--limit", "50"],
        )
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/creatives", params={"limit": 50, "offset": 0, "q": "promo"}
    )


def test_creatives_upload_vast_redirect(authenticated_config, tmp_path):
    f = tmp_path / "vast.xml"
    f.write_text("<VAST/>", encoding="utf-8")
    client = _mock_client(post_multipart={"id": "cr-9"})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(
            app, ["creatives", "upload-vast-redirect", str(f)]
        )
    assert result.exit_code == 0, result.output
    client.post_multipart.assert_called_once_with(
        "/api/creatives/upload-vast-redirect", str(f)
    )


def test_creatives_upload_companion(authenticated_config, tmp_path):
    f = tmp_path / "comp.png"
    f.write_bytes(b"\x89PNG\r\n")
    client = _mock_client(post_multipart={"id": "cr-10"})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "upload-companion", str(f)])
    assert result.exit_code == 0, result.output
    client.post_multipart.assert_called_once_with(
        "/api/creatives/upload-companion", str(f)
    )


def test_creatives_compress_image(authenticated_config, tmp_path):
    f = tmp_path / "img.jpg"
    f.write_bytes(b"\xff\xd8\xff")
    client = _mock_client(post_multipart={"size": 1234})
    with patch("orbiads_cli.commands.creatives.get_client", return_value=client):
        result = runner.invoke(app, ["creatives", "compress-image", str(f)])
    assert result.exit_code == 0, result.output
    client.post_multipart.assert_called_once_with(
        "/api/creatives/compress-image", str(f)
    )


# === licas (5 verbs) ======================================================


def test_licas_list_by_line_item(authenticated_config):
    client = _mock_client(get={"licas": [{"id": "x", "lineItemId": "li-1"}]})
    with patch("orbiads_cli.commands.licas.get_client", return_value=client):
        result = runner.invoke(app, ["licas", "list-by-line-item", "li-1"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/line-items/li-1/licas")


def test_licas_batch(authenticated_config, tmp_path):
    client = _mock_client(post={"li-1": []})
    f = _write_json(tmp_path, {"lineItemIds": ["li-1", "li-2"]})
    with patch("orbiads_cli.commands.licas.get_client", return_value=client):
        result = runner.invoke(app, ["licas", "batch", "--file", f])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/licas/batch", json={"lineItemIds": ["li-1", "li-2"]}
    )


def test_licas_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"updates": {"weight": 50}})
    with patch("orbiads_cli.commands.licas.get_client", return_value=client):
        result = runner.invoke(
            app, ["licas", "update", "li-1", "cr-1", "--file", f]
        )
    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/licas/li-1/cr-1", json={"updates": {"weight": 50}}
    )


def test_licas_deactivate(authenticated_config):
    client = _mock_client(post={"status": "INACTIVE"})
    with patch("orbiads_cli.commands.licas.get_client", return_value=client):
        result = runner.invoke(
            app, ["licas", "deactivate", "li-1", "cr-1", "--yes"]
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/licas/li-1/cr-1/deactivate")


def test_licas_delete(authenticated_config, tmp_path):
    client = _mock_client(post={"deactivated": 2})
    f = _write_json(tmp_path, {"lineItemId": "li-1", "creativeIds": ["cr-1", "cr-2"]})
    with patch("orbiads_cli.commands.licas.get_client", return_value=client):
        result = runner.invoke(
            app, ["licas", "delete", "--file", f, "--yes"]
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/licas/delete",
        json={"lineItemId": "li-1", "creativeIds": ["cr-1", "cr-2"]},
    )


# === native-styles (5 verbs) ==============================================


def test_native_styles_list(authenticated_config):
    client = _mock_client(get={"items": [{"id": "ns-1"}], "total": 1})
    with patch("orbiads_cli.commands.native_styles.get_client", return_value=client):
        result = runner.invoke(app, ["native-styles", "list"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/native-styles", params={"limit": 500, "offset": 0}
    )


def test_native_styles_list_with_filter(authenticated_config):
    client = _mock_client(get={"items": []})
    with patch("orbiads_cli.commands.native_styles.get_client", return_value=client):
        result = runner.invoke(
            app, ["native-styles", "list", "--name-filter", "promo"]
        )
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/native-styles",
        params={"limit": 500, "offset": 0, "nameFilter": "promo"},
    )


def test_native_styles_get(authenticated_config):
    client = _mock_client(get={"id": "ns-1", "name": "X"})
    with patch("orbiads_cli.commands.native_styles.get_client", return_value=client):
        result = runner.invoke(app, ["native-styles", "get", "ns-1"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/native-styles/ns-1")


def test_native_styles_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"name": "Renamed"})
    with patch("orbiads_cli.commands.native_styles.get_client", return_value=client):
        result = runner.invoke(
            app, ["native-styles", "update", "ns-1", "--file", f]
        )
    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/native-styles/ns-1", json={"name": "Renamed"}
    )


def test_native_styles_duplicate(authenticated_config):
    client = _mock_client(post={"id": "ns-2"})
    with patch("orbiads_cli.commands.native_styles.get_client", return_value=client):
        result = runner.invoke(
            app, ["native-styles", "duplicate", "ns-1", "--yes"]
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/native-styles/ns-1/duplicate")


def test_native_styles_archive(authenticated_config):
    client = _mock_client(post={"archived": True})
    with patch("orbiads_cli.commands.native_styles.get_client", return_value=client):
        result = runner.invoke(
            app, ["native-styles", "archive", "ns-1", "--yes"]
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/native-styles/ns-1/archive")


# === creative-templates (3 verbs) =========================================


def test_creative_templates_list(authenticated_config):
    client = _mock_client(get={"items": [{"id": "tpl-1"}], "total": 1})
    with patch(
        "orbiads_cli.commands.creative_templates.get_client", return_value=client
    ):
        result = runner.invoke(app, ["creative-templates", "list"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/creative-templates", params={"limit": 500, "offset": 0}
    )


def test_creative_templates_get(authenticated_config):
    client = _mock_client(get={"id": "tpl-1", "name": "X"})
    with patch(
        "orbiads_cli.commands.creative_templates.get_client", return_value=client
    ):
        result = runner.invoke(app, ["creative-templates", "get", "tpl-1"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/creative-templates/tpl-1")


def test_creative_templates_ensure_classic_native(authenticated_config, tmp_path):
    client = _mock_client(post={"templateId": "tpl-1"})
    f = _write_json(tmp_path, {"templateId": "tpl-1"})
    with patch(
        "orbiads_cli.commands.creative_templates.get_client", return_value=client
    ):
        result = runner.invoke(
            app, ["creative-templates", "ensure-classic-native", "--file", f]
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/creative-templates/classic-native/ensure",
        json={"templateId": "tpl-1"},
    )
