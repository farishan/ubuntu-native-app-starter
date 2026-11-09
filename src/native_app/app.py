"""Application entry point."""

from __future__ import annotations

import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # type: ignore  # noqa: E402

from .bridge import Bridge
from .config import AppConfig
from .logging import setup as setup_logging
from .window import MainWindow


def build_bridge() -> Bridge:
    bridge = Bridge()

    def ping(_payload: dict) -> dict:
        return {"pong": True}

    def echo(payload: dict) -> dict:
        return {"echo": payload}

    bridge.register("ping", ping)
    bridge.register("echo", echo)
    return bridge


class Application(Gtk.Application):
    def __init__(self, config: AppConfig) -> None:
        super().__init__(application_id=config.app_id)
        self.config = config
        self.bridge = build_bridge()
        self.window: MainWindow | None = None

    def do_activate(self) -> None:
        if self.window is None:
            self.window = MainWindow(self, self.config, self.bridge)
        self.window.present()


def main(argv: list[str] | None = None) -> int:
    config = AppConfig.from_env()
    log = setup_logging(config.log_level)
    log.info("starting %s", config.app_id)
    app = Application(config)
    return app.run(argv if argv is not None else sys.argv[1:])