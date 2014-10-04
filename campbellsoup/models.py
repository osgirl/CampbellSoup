# (c) 2014 Julian Gonggrijp (j.gonggrijp@gmail.com)

"""
    ORM classes for all objects stored in the database.
    
    The models are defined using SQLAlchemy declarative, meaning that
    the ORM classes double as table definitions.
"""

from sqlalchemy.ext.associationproxy import association_proxy
import flask.ext.sqlalchemy as fsqla

from .utilities import append_to

__all__ = []

db = fsqla.SQLAlchemy()

@append_to(__all__)
class Person (db.Model):
    """ Person, which may be both an application user and a question author. """
    id = db.Column(db.Integer, primary_key = True)
    short_name = db.Column(db.String(15), nullable = False)
    full_name = db.Column(db.String(40), nullable = False)
    email_address = db.Column(db.String(30))
    password_hash = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, nullable = False)
    is_active = db.Column(db.Boolean, nullable = False)
    
@append_to(__all__)
class Book (db.Model):
    """ Possible container of knowledge that may be tested. """

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40), nullable = False)
    author = db.Column(db.String(40), nullable = False)
    edition = db.Column(db.Integer)
    year = db.Column(db.Integer)
    
    topics = association_proxy('topic_bindings', 'topic')
    
@append_to(__all__)
class Topic (db.Model):
    """ Possible topic for questions, independent of Book. """

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique = True)
    
    books = association_proxy('book_bindings', 'book')
    questions = association_proxy('question_bindings', 'question')
    tests = association_proxy('test_bindings', 'test')
    
@append_to(__all__)
class TopicBookBinding (db.Model):
    """ Where in a particular book, a particular topic is addressed. """
    
    topic_id = db.Column(db.ForeignKey('topic.id'), primary_key = True)
    book_id = db.Column(db.ForeignKey('book.id'), primary_key = True)
    chapter = db.Column(db.String(10))
    section = db.Column(db.String(10))
    figure = db.Column(db.String(10))
    table = db.Column(db.String(10))
    page = db.Column(db.String(20))
    
    topic = db.relationship('Topic', backref = 'book_bindings')
    book = db.relationship('Book', backref = 'topic_bindings')
    
@append_to(__all__)
class Figure (db.Model):
    """ Figure that may appear anywhere in the test. """
    
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(30), nullable = False)
    mimetype = db.Column(db.String(30), nullable = False)
    is_answerfigure = db.Column(db.Boolean)
    ancestor_id = db.Column(db.ForeignKey('figure.id'))
    contents = db.Column(db.BLOB, nullable = False)
    
    ancestor = db.relationship('Figure', backref = 'descendants')
    introductions = association_proxy('intro_bindings', 'introduction')
    questions = association_proxy('question_bindings', 'question')
    
@append_to(__all__)
class Introduction (db.Model):
    """ Piece of introductory text that may precede questions. """
    
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    source_code = db.Column(db.Text)
    
    groups = association_proxy('group_bindings', 'group')
    figures = association_proxy('figure_bindings', 'figure')
    
@append_to(__all__)
class IntroductionFigureBinding (db.Model):
    """ Association between a figure and an introductory text. """
    
    intro_id = db.Column(db.ForeignKey('introduction.id'), primary_key = True)
    figure_id = db.Column(db.ForeignKey('figure.id'), primary_key = True)
    # reverse index may be useful
    
    introduction = db.relationship('Introduction', backref = 'figure_bindings')
    figure = db.relationship('Figure', backref = 'intro_bindings')
    
@append_to(__all__)
class QuestionCategory (db.Model):
    """ Type of question: multiple choice, pairing, etcetera. """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    
@append_to(__all__)
class Question (db.Model):
    """
        Single version of a question.
        
        Linked to previous and subsequent versions in a Git-like way.
    """
    
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False)
    author_id = db.Column(db.ForeignKey('person.id'))
    category_id = db.Column(db.ForeignKey('question_category.id'))
    text = db.Column(db.Text)
    answer = db.Column(db.Text)
    bibliography = db.Column(db.Text)
    weight = db.Column(db.Integer)
    difficulty = db.Column(db.Enum('low', 'average', 'high'))
    quality = db.Column(db.Enum('low', 'average', 'high'))
    source_code = db.Column(db.Text)
    
    author = db.relationship('Person', backref = 'questions')
    category = db.relationship('QuestionCategory', backref = 'questions')
    topics = association_proxy('topic_bindings', 'topic')
    figures = association_proxy('figure_bindings', 'figure')
    groups = association_proxy('group_bindings', 'group')
    ancestors = association_proxy('parent_bindings', 'parent')
    descendants = association_proxy('child_bindings', 'child')
    
