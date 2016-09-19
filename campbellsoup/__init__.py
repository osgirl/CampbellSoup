# (c) 2014 Julian Gonggrijp (j.gonggrijp@gmail.com)

"""
    CampbellSoup, the web-based archive of Campbell test questions.
    
    campbellsoup.create_application takes a configuration object and
    returns a Werkzeug WSGI application that can be deployed on a web
    server, or run directly for testing on localhost. The
    configuration object should at the very least include SECRET_KEY
    and SQLALCHEMY_DATABASE_URI.
"""

import flask

from .models import db
from .api import api
from . import defaults


def create_application(config=defaults):
    """ Return a Werkzeug-flavoured WSGI application. """
    app = flask.Flask(__name__)
    if type(config) in (str, bytes):
        app.config.from_pyfile(config)
    else:
        app.config.from_object(config)
    models.db.init_app(app)
    db.create_all(app = app)  # passing application because of context
    app.register_blueprint(api)
    return app
