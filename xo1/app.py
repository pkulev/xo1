"""EAF application implementation with curses support."""

from typing import Optional

import eaf.app

from xo1.window import create_window, deinit_window
from xo1.color import Palette
from xo1.render import Renderer


class Application(eaf.app.Application):
    """Curses-powered application class."""

    def __init__(
        self, x, y, palette: Optional[Palette] = None, title: str = "xo1 application"
    ):
        window = create_window(x, y, init=True)
        renderer = Renderer(window)

        super().__init__(renderer, window)

        self._palette = palette or Palette()
        self._palette.init_colors()

        self.set_caption(title)

    def set_caption(self, caption):
        """Set window caption.

        This is very hacky workaround, curses doesn't know that terminal state
        changed. Not all terminals support this.

        .. NOTE:: application doesn't revert title back, maybe later will be
                  implemented.
        """

        print(f"\x1b]0;{caption}\x07")

    def tick(self):
        """Handle `Ctrl C` gracefully."""

        try:
            super().tick()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Return terminal state back."""

        def deinit_curses():
            self.renderer.clear()
            deinit_window(self.renderer.screen)

        self._ioloop.add_callback(deinit_curses)
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