@append_to(__all__)
class QuestionHistory (db.Model):
    """
        Graph edge of the ancestry network of single questions.
        
        Versions may be forked and merged, so parent-child is potentially
        a many-to-many relationship.
    """
    
    parent_id = db.Column(db.ForeignKey('question.id'), primary_key = True)
    child_id = db.Column(db.ForeignKey('question.id'), primary_key = True)
    
    parent = db.relationship('Question', backref = 'child_bindings')
    child = db.relationship('Question', backref = 'parent_bindings')
    
@append_to(__all__)
class QuestionTopicBinding (db.Model):
    """ Association between a question and a topic. """
    
    question_id = db.Column(db.ForeignKey('question.id'), primary_key = True)
    topic_id = db.Column(db.ForeignKey('topic.id'), primary_key = True)
    # also needs a reverse index
    
    question = db.relationship('Question', backref = 'topic_bindings')
    topic = db.relationship('Topic', backref = 'question_bindings')
    
@append_to(__all__)
class QuestionFigureBinding (db.Model):
    """ Association between a question and a figure. """
    
    question_id = db.Column(db.ForeignKey('question.id'), primary_key = True)
    figure_id = db.Column(db.ForeignKey('figure.id'), primary_key = True)
    # reverse index may be useful
    
    question = db.relationship('Question', backref = 'figure_bindings')
    figure = db.relationship('Figure', backref = 'question_bindings')
    
@append_to(__all__)
class Format (db.Model):
    """ File format for question source code, e.g. LaTeXWriter. """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    
@append_to(__all__)
class Group (db.Model):
    """
        Singe version of a question group.
        
        Linked to previous and subsequent versions in a Git-like way.
    """

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False)
    author_id = db.Column(db.ForeignKey('person.id'))
    title = db.Column(db.String(30))
    format_id = db.Column(db.ForeignKey('format.id'))
    
    author = db.relationship('Person', backref = 'groups')
    format = db.relationship('Format', backref = 'groups')
    introductions = association_proxy('intro_bindings', 'introduction')
    questions = association_proxy('question_bindings', 'question')
    tests = association_proxy('test_bindings', 'test')
    ancestors = association_proxy('parent_bindings', 'parent')
    descendants = association_proxy('child_bindings', 'child')

@append_to(__all__)
class GroupHistory (db.Model):
    """ Graph edge of the ancestry network of question groups. """
    
    parent_id = db.Column(db.ForeignKey('group.id'), primary_key = True)
    child_id = db.Column(db.ForeignKey('group.id'), primary_key = True)
    # also needs a reverse index
    
    parent = db.relationship('Group', backref = 'child_bindings')
    child = db.relationship('Group', backref = 'parent_bindings')
    
@append_to(__all__)
class GroupIntroductionBinding (db.Model):
    """ Position of an introduction paragraph in a group. """
    
    group_id = db.Column(db.ForeignKey('group.id'), primary_key = True)
    intro_id = db.Column(db.ForeignKey('introduction.id'), primary_key = True)
    order = db.Column(db.Integer, nullable = False)
    # needs a composite uniqueness constraint
    
    group = db.relationship('Group', backref = 'intro_bindings')
    introduction = db.relationship('Introduction', backref = 'group_bindings')
    
@append_to(__all__)
class GroupQuestionBinding (db.Model):
    """ Clustering of single questions into question groups. """
    
    group_id = db.Column(db.ForeignKey('group.id'), primary_key = True)
    question_id = db.Column(db.ForeignKey('question.id'), primary_key = True)
    # might also need a reverse index
    order = db.Column(db.Integer, nullable = False)
    
    group = db.relationship('Group', backref = 'question_bindings')
    question = db.relationship('Question', backref = 'group_bindings')
    
@append_to(__all__)
class Test (db.Model):
    """ A series of question groups, as presented to olympiad participants. """
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    date = db.Column(db.Date, nullable = False)
    
    topics = association_proxy('topic_bindings', 'topic')
    groups = association_proxy('group_bindings', 'group')
    
@append_to(__all__)
class TestTopicBinding (db.Model):
    """ Association of a topic with a test. """
    
    test_id = db.Column(db.ForeignKey('test.id'), primary_key = True)
    topic_id = db.Column(db.ForeignKey('topic.id'), primary_key = True)
    # reverse index probably not necessary in this case
    
    test = db.relationship('Test', backref = 'topic_bindings')
    topic = db.relationship('Topic', backref = 'test_bindings')
    
@append_to(__all__)
class TestGroupBinding (db.Model):
    """ Order of a question group within a test. """
    
    test_id = db.Column(db.ForeignKey('test.id'), primary_key = True)
    group_id = db.Column(db.ForeignKey('group.id'), primary_key = True)
    order = db.Column(db.Integer, nullable = False)
    
    test = db.relationship('Test', backref = 'group_bindings')
    group = db.relationship('Group', backref = 'test_bindings')
    
