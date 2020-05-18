"""Text image definitions and manipulation routines."""

import curses

from dataclasses import dataclass
from itertools import zip_longest
from typing import List, Optional

import eaf
import toml

from xo1.color import Pair, Palette


@dataclass
class Textel:
    """TExt teXTure ELement.

    Representation of single element of surface.
    """

    char: str
    color: str
    attrs: List[str]
    pos: eaf.Vec3 = None

    @property
    def attr(self) -> int:
        """Calculate and return curses attr for char rendering.

        This property must be used by renderer at time, when application and
        loop are created and initialized, so this property tightly connected to
        running application instance.
        """

        palette = eaf.app.current().palette

        color = palette["default" if self.color is None else self.color]

        for attr in self.attrs or []:
            attr = palette.decode_attr(attr)

            color |= attr

        return color


class Surface(eaf.Image):
    """Representation of text graphics object, somewhat like "text texture".

    Layered object, that contains 3 layers:
    * `image` - image consisting of characters
    * `color` - encoded colors of each character corresponding to image
    * `attr` - additional attributes and their combinations, also mapped to image

    Attr layer may consist of several layers that will be merged together.
    """

    @dataclass
    class Raw:
        """Raw surface layer data object.

        Has minimum set of validations.
        """

        image: List[str]
        color: List[str]
        attr: List[List[str]]

        def __post_init__(self):
            self.color = self.color or []
            self.attr = self.attr or []

    class Malformed(Exception):
        def __init__(self, name, reason):
            super().__init__(f"Surface '{name}' malformed: {reason}.")

    __slots__ = ["_image", "_width", "_height", "_name"]

    def __init__(self, image, color=None, attr=None, name="untitled"):
        self._name = name

        self.check_image(image)

        self._raw = Surface.Raw(image, color, attr)

        self._width = len(self.raw.image[0]) if self.raw.image else 0
        self._height = len(self.raw.image)

        self._image = [
            [
                Textel(char, color, attr,)
                for char, color, attr in zip_longest(
                    char_row, color_row or [], attr_row or []
                )
            ]
            for char_row, color_row, attr_row in zip_longest(
                self.raw.image, self.raw.color, self.raw.attr
            )
        ]

    def check_image(self, image):
        """Check image."""

        widths = list(map(len, image))
        for width in widths[1:] or []:
            if widths[0] != width:
                raise Surface.Malformed(self.name, "line widths must be equal")

    @classmethod
    def from_file(cls, filename: str):
        tex = TomlFile.load(filename)

        return cls(tex.raw.image, tex.raw.color, tex.raw.attr, tex.name)

    @property
    def raw(self):
        """Raw surface data."""

        return self._raw

    @property
    def image(self):
        """Image layer."""

        return self._image

    @property
    def height(self):
        """Height of the surface.

        :getter: yes
        :setter: no
        :type: integer
        """
        return self._height

    @property
    def width(self):
        """Width of the surface.

        :getter: yes
        :setter: no
        :type: integer
        """
        return self._width

    @property
    def name(self) -> str:
        """Image name getter."""

        return self._name

    def __iter__(self):

        return next(self)

    def __next__(self):
        for y, row in enumerate(self.image):
            for x, textel in enumerate(row):
                textel.pos = eaf.Vec3(x, y)
                yield textel


class TomlFile:
    """TOML parser of Surface. Contains raw fields.

    Layers must be represented as list of strings.
    """

    def __init__(
        self,
        raw_surface_data: Surface.Raw,
        name: Optional[str] = None,
        filename: Optional[str] = None,
    ):
        self.raw = raw_surface_data
        self.name = name
        self.filename = filename

        if not isinstance(self.raw.image, list):
            raise Surface.Malformed(
                self.filename, "image layer must be list of strings"
            )

        if not isinstance(self.raw.color, list):
            raise Surface.Malformed(
                self.filename, "color layer must be list of strings"
            )

        if not isinstance(self.raw.attr, list):
            raise Surface.Malformed(self.filename, "attr layer must be list of strings")

    def to_dict(self):
        """Serialize Surface to dict."""

        surface = {}

        if self.name:
            surface["meta"] = {
                "name": self.name,
            }

            surface["layers"]: {
                "image": self.raw.image,
                "color": self.raw.color,
                "attr": self.raw.attr,
            }

        return surface

    @classmethod
    def load(cls, filename: str):
        """Load surface from file."""

        raw_surface = toml.load(filename)

        return cls(
            name=raw_surface.get("meta").get("name", "Unnamed"),
            filename=filename,
            raw_surface_data=Surface.Raw(
                image=raw_surface["layers"]["image"],
                color=raw_surface["layers"].get("color", []),
                attr=raw_surface["layers"].get("attr", []),
            ),
        )

    def save_as(self, filename: str):
        """Dump Surface into TOML file."""

        toml.dump(self.to_dict(), filename)

    def save(self):
        """Save current file, if opened."""

        if self.filename:
            self.save_as(self.filename)

        raise IOError("File name was not provided.")
