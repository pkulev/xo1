"""EAF Renderer implementation for curses graphics backend."""

from operator import attrgetter

import eaf

from eaf.core import Vec3


class Renderable(eaf.Renderable):
    """Curses Renderable implementation."""

    # Allow or not drawing on border. Most of the time you probably want to
    # draw on border only some user interface widgets.
    draw_on_border = False


class Renderer(eaf.Renderer):
    """Curses renderer implementation."""

    INVISIBLE_SYMBOLS = " "
    """Symbols that renderer must not render on the screen."""

    def __init__(self, screen):
        super().__init__(screen)

    def clear(self):
        self.screen.erase()
        self.screen.border(0)

    def render_objects(self, objects):
        """Render all renderable objects."""

        # Window border, rendering behind it will cause curses.error
        border = Vec3(*self.screen.getmaxyx()[::-1])

        # TODO: Move sorting to some kind of object manager
        # Must be sorted on adding objects
        for obj in sorted(objects, key=attrgetter("render_priority")):

            if obj.image is None:
                continue

            for textel in obj.image:
                pos = (obj.pos + textel.pos)[int]

                if (
                    (pos.x >= border.x - 1 or pos.y >= border.y - 1)
                    or (pos.x <= 0 or pos.y <= 0)
                ) and not obj.draw_on_border:
                    continue

                if textel.char in self.INVISIBLE_SYMBOLS:
                    continue

                self.screen.addstr(pos.y, pos.x, textel.char, textel.attr)

    def present(self):
        self.screen.refresh()

    def get_width(self):
        return self.screen.getmaxyx()[0]

    def get_height(self):
        return self.screen.getmaxyx()[1]
