# (c) 2017, 2018 Julian Gonggrijp

"""
    Definition of the API endpoints, based on Flask-Restless.
"""

import flask_restless as rest

from .models import *


def create_api(app, db):
    """ Factory function for the Flask-Restless APIManager. """
    manager = rest.APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(Test, methods=['GET'])
    return manager
