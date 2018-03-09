# (c) 2018 Julian Gonggrijp

from flask_login import LoginManager

from .models import Account


def create_login_manager():
    """ Factory function for an instance of LoginManager. """
    manager = LoginManager()
    manager.user_loader(get_account_by_unicode)
    manager.session_protection = 'strong'
    return manager


def get_account_by_unicode(user_id):
    """ Returns the Account instance with given `user_id` or None. """
    return Account.query.get(user_id)
