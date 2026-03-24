"""HTTP client with auto-refresh, retry, and JSend envelope parsing."""

from __future__ import annotations

import re
import time
from typing import Any

import httpx
import typer

from orbiads_cli import config

# Public Firebase client identifier (same as frontend).
# This is NOT a secret — it only identifies the Firebase project.
FIREBASE_API_KEY = "AIzaSyAr2J5-a6GjIStBSOoIKB48DzSr0K-wHiQ"
FIREBASE_REFRESH_URL = (
    f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"
)

# Exponential backoff delays for 429 retries (seconds).
_BACKOFF_DELAYS = [1, 2, 4]


# ---------------------------------------------------------------------------
# Exit-code mapping
# ---------------------------------------------------------------------------

_STATUS_TO_EXIT: dict[int, int] = {
    404: 3,
    401: 4,
    403: 4,
    409: 5,
    412: 6,
}


def _exit_code(status: int) -> int:
    """Map HTTP status to CLI exit code."""
    return _STATUS_TO_EXIT.get(status, 1)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class CliApiError(Exception):
    """API error with semantic exit code for CLI commands."""

    def __init__(
        self,
        exit_code: int,
        message: str,
        error_code: str = "",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.exit_code = exit_code
        self.message = message
        self.error_code = error_code
        self.details: dict[str, Any] = details or {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CREDITS_RE = re.compile(
    r"[Bb]alance[:\s]+(\d+).*[Rr]equired[:\s]+(\d+)"
)


def _parse_credits_message(message: str, details: dict[str, Any]) -> None:
    """Best-effort extraction of balance/required from an error message."""
    m = _CREDITS_RE.search(message)
    if m:
        details["balance"] = int(m.group(1))
        details["required"] = int(m.group(2))


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class OrbiAdsClient:
    """Thin wrapper around ``httpx.Client`` with auth and retry logic."""

    def __init__(self, cfg: dict) -> None:
        self._cfg = cfg
        self._http = httpx.Client(
            base_url=cfg["apiUrl"],
            headers={"Authorization": f"Bearer {cfg['token']}"},
            timeout=30.0,
        )
        self._refreshed = False  # guard: at most one refresh per request

    # -- public convenience methods ------------------------------------------

    def get(self, path: str, **kwargs: Any) -> Any:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self._request("DELETE", path, **kwargs)

    # -- core request loop ---------------------------------------------------

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        self._refreshed = False
        resp = self._http.request(method, path, **kwargs)

        # 401 → attempt one token refresh then retry
        if resp.status_code == 401 and not self._refreshed:
            if self._refresh_token():
                self._refreshed = True
                resp = self._http.request(method, path, **kwargs)
            else:
                raise CliApiError(
                    4, "Session expired. Run `orbiads auth login`."
                )

        # 429 → exponential backoff (max 3 retries)
        if resp.status_code == 429:
            resp = self._retry_with_backoff(method, path, **kwargs)

        # Parse JSend envelope
        return self._parse_response(resp)

    # -- token refresh -------------------------------------------------------

    def _refresh_token(self) -> bool:
        """Refresh Firebase ID token using the stored refresh token.

        Returns ``True`` on success, ``False`` otherwise.
        """
        refresh_token = self._cfg.get("refreshToken")
        if not refresh_token:
            return False

        try:
            resp = httpx.post(
                FIREBASE_REFRESH_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
                timeout=15.0,
            )
        except httpx.HTTPError:
            return False

        if resp.status_code != 200:
            return False

        data = resp.json()
        new_token = data.get("id_token", "")
        new_refresh = data.get("refresh_token", "")
        if not new_token:
            return False

        # Persist new tokens
        config.set_token(new_token, new_refresh)
        self._cfg["token"] = new_token
        self._cfg["refreshToken"] = new_refresh
        self._http.headers["Authorization"] = f"Bearer {new_token}"
        return True

    # -- 429 backoff ---------------------------------------------------------

    def _retry_with_backoff(
        self, method: str, path: str, **kwargs: Any
    ) -> httpx.Response:
        resp: httpx.Response | None = None
        for delay in _BACKOFF_DELAYS:
            typer.echo(
                f"Rate limited, retrying in {delay}s...", err=True
            )
            time.sleep(delay)
            resp = self._http.request(method, path, **kwargs)
            if resp.status_code != 429:
                return resp
        # Return the last 429 so the caller can raise the appropriate error.
        assert resp is not None
        return resp

    # -- response parsing ----------------------------------------------------

    @staticmethod
    def _parse_response(resp: httpx.Response) -> Any:
        """Parse a JSend-style envelope.

        On success returns the ``data`` field.
        On error raises :class:`CliApiError` with the correct exit code.
        """
        try:
            body = resp.json()
        except Exception:
            if resp.status_code >= 400:
                raise CliApiError(
                    _exit_code(resp.status_code),
                    f"HTTP {resp.status_code} (non-JSON response)",
                )
            return None

        if resp.status_code >= 400:
            err = body.get("error") or {}
            code = err.get("code", "")
            message = err.get("message", f"HTTP {resp.status_code}")
            details: dict[str, Any] = {}

            # Extract structured details from the error payload.
            if isinstance(err.get("details"), dict):
                details = err["details"]

            # Map INSUFFICIENT_CREDITS (HTTP 412) to exit code 6 with
            # balance/required details parsed from the message or payload.
            exit = _exit_code(resp.status_code)
            if code == "INSUFFICIENT_CREDITS":
                exit = 6
                # Backend may include balance/required in details or message.
                if "balance" not in details:
                    _parse_credits_message(message, details)

            # For 404, include the request path as the resource hint.
            if resp.status_code == 404 and "resource" not in details:
                try:
                    details["resource"] = resp.request.url.path
                except RuntimeError:
                    pass  # request not set (e.g. in tests)

            raise CliApiError(exit, message, code, details)

        return body.get("data")

    # -- cleanup -------------------------------------------------------------

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "OrbiAdsClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_singleton: OrbiAdsClient | None = None


def get_client() -> OrbiAdsClient:
    """Return a configured :class:`OrbiAdsClient`.

    Reuses a single instance within the process (singleton).
    Exits with code 4 if the user is not authenticated.
    """
    global _singleton
    if _singleton is not None:
        return _singleton

    cfg = config.load()
    if not cfg or not cfg.get("token"):
        typer.echo(
            "Not authenticated. Run `orbiads auth login` first.", err=True
        )
        raise typer.Exit(code=4)

    _singleton = OrbiAdsClient(cfg)
    return _singleton
