"""Stories 62.5 + 62.6 — CLI wrappers tests.

Covers:
  - creative-qa (7 verbs)            — Story 62.6
  - custom-targeting-values (4)      — Story 62.5
  - audiences get/create/update/action — Story 62.5 (audiences.py extension)
  - inventory residual + search/sizes  — Story 62.5 (inventory.py extension)
  - network update                   — Story 62.5
  - pql query                        — Story 62.5
  - preview coverage                 — Story 62.5
"""

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


# ── creative-qa (Story 62.6) ─────────────────────────────────────────────

CREATIVE_QA_GET_CASES = [
    (["creative-qa", "validate-ssl", "cr-1"], "/api/gam/creative-qa/creatives/cr-1/ssl",
     {"followRedirects": "false"}),
    (["creative-qa", "audit-tracking", "cr-1"], "/api/gam/creative-qa/creatives/cr-1/tracking", None),
    (["creative-qa", "audit-order-tracking", "o-1"], "/api/gam/creative-qa/orders/o-1/tracking", None),
]


@pytest.mark.parametrize("argv,path,params", CREATIVE_QA_GET_CASES)
def test_creative_qa_get_verbs(authenticated_config, argv, path, params):
    client = _mock_client(get={"ok": True})
    with patch("orbiads_cli.commands.creative_qa.get_client", return_value=client):
        result = runner.invoke(app, argv)
    assert result.exit_code == 0, result.output
    if params is None:
        client.get.assert_called_once_with(path)
    else:
        client.get.assert_called_once_with(path, params=params)


CREATIVE_QA_POST_CASES = [
    (["creative-qa", "scan-compliance"],     "/api/gam/creative-qa/scan-compliance"),
    (["creative-qa", "validate-ssl-batch"],  "/api/gam/creative-qa/validate-ssl-batch"),
    (["creative-qa", "validate-tag"],        "/api/gam/creative-qa/validate-tag"),
    (["creative-qa", "pre-archive-check"],   "/api/gam/creative-qa/pre-archive-check"),
]


@pytest.mark.parametrize("argv,path", CREATIVE_QA_POST_CASES)
def test_creative_qa_post_verbs(authenticated_config, tmp_path, argv, path):
    client = _mock_client(post={"ok": True})
    f = _write_json(tmp_path, {"x": 1})
    with patch("orbiads_cli.commands.creative_qa.get_client", return_value=client):
        result = runner.invoke(app, argv + ["--file", f])
    assert result.exit_code == 0, result.output
    client.post.assert_called_once_with(path, json={"x": 1})


# ── custom-targeting-values (Story 62.5) ──────────────────────────────────


def test_ctv_list(authenticated_config):
    client = _mock_client(get={"values": []})
    with patch("orbiads_cli.commands.custom_targeting_values.get_client", return_value=client):
        result = runner.invoke(app, ["custom-targeting-values", "list", "--key-id", "k1"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/custom-targeting-values", params={"limit": 50, "keyId": "k1"}
    )


def test_ctv_create(authenticated_config, tmp_path):
    client = _mock_client(post={"created": 2})
    f = _write_json(tmp_path, {"values": [{"name": "v1"}, {"name": "v2"}]})
    with patch("orbiads_cli.commands.custom_targeting_values.get_client", return_value=client):
        result = runner.invoke(
            app, ["custom-targeting-values", "create", "k1", "--file", f]
        )
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/custom-targeting-keys/k1/values",
        json={"values": [{"name": "v1"}, {"name": "v2"}]},
    )


def test_ctv_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"displayName": "New"})
    with patch("orbiads_cli.commands.custom_targeting_values.get_client", return_value=client):
        result = runner.invoke(
            app, ["custom-targeting-values", "update", "v1", "--file", f]
        )
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/custom-targeting-values/v1", json={"displayName": "New"}
    )


def test_ctv_action(authenticated_config, tmp_path):
    client = _mock_client(post={"affected": 3})
    f = _write_json(tmp_path, {"valueIds": ["v1", "v2"], "action": "ACTIVATE"})
    with patch("orbiads_cli.commands.custom_targeting_values.get_client", return_value=client):
        result = runner.invoke(app, ["custom-targeting-values", "action", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/custom-targeting-values/action",
        json={"valueIds": ["v1", "v2"], "action": "ACTIVATE"},
    )


# ── audiences CRUD (Story 62.5 extension) ────────────────────────────────


def test_audiences_get(authenticated_config):
    client = _mock_client(get={"id": "s1"})
    with patch("orbiads_cli.commands.audiences.get_client", return_value=client):
        result = runner.invoke(app, ["audiences", "get", "s1"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/audience-segments/s1")


def test_audiences_create(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "s1"})
    f = _write_json(tmp_path, {"name": "Seg1"})
    with patch("orbiads_cli.commands.audiences.get_client", return_value=client):
        result = runner.invoke(app, ["audiences", "create", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with("/api/gam/audience-segments", json={"name": "Seg1"})


def test_audiences_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"description": "..."})
    with patch("orbiads_cli.commands.audiences.get_client", return_value=client):
        result = runner.invoke(app, ["audiences", "update", "s1", "--file", f])
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/audience-segments/s1", json={"description": "..."}
    )


def test_audiences_action(authenticated_config, tmp_path):
    client = _mock_client(post={"affected": 2})
    f = _write_json(tmp_path, {"segmentIds": ["s1", "s2"], "action": "DEACTIVATE"})
    with patch("orbiads_cli.commands.audiences.get_client", return_value=client):
        result = runner.invoke(app, ["audiences", "action", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/audience-segments/action",
        json={"segmentIds": ["s1", "s2"], "action": "DEACTIVATE"},
    )


# ── inventory residual + search/sizes (Story 62.5) ────────────────────────


def test_inv_placement_create(authenticated_config, tmp_path):
    client = _mock_client(post={"id": "p1"})
    f = _write_json(tmp_path, {"name": "P1", "adUnitIds": [1, 2]})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "placement-create", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/placements", json={"name": "P1", "adUnitIds": [1, 2]}
    )


def test_inv_search_ad_units(authenticated_config):
    client = _mock_client(get={"results": []})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "search-ad-units", "--query", "home"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/ad-units/search", params={"q": "home", "limit": 50, "offset": 0}
    )


