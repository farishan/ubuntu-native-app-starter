# Ubuntu Native App Starter

A **production-ready, minimal starter** for building native desktop
applications on Ubuntu using:

- **Python 3** (3.10+)
- **GTK 3** (`libgtk-3`)
- **WebKit2GTK 4.0** (HTML/CSS/JS UI in a native window)

No Electron, no Chromium bundle, no Rust build, no Node toolchain. The
whole app is a few hundred lines of Python plus static web assets. It
runs on a stock Ubuntu 22.04 install with the packages below.

Verified on: Ubuntu 22.04.5 LTS, X11, GNOME, Python 3.10, GTK 3.24.33,
WebKit2GTK 4.0 (2.50.4).

## Why this starter

Building a native Linux GUI usually means choosing between heavy stacks
(Electron/Chromium, Tauri/Rust) and low-level toolkits. This starter
picks the **lightest stack that still gives a modern web-based UI**:

- GTK 3 + WebKit2GTK 4.0 are already installed on Ubuntu with dev
  headers (`libgtk-3-dev`, `libwebkit2gtk-4.0-dev`).
- Zero build step: `python3 -m native_app` runs immediately.
- No multi-GB `target/` or `node_modules`.
- Native window integration, theming, and `.desktop` packaging.
- A validated JS ↔ Python bridge (no `eval`).

## Quick start

```bash
git clone https://github.com/farishan/ubuntu-native-app-starter.git
cd ubuntu-native-app-starter
sudo apt install -y python3 python3-gi libgtk-3-0 libwebkit2gtk-4.0-37
PYTHONPATH=src python3 -m native_app
```

Or, after install:

```bash
make install
native-app-starter
```

## System dependencies

```bash
sudo apt install -y \
  python3 python3-gi python3-pytest \
  libgtk-3-dev libwebkit2gtk-4.0-dev
```

## Run

```bash
make run          # PYTHONPATH=src python3 -m native_app
make test         # pytest
make lint         # compileall
make smoke        # import smoke test
```

## Configuration

All settings are overridable via environment variables (see
`src/native_app/config.py`):

| Variable | Default | Description |
|---|---|---|
| `NATIVE_APP_TITLE` | `Native App Starter` | Window title |
| `NATIVE_APP_WIDTH` / `_HEIGHT` | `960` / `640` | Initial size |
| `NATIVE_APP_MIN_WIDTH` / `_HEIGHT` | `480` / `320` | Minimum size |
| `NATIVE_APP_MAXIMIZED` | `false` | Start maximized |
| `NATIVE_APP_DEVTOOLS` | `false` | Enable WebKit inspector |
| `NATIVE_APP_LOG_LEVEL` | `INFO` | Logging level |
| `NATIVE_APP_ASSETS` | bundled `assets/` | Path to web assets |

Example:

```bash
NATIVE_APP_TITLE="My App" NATIVE_APP_DEVTOOLS=1 make run
```

## Project layout

```
ubuntu-native-app-starter/
├── src/native_app/        # Python package
│   ├── app.py             # Gtk.Application lifecycle
│   ├── window.py          # Main window + webview host
│   ├── webview.py         # WebKit2 4.0 helpers
│   ├── bridge.py          # Validated JS <-> Python bridge
│   ├── config.py          # Env-based configuration
│   ├── platform.py        # X11/Wayland detection
│   └── logging.py
├── assets/                # index.html, style.css, app.js
├── tests/                 # pytest (GUI-free)
├── examples/              # .desktop entry
├── docs/                  # architecture & platform notes
└── .github/workflows/     # CI on Ubuntu
```

## Customization

1. Edit `assets/index.html`, `style.css`, `app.js` for the UI.
2. Register new bridge actions in `app.py` (`build_bridge`).
3. Call Python from JS:
   ```js
   window.webkit.messageHandlers.nativeApp.postMessage(
     JSON.stringify({ action: "ping", payload: {} })
   );
   ```
4. Receive replies in JS via `window.nativeAppReceive(reply)`.

## Packaging

A `.desktop` entry is provided in `examples/hello.desktop`. Install it:

```bash
mkdir -p ~/.local/share/applications
cp examples/hello.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications
```

For distribution, prefer a `.deb` or an AppImage; avoid bundling
Chromium/Electron to keep the package small.

## Wayland caveat

On GNOME/Wayland, X11 window hints are ignored by Mutter. The app still
runs, but desktop-level features (keep-below, desktop window type) will
not apply. See `docs/PLATFORM.md`.

## Testing

Tests are GUI-free and run in CI on `ubuntu-latest`:

```bash
PYTHONPATH=src pytest -q
```

## Security

- The bridge never evaluates arbitrary code from the UI.
- `allow_universal_access_from_file_urls` is disabled.
- File access from file URLs is limited to the bundled assets.

## License

GPL-3.0-or-later (GNU General Public License v3 or later).

See `LICENSE` for the full text. Copyright (C) 2026 Faris Han.