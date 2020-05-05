"""EAF application implementation with curses support."""

from typing import Optional

import eaf.app

from xo1.window import create_window, deinit_window
from xo1.color import Palette
from xo1.render import Renderer


class Application(eaf.app.Application):
    """Curses-powered application class."""

    def __init__(self, x, y, palette: Optional[Palette] = None):
        window = create_window(x, y, init=True)
        renderer = Renderer(window)

        super().__init__(renderer, window)

        self._palette = palette or Palette()
        self._palette.init_colors()

    def set_caption(self, caption: str = "xo1 application", icontitle: str = ""):
        """Set window caption."""

        # FIXME: Maybe we can update text via terminal API
        pass

    def stop(self):
        self._ioloop.add_callback(lambda: deinit_window(self.renderer.screen))
        super().stop()

    @property
    def palette(self) -> Palette:
        """Palette getter."""

        return self._palette

    @palette.setter
    def palette(self, palette: Palette):
        """Palette setter."""

        if not isinstance(palette, Palette):
            raise TypeError(f"Expected Palette class, got {type(palette)}")

        self.palette = palette
