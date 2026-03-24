"""Tests for OrbiAdsClient — Story 54.7.

Covers: Bearer header injection, 401 token refresh + retry, 429 exponential
backoff, refresh token expiry, JSend envelope parsing, exit code mapping.

All HTTP calls are mocked via unittest.mock patching of httpx.
"""

from unittest.mock import patch, MagicMock, call

import httpx
import pytest

from orbiads_cli import config as config_mod
from orbiads_cli.client import OrbiAdsClient, CliApiError, _exit_code


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_cfg(tmp_config, *, token="tok-123", refresh_token="ref-456"):
    """Create and persist a config, return the dict."""
    config_mod.set_token(token, refresh_token)
    return config_mod.load()


def _jsend_ok(data: dict) -> httpx.Response:
    return httpx.Response(200, json={"data": data, "error": None})


def _jsend_error(status_code: int, code: str = "ERR", message: str = "fail") -> httpx.Response:
    return httpx.Response(
        status_code,
        json={"data": None, "error": {"code": code, "message": message}},
    )


# ===========================================================================
# Bearer header injection
# ===========================================================================


class TestBearerHeader:

    def test_authorization_header_set(self, tmp_config):
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)
        assert client._http.headers["Authorization"] == "Bearer tok-123"
        client.close()

    def test_header_sent_on_request(self, tmp_config):
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        with patch.object(client._http, "request", return_value=_jsend_ok({"ok": True})) as mock_req:
            client.get("/test")
            mock_req.assert_called_once()
            # The header is on the client, not passed per-request

        client.close()


# ===========================================================================
# 401 → token refresh → retry
# ===========================================================================


