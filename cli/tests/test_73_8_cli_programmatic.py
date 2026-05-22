"""Story 73.8 CLI wrappers for programmatic deals, auctions, and buyers."""

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


DEAL_PAYLOAD = {
    "privateAuctionId": "auction-1",
    "buyerAccountId": "buyer-1",
    "floorPriceMicros": 2500000,
    "currencyCode": "EUR",
}

DEAL_PATCH = {"floorPriceMicros": 3000000, "currencyCode": "EUR"}

AUCTION_PAYLOAD = {
    "displayName": "Preferred auction",
    "description": "Private marketplace inventory",
}

AUCTION_PATCH = {"displayName": "Updated auction"}


@pytest.mark.parametrize(
    ("command_args", "method", "expected_path", "expected_kwargs", "payload"),
    [
        (
            [
                "programmatic",
                "deals",
                "list",
                "--page-size",
                "50",
                "--filter",
                "status=ACTIVE",
            ],
            "get",
            "/api/gam/pmp-deals",
            {"params": {"pageSize": 50, "filter": "status=ACTIVE"}},
            None,
        ),
        (
            ["programmatic", "deals", "get", "deal-1"],
            "get",
            "/api/gam/pmp-deals/deal-1",
            {},
            None,
        ),
        (
            ["programmatic", "deals", "create", "--file", "{file}"],
            "post",
            "/api/gam/pmp-deals",
            {"json": DEAL_PAYLOAD},
            DEAL_PAYLOAD,
        ),
        (
            ["programmatic", "deals", "update", "deal-1", "--file", "{file}"],
            "patch",
            "/api/gam/pmp-deals/deal-1",
            {"json": DEAL_PATCH},
            DEAL_PATCH,
        ),
        (
            ["programmatic", "auctions", "list"],
            "get",
            "/api/gam/private-auctions",
            {"params": {"pageSize": 200}},
            None,
        ),
        (
            ["programmatic", "auctions", "get", "auction-1"],
            "get",
            "/api/gam/private-auctions/auction-1",
            {},
            None,
        ),
        (
            ["programmatic", "auctions", "create", "--file", "{file}"],
            "post",
            "/api/gam/private-auctions",
            {"json": AUCTION_PAYLOAD},
            AUCTION_PAYLOAD,
        ),
        (
            ["programmatic", "auctions", "update", "auction-1", "--file", "{file}"],
            "patch",
            "/api/gam/private-auctions/auction-1",
            {"json": AUCTION_PATCH},
            AUCTION_PATCH,
        ),
        (
            ["programmatic", "buyers", "list"],
            "get",
            "/api/gam/programmatic-buyers",
            {"params": {"pageSize": 200}},
            None,
        ),
        (
            ["programmatic", "buyers", "get", "buyer-1"],
            "get",
            "/api/gam/programmatic-buyers/buyer-1",
            {},
            None,
        ),
    ],
)
def test_story_73_8_programmatic_wrappers_call_expected_routes(
    authenticated_config,
    tmp_path,
    command_args,
    method,
    expected_path,
    expected_kwargs,
    payload,
):
    client = _mock_client(
        get={
            "privateAuctionDeals": [{"dealId": "deal-1", "displayName": "Deal"}],
            "privateAuctions": [
                {"privateAuctionId": "auction-1", "displayName": "Auction"}
            ],
            "programmaticBuyers": [
                {"accountId": "buyer-1", "displayName": "Buyer"}
            ],
        },
        post={"ok": True},
        patch={"ok": True},
    )
    if payload is not None:
        file_path = _write_json(tmp_path, payload)
        command_args = [file_path if arg == "{file}" else arg for arg in command_args]

    with patch("orbiads_cli.commands.programmatic.get_client", return_value=client):
        result = runner.invoke(app, ["--json", *command_args])

    assert result.exit_code == 0, result.output
    mocked_method = getattr(client, method)
    mocked_method.assert_called_once()
    call_args, call_kwargs = mocked_method.call_args
    assert call_args == (expected_path,)
    assert call_kwargs == expected_kwargs


def test_programmatic_group_is_registered(authenticated_config):
    result = runner.invoke(app, ["programmatic", "--help"])

    assert result.exit_code == 0, result.output
    assert "deals" in result.output
    assert "auctions" in result.output
    assert "buyers" in result.output


def test_auctions_list_rejects_filter(authenticated_config):
    result = runner.invoke(
        app, ["programmatic", "auctions", "list", "--filter", "x=1"]
    )

    assert result.exit_code != 0
    assert "No such option" in result.output


def test_programmatic_create_missing_file_exits_2(authenticated_config, tmp_path):
    missing_path = tmp_path / "missing.json"

    result = runner.invoke(
        app,
        ["programmatic", "deals", "create", "--file", str(missing_path)],
    )

    assert result.exit_code == 2
    assert "file not found" in result.output


def test_programmatic_create_invalid_json_exits_2(authenticated_config, tmp_path):
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text("{not-json", encoding="utf-8")

    result = runner.invoke(
        app,
        ["programmatic", "auctions", "create", "--file", str(invalid_path)],
    )

    assert result.exit_code == 2
    assert "invalid JSON" in result.output
