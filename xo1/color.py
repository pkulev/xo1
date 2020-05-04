"""Curses color manipulation objects."""

import curses

from typing import List

from eaf.errors import Error


class PairAlreadyRegistered(Error):
    def __init__(self, attr, value):
        super().__init__(
            f"Pair with {attr} = {value} already registered."
            " You can use force=True to redefine it."
        )


class Pair:
    """Color pair representation."""

    def __init__(self, idx, fg, bg, attrs=None):
        self.idx = idx
        self.bg = bg
        self.fg = fg
        self.attrs = attrs

    def init(self):
        """Init curses color pair.

        Does nothing if terminal doesn't support colors.
        """

        if not curses.has_colors():
            return

        curses.init_pair(self.idx, self.fg, self.bg)


class Palette:
    """Palette abstraction for curses color pairs.

    Has some predefined constants (taken directly from curses),

    Pass to init initial palette as list of tuples of 3 elements: name,
    foreground color, background color:

    palette = Palette([
        ("normal", Palette.COLOR_WHITE, Palette.COLOR_BLACK),
        ("error", Palette.COLOR_RED, Palette.COLOR_BLACK),
    ])
    """

    COLOR_BLACK = curses.COLOR_BLACK
    COLOR_BLUE = curses.COLOR_BLUE
    COLOR_CYAN = curses.COLOR_CYAN
    COLOR_GREEN = curses.COLOR_GREEN
    COLOR_MAGENTA = curses.COLOR_MAGENTA
    COLOR_RED = curses.COLOR_RED
    COLOR_WHITE = curses.COLOR_WHITE
    COLOR_YELLOW = curses.COLOR_YELLOW

    A_BOLD = curses.A_BOLD

    def __init__(self, palette=None):
        self.palette = {}

        idx = 1
        for name, fg, bg in palette or []:
            self.add_pair(name, Pair(idx, fg, bg), init=False)
            idx += 1

    def add_pair(self, name: str, pair: Pair, force: bool = False, init: bool = True):
        """Add new color pair. Use force to override name and idx."""

        if name in self.palette and not force:
            raise PairAlreadyRegistered("name", name)

        if pair.idx in [pair.idx for pair in self.palette.values()] and not force:
            raise PairAlreadyRegistered("idx", pair.idx)

        self.palette[name] = pair

        if init:
            pair.init()

    def init_colors(self):
        """Init all color pairs."""

        for pair in self.palette.values():
            pair.init()

    @property
    def pair_names(self) -> List[str]:
        return sorted(self.palette, key=lambda it: self[it].idx)

    def __getattr__(self, name: str) -> int:
        return self.palette[name].idx
