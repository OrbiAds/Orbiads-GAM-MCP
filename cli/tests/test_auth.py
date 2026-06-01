"""Tests for CLI auth commands (login, logout, status) — Story 54.7.

Uses typer.testing.CliRunner with mocked httpx calls to avoid real API traffic.
"""

import json
import os
import platform
from unittest.mock import MagicMock, patch

import httpx
import pytest
from typer.testing import CliRunner

from orbiads_cli import __version__, config as config_mod
from orbiads_cli.client import CliApiError
from orbiads_cli.commands.auth import app
from orbiads_cli.main import app as main_app

runner = CliRunner()

# Dummy request for httpx.Response — required so .raise_for_status() works
_DUMMY_REQUEST = httpx.Request("GET", "http://test")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resp(status_code: int, json_data: dict) -> httpx.Response:
    """Create an httpx.Response with a request set (needed for raise_for_status)."""
    return httpx.Response(status_code, json=json_data, request=_DUMMY_REQUEST)


def _device_code_response() -> dict:
    return {
        "data": {
            "deviceCode": "dc-test-123",
            "userCode": "ABC123",
            "verificationUrl": "https://orbiads.com/auth/device?code=ABC123",
            "expiresIn": 900,
            "pollInterval": 0,  # 0 to avoid sleeping in tests
        },
        "error": None,
    }


def _poll_pending() -> httpx.Response:
    return _resp(200, {"data": {"status": "pending"}, "error": None})


def _poll_authorized() -> httpx.Response:
    return _resp(200, {
        "data": {
            "status": "authorized",
            "accessToken": "id-tok-abc",
            "refreshToken": "ref-tok-abc",
        },
        "error": None,
    })


def _poll_authorized_custom_token() -> httpx.Response:
    return _resp(200, {
        "data": {
            "status": "authorized",
            "customToken": "firebase-custom-token",
            "accessToken": None,
            "refreshToken": None,
        },
        "error": None,
    })


def _poll_expired() -> httpx.Response:
    return _resp(200, {"data": {"status": "expired"}, "error": None})


# ===========================================================================
# orbiads auth login
# ===========================================================================


