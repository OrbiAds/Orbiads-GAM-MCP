"""Story 62.4 — CLI wrappers for advertisers/orders/contacts/users/roles Tier B."""

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
    return c


def _write_json(tmp_path, payload):
    f = tmp_path / "p.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


# advertisers (6) ─────────────────────────────────────────────────────────


def test_advertisers_get(authenticated_config):
    client = _mock_client(get={"id": "adv-1", "name": "Acme"})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(app, ["advertisers", "get", "adv-1"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/advertisers/adv-1")


def test_advertisers_find(authenticated_config):
    client = _mock_client(get={"id": "adv-1"})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(app, ["advertisers", "find", "--name", "Acme"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/advertisers/search", params={"name": "Acme"}
    )


def test_advertisers_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"name": "Renamed"})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(app, ["advertisers", "update", "adv-1", "--file", f])
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/advertisers/adv-1", json={"name": "Renamed"}
    )


def test_advertisers_rich_media_list(authenticated_config):
    client = _mock_client(get={"richMediaCompanies": [{"id": "1", "displayName": "Celtra"}]})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(
            app, ["advertisers", "rich-media-list", "--verified", "--page-size", "25"]
        )
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/companies/rich-media",
        params={"verifiedOnly": True, "pageSize": 25},
    )


def test_advertisers_rich_media_get(authenticated_config):
    client = _mock_client(get={"id": "1", "displayName": "Celtra"})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(app, ["advertisers", "rich-media-get", "1"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/companies/rich-media/1")


def test_advertisers_agencies_list(authenticated_config):
    client = _mock_client(get={"agencies": [{"id": "ag-1"}]})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(app, ["advertisers", "agencies", "list"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/agencies")


def test_advertisers_agencies_create(authenticated_config):
    client = _mock_client(post={"id": "ag-1", "name": "Publicis"})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(
            app, ["advertisers", "agencies", "create", "--name", "Publicis"]
        )
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/gam/agencies", json={"name": "Publicis"})


def test_advertisers_agencies_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"name": "Renamed Agency"})
    with patch("orbiads_cli.commands.advertisers.get_client", return_value=client):
        result = runner.invoke(
            app, ["advertisers", "agencies", "update", "ag-1", "--file", f]
        )
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/agencies/ag-1", json={"name": "Renamed Agency"}
    )


# orders (2) ──────────────────────────────────────────────────────────────


def test_orders_archive(authenticated_config):
    client = _mock_client(post={"archived": True})
    with patch("orbiads_cli.commands.orders.get_client", return_value=client):
        result = runner.invoke(app, ["orders", "archive", "o1", "--yes"])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/gam/orders/o1/archive")


def test_orders_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"notes": "Updated"})
    with patch("orbiads_cli.commands.orders.get_client", return_value=client):
        result = runner.invoke(app, ["orders", "update", "o1", "--file", f])
    assert result.exit_code == 0
    client.patch.assert_called_once_with("/api/gam/orders/o1", json={"notes": "Updated"})


# contacts (3) ────────────────────────────────────────────────────────────


def test_contacts_list(authenticated_config):
    client = _mock_client(get={"contacts": []})
    with patch("orbiads_cli.commands.contacts.get_client", return_value=client):
        result = runner.invoke(app, ["contacts", "list"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/contacts", params={})


def test_contacts_list_filtered(authenticated_config):
    client = _mock_client(get={"contacts": []})
    with patch("orbiads_cli.commands.contacts.get_client", return_value=client):
        result = runner.invoke(app, ["contacts", "list", "--company-id", "adv-1"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/contacts", params={"companyId": "adv-1"}
    )


def test_contacts_create(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "ct-1"})
    f = _write_json(tmp_path, {"name": "Jane", "email": "j@x.com", "companyId": 42})
    with patch("orbiads_cli.commands.contacts.get_client", return_value=client):
        result = runner.invoke(app, ["contacts", "create", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/contacts",
        json={"name": "Jane", "email": "j@x.com", "companyId": 42},
    )


def test_contacts_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"title": "VP Marketing"})
    with patch("orbiads_cli.commands.contacts.get_client", return_value=client):
        result = runner.invoke(app, ["contacts", "update", "ct-1", "--file", f])
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/contacts/ct-1", json={"title": "VP Marketing"}
    )


# users + roles (2) ────────────────────────────────────────────────────────


def test_users_list(authenticated_config):
    client = _mock_client(get={"users": []})
    with patch("orbiads_cli.commands.users.get_client", return_value=client):
        result = runner.invoke(app, ["users", "list"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/users", params={"limit": 200, "offset": 0}
    )


def test_roles_list(authenticated_config):
    client = _mock_client(get={"roles": []})
    with patch("orbiads_cli.commands.roles.get_client", return_value=client):
        result = runner.invoke(app, ["roles", "list"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/roles")
