"""Story 61.5 — reporting setup sweep tests."""

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
    c.put.return_value = ret.get("put")
    c.delete.return_value = ret.get("delete")
    return c


def _write_json(tmp_path, payload):
    f = tmp_path / "p.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return str(f)


# Parameterised matrix: command argv -> (mocked_method, expected_path, [json_payload])
GET_CASES = [
    (["reporting", "dimensions"],                  "get", "/api/gam/reports/available-dimensions", {"params": {"api": "rest"}}),
    (["reporting", "metrics"],                     "get", "/api/gam/reports/available-metrics", {"params": {"api": "rest"}}),
    (["reporting", "dimensions", "--api", "all"], "get", "/api/gam/reports/available-dimensions", {"params": {"api": "all"}}),
    (["reporting", "metrics", "--api", "soap"],   "get", "/api/gam/reports/available-metrics", {"params": {"api": "soap"}}),
]

GET_NO_PARAM_CASES = [
    (["reporting", "date-ranges"],                 "get", "/api/gam/reports/available-date-ranges"),
    (["reporting", "executions"],                  "get", "/api/gam/reports/executions"),
    (["reporting", "delivery-status", "j1"],       "get", "/api/gam/jobs/j1/delivery-status"),
    (["reporting", "delivery-report", "j1"],       "get", "/api/jobs/j1/report"),
    (["reporting", "forecast-line-item", "j1"],    "get", "/api/jobs/j1/forecast"),
    (["reporting", "alerts-underdelivery"],        "get", "/api/campaigns/alerts"),
    (["reporting", "alerts-budget", "c1"],         "get", "/api/campaigns/c1/health-alerts"),
    (["reporting", "templates", "list"],           "get", "/api/gam/reports/templates"),
    (["reporting", "gam-reports", "list"],         "get", "/api/gam/reports/gam-reports"),
    (["reporting", "gam-reports", "get", "g1"],    "get", "/api/gam/reports/gam-reports/g1"),
]

POST_NO_BODY_CASES = [
    (["reporting", "templates", "duplicate", "t1"],                       "post", "/api/gam/reports/templates/t1/clone"),
    (["reporting", "templates", "run", "t1"],                             "post", "/api/gam/reports/templates/t1/run"),
    (["reporting", "gam-reports", "create-from-template", "t1"],          "post", "/api/gam/reports/templates/t1/publish-to-gam"),
    (["reporting", "gam-reports", "update-from-template", "t1"],          "post", "/api/gam/reports/templates/t1/update-in-gam"),
]


@pytest.mark.parametrize("argv,method,path,kwargs", GET_CASES)
def test_reporting_get_verbs_with_params(authenticated_config, argv, method, path, kwargs):
    client = _mock_client(**{method: {"ok": True, "results": [], "templates": [], "gamReports": []}})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, argv)
    assert result.exit_code == 0, result.output
    getattr(client, method).assert_called_once_with(path, **kwargs)


@pytest.mark.parametrize("argv,method,path", GET_NO_PARAM_CASES)
def test_reporting_get_verbs(authenticated_config, argv, method, path):
    client = _mock_client(**{method: {"ok": True, "results": [], "templates": [], "gamReports": []}})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, argv)
    assert result.exit_code == 0, result.output
    getattr(client, method).assert_called_once_with(path)


def test_reporting_catalogue_rejects_invalid_api(authenticated_config):
    result = runner.invoke(app, ["reporting", "dimensions", "--api", "legacy"])
    assert result.exit_code == 2
    assert "--api must be one of" in result.output


@pytest.mark.parametrize("collection_key", ["reports", "items"])
def test_gam_reports_list_accepts_rest_collection_keys(authenticated_config, collection_key):
    client = _mock_client(
        get={
            collection_key: [
                {
                    "reportId": "7040403369",
                    "displayName": "Daily delivery",
                    "dimensions": ["DATE"],
                    "metrics": ["AD_SERVER_IMPRESSIONS"],
                }
            ],
            "total": 1,
        }
    )

    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["--json", "reporting", "gam-reports", "list"])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload[0]["reportId"] == "7040403369"
    client.get.assert_called_once_with("/api/gam/reports/gam-reports")


@pytest.mark.parametrize("argv,method,path", POST_NO_BODY_CASES)
def test_reporting_post_no_body(authenticated_config, argv, method, path):
    client = _mock_client(**{method: {"ok": True}})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, argv)
    assert result.exit_code == 0, result.output
    getattr(client, method).assert_called_once_with(path)


def test_inventory_posts_with_file(authenticated_config, tmp_path):
    client = _mock_client(post={"rows": []})
    f = _write_json(tmp_path, {"dimensions": ["DATE"]})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "inventory", "--file", f])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with("/api/gam/reports/inventory", json={"dimensions": ["DATE"]})


def test_templates_save(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "t1"})
    f = _write_json(tmp_path, {"name": "tpl", "config": {}})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "templates", "save", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/reports/templates", json={"name": "tpl", "config": {}}
    )


def test_templates_update_puts(authenticated_config, tmp_path):
    client = _mock_client(put={"id": "t1", "updated": True})
    f = _write_json(tmp_path, {"name": "renamed"})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "templates", "update", "t1", "--file", f])
    assert result.exit_code == 0
    client.put.assert_called_once_with(
        "/api/gam/reports/templates/t1", json={"name": "renamed"}
    )


def test_templates_delete(authenticated_config):
    client = _mock_client(delete={"ok": True})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "templates", "delete", "t1"])
    assert result.exit_code == 0
    client.delete.assert_called_once_with("/api/gam/reports/templates/t1")