class TestAuthLogin:

    def test_login_success_saves_token(self, tmp_config):
        """Happy path: device-code → pending → authorized → token saved."""
        responses = [_poll_pending(), _poll_authorized()]
        call_idx = {"i": 0}

        def mock_get(url, **kwargs):
            resp = responses[call_idx["i"]]
            call_idx["i"] += 1
            return resp

        with patch("orbiads_cli.commands.auth.httpx.post") as mock_post, \
             patch("orbiads_cli.commands.auth.httpx.get", side_effect=mock_get), \
             patch("orbiads_cli.commands.auth.webbrowser.open"), \
             patch("orbiads_cli.commands.auth.time.sleep"):

            mock_post.return_value = _resp(200, _device_code_response())

            result = runner.invoke(app, ["login"])

        # typer.Exit(code=0) may surface as exit_code 0
        assert result.exit_code == 0
        assert "Authenticated successfully" in result.output

        # Verify token was saved
        cfg = config_mod.load()
        assert cfg is not None
        assert cfg["token"] == "id-tok-abc"
        assert cfg["refreshToken"] == "ref-tok-abc"

    def test_login_success_exchanges_custom_token(self, tmp_config):
        """Current path: device-code returns customToken, CLI exchanges via Firebase."""
        responses = [_poll_pending(), _poll_authorized_custom_token()]
        call_idx = {"i": 0}

        def mock_get(url, **kwargs):
            resp = responses[call_idx["i"]]
            call_idx["i"] += 1
            return resp

        post_responses = [
            _resp(200, _device_code_response()),
            _resp(200, {
                "idToken": "firebase-id-token",
                "refreshToken": "firebase-refresh-token",
            }),
        ]

        with patch("orbiads_cli.commands.auth.httpx.post", side_effect=post_responses) as mock_post, \
             patch("orbiads_cli.commands.auth.httpx.get", side_effect=mock_get), \
             patch("orbiads_cli.commands.auth.webbrowser.open"), \
             patch("orbiads_cli.commands.auth.time.sleep"):

            result = runner.invoke(app, ["login"])

        assert result.exit_code == 0
        assert "Authenticated successfully" in result.output

        cfg = config_mod.load()
        assert cfg is not None
        assert cfg["token"] == "firebase-id-token"
        assert cfg["refreshToken"] == "firebase-refresh-token"
        assert mock_post.call_count == 2
        firebase_call = mock_post.call_args_list[1]
        assert "accounts:signInWithCustomToken" in firebase_call.args[0]
        assert firebase_call.kwargs["headers"] == {"Referer": "https://orbiads.com/"}
        assert firebase_call.kwargs["json"]["token"] == "firebase-custom-token"

    def test_login_expired_exits_4(self, tmp_config):
        """Device code expires → exit code 4."""
        with patch("orbiads_cli.commands.auth.httpx.post") as mock_post, \
             patch("orbiads_cli.commands.auth.httpx.get") as mock_get, \
             patch("orbiads_cli.commands.auth.webbrowser.open"), \
             patch("orbiads_cli.commands.auth.time.sleep"):

            mock_post.return_value = _resp(200, _device_code_response())
            mock_get.return_value = _resp(
                200, {"data": {"status": "expired"}, "error": None},
            )

            result = runner.invoke(app, ["login"])

        assert result.exit_code == 4
        assert "expired" in result.output.lower()

    def test_login_http_error_exits_1(self, tmp_config):
        """HTTP error during device-code request → exit code 1."""
        with patch("orbiads_cli.commands.auth.httpx.post") as mock_post, \
             patch("orbiads_cli.commands.auth.webbrowser.open"):

            mock_post.side_effect = httpx.ConnectError("Connection refused")

            result = runner.invoke(app, ["login"])

        assert result.exit_code == 1
        assert "Failed to initiate login" in result.output

    def test_login_server_error_in_body(self, tmp_config):
        """Server returns an error in the JSend envelope → exit 1."""
        with patch("orbiads_cli.commands.auth.httpx.post") as mock_post, \
             patch("orbiads_cli.commands.auth.webbrowser.open"):

            mock_post.return_value = _resp(200, {
                "data": None,
                "error": {"code": "SOME_ERR", "message": "Something went wrong"},
            })

            result = runner.invoke(app, ["login"])

        assert result.exit_code == 1
        assert "Something went wrong" in result.output

    def test_login_opens_browser(self, tmp_config):
        """Verify webbrowser.open is called with the verification URL."""
        with patch("orbiads_cli.commands.auth.httpx.post") as mock_post, \
             patch("orbiads_cli.commands.auth.httpx.get", return_value=_resp(
                 200, {"data": {"status": "authorized", "accessToken": "t", "refreshToken": "r"}, "error": None}
             )), \
             patch("orbiads_cli.commands.auth.webbrowser.open") as mock_browser, \
             patch("orbiads_cli.commands.auth.time.sleep"):

            mock_post.return_value = _resp(200, _device_code_response())

            runner.invoke(app, ["login"])

        mock_browser.assert_called_once_with(
            "https://orbiads.com/auth/device?code=ABC123"
        )


# ===========================================================================
# orbiads auth logout
# ===========================================================================


class TestAuthLogout:

    def test_logout_clears_config(self, tmp_config):
        """Logout deletes the config file."""
        # Create a config first
        config_mod.set_token("tok", "ref")
        assert config_mod.has_token()

        result = runner.invoke(app, ["logout"])

        assert result.exit_code == 0
        assert "Logged out" in result.output
        assert not config_mod.has_token()

    def test_logout_no_config_still_exits_0(self, tmp_config):
        """Logout when no config file exists should still exit 0."""
        result = runner.invoke(app, ["logout"])
        assert result.exit_code == 0


# ===========================================================================
# orbiads auth status
# ===========================================================================


