# (c) 2017 Julian Gonggrijp

import flask

frontend = flask.Blueprint(
    'Frontend',
    __name__,
    static_folder='../.tmp',
    static_url_path='/static',
)


@frontend.route('/')
def index():
    return frontend.send_static_file('index.html')
