# (c) 2017 Julian Gonggrijp

from flask_script import Manager

from .parsers import document
import .models as m


def process_options(app, **kwargs):
    """ Obligatory, possibly useful in the future (see Flask-Script docs). """
    pass


# Attach to a parent Manager in order to use
import_manager = Manager(process_options)


@import_manager.command
def import_directory(paths, year=None):
    """ Import all question group files in globbing pattern `path`. """
    pass
