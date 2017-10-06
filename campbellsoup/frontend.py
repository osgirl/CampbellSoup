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
    print(frontend.static_folder)
    print(frontend.static_url_path)
    print(flask.url_for('Frontend.static', filename='script/main.js'))
    return frontend.send_static_file('index.html')