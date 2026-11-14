"""Small async-safe JSON store for per-guild settings."""

from __future__ import annotations

import asyncio
import json
import os
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any

from core.config import DEFAULT_PREFIX

DEFAULT_SHOP: dict[str, Any] = {
    "channel_id": None,
    "message_id": None,
    "staff_role_id": None,
    "heading": {
        "title": "🛒 Marketplace",
        "description": (
            "Welcome to the marketplace! Browse the sections below.\n"
            "Open a ticket to purchase anything you see here."
        ),
        "image": "",
        "thumbnail": "",
        "footer": "Prices may change without notice • Open a ticket to purchase",
        "color": "#5865F2",
    },
    "sections": [],
}

DEFAULT_TICKETS: dict[str, Any] = {
    "channel_id": None,
    "message_id": None,
    "category_id": None,
    "staff_role_id": None,
    "ticket_log_channel_id": None,
    "counter": 0,
    "title": "🎟️ Buy something",
    "description": (
        "Click the button below to open a private ticket.\n"
        "Tell us **what you are buying** and **how many**, and our staff will handle the rest."
    ),
    "button_label": "Open a ticket",
    "image": "",
    "thumbnail": "",
    "footer": "Our staff will claim your ticket shortly",
    "color": "#5865F2",
    "open": {},
}

DEFAULT_VERIFICATION: dict[str, Any] = {
    "channel_id": None,
    "role_id": None,
    "message_id": None,
    "title": "✅ Verify to enter",
    "description": (
        "Click the **Verify** button below to unlock the server.\n\n"
        "By verifying you agree to follow the server rules."
    ),
    "button_label": "Verify",
    "image": "",
    "color": "#57F287",
}

DEFAULTS: dict[str, Any] = {
    "prefix": None,
    "log_channel_id": None,
    "mod_role_id": None,
    "verification": DEFAULT_VERIFICATION,
    "tickets": DEFAULT_TICKETS,
    "shop": DEFAULT_SHOP,
    "warnings": {},
    "warning_seq": 0,
}


def _merge(defaults: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    """Fill in any missing keys without clobbering existing values."""
    for key, value in defaults.items():
        if key not in current:
            current[key] = deepcopy(value)
        elif isinstance(value, dict) and isinstance(current[key], dict):
            _merge(value, current[key])
    return current


class Database:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._data: dict[str, Any] = {"guilds": {}}
        self._lock = asyncio.Lock()

    async def load(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    self._data = raw
            except (json.JSONDecodeError, OSError):
                backup = self.path.with_suffix(".corrupt.json")
                try:
                    shutil.copy2(self.path, backup)
                except OSError:
                    pass
                self._data = {"guilds": {}}
        self._data.setdefault("guilds", {})

    async def save(self) -> None:
        async with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_name(self.path.name + ".tmp")
            tmp.write_text(
                json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            os.replace(tmp, self.path)

    def guild(self, guild_id: int) -> dict[str, Any]:
        store = self._data.setdefault("guilds", {})
        data = store.setdefault(str(guild_id), {})
        return _merge(DEFAULTS, data)

    async def get_prefix(self, guild_id: int) -> str:
        return self.guild(guild_id).get("prefix") or DEFAULT_PREFIX