class TestAuthStatus:
    """Status now routes through ``OrbiAdsClient`` so the request carries the
    ``X-OrbiAds-Client: cli/<v>`` header that drives ``CliAnalyticsMiddleware``
    (Story 74.2). Tests mock ``get_client`` directly — the 401 → refresh →
    retry loop is covered separately in ``test_client.py::TestTokenRefresh``.
    """

    def test_status_authenticated(self, tmp_config):
        """With valid token and server response, shows user info."""
        config_mod.set_token("valid-tok", "ref-tok")

        fake_client = MagicMock()
        fake_client.get.return_value = {
            "email": "user@example.com",
            "networkCode": "12345",
        }

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ):
            result = runner.invoke(app, ["status"])

        assert result.exit_code == 0
        assert "user@example.com" in result.output
        assert "12345" in result.output
        fake_client.get.assert_called_once_with("/api/me")

    def test_status_uses_config_network_when_server_state_unavailable(self, tmp_config):
        """Human output should fall back to local config only if server state is unavailable."""
        config_mod.save({
            "apiUrl": "https://test.example.com",
            "token": "valid-tok",
            "refreshToken": "ref-tok",
            "networkCode": "66235823",
        })

        fake_client = MagicMock()
        fake_client.get.side_effect = [
            {"email": "user@example.com"},
            CliApiError(1, "connection state unavailable"),
        ]

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ):
            result = runner.invoke(app, ["status"])

        assert result.exit_code == 0
        assert "66235823" in result.output
        assert "not set" not in result.output

    def test_status_prefers_connection_state_over_stale_config(self, tmp_config):
        """The server connection-state is authoritative over a stale local cache."""
        config_mod.save({
            "apiUrl": "https://test.example.com",
            "token": "valid-tok",
            "refreshToken": "ref-tok",
            "networkCode": "66235823",
        })

        fake_client = MagicMock()
        fake_client.get.side_effect = [
            {"email": "user@example.com"},
            {"networkCode": "33047445"},
        ]

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ):
            result = runner.invoke(app, ["status"])

        assert result.exit_code == 0
        assert "33047445" in result.output
        assert "66235823" not in result.output
        assert fake_client.get.call_args_list[1].args == (
            "/api/auth/gam/connection-state",
        )

    def test_status_json_resolves_network_from_connection_state(self, tmp_config):
        """Global --json should emit valid JSON and resolve the active network."""
        config_mod.save({
            "apiUrl": "https://test.example.com",
            "token": "valid-tok",
            "refreshToken": "ref-tok",
        })

        fake_client = MagicMock()
        fake_client.get.side_effect = [
            {"email": "user@example.com"},
            {"networkCode": "66235823"},
        ]

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ):
            result = runner.invoke(main_app, ["--json", "auth", "status"])

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["email"] == "user@example.com"
        assert data["networkCode"] == "66235823"
        # Both calls must go through OrbiAdsClient so the CLI analytics header
        # is attached — never raw httpx.
        assert fake_client.get.call_args_list[0].args == ("/api/me",)
        assert fake_client.get.call_args_list[1].args == (
            "/api/auth/gam/connection-state",
        )

    def test_status_not_authenticated(self, tmp_config):
        """No config file → exit code 4."""
        result = runner.invoke(app, ["status"])

        assert result.exit_code == 4
        assert "Not authenticated" in result.output

    def test_status_token_invalid_exits_4(self, tmp_config):
        """Server returns 401 + refresh fails → ``OrbiAdsClient`` raises
        ``CliApiError(exit_code=4)``. The status command surfaces a re-login
        hint and exits 4.
        """
        config_mod.set_token("expired-tok", "ref-tok")

        fake_client = MagicMock()
        fake_client.get.side_effect = CliApiError(
            4, "Session expired. Run `orbiads auth login`."
        )

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ):
            result = runner.invoke(app, ["status"])

        assert result.exit_code == 4
        assert "invalid" in result.output.lower() or "login" in result.output.lower()

    def test_status_refreshes_expired_token(self, tmp_config):
        """End-to-end: expired token → refresh inside ``OrbiAdsClient`` →
        retry → status data. The refresh mechanics are covered in detail by
        ``test_client.py::TestTokenRefresh::test_401_triggers_refresh_and_retry``;
        here we only assert the status command works once the client returns
        a successful payload.
        """
        config_mod.set_token("expired-tok", "ref-tok")

        fake_client = MagicMock()
        fake_client.get.return_value = {
            "email": "user@example.com",
            "networkCode": "12345",
        }

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ):
            result = runner.invoke(app, ["status"])

        assert result.exit_code == 0
        assert "user@example.com" in result.output


# ===========================================================================
# Story 74.2 follow-up — X-OrbiAds-Client header must be sent on every CLI
# request, including the device-flow bootstrap (no token yet) and the
# authenticated commands. Without these headers the backend
# CliAnalyticsMiddleware short-circuits and ``cli_command_called`` GA4
# events never fire — symptom in GA4: CLI Version / CLI Context / Tool
# name dimensions report 100% (not set).
# ===========================================================================


