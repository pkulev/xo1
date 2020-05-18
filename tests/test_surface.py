import pytest

from xo1.surface import (
    Surface,
    Textel,
)

IMAGE = r"""
    _
  =/ \=  
  /-A-\ 
|/ / \ \|  \
 \_\^/_/___/
  m   m
"""


def test_surface_negative():

    with pytest.raises(Surface.Malformed):
        Surface(["1", "12"])


def test_surface_attributes():
    surface = Surface(IMAGE)
    assert surface.height == len(IMAGE)
    assert surface.width == len(IMAGE[0])


def test_textel():
    textel = Textel("a", None, None)

    assert textel.char == "a"
    assert textel.color == None
    assert textel.attrs == None
