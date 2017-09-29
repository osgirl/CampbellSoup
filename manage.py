# (c) 2016 Julian Gonggrijp

import logging

from flask_script import Manager
from flask_migrate import MigrateCommand

from campbellsoup import create_application
from campbellsoup.import_command import import_manager

root_logger = logging.getLogger()
handler = logging.StreamHandler()


def wrapper_factory(verbose, *args, **kwargs):
    """ Wrapper to handle parameters that create_application doesn't accept. """
    if verbose:
        root_logger.setLevel(logging.DEBUG)
    return create_application(*args, **kwargs)


manager = Manager(wrapper_factory)
manager.add_option('-c', '--config', dest='config')
manager.add_option('-v', '--verbose', action='store_true', dest='verbose')
manager.add_command('db', MigrateCommand)
manager.add_command('archive', import_manager)

if __name__ == '__main__':
    root_logger.addHandler(handler)
    manager.run()
