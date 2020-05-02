"""Curses window object."""

import curses


def create_window(
    x: int, y: int, begin_x: int = 0, begin_y: int = 0, init: bool = False
):
    """Initialize curses, make and return window."""

    if init:
        curses.initscr()
        curses.start_color()

    screen = curses.newwin(y, x, begin_x, begin_y)
    screen.keypad(0)
    screen.nodelay(1)

    if init:
        curses.noecho()
        curses.cbreak()
        try:
            curses.curs_set(0)
        except curses.error:
            # old terminals may have no cursor modes support
            pass

    return screen


def deinit_window(screen, deinit: bool = True):
    """Destroy window, deinit curses, make console changes back."""

    screen.nodelay(0)
    screen.keypad(0)

    if deinit:
        curses.nocbreak()
        curses.echo()
        try:
            curses.curs_set(1)
        except curses.error:
            # old terminals may have no cursor modes support
            pass

        curses.endwin()
