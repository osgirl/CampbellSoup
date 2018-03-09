# (c) 2018 Julian Gonggrijp

import http.client as status

import pytest

from flask import json
from flask_login import current_user

from .models import Account, Person

JSON = 'application/json'
VALID_EMAIL = 'bla@bla.com'
VALID_PASSWORD = '12345'
SHORT_NAME = 'test'
FULL_NAME = 'test test'

LOGIN_CASES = {
    'nodata': ({}, status.BAD_REQUEST, {'email': 'Field missing.'}),
    'nopw': (
        {'email': 'bla@bla.com'},
        status.BAD_REQUEST,
        {'password': 'Field missing.'},
    ),
    'unknown': (
        {'email': 'bla' + VALID_EMAIL, 'password': VALID_PASSWORD},
        status.UNAUTHORIZED,
        {'error': 'User does not exist or password is invalid.'},
    ),
    'invalidpw': (
        {'email': VALID_EMAIL, 'password': VALID_PASSWORD + 'oops'},
        status.UNAUTHORIZED,
        {'error': 'User does not exist or password is invalid.'},
    ),
    'success': (
        {'email': VALID_EMAIL, 'password': VALID_PASSWORD},
        status.OK,
        {
            'id': 1,
            'email_address': VALID_EMAIL,
            'role': None,
            'person': {
                'id': 1,
                'short_name': SHORT_NAME,
                'full_name': FULL_NAME,
            },
        },
    ),
}


@pytest.fixture
def person_fix():
    return Person(short_name=SHORT_NAME, full_name=FULL_NAME)


@pytest.fixture
def account_fix(app_db_fix, person_fix):
    app, db = app_db_fix
    account = Account(person=person_fix, email_address=VALID_EMAIL)
    account.password = VALID_PASSWORD
    db.session.add(account)
    db.session.commit()
    return account


@pytest.fixture(params=LOGIN_CASES.values(), ids=list(LOGIN_CASES.keys()))
def login_fix(request):
    return request.param


def test_login(app_db_fix, account_fix, login_fix):
    app, db = app_db_fix
    post_data, status_code, response_data = login_fix
    with app.test_client() as client:
        response = client.post(
            '/api/login',
            data=json.dumps(post_data),
            content_type=JSON,
        )
        if status_code == status.OK:
            assert current_user == account_fix
            assert not current_user.is_anonymous
        else:
            assert current_user.get_id() == None
            assert current_user.is_anonymous
    assert response.status_code == status_code
    assert response.mimetype == JSON
    assert json.loads(response.data) == response_data


def test_logout(app_db_fix, account_fix):
    app, db = app_db_fix
    with app.test_client() as client:
        login = client.post(
            '/api/login',
            data=json.dumps(LOGIN_CASES['success'][0]),
            content_type=JSON,
        )
        assert current_user == account_fix
        cookie = login.headers.get('Set-Cookie')
        logout = client.get('/api/logout', headers={'Cookie': cookie})
        assert current_user.is_anonymous
    assert logout.status_code == status.RESET_CONTENT
    assert not getattr(logout, 'data')
