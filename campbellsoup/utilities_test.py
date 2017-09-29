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


def test_maybe():
    tester = {
        'banana': [
            0,
            'x',
            [1, 2, 3],
            {
                'deep_banana': {'value': 'deeper_banana'},
            }
        ],
        'orange': [],
    }
    assert len(maybe(tester, 'banana')) == 4
    assert maybe(tester, 'banana', 0) == 0
    assert maybe(tester, 'banana', 1) == 'x'
    assert maybe(tester, 'banana', 1, 0) == 'x'
    assert maybe(tester, 'banana', 1, 1) == None
    assert maybe(tester, 'banana', 2) == [1, 2, 3]
    assert maybe(tester, 'banana', 2, 2) == 3
    assert maybe(tester, 'banana', 2, 3) == None
    assert maybe(tester, 'banana', 3, 'deep_banana', 'value') == 'deeper_banana'
    assert maybe(tester, 'banana', 3, 'deep_banana', 'other') == None
    assert maybe(tester, 'banana', 4) == None
    assert maybe(tester, 'orange') == []
    assert maybe(tester, 'orange', 3) == None
    assert maybe(tester, 'orange', 3, fallback='') == ''
    assert maybe(tester, 'kiwi') == None
    assert maybe(tester, 'kiwi', fallback=10) == 10
