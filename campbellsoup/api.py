# (c) 2014, 2016 Julian Gonggrijp

"""
    Application routes that serve the API.
"""

import flask

from .models import *
from .queries import *

api = flask.Blueprint('API', __name__, static_url_path='', static_folder='../.tmp')


@api.route('/')
def index():
    return flask.send_from_directory(api.static_folder, 'index.html')
