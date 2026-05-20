"""Story 61.6 — inventory/targeting/placements sweep tests."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    c = MagicMock()
    c.get.return_value = ret.get("get")
    c.post.return_value = ret.get("post")
    c.patch.return_value = ret.get("patch")
    c.delete.return_value = ret.get("delete")
    return c


def _write_json(tmp_path, payload):
    f = tmp_path / "p.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


# GET / DELETE catalogue verbs (no body)
GET_DELETE = [
    (["inventory", "ads-json"],                  "get",    "/api/gam/inventory/manifest/ads.json"),
    (["inventory", "countries"],                 "get",    "/api/gam/geo-targets"),
    (["inventory", "device-categories"],         "get",    "/api/gam/device-categories"),
    (["inventory", "archive-ad-unit", "au1"],    "delete", "/api/gam/ad-units/au1"),
    (["inventory", "delete-key", "k1"],          "delete", "/api/gam/custom-targeting-keys/k1"),
    (["inventory", "placement-archive", "p1"],   "delete", "/api/gam/placements/p1"),
]


@pytest.mark.parametrize("argv,method,path", GET_DELETE)
def test_inventory_get_delete_verbs(authenticated_config, argv, method, path):
    client = _mock_client(**{method: {"ok": True}})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, argv)
    assert result.exit_code == 0, result.output
    getattr(client, method).assert_called_once_with(path)


# POST verbs with --file body
POST_WITH_FILE = [
    (["inventory", "create-ad-units"],           "/api/gam/ad-units/save-adunits"),
    (["inventory", "audit"],                     "/api/gam/inventory/audit"),
    (["inventory", "blueprint-generate"],        "/api/gam/blueprint/generate"),
    (["inventory", "blueprint-push"],            "/api/gam/blueprint/push"),
    (["inventory", "validate-fluid"],            "/api/gam/ad-units/validate-fluid"),
    (["inventory", "forecast"],                  "/api/gam/inventory/forecast"),
    (["inventory", "create-key"],                "/api/gam/custom-targeting-keys"),
]


@pytest.mark.parametrize("argv_base,path", POST_WITH_FILE)
def test_inventory_post_with_file(authenticated_config, tmp_path, argv_base, path):
    client = _mock_client(post={"ok": True})
    f = _write_json(tmp_path, {"x": 1})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, argv_base + ["--file", f])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(path, json={"x": 1})


# PATCH verbs (positional id + --file)
def test_update_ad_unit_patches(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"name": "renamed"})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(
            app, ["inventory", "update-ad-unit", "au1", "--file", f]
        )
    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with("/api/gam/ad-units/au1", json={"name": "renamed"})


def test_update_key_patches(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"displayName": "New"})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "update-key", "k1", "--file", f])
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/custom-targeting-keys/k1", json={"displayName": "New"}
    )


def test_placement_update_patches(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"description": "Updated"})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(
            app, ["inventory", "placement-update", "p1", "--file", f]
        )
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/placements/p1", json={"description": "Updated"}
    )


def test_audit_without_file_posts_empty_body(authenticated_config):
    client = _mock_client(post={"audited": True})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "audit"])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/gam/inventory/audit", json={})
