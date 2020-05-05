import curses

import xo1.app
import xo1.window


def test_application(monkeypatch):
    """Tests for xo1.app.Application()."""

    monkeypatch.setattr(xo1.app, "create_window", lambda *args, **kwargs: True)
    monkeypatch.setattr(xo1.app, "deinit_window", lambda *args, **kwargs: True)
    monkeypatch.setattr(curses, "has_colors", lambda: False)

    app = xo1.app.Application(80, 24)
    assert isinstance(app.current(), xo1.app.Application)
    assert app.current() is app

    assert app.renderer is not None
    assert app.set_caption("test") is None
