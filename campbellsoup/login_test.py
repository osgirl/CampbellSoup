# (c) 2018 Julian Gonggrijp

import http.client as status

from flask import make_response, json
from flask_login import login_required

from .login import *


def test_unauthorized_handler(app_fix):
    @app_fix.route('/test')
    @login_required
    def view():
        return ''
    response = app_fix.test_client().get('/test')
    assert response.status_code == status.UNAUTHORIZED
    assert response.mimetype == 'application/json'
    assert json.loads(response.data) == {'error': 'Login required.'}
