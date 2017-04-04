# (c) 2017 Julian Gonggrijp

import sys
import os
import os.path as op
from datetime import date

from flask_script import Manager

from .parsers import document, filename_parts
import .models as m


def process_options(app, **kwargs):
    """ Obligatory, possibly useful in the future (see Flask-Script docs). """
    pass


# Attach to a parent Manager in order to use
import_manager = Manager(process_options)


@import_manager.command
def import_test(directory, title=None, year=None, order_by_stdin=False):
    """ Import all question group and image files in `directory`. """
    if year is None:
        year = op.split(op.normpath(path))[1]
    if title is None:
        title = year
    test_date = date(int(year), 6, 1)
    if order_by_stdin:
        files = sys.stdin.readlines()
    else:
        files = sorted(os.listdir(directory), key=filename_order_key)
    os.chdir(directory)
    session = m.db.session
    try:
        me = get_auto_import_person(session)
        revision = m.Revision(author=me, date=datetime.now())
        test = m.Test(title=title, date=test_date)
        import_groups(files, test, revision, session)
        revision.date = datetime.now()
        revision.commit_msg = 'Auto import of test "{}"'.format(title)
        session.add_all([test, revision])
        session.commit()
    except:
        session.rollback()
        raise


def get_auto_import_person(session):
    """ Return the auto_import `Person`. Create if it does not exist. """
    me = session.query(m.Person).filter_by(
        short_name='auto_import',
    ).one_or_none()
    if me is None:
        me = m.Person(short_name='auto_import', full_name='Automated Import')
        session.add(me)
    return me


def import_groups(files, test, revision, session):
    """ Import `files` in the given order and add to `test`. """
    order = 1
    blocks = []   # blocks that mention figures
    figures = []  # that will fill the gaps in `blocks`
    for filename in files:
        if op.splitext(filename)[1] == '.txt':
            session.add_all(bind_figures(blocks, figures))
            blocks, figures = [], []
            try:
                text = open(filename).read()
            except ValueError:  # Silly Windows file
                text = open(filename, encoding='cp1252').read()
            group, blocks = import_textfile(text, revision, session)
            session.add(m.TestGroupBinding(test=test, group=group, order=order))
            order += 1
        else:
            figures.append(import_figure(filename, revision, session))
    session.add_all(bind_figures(blocks, figures))


def import_textfile(text, revision, session):
    """ Parse and import the contents of an archive textfile. """
    pass


def filename_order_key(name):
    """
        Returns a tuple reflecting the proper order of `name`.
    
        Use as sorting key function.
    """
    return filename_parts.parseString(op.splitext(name)[0], True).asList()
