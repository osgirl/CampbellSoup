# (c) 2017, 2018 Julian Gonggrijp

"""
    Definition of the API endpoints, based on Flask-Restless.
"""

import http.client as status

from flask import request, jsonify, Blueprint
import flask_restless as rest
from flask_restless.helpers import to_dict  # undocumented
from flask_login import login_user, login_required, logout_user

from .models import *

# This needs to coincide with the default value for the url_prefix
# parameter of flask_restless.APIManager.create_api_blueprint.
REST_API_PREFIX = '/api'

# JSON APIs not based on sqla models need to be created manually.
auth = Blueprint('API-Auth', __name__, url_prefix=REST_API_PREFIX)


def create_api(app, db):
    """ Factory function for the Flask-Restless APIManager. """
    manager = rest.APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(Test, methods=['GET'])
    app.register_blueprint(auth)
    return manager


@auth.route('/login', methods=('POST',))
def login():
    if not request.is_json:
        return jsonify(
            error='Request must be JSON encoded.',
        ), status.BAD_REQUEST
    try:
        json = request.get_json()
    except:
        return jsonify(error='JSON data are malformed.'), status.BAD_REQUEST
    try:
        email, password = json['email'], json['password']
    except KeyError as error:
        return jsonify({error.args[0]: 'Field missing.'}), status.BAD_REQUEST
    account = Account.query.filter_by(email_address=email).first()
    if account is None or not account.verify_password(password):
        return jsonify(
            error='User does not exist or password is invalid.',
        ), status.UNAUTHORIZED
    login_user(account)
    return jsonify(to_dict(account, include=(
        'id',
        'email_address',
    ), deep={
        'role': {},
        'person': {},
    }))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return '', status.RESET_CONTENT
