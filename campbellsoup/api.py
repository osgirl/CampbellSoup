# (c) 2014 Julian Gonggrijp (j.gonggrijp@gmail.com)

"""
    Application routes that serve the API.
"""

import flask

from .models import *
from .queries import *

api = flask.Blueprint('API', __name__)

@api.route('/')
def index ( ):
    return 'Hello, World!'
