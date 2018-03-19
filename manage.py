# (c) 2016, 2018 Julian Gonggrijp

import logging

from flask_script import Manager, prompt, prompt_pass
from flask_migrate import MigrateCommand

from campbellsoup import create_application
from campbellsoup.import_command import import_manager
from campbellsoup.models import db, Person, Account

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


@manager.command
def create_superuser():
    """ Create a superuser for the application. """
    while True:
        alias = prompt('Alias')
        person = Person.query.filter_by(short_name=alias).first()
        if not (person and person.account): break
        print('Sorry, that alias is already taken. Please try again.')
    if not person:
        person = Person(short_name=alias, full_name=alias)
    while True:
        email = prompt('Email')
        if not Account.query.filter_by(email_address=email).first(): break
        print('Sorry, that email address is already taken. Please try again.')
    account = Account(person=person, email_address=email)
    while True:
        password = prompt_pass('Password')
        password_again = prompt_pass('Password (again)')
        if password_again == password: break
        print('Sorry, the passwords didn\'t match. Please try again.')
    account.password = password
    db.session.add(account)
    db.session.commit()


if __name__ == '__main__':
    root_logger.addHandler(handler)
    manager.run()
