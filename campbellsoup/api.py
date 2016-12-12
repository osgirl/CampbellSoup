# (c) 2014, 2016 Julian Gonggrijp

"""
    Application routes that serve the API.
"""

import flask

from .models import *
from .queries import *

api = flask.Blueprint('API', __name__)


@api.route('/')
def index():
    return 'TODO: write an API.'
