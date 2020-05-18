"""Curses color manipulation objects."""

import curses

from typing import List, Optional, Union

from eaf.errors import Error


class PairAlreadyRegistered(Error):
    def __init__(self, attr, value):
        super().__init__(
            f"Pair with {attr} = {value} already registered."
            " You can use force=True to redefine it."
        )


class InvalidPaletteEntry(Error):
    def __init__(self, entry):
        super().__init__(f"Invalid palette entry: {entry}, must be 1-3 element tuple.")


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

    COLOR_DEFAULT = -1

    A_NORMAL = curses.A_NORMAL
    A_BOLD = curses.A_BOLD
    A_BLINK = curses.A_BLINK
    A_REVERSE = curses.A_REVERSE
    A_STANDOUT = curses.A_STANDOUT

    def __init__(self, palette=None, attr_map=None):
        self.palette = {}
        self.attr_map = attr_map or {}

        idx = 1
        for name, fg, bg in self._destructure(palette):
            self.add_pair(name, Pair(idx, fg, bg), init=False)
            idx += 1

    @classmethod
    def _destructure(cls, palette: Optional[List[tuple]]) -> List[tuple]:
        """Apply _destructure_entry to the whole palette."""

        for entry in palette or []:
            yield cls._destructure_entry(entry)

    @classmethod
    def _destructure_entry(cls, entry: tuple) -> tuple:
        """Validate incoming entry and return tuple with defaults on missing."""
        if len(entry) == 1:
            name, fg, bg = entry + (cls.COLOR_DEFAULT, cls.COLOR_DEFAULT)
        elif len(entry) == 2:
            name, fg, bg = entry + (cls.COLOR_DEFAULT,)
        elif len(entry) == 3:
            name, fg, bg = entry
        else:
            raise InvalidPaletteEntry(entry)

        return name, fg, bg

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

    def __getattr__(self, name: Union[str, int]) -> int:

        # we suppose that it's already curses value
        if isinstance(name, int):
            return name

        # FIXME: register default pair
        if name == "default":
            return curses.color_pair(0)

        return curses.color_pair(self.palette[name].idx)

    def __getitem__(self, name: Union[str, int]) -> int:
        return self.__getattr__(name)

    def decode_attr(self, key, default=A_NORMAL):
        """Return attr by code."""

        if isinstance(key, int):
            return key

        return self.attr_map.get(key, default)