def test_inv_ad_units_by_ids(authenticated_config, tmp_path):
    client = _mock_client(post={"items": []})
    f = _write_json(tmp_path, {"adUnitIds": ["a1", "a2"]})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "ad-units-by-ids", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/ad-units/by-ids", json={"adUnitIds": ["a1", "a2"]}
    )


def test_inv_sizes(authenticated_config):
    client = _mock_client(get={"sizes": []})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "sizes"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/ad-units/sizes")


def test_inv_search_custom_targeting(authenticated_config):
    client = _mock_client(get={"results": []})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "search-custom-targeting", "--query", "geo"])
    assert result.exit_code == 0
    client.get.assert_called_once_with(
        "/api/gam/custom-targeting/search", params={"q": "geo"}
    )


def test_inv_languages(authenticated_config):
    client = _mock_client(get={"languages": []})
    with patch("orbiads_cli.commands.inventory.get_client", return_value=client):
        result = runner.invoke(app, ["inventory", "languages"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/languages", params={"limit": 50})


# ── network update (Story 62.5) ──────────────────────────────────────────


def test_network_update(authenticated_config, tmp_path):
    client = _mock_client(patch={"updated": True})
    f = _write_json(tmp_path, {"displayName": "Renamed"})
    with patch("orbiads_cli.commands.network.get_client", return_value=client):
        result = runner.invoke(app, ["network", "update", "--file", f])
    assert result.exit_code == 0
    client.patch.assert_called_once_with(
        "/api/gam/network", json={"displayName": "Renamed"}
    )


# ── pql + preview coverage (Story 62.5) ──────────────────────────────────


def test_pql_query(authenticated_config):
    client = _mock_client(post={"rows": []})
    with patch("orbiads_cli.commands.pql.get_client", return_value=client):
        result = runner.invoke(app, ["pql", "query", "SELECT * FROM Order_"])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/pql", json={"query": "SELECT * FROM Order_"}
    )


def test_preview_coverage(authenticated_config, tmp_path):
    client = _mock_client(post={"covered": 5})
    f = _write_json(tmp_path, {"adUnitIds": [1, 2], "lineItemIds": [10]})
    with patch("orbiads_cli.commands.preview.get_client", return_value=client):
        result = runner.invoke(app, ["preview", "coverage", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/coverage",
        json={"adUnitIds": [1, 2], "lineItemIds": [10]},
    )


# ── reporting 62.2 extensions ────────────────────────────────────────────


def test_reporting_ga4_dimensions(authenticated_config):
    client = _mock_client(get={"dimensions": []})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "ga4", "dimensions"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/reports/ga4/dimensions")


def test_reporting_ga4_metrics(authenticated_config):
    client = _mock_client(get={"metrics": []})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "ga4", "metrics"])
    assert result.exit_code == 0
    client.get.assert_called_once_with("/api/gam/reports/ga4/metrics")


def test_reporting_ga4_run(authenticated_config, tmp_path):
    client = _mock_client(post={"rows": []})
    f = _write_json(tmp_path, {"propertyId": "123"})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "ga4", "run", "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(
        "/api/gam/reports/ga4/run", json={"propertyId": "123"}
    )


@pytest.mark.parametrize("verb,path", [
    ("standalone",  "/api/gam/reports/forecast/standalone"),
    ("prospective", "/api/gam/reports/forecast/prospective"),
    ("traffic",     "/api/gam/reports/forecast/traffic"),
])
def test_reporting_forecast(authenticated_config, tmp_path, verb, path):
    client = _mock_client(post={"ok": True})
    f = _write_json(tmp_path, {"x": 1})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "forecast", verb, "--file", f])
    assert result.exit_code == 0
    client.post.assert_called_once_with(path, json={"x": 1})


def test_reporting_gam_reports_delete(authenticated_config):
    client = _mock_client(delete={"ok": True})
    with patch("orbiads_cli.commands.reporting.get_client", return_value=client):
        result = runner.invoke(app, ["reporting", "gam-reports", "delete", "g1"])
    assert result.exit_code == 0
    client.delete.assert_called_once_with("/api/gam/reports/gam-reports/g1")
