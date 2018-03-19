# (c) 2018 Julian Gonggrijp

import http.client as status

from flask import make_response, json
from flask_login import login_required

from .conftest_constants import JSON
from .login import *


def test_get_account_by_unicode(account_db_fix):
    id = account_db_fix.id
    nonexistent_id = 10000
    assert get_account_by_unicode(str(id)) == account_db_fix
    assert get_account_by_unicode(str(nonexistent_id)) == None


def test_unauthorized_handler(app_fix):
    @app_fix.route('/test')
    @login_required
    def view():
        return ''
    response = app_fix.test_client().get('/test')
    assert response.status_code == status.UNAUTHORIZED
    assert response.mimetype == JSON
    assert json.loads(response.data) == {'error': 'Login required.'}
