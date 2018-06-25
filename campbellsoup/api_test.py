# (c) 2018 Julian Gonggrijp

import http.client as status

import pytest

from flask import json
from flask_login import current_user

from .conftest_constants import JSON, VALID_EMAIL, VALID_PASSWORD, SHORT_NAME, FULL_NAME, LIVE_TOKEN, EXPIRED_TOKEN, NONEXISTENT_TOKEN

VALID_LOGIN = {'email': VALID_EMAIL, 'password': VALID_PASSWORD}

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
        VALID_LOGIN,
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

ACTIVATION_CASES = {
    # scenario: (token, input, status, output),
    'unknown': (
        NONEXISTENT_TOKEN,
        VALID_LOGIN,
        status.NOT_FOUND,
        {'error': 'No activation with this token available.'},
    ),
    'expired': (
        EXPIRED_TOKEN,
        VALID_LOGIN,
        status.NOT_FOUND,
        {'error': 'No activation with this token available.'},
    ),
    'nodata': (
        LIVE_TOKEN,
        {},
        status.BAD_REQUEST,
        {'email': 'Field missing.'},
    ),
    'nopw': (
        LIVE_TOKEN,
        {'email': 'x@bla.com'},
        status.BAD_REQUEST,
        {'password': 'Field missing.'},
    ),
    'mismatch_email': (
        LIVE_TOKEN,
        {'email': 'x' + VALID_EMAIL, 'password': VALID_PASSWORD},
        status.UNAUTHORIZED,
        {'error': 'Credentials do not match previously provided values.'},
    ),
    'mismatch_pw': (
        LIVE_TOKEN,
        {'email': VALID_EMAIL, 'password': 'x' + VALID_PASSWORD},
        status.UNAUTHORIZED,
        {'error': 'Credentials do not match previously provided values.'},
    ),
    'success': (
        LIVE_TOKEN,
        VALID_LOGIN,
        status.NO_CONTENT,
        b'',
    ),
}


@pytest.fixture(params=LOGIN_CASES.values(), ids=list(LOGIN_CASES.keys()))
def login_fix(request):
    return request.param


def test_login(app_db_fix, account_db_fix, login_fix):
    app, db = app_db_fix
    post_data, status_code, response_data = login_fix
    with app.test_client() as client:
        response = client.post(
            '/api/login',
            data=json.dumps(post_data),
            content_type=JSON,
        )
        if status_code == status.OK:
            assert current_user == account_db_fix
            assert not current_user.is_anonymous
        else:
            assert current_user.get_id() == None
            assert current_user.is_anonymous
    assert response.status_code == status_code
    assert response.mimetype == JSON
    assert json.loads(response.data) == response_data


def test_logout(app_db_fix, account_db_fix):
    app, db = app_db_fix
    with app.test_client() as client:
        login = client.post(
            '/api/login',
            data=json.dumps(VALID_LOGIN),
            content_type=JSON,
        )
        assert current_user == account_db_fix
        cookie = login.headers.get('Set-Cookie')
        logout = client.get('/api/logout', headers={'Cookie': cookie})
        assert current_user.is_anonymous
    assert logout.status_code == status.RESET_CONTENT
    assert not getattr(logout, 'data')


def test_logout_unauthorized(app_db_fix):
    app, db = app_db_fix
    logout = app.test_client().get('/api/logout')
    assert logout.status_code == status.UNAUTHORIZED
    assert json.loads(logout.data) == {'error': 'Login required.'}


@pytest.fixture(
    params=ACTIVATION_CASES.values(),
    ids=list(ACTIVATION_CASES.keys()),
)
def activate_fix(request):
    return request.param


def test_activation(app_db_fix, activation_db_fix, activate_fix):
    app, db = app_db_fix
    token, request_data, status_code, response_data = activate_fix
    response = app.test_client().post(
        '/api/activate/' + token,
        data=json.dumps(request_data),
        content_type=JSON,
    )
    assert response.status_code == status_code
    if isinstance(response_data, bytes):
        assert response.data == response_data
    else:
        assert json.loads(response.data) == response_data


def test_activation_fixed_email(app_db_fix, activation_db_fix, random_email_fix):
    app, db = app_db_fix
    token, request_data, status_code, response_data = ACTIVATION_CASES['mismatch_email']
    request_data['email'] = random_email_fix
    response = app.test_client().post(
        '/api/activate/' + token,
        data=json.dumps(request_data),
        content_type=JSON,
    )
    assert response.status_code == status_code
    assert json.loads(response.data) == response_data


def test_activation_fixed_pw(app_db_fix, activation_db_fix, random_password_fix):
    app, db = app_db_fix
    token, request_data, status_code, response_data = ACTIVATION_CASES['mismatch_pw']
    request_data['password'] = random_password_fix
    response = app.test_client().post(
        '/api/activate/' + token,
        data=json.dumps(request_data),
        content_type=JSON,
    )
    assert response.status_code == status_code
    assert json.loads(response.data) == response_data


def test_activation_free_email(app_db_fix, account_fix, activation_db_fix, random_email_fix):
    app, db = app_db_fix
    account_fix.email_address = None
    account_fix.password_hash = None
    db.session.add(account_fix)
    db.session.commit()
    token, request_data, status_code, response_data = ACTIVATION_CASES['success']
    request_data['email'] = random_email_fix
    response = app.test_client().post(
        '/api/activate/' + token,
        data=json.dumps(request_data),
        content_type=JSON,
    )
    assert response.status_code == status_code
    assert response.data == response_data


def test_activation_free_pw(app_db_fix, account_fix, activation_db_fix, random_password_fix):
    app, db = app_db_fix
    account_fix.email_address = None
    account_fix.password_hash = None
    db.session.add(account_fix)
    db.session.commit()
    token, request_data, status_code, response_data = ACTIVATION_CASES['success']
    request_data['password'] = random_password_fix
    response = app.test_client().post(
        '/api/activate/' + token,
        data=json.dumps(request_data),
        content_type=JSON,
    )
    assert response.status_code == status_code
    assert response.data == response_data
