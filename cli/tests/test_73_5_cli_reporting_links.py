"""Story 73.5 CLI wrappers for reporting templates, links, and GAM reports."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()


def _mock_client(**ret):
    client = MagicMock()
    for method in ("get", "post", "put", "patch", "delete"):
        getattr(client, method).return_value = ret.get(method, {"ok": True})
    return client


def _write_json(tmp_path, payload):
    path = tmp_path / "payload.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


@pytest.mark.parametrize(
    ("command_args", "method", "expected_path", "expected_kwargs", "payload"),
    [
        (
            ["reporting", "templates", "get", "tmpl-42"],
            "get",
            "/api/gam/reports/templates/tmpl-42",
            {},
            None,
        ),
        (
            ["reporting", "templates", "favorite", "tmpl-42"],
            "post",
            "/api/gam/reports/templates/tmpl-42/favorite",
            {},
            None,
        ),
        (
            ["reporting", "links", "list"],
            "get",
            "/api/gam/reports/links",
            {},
            None,
        ),
        (
            ["reporting", "links", "sync", "lnk-1"],
            "patch",
            "/api/gam/reports/links/lnk-1/sync",
            {"json": {}},
            None,
        ),
        (
            ["reporting", "links", "resolve", "lnk-1", "--directive", "applyTemplate"],
            "patch",
            "/api/gam/reports/links/lnk-1/resolve",
            {"json": {"directive": "applyTemplate"}},
            None,
        ),
        (
            ["reporting", "links", "diff", "lnk-1"],
            "get",
            "/api/gam/reports/links/lnk-1/diff",
            {},
            None,
        ),
        (
            ["reporting", "links", "delete", "lnk-1", "--yes"],
            "delete",
            "/api/gam/reports/links/lnk-1",
            {},
            None,
        ),
        (
            ["reporting", "gam-reports", "link", "gr-1", "--file", "{file}"],
            "post",
            "/api/gam/reports/gam-reports/gr-1/link",
            {"json": {"templateId": "tmpl-42", "linkMode": "manual"}},
            {"templateId": "tmpl-42", "linkMode": "manual"},
        ),
        (
            [
                "reporting",
                "gam-reports",
                "clone-to-template",
                "gr-1",
                "--file",
                "{file}",
            ],
            "post",
            "/api/gam/reports/gam-reports/gr-1/clone-to-template",
            {"json": {"templateName": "Q2 Cloned"}},
            {"templateName": "Q2 Cloned"},
        ),
        (
            ["reporting", "gam-reports", "open-url", "gr-1"],
            "get",
            "/api/gam/reports/gam-reports/gr-1/open-url",
            {},
            None,
        ),
    ],
)
def test_story_73_5_reporting_wrappers_call_expected_routes(
    authenticated_config,
    tmp_path,
    command_args,
    method,
    expected_path,
    expected_kwargs,
    payload,
):
    client = _mock_client(
        get={"ok": True, "links": [], "url": "https://admanager.google.com/report"},
        post={"ok": True, "isFavorite": True},
        patch={"ok": True},
        delete={"ok": True},
    )
    if payload is not None:
        file_path = _write_json(tmp_path, payload)
        command_args = [file_path if arg == "{file}" else arg for arg in command_args]

    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["--json", *command_args])

    assert result.exit_code == 0, result.output
    mocked_method = getattr(client, method)
    mocked_method.assert_called_once()
    call_args, call_kwargs = mocked_method.call_args
    assert call_args == (expected_path,)
    assert call_kwargs == expected_kwargs


def test_links_resolve_forwards_apply_template_directive(authenticated_config):
    client = _mock_client(patch={"ok": True})

    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "--json",
                "reporting",
                "links",
                "resolve",
                "lnk-1",
                "--directive",
                "applyTemplate",
            ],
        )

    assert result.exit_code == 0, result.output
    client.patch.assert_called_once_with(
        "/api/gam/reports/links/lnk-1/resolve",
        json={"directive": "applyTemplate"},
    )


def test_links_delete_yes_passes_effective_confirmation_context(authenticated_config):
    client = _mock_client(delete={"ok": True})

    with (
        patch("orbiads_cli.commands.reporting.get_client", return_value=client),
        patch("orbiads_cli.commands.reporting.confirm", return_value=True) as confirm_mock,
    ):
        result = runner.invoke(
            app,
            ["reporting", "links", "delete", "lnk-1", "--yes"],
        )

    assert result.exit_code == 0, result.output
    confirm_mock.assert_called_once()
    _, effective_ctx = confirm_mock.call_args.args
    assert effective_ctx.yes is True
    client.delete.assert_called_once_with("/api/gam/reports/links/lnk-1")


def test_gam_reports_link_invalid_json_exits_2(authenticated_config, tmp_path):
    payload_path = tmp_path / "bad.json"
    payload_path.write_text("{not json", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "reporting",
            "gam-reports",
            "link",
            "gr-1",
            "--file",
            str(payload_path),
        ],
    )

    assert result.exit_code == 2
    assert "invalid JSON" in result.output
