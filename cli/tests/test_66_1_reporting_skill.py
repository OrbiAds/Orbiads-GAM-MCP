"""CLI tests — `orbiads reporting skill` (Epic 66 Story 66.1).

Verifies the new `reporting skill` verb posts to the right endpoint with
the right body shape. Mocks the HTTP client — no live calls.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app


runner = CliRunner()


def _mock_client(post_ret=None):
    c = MagicMock()
    c.post.return_value = post_ret or {"action": "cancel_run", "cancelRequested": True}
    return c


def _write_json(tmp_path, payload):
    f = tmp_path / "params.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


def test_skill_inline_json_cancel_run(authenticated_config):
    """`--params-json` accepts inline JSON, posts {action, params} to /skill."""
    client = _mock_client(
        post_ret={
            "action": "cancel_run",
            "operationName": "networks/123/operations/reports/runs/456",
            "cancelRequested": True,
        }
    )
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "reporting",
                "skill",
                "--action",
                "cancel_run",
                "--params-json",
                '{"operationName":"networks/123/operations/reports/runs/456"}',
            ],
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(
        "/api/gam/reporting/skill",
        json={
            "action": "cancel_run",
            "params": {"operationName": "networks/123/operations/reports/runs/456"},
        },
    )


def test_skill_params_file_schedule_from_template(authenticated_config, tmp_path):
    """`--params-file` loads params from a JSON file."""
    payload_file = _write_json(
        tmp_path,
        {"templateReportId": "tpl-42", "newDisplayName": "Custom"},
    )
    client = _mock_client(post_ret={"action": "schedule_from_template", "newReportId": "r-99"})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "reporting",
                "skill",
                "--action",
                "schedule_from_template",
                "--params-file",
                payload_file,
            ],
        )
    assert result.exit_code == 0, result.output
    client.post.assert_called_once()
    posted_json = client.post.call_args.kwargs["json"]
    assert posted_json["action"] == "schedule_from_template"
    assert posted_json["params"]["templateReportId"] == "tpl-42"
    assert posted_json["params"]["newDisplayName"] == "Custom"


def test_skill_rejects_both_params_sources(authenticated_config, tmp_path):
    """Mutually exclusive options : providing BOTH --params-file and --params-json
    must error (exit code 2)."""
    payload_file = _write_json(tmp_path, {"foo": "bar"})
    client = _mock_client()
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "reporting",
                "skill",
                "--action",
                "cancel_run",
                "--params-file",
                payload_file,
                "--params-json",
                '{"foo":"bar"}',
            ],
        )
    assert result.exit_code == 2, result.output
    # HTTP client never called when the args are rejected
    client.post.assert_not_called()


def test_skill_rejects_neither_params_source(authenticated_config):
    """Mutually exclusive options : providing NEITHER must also error."""
    client = _mock_client()
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(
            app,
            ["reporting", "skill", "--action", "cancel_run"],
        )
    assert result.exit_code == 2, result.output
    client.post.assert_not_called()


def test_skill_invalid_inline_json_returns_2(authenticated_config):
    """Malformed inline JSON surfaces as exit 2 (caller's responsibility)."""
    client = _mock_client()
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(
            app,
            [
                "reporting",
                "skill",
                "--action",
                "cancel_run",
                "--params-json",
                "{not valid json",
            ],
        )
    assert result.exit_code == 2, result.output
    client.post.assert_not_called()
