# (c) 2014, 2016, 2017 Julian Gonggrijp

"""
    CampbellSoup, the web-based archive of Campbell test questions.
    
    campbellsoup.create_application takes a configuration object and
    returns a Werkzeug WSGI application that can be deployed on a web
    server, or run directly for testing on localhost. The
    configuration object should at the very least include SECRET_KEY
    and SQLALCHEMY_DATABASE_URI.
"""

import flask
from flask_migrate import Migrate

from .models import db
from .api import api
from .frontend import frontend
from . import defaults


migrate = Migrate()


def create_application(config=defaults, create_db=False):
    """ Return a Werkzeug-flavoured WSGI application. """
    app = flask.Flask(__name__)
    if type(config) in (str, bytes):
        app.config.from_pyfile(config)
    else:
        app.config.from_object(config)
    models.db.init_app(app)
    if create_db:
        db.create_all(app=app)  # passing application because of context
    migrate.init_app(app, db)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(
        frontend,
        # Next two lines may seem redundant, but turned out necessary
        static_folder=frontend.static_folder,
        static_url_path=frontend.static_url_path,
    )
    return app
