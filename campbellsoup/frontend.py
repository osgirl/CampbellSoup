# (c) 2017 Julian Gonggrijp

import flask

frontend = flask.Blueprint(
    'Frontend',
    __name__,
)


@frontend.route('/')
def index():
    return frontend.send_static_file('index.html')
