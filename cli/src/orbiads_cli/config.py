"""Configuration manager — secure storage in ~/.orbiads/config.json."""

import json
import os
import platform
from pathlib import Path

CONFIG_DIR = Path.home() / ".orbiads"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_API_URL = "https://gam-native-backend-754225819371.europe-west1.run.app"
DEFAULT_OUTPUT = "table"

_IS_WINDOWS = platform.system() == "Windows"


def load() -> dict | None:
    """Load config from ~/.orbiads/config.json. Returns None if missing."""
    if not CONFIG_FILE.exists():
        return None
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save(config: dict) -> None:
    """Save config with secure permissions (dir 700, file 600)."""
    if _IS_WINDOWS:
        CONFIG_DIR.mkdir(exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
    else:
        CONFIG_DIR.mkdir(mode=0o700, exist_ok=True)
        fd = os.open(
            str(CONFIG_FILE),
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            0o600,
        )
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)


def get_token() -> str | None:
    """Shortcut: load config and return the token, or None."""
    cfg = load()
    return cfg.get("token") if cfg else None


def set_token(token: str, refresh_token: str) -> None:
    """Update token and refreshToken in config, creating defaults if needed."""
    cfg = load() or {
        "apiUrl": DEFAULT_API_URL,
        "defaultOutput": DEFAULT_OUTPUT,
    }
    cfg["token"] = token
    cfg["refreshToken"] = refresh_token
    save(cfg)


def has_token() -> bool:
    """Check if a valid token exists in config."""
    cfg = load()
    return cfg is not None and bool(cfg.get("token"))


def clear() -> None:
    """Delete config file (not the directory)."""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
