# (c) 2018 Julian Gonggrijp

from itertools import groupby
import datetime

import pytest

from .models import Person, Account, Activation


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


@pytest.fixture
def hundred_persons_fix():
    return (Person(short_name=num, full_name=num) for num in range(100))


@pytest.fixture
def hundred_accounts_fix(hundred_persons_fix):
    return (Account(person=person) for person in hundred_persons_fix)


@pytest.fixture
def hundred_activations_in_db_fix(app_db_fix, hundred_accounts_fix):
    app, db = app_db_fix
    activations = []
    for account in hundred_accounts_fix:
        activation = Activation(account=account)
        activations.append(activation)
        db.session.add(activation)
        db.session.commit()
    return activations


def test_unique_activation_token(hundred_activations_in_db_fix):
    # Fuzz test: tokens will be different every time.
    tokens = sorted(map(lambda c: c.token, hundred_activations_in_db_fix))
    token_groups = list(groupby(tokens))
    assert len(tokens) == 100
    assert len(token_groups) == 100


def test_tomorrow(hundred_activations_in_db_fix):
    now = datetime.datetime.now()
    first_expiry = min(hundred_activations_in_db_fix, key=lambda c: c.expires)
    last_expiry = max(hundred_activations_in_db_fix, key=lambda c: c.expires)
    assert first_expiry.expires - now >= datetime.timedelta(days=1, seconds=-10)
    assert last_expiry.expires - now <= datetime.timedelta(days=1, seconds=10)
