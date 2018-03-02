# (c) 2018 Julian Gonggrijp

from random import Random
from string import printable

import pytest

from . import create_application, db, defaults
from .models import Person


def generate_random_passwords(count=None, mean_length=12, seed=None):
    """ Generate `count` random passwords, or infinitely many if None. """
    prng = Random(seed)
    labda = 1 / mean_length
    if count is None:
        count = -1
    while count != 0:
        count -= 1
        length = round(prng.expovariate(labda))
        yield ''.join((prng.choice(printable) for i in range(length)))


@pytest.fixture(params=generate_random_passwords(15))
def random_password_fix(request):
    return request.param


class UnittestConfig:
    SECRET_KEY = 'poiuytrewqlkjhgfdsamnbvcxz'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in-memory
    SQLALCHEMY_TRACK_MODIFICATIONS = defaults.SQLALCHEMY_TRACK_MODIFICATIONS
    STATIC_FOLDER = defaults.STATIC_FOLDER
    STATIC_URL_PATH = defaults.STATIC_URL_PATH


@pytest.fixture
def app_fix():
    """ Provide an instance of the application with Flask's test_client. """
    app = create_application(UnittestConfig)
    app.testing = True
    return app


@pytest.fixture
def app_db_fix():
    """
        Like app_fix, but with the database fully set up and in context.
        
        Functions that use this fixture, inherit the application context in
        which the contents of the database are available. DO NOT create your
        own application context when using this fixture.
    """
    app = create_application(UnittestConfig, True)
    app.testing = True
    with app.app_context():
        db.session.begin(subtransactions=True)
        yield app, db
        db.session.rollback()


class Arguments(object):
    """ A simple class for holding function arguments in a readable way. """
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


class FunctionSpy(object):
    """ A fake function that keeps track of all calls to itself. """
    def __init__(self, callthrough=None):
        self.callthrough = callthrough
        self.calls = []
    
    def __call__(self, *args, **kwargs):
        self.calls.append(Arguments(args, kwargs))
        if callable(self.callthrough):
            return self.callthrough(*args, **kwargs)
    
    def __len__(self):
        return len(self.calls)
    
    def __getitem__(self, index):
        return self.calls[index]


@pytest.fixture
def create_spy(monkeypatch):
    """ Provide a function to create spies, similar to Jasmine. """
    def create(target, callthrough=None):
        """
            Replace the target callable with a FunctionSpy, return the latter.
            
            `target` should be a dotted import path as a string, with the last
            part being the callable to be spied upon.
            `callthrough` (optional) may be any callable to replace the
            spied-upon callable.
        """
        spy = FunctionSpy(callthrough)
        monkeypatch.setattr(target, spy)
        return spy
    return create


@pytest.fixture
def person_fix():
    """ Provides an instance of Person where the contents don't matter. """
    return Person(short_name='test', full_name='test test')
