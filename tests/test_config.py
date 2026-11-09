import os

from native_app.config import AppConfig


def test_from_env_overrides(monkeypatch, tmp_path):
    monkeypatch.setenv("NATIVE_APP_TITLE", "Hello")
    monkeypatch.setenv("NATIVE_APP_WIDTH", "800")
    monkeypatch.setenv("NATIVE_APP_HEIGHT", "600")
    monkeypatch.setenv("NATIVE_APP_ASSETS", str(tmp_path))
    cfg = AppConfig.from_env()
    assert cfg.title == "Hello"
    assert cfg.width == 800
    assert cfg.height == 600
    assert cfg.assets_dir == str(tmp_path)


def test_invalid_int_raises(monkeypatch):
    monkeypatch.setenv("NATIVE_APP_WIDTH", "nope")
    try:
        AppConfig.from_env()
    except ValueError as exc:
        assert "NATIVE_APP_WIDTH" in str(exc)
    else:
        raise AssertionError("expected ValueError")