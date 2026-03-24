"""Shared fixtures for OrbiAds CLI tests — Stories 54.7 / 55.9."""

from unittest.mock import MagicMock

import pytest
from typer.testing import CliRunner

from orbiads_cli import config as config_mod
from orbiads_cli import client as client_mod


@pytest.fixture
def tmp_config(tmp_path, monkeypatch):
    """Redirect config to a temporary directory for test isolation.

    Patches CONFIG_DIR and CONFIG_FILE so that all config reads/writes
    go to ``tmp_path`` instead of ``~/.orbiads/``.
    """
    monkeypatch.setattr(config_mod, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(config_mod, "CONFIG_FILE", tmp_path / "config.json")
    return tmp_path


@pytest.fixture
def authenticated_config(tmp_config):
    """Create a config with a fake token so auth guards pass."""
    config_mod.save({
        "apiUrl": "https://test.example.com",
        "token": "test-token-fake",
        "refreshToken": "test-refresh-fake",
    })
    return tmp_config


@pytest.fixture
def mock_client():
    """Return a MagicMock mimicking OrbiAdsClient.

    Usage::

        def test_something(mock_client):
            mock_client.get.return_value = {"key": "val"}
            with patch("orbiads_cli.commands.foo.get_client", return_value=mock_client):
                ...
    """
    client = MagicMock(spec=client_mod.OrbiAdsClient)
    return client


@pytest.fixture
def runner():
    """Provide a reusable CliRunner instance."""
    return CliRunner()


@pytest.fixture(autouse=True)
def _reset_client_singleton():
    """Reset the client singleton between tests to avoid leaking state."""
    client_mod._singleton = None
    yield
    client_mod._singleton = None
