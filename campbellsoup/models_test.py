# (c) 2018 Julian Gonggrijp

import pytest

from .models import Account


@pytest.fixture
def account_password_fix(person_fix):
    account = Account(person=person_fix)
    password = 'banana'
    return person_fix, account, password


def test_Account_password_storage(account_password_fix):
    person, account, password = account_password_fix
    assert account.password_hash is None
    with pytest.raises(AttributeError):
        assert account.password == password
    account.password = password
    assert account.password_hash is not None
    assert account.password_hash != ''
    assert account.password_hash != password
    with pytest.raises(AttributeError):
        assert account.password == password
    assert account.verify_password(password)


def test_Account_password_invalid(account_password_fix, random_password_fix):
    # This is a fuzz test: every time pytest runs, 15 different
    # `random_password_fix`es are tried against this test. Eventually,
    # all possible passwords will have been tested. ;-)
    person, account, password = account_password_fix
    account.password = password
    assert not account.verify_password(random_password_fix)
