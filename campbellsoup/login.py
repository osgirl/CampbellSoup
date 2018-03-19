# (c) 2018 Julian Gonggrijp

import http.client as status

from flask import jsonify
from flask_login import LoginManager

from .models import Account


def create_login_manager():
    """ Factory function for an instance of LoginManager. """
    manager = LoginManager()
    manager.user_loader(get_account_by_unicode)
    manager.session_protection = 'strong'
    manager.unauthorized_handler(unauthorized_handler)
    return manager


def get_account_by_unicode(user_id):
    """ Returns the Account instance with given `user_id` or None. """
    return Account.query.get(user_id)


def unauthorized_handler():
    """ Standard response for views that require authentication. """
    return jsonify(error='Login required.'), status.UNAUTHORIZED