class TestTokenRefresh:

    def test_401_triggers_refresh_and_retry(self, tmp_config):
        """First request returns 401, refresh succeeds, retry succeeds."""
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        call_count = {"n": 0}
        def fake_request(method, path, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return httpx.Response(401, json={"data": None, "error": {"code": "AUTH", "message": "Unauthorized"}})
            return _jsend_ok({"refreshed": True})

        with patch.object(client._http, "request", side_effect=fake_request), \
             patch("orbiads_cli.client.httpx.post") as mock_refresh_post:

            # Mock Firebase refresh endpoint
            mock_refresh_post.return_value = httpx.Response(200, json={
                "id_token": "new-tok",
                "refresh_token": "new-ref",
            })

            result = client.get("/protected")

        assert result == {"refreshed": True}
        assert call_count["n"] == 2

        # Verify new token was persisted
        updated_cfg = config_mod.load()
        assert updated_cfg["token"] == "new-tok"
        assert updated_cfg["refreshToken"] == "new-ref"

        client.close()

    def test_refresh_token_expired_raises_exit_4(self, tmp_config):
        """401 + failed refresh → CliApiError with exit_code=4."""
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        with patch.object(
            client._http, "request",
            return_value=httpx.Response(401, json={"data": None, "error": {"code": "AUTH", "message": "Unauthorized"}}),
        ), \
             patch("orbiads_cli.client.httpx.post") as mock_refresh_post:

            # Firebase refresh fails (e.g., refresh token revoked)
            mock_refresh_post.return_value = httpx.Response(400, json={"error": {"message": "TOKEN_EXPIRED"}})

            with pytest.raises(CliApiError) as exc_info:
                client.get("/protected")

        assert exc_info.value.exit_code == 4
        assert "login" in exc_info.value.message.lower()

        client.close()

    def test_no_refresh_token_raises_exit_4(self, tmp_config):
        """401 with no refreshToken in config → CliApiError exit 4."""
        config_mod.save({"apiUrl": "http://localhost", "token": "tok"})
        cfg = config_mod.load()
        client = OrbiAdsClient(cfg)

        with patch.object(
            client._http, "request",
            return_value=httpx.Response(401, json={"data": None, "error": {"code": "AUTH", "message": "x"}}),
        ):
            with pytest.raises(CliApiError) as exc_info:
                client.get("/foo")

        assert exc_info.value.exit_code == 4
        client.close()


# ===========================================================================
# 429 → exponential backoff
# ===========================================================================


class TestBackoff:

    def test_429_retries_with_backoff(self, tmp_config):
        """First 2 requests return 429, third succeeds."""
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        responses = [
            httpx.Response(429, json={"data": None, "error": {"code": "RATE_LIMITED", "message": "slow down"}}),
            httpx.Response(429, json={"data": None, "error": {"code": "RATE_LIMITED", "message": "slow down"}}),
            _jsend_ok({"result": 42}),
        ]
        call_count = {"n": 0}

        def fake_request(method, path, **kwargs):
            call_count["n"] += 1
            # First call is the original, subsequent are retries from _retry_with_backoff
            return responses[call_count["n"] - 1]

        with patch.object(client._http, "request", side_effect=fake_request), \
             patch("orbiads_cli.client.time.sleep") as mock_sleep, \
             patch("orbiads_cli.client.typer.echo"):

            result = client.get("/data")

        assert result == {"result": 42}
        # sleep called with 1s and 2s (first two backoff delays)
        assert mock_sleep.call_args_list == [call(1), call(2)]

        client.close()

    def test_429_max_retries_exhausted(self, tmp_config):
        """All retries return 429 → CliApiError with exit_code 1."""
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        resp_429 = httpx.Response(429, json={"data": None, "error": {"code": "RATE_LIMITED", "message": "slow"}})

        with patch.object(client._http, "request", return_value=resp_429), \
             patch("orbiads_cli.client.time.sleep"), \
             patch("orbiads_cli.client.typer.echo"):

            with pytest.raises(CliApiError) as exc_info:
                client.get("/data")

        assert exc_info.value.exit_code == 1
        client.close()

    def test_429_backoff_logs_to_stderr(self, tmp_config):
        """Verify retry messages are echoed to stderr."""
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        resp_429 = httpx.Response(429, json={"data": None, "error": {"code": "RL", "message": "x"}})
        responses = [resp_429, resp_429, _jsend_ok({"ok": True})]
        idx = {"i": 0}

        def fake_request(method, path, **kwargs):
            r = responses[idx["i"]]
            idx["i"] += 1
            return r

        with patch.object(client._http, "request", side_effect=fake_request), \
             patch("orbiads_cli.client.time.sleep"), \
             patch("orbiads_cli.client.typer.echo") as mock_echo:

            client.get("/data")

        # Should have echoed backoff messages
        assert mock_echo.call_count >= 2
        for c in mock_echo.call_args_list:
            assert "retrying" in c.args[0].lower() or "Rate limited" in c.args[0]

        client.close()


# ===========================================================================
# JSend envelope parsing
# ===========================================================================


class TestJSendParsing:

    def test_success_extracts_data(self, tmp_config):
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        with patch.object(
            client._http, "request",
            return_value=_jsend_ok({"campaigns": [1, 2, 3]}),
        ):
            result = client.get("/campaigns")

        assert result == {"campaigns": [1, 2, 3]}
        client.close()

    def test_error_raises_cli_api_error(self, tmp_config):
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        with patch.object(
            client._http, "request",
            return_value=_jsend_error(400, "INVALID_INPUT", "Bad field X"),
        ):
            with pytest.raises(CliApiError) as exc_info:
                client.get("/bad")

        assert exc_info.value.error_code == "INVALID_INPUT"
        assert exc_info.value.message == "Bad field X"
        client.close()

    def test_non_json_error_response(self, tmp_config):
        """Non-JSON 500 response → CliApiError with status info."""
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        with patch.object(
            client._http, "request",
            return_value=httpx.Response(500, text="Internal Server Error"),
        ):
            with pytest.raises(CliApiError) as exc_info:
                client.get("/crash")

        assert exc_info.value.exit_code == 1
        assert "500" in exc_info.value.message
        client.close()


# ===========================================================================
# Exit code mapping
# ===========================================================================


class TestExitCodeMapping:

    @pytest.mark.parametrize(
        "http_status,expected_exit",
        [
            (404, 3),
            (401, 4),
            (403, 4),
            (409, 5),
            (412, 6),
            (500, 1),
            (502, 1),
            (503, 1),
        ],
    )
    def test_status_to_exit_code(self, http_status, expected_exit):
        assert _exit_code(http_status) == expected_exit

    @pytest.mark.parametrize(
        "http_status,expected_exit",
        [
            (404, 3),
            (403, 4),
            (409, 5),
            (412, 6),
            (500, 1),
        ],
    )
    def test_error_response_maps_exit_code(self, tmp_config, http_status, expected_exit):
        """Full round-trip: HTTP error → CliApiError with correct exit_code."""
        cfg = _make_cfg(tmp_config)
        client = OrbiAdsClient(cfg)

        with patch.object(
            client._http, "request",
            return_value=_jsend_error(http_status, "SOME_CODE", "Error"),
        ):
            with pytest.raises(CliApiError) as exc_info:
                client.get("/resource")

        assert exc_info.value.exit_code == expected_exit
        client.close()
