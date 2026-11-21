"""Story 116-10b - CLI two-step flow for discard-drafts, reserve --allow-overbook and ad-break
delete, plus the clear error against a backend older than the CLI (116-10a audit follow-up).

HTTP is mocked at the client boundary. Contract: dryRun -> {preview, confirmationToken} -> same
payload + confirmationToken; ``--yes`` skips only the human prompt.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest
from typer.testing import CliRunner

from orbiads_cli.client import CliApiError, OrbiAdsClient
from orbiads_cli.guarded import run_guarded_post
from orbiads_cli.main import app

runner = CliRunner()

PREVIEW = {
    "dryRun": True,
    "preview": [
        {
            "operation": "deals.discard_proposal_drafts",
            "proposal_ids": ["10"],
            "irreversible": True,
            "warning": "IRREVERSIBLE: throws away the local edits",
        }
    ],
    "confirmationToken": "tok-1",
    "estimatedCost": 0.0,
}


def _client(result=None):
    client = MagicMock()

    def _post(path, json=None, **_):
        return PREVIEW if json.get("dryRun") else (result or {"numChanges": 1})

    client.post.side_effect = _post
    return client


def _run(module, args, client):
    with patch(f"orbiads_cli.commands.{module}.get_client", return_value=client):
        return runner.invoke(app, args)


def _bodies(client):
    return [c.kwargs["json"] for c in client.post.call_args_list]


def test_discard_drafts_previews_then_confirms_with_the_token():
    client = _client()

    result = _run(
        "programmatic", ["programmatic", "proposals", "discard-drafts", "10", "--yes"], client
    )

    assert result.exit_code == 0, result.output
    assert _bodies(client) == [
        {"proposalIds": ["10"], "dryRun": True},
        {"proposalIds": ["10"], "confirmationToken": "tok-1"},
    ]
    assert "IRREVERSIBLE" in result.output  # the preview is shown (stderr mixed by CliRunner)


def test_declining_discard_drafts_never_sends_the_token():
    client = _client()
    with patch("orbiads_cli.commands.programmatic.confirm", return_value=False):
        result = _run("programmatic", ["programmatic", "proposals", "discard-drafts", "10"], client)

    assert result.exit_code == 0
    assert _bodies(client) == [{"proposalIds": ["10"], "dryRun": True}]


def test_reserve_without_overbook_stays_one_call():
    client = MagicMock()
    client.post.return_value = {"numChanges": 1}

    result = _run(
        "programmatic", ["programmatic", "proposal-line-items", "reserve", "7", "--yes"], client
    )

    assert result.exit_code == 0, result.output
    assert _bodies(client) == [{"pliIds": ["7"]}]


def test_reserve_without_overbook_falls_back_to_two_step_when_the_server_requires_it():
    client = MagicMock()
    calls = []

    def _post(path, json=None, **_):
        calls.append(json)
        if "dryRun" in json:
            return {"dryRun": True, "confirmationToken": "t", "preview": []}
        if "confirmationToken" in json:
            return {"numChanges": 1}
        raise CliApiError(1, "needs confirmation", "CONFIRMATION_REQUIRED")

    client.post.side_effect = _post
    result = _run(
        "programmatic", ["programmatic", "proposal-line-items", "reserve", "7", "--yes"], client
    )

    assert result.exit_code == 0, result.output
    assert calls == [
        {"pliIds": ["7"]},
        {"pliIds": ["7"], "dryRun": True},
        {"pliIds": ["7"], "confirmationToken": "t"},
    ]


def test_ad_break_delete_uses_the_post_delete_route_two_step():
    client = _client({"deleted": True})

    result = _run(
        "live_stream", ["live-stream", "delete", "9", "--asset-key", "ak", "--yes"], client
    )

    assert result.exit_code == 0, result.output
    assert {c.args[0] for c in client.post.call_args_list} == {
        "/api/gam/live-stream/ad-breaks/9/delete"
    }
    assert _bodies(client) == [
        {"assetKey": "ak", "area": "asset_key", "dryRun": True},
        {"assetKey": "ak", "area": "asset_key", "confirmationToken": "tok-1"},
    ]
    client.delete.assert_not_called()


# --------------------------------------------------------------------------- #
# Backend older than the CLI: clear message instead of "Request validation failed"
# --------------------------------------------------------------------------- #


def _old_backend_422(field):
    return CliApiError(
        1,
        "Request validation failed",
        "VALIDATION_ERROR",
        {"fields": [{"field": field, "type": "extra_forbidden"}]},
    )


@pytest.mark.parametrize("field", ["dryRun", "confirmationToken"])
def test_extra_forbidden_two_step_field_means_the_server_is_older_than_the_cli(field):
    def post(body):
        raise _old_backend_422(field)

    with pytest.raises(CliApiError) as exc:
        run_guarded_post(
            post, {"x": 1}, ctx=MagicMock(), prompt="?", confirm_fn=lambda *_: True, two_step=True
        )

    assert exc.value.error_code == "SERVER_OLDER_THAN_CLI"
    assert "older than this CLI" in exc.value.message and "backend" in exc.value.message
    assert "Request validation failed" not in exc.value.message


def test_other_validation_errors_are_not_rewritten():
    def post(body):
        raise CliApiError(
            1,
            "Request validation failed",
            "VALIDATION_ERROR",
            {"fields": [{"field": "orderIds", "type": "missing"}]},
        )

    with pytest.raises(CliApiError) as exc:
        run_guarded_post(
            post, {"x": 1}, ctx=MagicMock(), prompt="?", confirm_fn=lambda *_: True, two_step=True
        )

    assert exc.value.error_code == "VALIDATION_ERROR"


def test_client_keeps_the_validation_fields_of_a_422():
    """The backend validation handler puts ``fields`` next to ``code`` / ``message``; the
    client must not drop them (the CLI needs ``type: extra_forbidden``)."""
    body = {
        "data": None,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "fields": [{"field": "dryRun", "type": "extra_forbidden"}],
        },
    }

    with pytest.raises(CliApiError) as exc:
        OrbiAdsClient._parse_response(httpx.Response(422, json=body))

    assert exc.value.details["fields"] == [{"field": "dryRun", "type": "extra_forbidden"}]
