# (c) 2016 Julian Gonggrijp

from .utilities import *


def test_un_camelcase():
    assert un_camelcase('CampbellSoupX') == 'campbell_soup_x'
    assert un_camelcase('NBOCampbellToets') == 'n_b_o_campbell_toets'


def test_append_to():
    __all__ = []
    class Example(object):
        pass
    @append_to(__all__)
    class Illustration(object):
        pass
    @append_to(__all__)
    def foo():
        pass
    def bar():
        pass
    assert __all__ == ['Illustration', 'foo']
