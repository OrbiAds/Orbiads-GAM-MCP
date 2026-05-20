"""Story 62.3 — CLI wrappers for advanced line-item Tier B routes."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    c = MagicMock()
    for k in ("get", "post", "patch", "delete"):
        getattr(c, k).return_value = ret.get(k)
    return c


def test_line_items_get(authenticated_config):
    client = _mock_client(get={"id": "li-1", "status": "DRAFT"})
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(app, ["line-items", "get", "li-1"])
    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/line-items/li-1")


def test_line_items_approve(authenticated_config):
    client = _mock_client(post={"approved": True})
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(app, ["line-items", "approve", "li-1", "--yes"])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/gam/line-items/li-1/approve")


def test_line_items_list_by_order(authenticated_config):
    client = _mock_client(get={"lineItems": [{"id": "li-1", "name": "X"}]})
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(app, ["line-items", "list-by-order", "o-1"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/orders/o-1/line-items", params={"limit": 50, "offset": 0}
    )


def test_line_items_private_deals(authenticated_config):
    client = _mock_client(get={"deals": []})
    with patch("orbiads_cli.commands.line_items.get_client", return_value=client):
        result = runner.invoke(app, ["line-items", "private-deals"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/private-deals", params={"limit": 50, "offset": 0}
    )
