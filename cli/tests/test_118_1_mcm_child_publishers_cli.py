"""Story 118-1 - `orbiads mcm child-publishers list|get|withdraw|renegotiate|resend-invitation`.

HTTP is mocked at the client boundary (``get_client``). The three agreement commands are
two-step: dryRun -> {preview, confirmationToken} -> same payload + confirmationToken.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from orbiads_cli.main import app

runner = CliRunner()

PREVIEW = {
    "dryRun": True,
    "preview": [{"operation": "mcm.withdraw_child_publisher", "company_ids": ["10"]}],
    "confirmationToken": "tok-1",
    "soapAction": "EndAgreementAction",
    "targets": [{"id": "10", "invitationStatus": "ACCEPTED"}],
}


def _client():
    client = MagicMock()

    def _post(path, json=None, **_):
        return PREVIEW if json.get("dryRun") else {"numChanges": 1}

    client.post.side_effect = _post
    return client


def _run(args, client):
    with patch("orbiads_cli.commands.mcm.get_client", return_value=client):
        return runner.invoke(app, args)


def _posts(client):
    return [(c.args[0], c.kwargs["json"]) for c in client.post.call_args_list]


def test_list_sends_the_filters_and_flattens_the_child_publisher(authenticated_config):
    client = MagicMock()
    client.get.return_value = {
        "childPublishers": [
            {
                "id": "10",
                "name": "Child",
                "childPublisher": {
                    "invitationStatus": "PENDING",
                    "childNetworkCode": "123",
                },
            }
        ]
    }

    result = _run(
        [
            "mcm",
            "child-publishers",
            "list",
            "--invitation-status",
            "pending",
            "--account-status",
            "invited",
            "--limit",
            "20",
        ],
        client,
    )

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/mcm/child-publishers",
        params={
            "limit": 20,
            "offset": 0,
            "invitation_status": "PENDING",
            "account_status": "INVITED",
        },
    )
    assert "PENDING" in result.output and "123" in result.output


def test_get_reads_one_child_publisher(authenticated_config):
    client = MagicMock()
    client.get.return_value = {"childPublisher": {"id": "10", "name": "Child"}}

    result = _run(["mcm", "child-publishers", "get", "10"], client)

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with("/api/gam/mcm/child-publishers/10")


def test_withdraw_previews_then_confirms_with_the_token(authenticated_config):
    client = _client()

    result = _run(["mcm", "child-publishers", "withdraw", "10", "--yes"], client)

    assert result.exit_code == 0, result.output
    path = "/api/gam/mcm/child-publishers/withdraw"
    assert _posts(client) == [
        (path, {"companyIds": ["10"], "dryRun": True}),
        (path, {"companyIds": ["10"], "confirmationToken": "tok-1"}),
    ]


def test_declining_withdraw_never_sends_the_token(authenticated_config):
    client = _client()
    with patch("orbiads_cli.commands.mcm.confirm", return_value=False):
        result = _run(["mcm", "child-publishers", "withdraw", "10"], client)

    assert result.exit_code == 0
    assert _posts(client) == [
        (
            "/api/gam/mcm/child-publishers/withdraw",
            {"companyIds": ["10"], "dryRun": True},
        )
    ]


def test_renegotiate_sends_the_proposed_terms(authenticated_config):
    client = _client()

    result = _run(
        [
            "mcm",
            "child-publishers",
            "renegotiate",
            "10",
            "--delegation-type",
            "manage_account",
            "--revenue-share-millipercent",
            "15000",
            "--email",
            "child@example.com",
            "--yes",
        ],
        client,
    )

    assert result.exit_code == 0, result.output
    path, body = _posts(client)[-1]
    assert path == "/api/gam/mcm/child-publishers/renegotiate"
    assert body == {
        "companyIds": ["10"],
        "proposedDelegationType": "MANAGE_ACCOUNT",
        "proposedRevenueShareMillipercent": 15000,
        "proposedEmail": "child@example.com",
        "confirmationToken": "tok-1",
    }


def test_resend_invitation_is_two_step(authenticated_config):
    client = _client()

    result = _run(
        ["mcm", "child-publishers", "resend-invitation", "10", "11", "--yes"], client
    )

    assert result.exit_code == 0, result.output
    assert [p for p, _ in _posts(client)] == [
        "/api/gam/mcm/child-publishers/resend-invitation"
    ] * 2
    assert _posts(client)[0][1] == {"companyIds": ["10", "11"], "dryRun": True}


def test_revenue_share_out_of_range_is_a_usage_error(authenticated_config):
    client = _client()
    result = _run(
        [
            "mcm",
            "child-publishers",
            "renegotiate",
            "10",
            "--revenue-share-millipercent",
            "100001",
        ],
        client,
    )
    assert result.exit_code == 2
    client.post.assert_not_called()


def test_earnings_command_is_unchanged(authenticated_config):
    client = MagicMock()
    client.get.return_value = {"month": 1, "year": 2026, "mcmEarnings": []}

    result = _run(["mcm", "earnings", "--month", "1", "--year", "2026"], client)

    assert result.exit_code == 0, result.output
    client.get.assert_called_once_with(
        "/api/gam/mcm/earnings", params={"month": 1, "year": 2026}
    )
