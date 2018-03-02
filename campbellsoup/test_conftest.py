# (c) 2018 Julian Gonggrijp

""" Sometimes fixtures need to be tested, too. """


def example(left, right):
    return left + right


def test_create_spy(create_spy):
    assert example(1, 2) == 3
    spy = create_spy('campbellsoup.test_conftest.example')
    assert example(3, 4) == None
    assert example(5, 6) == None
    assert example(this='suddenly possible') == None
    assert len(spy) == 3
    assert spy[0].args == (3, 4)
    assert spy[0].kwargs == {}
    assert spy[1].args == (5, 6)
    assert spy[2].args == ()
    assert spy[2].kwargs == {'this': 'suddenly possible'}


def test_create_spy_callthrough(create_spy):
    spy = create_spy('campbellsoup.test_conftest.example', callthrough=example)
    assert example(3, 4) == 7
    assert len(spy) == 1
    assert spy[0].args == (3, 4)