class TestCliHeaderInjection:
    """Defensive regression suite — these tests fail loud if anyone removes
    the X-OrbiAds-Client / X-OrbiAds-Client-Context headers from any of the
    five HTTP call sites in ``commands/auth.py``.
    """

    def _assert_cli_headers(self, call_kwargs: dict) -> None:
        headers = call_kwargs.get("headers") or {}
        assert headers.get("X-OrbiAds-Client") == f"cli/{__version__}", (
            f"Missing or wrong X-OrbiAds-Client header: {headers!r}. "
            "CliAnalyticsMiddleware (Story 74.2) requires literal 'cli/<v>'."
        )
        assert headers.get("X-OrbiAds-Client-Context"), (
            f"Missing X-OrbiAds-Client-Context header: {headers!r}. "
            "Required for the cli_context GA4 dimension."
        )

    def test_login_device_code_request_sends_cli_headers(self, tmp_config):
        """``auth login`` step 1 (no token yet) → manual header injection."""
        with patch("orbiads_cli.commands.auth.httpx.post") as mock_post, \
             patch("orbiads_cli.commands.auth.httpx.get") as mock_get, \
             patch("orbiads_cli.commands.auth.webbrowser.open"), \
             patch("orbiads_cli.commands.auth.time.sleep"):

            mock_post.return_value = _resp(200, _device_code_response())
            mock_get.return_value = _poll_authorized()

            runner.invoke(app, ["login"])

        # call_args_list[0] = device-code POST (the only one before custom-token
        # exchange could fire — and the test's authorized response uses
        # accessToken path so the exchange does NOT fire).
        self._assert_cli_headers(mock_post.call_args_list[0].kwargs)

    def test_login_polling_request_sends_cli_headers(self, tmp_config):
        """``auth login`` step 2 (device-token-status poll) → headers required.

        Each poll iteration calls /api/auth/gam/device-token-status. The
        backend identifies these as CLI traffic via the same headers as the
        device-code request.
        """
        with patch("orbiads_cli.commands.auth.httpx.post") as mock_post, \
             patch("orbiads_cli.commands.auth.httpx.get") as mock_get, \
             patch("orbiads_cli.commands.auth.webbrowser.open"), \
             patch("orbiads_cli.commands.auth.time.sleep"):

            mock_post.return_value = _resp(200, _device_code_response())
            mock_get.return_value = _poll_authorized()

            runner.invoke(app, ["login"])

        assert mock_get.call_count >= 1
        for call in mock_get.call_args_list:
            self._assert_cli_headers(call.kwargs)

    def test_status_routes_through_client_not_raw_httpx(self, tmp_config):
        """``auth status`` must NOT bypass OrbiAdsClient — the persistent client
        is what attaches the X-OrbiAds-Client headers on every request.

        Strategy: patch ``get_client`` AND ``httpx.get`` simultaneously. The
        former is expected to be called, the latter must NOT be — if it is,
        the implementation has regressed back to the pre-Story-74.2-followup
        bypass pattern.
        """
        config_mod.set_token("valid-tok", "ref-tok")

        fake_client = MagicMock()
        fake_client.get.return_value = {
            "email": "user@example.com",
            "networkCode": "12345",
        }

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ) as mock_factory, \
             patch("orbiads_cli.commands.auth.httpx.get") as raw_httpx_get:
            runner.invoke(app, ["status"])

        mock_factory.assert_called_once()
        raw_httpx_get.assert_not_called()

    def test_resolve_network_code_routes_through_client(self, tmp_config):
        """``_resolve_network_code`` fallback to /api/auth/gam/connection-state
        must also go through OrbiAdsClient, never raw httpx.
        """
        config_mod.save({
            "apiUrl": "https://test.example.com",
            "token": "valid-tok",
            "refreshToken": "ref-tok",
        })

        fake_client = MagicMock()
        # First call: /api/me — no networkCode → triggers connection-state lookup
        fake_client.get.side_effect = [
            {"email": "user@example.com"},
            {"networkCode": "66235823"},
        ]

        with patch(
            "orbiads_cli.commands.auth.get_client", return_value=fake_client
        ), patch("orbiads_cli.commands.auth.httpx.get") as raw_httpx_get:
            runner.invoke(app, ["status"])

        # Both /api/me AND /api/auth/gam/connection-state must go through
        # the client — raw httpx must not be touched.
        assert fake_client.get.call_count == 2
        raw_httpx_get.assert_not_called()


# ===========================================================================
# Config file permissions (Unix only)
# ===========================================================================


@pytest.mark.skipif(
    platform.system() == "Windows",
    reason="File permission mode 0o600 is Unix-only",
)
class TestConfigPermissions:

    def test_config_file_permissions_600(self, tmp_config):
        """After set_token, config file should have mode 0o600."""
        config_mod.set_token("tok", "ref")
        config_file = config_mod.CONFIG_FILE
        mode = os.stat(config_file).st_mode & 0o777
        assert mode == 0o600, f"Expected 0o600, got {oct(mode)}"
