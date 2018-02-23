# (c) 2018 Julian Gonggrijp

from random import Random
from string import printable

import pytest


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
