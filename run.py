#! /usr/bin/env python2
# (c) 2014 Julian Gonggrijp (j.gonggrijp@gmail.com)

"""
    Run a testing version of the application on localhost.
    
    To view the web interface, visit http://localhost:5000.
"""

import campbellsoup


class Config:
    SECRET_KEY = '1234567890qwertyuiopasdfghjkl'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///debug.db'


if __name__ == '__main__':
    app = campbellsoup.create_application(Config)
    app.testing = True
    app.debug = True
    app.run()
