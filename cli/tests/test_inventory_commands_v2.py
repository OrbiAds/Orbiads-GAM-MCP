from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client() -> MagicMock:
    client = MagicMock()
    client.get.return_value = {"ok": True}
    client.post.return_value = {"ok": True}
    return client


@pytest.mark.parametrize(
    ("argv", "path", "kwargs"),
    [
        (
            ["inventory", "blueprint", "get", "active", "--version", "v2"],
            "/api/inventory/blueprints/active",
            {"params": {"version": "v2"}},
        ),
        (
            ["inventory", "blueprint", "list-drafts", "active"],
            "/api/inventory/blueprints/active/drafts",
            {},
        ),
        (
            ["inventory", "blueprint", "diff", "active", "--draft-id", "draft-1"],
            "/api/inventory/blueprints/active/diff",
            {"params": {"draftId": "draft-1"}},
        ),
        (
            ["inventory", "catalog", "get", "--network-code", "123"],
            "/api/inventory/catalog",
            {"params": {"networkCode": "123"}},
        ),
        (
            ["inventory", "blocks", "list-versions", "block-1"],
            "/api/inventory/blocks/block-1/versions",
            {},
        ),
        (
            ["inventory", "blocks", "get-version", "block-1", "1.0.0"],
            "/api/inventory/blocks/block-1/versions/1.0.0",
            {},
        ),
        (
            ["inventory", "packages", "list", "active"],
            "/api/inventory/blueprints/active/packages",
            {},
        ),
    ],
)
def test_inventory_v2_get_commands_call_expected_routes(
    authenticated_config,
    argv,
    path,
    kwargs,
) -> None:
    client = _mock_client()

    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["--json", *argv])

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(path, **kwargs)


def test_cli_preview_get_url_posts_session(authenticated_config) -> None:
    client = _mock_client()

    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["--json", "inventory", "preview", "get-url", "active", "news", "home"],
        )

    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/preview/sessions",
        json={"blueprintId": "active", "site": "news", "groupingId": "home"},
    )


def test_inventory_help_lists_v2_groups(authenticated_config) -> None:
    result = runner.invoke(app, ["inventory", "--help"])

    assert result.exit_code == 0
    assert "catalog" in result.output
    assert "blocks" in result.output
    assert "packages" in result.output
    assert "preview" in result.output
