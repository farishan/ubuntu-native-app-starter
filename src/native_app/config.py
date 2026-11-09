# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Faris Han
"""Configuration for the starter app.

All values can be overridden with environment variables so the same binary
works in development and production without recompiling.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AppConfig:
    app_id: str = "com.example.NativeAppStarter"
    title: str = "Native App Starter"
    width: int = 960
    height: int = 640
    min_width: int = 480
    min_height: int = 320
    start_maximized: bool = False
    devtools: bool = False
    log_level: str = "INFO"
    assets_dir: str = field(default_factory=lambda: os.environ.get("NATIVE_APP_ASSETS", ""))

    @classmethod
    def from_env(cls) -> "AppConfig":
        def _int(name: str, default: int) -> int:
            raw = os.environ.get(name)
            if raw is None or raw == "":
                return default
            try:
                return int(raw)
            except ValueError as exc:
                raise ValueError(f"{name} must be an integer, got {raw!r}") from exc

        def _bool(name: str, default: bool) -> bool:
            raw = os.environ.get(name)
            if raw is None or raw == "":
                return default
            return raw.strip().lower() in {"1", "true", "yes", "on"}

        assets = os.environ.get("NATIVE_APP_ASSETS", "")
        if not assets:
            # Default to the bundled assets shipped next to this package.
            import pathlib

            assets = str(pathlib.Path(__file__).resolve().parent.parent.parent / "assets")
            if not os.path.isdir(assets):
                assets = str(pathlib.Path.cwd() / "assets")

        return cls(
            app_id=os.environ.get("NATIVE_APP_ID", cls.app_id),
            title=os.environ.get("NATIVE_APP_TITLE", cls.title),
            width=_int("NATIVE_APP_WIDTH", cls.width),
            height=_int("NATIVE_APP_HEIGHT", cls.height),
            min_width=_int("NATIVE_APP_MIN_WIDTH", cls.min_width),
            min_height=_int("NATIVE_APP_MIN_HEIGHT", cls.min_height),
            start_maximized=_bool("NATIVE_APP_MAXIMIZED", cls.start_maximized),
            devtools=_bool("NATIVE_APP_DEVTOOLS", cls.devtools),
            log_level=os.environ.get("NATIVE_APP_LOG_LEVEL", cls.log_level).upper(),
            assets_dir=assets,
        )