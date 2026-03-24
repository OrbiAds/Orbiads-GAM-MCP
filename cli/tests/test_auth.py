"""Tests for CLI auth commands (login, logout, status) — Story 54.7.

Uses typer.testing.CliRunner with mocked httpx calls to avoid real API traffic.
"""

import os
import platform
from unittest.mock import patch

import httpx
import pytest
from typer.testing import CliRunner

from orbiads_cli import config as config_mod
from orbiads_cli.commands.auth import app

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

    def test_status_authenticated(self, tmp_config):
        """With valid token and server response, shows user info."""
        config_mod.set_token("valid-tok", "ref-tok")

        with patch("orbiads_cli.commands.auth.httpx.get") as mock_get:
            mock_get.return_value = _resp(200, {
                "data": {"email": "user@example.com", "networkCode": "12345"},
                "error": None,
            })

            result = runner.invoke(app, ["status"])

        assert result.exit_code == 0
        assert "user@example.com" in result.output
        assert "12345" in result.output

    def test_status_not_authenticated(self, tmp_config):
        """No config file → exit code 4."""
        result = runner.invoke(app, ["status"])

        assert result.exit_code == 4
        assert "Not authenticated" in result.output

    def test_status_token_invalid_exits_4(self, tmp_config):
        """Server returns 401 → exit code 4 with re-login hint."""
        config_mod.set_token("expired-tok", "ref-tok")

        with patch("orbiads_cli.commands.auth.httpx.get") as mock_get:
            mock_get.return_value = httpx.Response(401, request=_DUMMY_REQUEST)

            result = runner.invoke(app, ["status"])

        assert result.exit_code == 4
        assert "invalid" in result.output.lower() or "login" in result.output.lower()


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
