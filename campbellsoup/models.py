# (c) 2014, 2016 Julian Gonggrijp

"""
    ORM classes for all objects stored in the database.
    
    The models are defined using SQLAlchemy declarative, meaning that
    the ORM classes double as table definitions.
"""

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
import flask_sqlalchemy as fsqla

from .utilities import append_to, un_camelcase


__all__ = []

db = fsqla.SQLAlchemy()


def _integer_pkey():
    return db.Column(db.Integer, primary_key=True)


class Category(object):
    """
        Common pattern for models that divide something else into categories.
    """
    
    @declared_attr
    def __tablename__(cls):
        return un_camelcase(cls.__name__)

    id = _integer_pkey()
    name = db.Column(db.String(30), nullable=False, unique=True)


class Family(object):
    """
        Common pattern for networks of parent-child relations.
        
        A family relation is the transitive symmetric reflexive
        closure of a parent-child relation. A subclass of Family
        represents the partition into equivalence classes of such a
        family relation. An instance of such a subclass represents a
        single equivalence class.
        
        if A parent B: A family B and B family A
        if A family B and B family C: A family C
        A family B <--> A.family_id == B.family_id
    """
    
    @declared_attr
    def __tablename__(cls):
        return un_camelcase(cls.__name__)

    id = _integer_pkey()


@append_to(__all__)
class UserRole(db.Model, Category):
    """ Category of user, e.g. admin or inactive user. """


@append_to(__all__)
class Person(db.Model):
    """ Person, which may be both an application user and a question author. """
    
    id = _integer_pkey()
    short_name = db.Column(db.String(30), nullable=False, unique=True)
    full_name = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.ForeignKey('user_role.id'))
    email_address = db.Column(db.String(30))
    password_hash = db.Column(db.String(30))
    
    role = db.relationship('UserRole', backref='users')


@append_to(__all__)
class Revision(db.Model):
    """ Changeset to the database with author and date. """
    
    id = _integer_pkey()
    author_id = db.Column(db.ForeignKey('person.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    commit_msg = db.Column(db.Text)
    
    author = db.relationship('Person', backref='revisions')


@append_to(__all__)
class Book(db.Model):
    """ Possible container of knowledge that may be tested. """

    id = _integer_pkey()
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    edition = db.Column(db.String(30))
    year = db.Column(db.Integer)
    
    topics = association_proxy('topic_bindings', 'topic')


@append_to(__all__)
class Topic(db.Model):
    """ Possible topic for questions, independent of Book. """

    id = _integer_pkey()
    name = db.Column(db.String(60), nullable=False, unique=True)
    
    books = association_proxy('book_bindings', 'book')
    questions = association_proxy('question_bindings', 'question')
    tests = association_proxy('test_bindings', 'test')


@append_to(__all__)
class TopicBookBinding(db.Model):
    """ Where in a particular book, a particular topic is addressed. """
    
    topic_id = db.Column(db.ForeignKey('topic.id'), primary_key=True)
    book_id = db.Column(db.ForeignKey('book.id'), primary_key=True)
    chapter = db.Column(db.String(30))
    section = db.Column(db.String(30))
    figure = db.Column(db.String(30))
    table = db.Column(db.String(30))
    page = db.Column(db.String(30))
    
    topic = db.relationship('Topic', backref='book_bindings')
    book = db.relationship('Book', backref='topic_bindings')


@append_to(__all__)
class FigureKind(db.Model, Category):
    """ Category of use for figures, such as answerfigure. """


@append_to(__all__)
class FigureTree(db.Model, Family):
    """ Set of all versions of a figure. """


@append_to(__all__)
class Figure(db.Model):
    """ Figure that may appear anywhere in the test. """
    
    id = _integer_pkey()
    revision_id = db.Column(db.ForeignKey('revision.id'), nullable=False)
    kind_id = db.Column(db.ForeignKey('figure_kind.id'), nullable=False)
    tree_id = db.Column(db.ForeignKey('figure_tree.id'), nullable=False)
    ancestor_id = db.Column(db.ForeignKey('figure.id'))
    filename = db.Column(db.String(30), nullable=False)
    mimetype = db.Column(db.String(30), nullable=False)
    contents = db.Column(db.LargeBinary, nullable=False)
    
    revision = db.relationship('Revision', backref='figures')
    kind = db.relationship('FigureKind', backref='figures')
    tree = db.relationship('FigureTree', backref='figures')
    ancestor = db.relationship('Figure', backref='descendants')
    introductions = association_proxy('intro_bindings', 'introduction')
    questions = association_proxy('question_bindings', 'question')


@append_to(__all__)
class Introduction(db.Model):
    """ Piece of introductory text that may precede questions. """
    
    id = _integer_pkey()
    revision_id = db.Column(db.ForeignKey('revision.id'), nullable=False)
    text = db.Column(db.Text)
    source_code = db.Column(db.Text)
    
    revision = db.relationship('Revision', backref='introductions')
    groups = association_proxy('group_bindings', 'group')
    figures = association_proxy('figure_bindings', 'figure')


@append_to(__all__)
class IntroductionFigureBinding(db.Model):
    """ Association between a figure and an introductory text. """
    
    intro_id = db.Column(db.ForeignKey('introduction.id'), primary_key=True)
    figure_id = db.Column(db.ForeignKey('figure.id'), primary_key=True)
    # reverse index may be useful
    
    introduction = db.relationship('Introduction', backref='figure_bindings')
    figure = db.relationship('Figure', backref='intro_bindings')


@append_to(__all__)
class QuestionKind(db.Model, Category):
    """ Type of question: multiple choice, pairing, etcetera. """


@append_to(__all__)
class QuestionStatus(db.Model, Category):
    """ Status of progress of a Question: stub, draft, complete, etcetera. """


@append_to(__all__)
class QuestionNetwork(db.Model, Family):
    """ Set of all versions and variants of a question. """


@append_to(__all__)
class Question(db.Model):
    """
        Single version of a question.
        
        Linked to previous and subsequent versions in a Git-like way.
    """
    
    id = _integer_pkey()
    revision_id = db.Column(db.ForeignKey('revision.id'), nullable=False)
    status_id = db.Column(db.ForeignKey('question_status.id'), nullable=False)
    kind_id = db.Column(db.ForeignKey('question_kind.id'))
    network_id = db.Column(
        db.ForeignKey('question_network.id'),
        nullable = False )
    text = db.Column(db.Text)
    answer = db.Column(db.Text)
    notes = db.Column(db.Text)  # by the author, not discussion
    bibliography = db.Column(db.Text)
    difficulty = db.Column(db.Enum('low', 'average', 'high', name='difficulty'))
    quality = db.Column(db.Enum('low', 'average', 'high', name='quality'))
    source_code = db.Column(db.Text)
    
    revision = db.relationship('Revision', backref='questions')
    status = db.relationship('QuestionStatus', backref='questions')
    kind = db.relationship('QuestionKind', backref='questions')
    network = db.relationship('QuestionNetwork', backref='questions')
    topics = association_proxy('topic_bindings', 'topic')
    figures = association_proxy('figure_bindings', 'figure')
    groups = association_proxy('group_bindings', 'group')
    ancestors = association_proxy('parent_bindings', 'parent')
    descendants = association_proxy('child_bindings', 'child')


@append_to(__all__)
class QuestionHistory(db.Model):
    """
        Graph edge of the ancestry network of single questions.
        
        Versions may be forked and merged, so parent-child is potentially
        a many-to-many relationship.
    """
    
    parent_id = db.Column(db.ForeignKey('question.id'), primary_key=True)
    child_id = db.Column(db.ForeignKey('question.id'), primary_key=True)
    
    parent = db.relationship('Question', backref='child_bindings')
    child = db.relationship('Question', backref='parent_bindings')


@append_to(__all__)
class QuestionTopicBinding(db.Model):
    """ Association between a question and a topic. """
    
    question_id = db.Column(db.ForeignKey('question.id'), primary_key=True)
    topic_id = db.Column(db.ForeignKey('topic.id'), primary_key=True)
    # also needs a reverse index
    
    question = db.relationship('Question', backref='topic_bindings')
    topic = db.relationship('Topic', backref='question_bindings')


@append_to(__all__)
class QuestionFigureBinding(db.Model):
    """ Association between a question and a figure. """
    
    question_id = db.Column(db.ForeignKey('question.id'), primary_key=True)
    figure_id = db.Column(db.ForeignKey('figure.id'), primary_key=True)
    # reverse index may be useful
    
    question = db.relationship('Question', backref='figure_bindings')
    figure = db.relationship('Figure', backref='question_bindings')


@append_to(__all__)
class Format(db.Model, Category):
    """ File format for question source code, e.g. LaTeXWriter. """


@append_to(__all__)
class GroupNetwork(db.Model, Family):
    """ Set of all versions and variants of a question group. """


@append_to(__all__)
class Group(db.Model):
    """
        Singe version of a question group.
        
        Linked to previous and subsequent versions in a Git-like way.
    """

    id = _integer_pkey()
    revision_id = db.Column(db.ForeignKey('revision.id'), nullable=False)
    format_id = db.Column(db.ForeignKey('format.id'))
    network_id = db.Column(db.ForeignKey('group_network.id'), nullable=False)
    title = db.Column(db.Text)
    
    revision = db.relationship('Revision', backref='groups')
    format = db.relationship('Format', backref='groups')
    network = db.relationship('GroupNetwork', backref='groups')
    introductions = association_proxy('intro_bindings', 'introduction')
    questions = association_proxy('question_bindings', 'question')
    tests = association_proxy('test_bindings', 'test')
    ancestors = association_proxy('parent_bindings', 'parent')
    descendants = association_proxy('child_bindings', 'child')


@append_to(__all__)
class GroupHistory(db.Model):
    """ Graph edge of the ancestry network of question groups. """
    
    parent_id = db.Column(db.ForeignKey('group.id'), primary_key=True)
    child_id = db.Column(db.ForeignKey('group.id'), primary_key=True)
    # also needs a reverse index
    
    parent = db.relationship('Group', backref='child_bindings')
    child = db.relationship('Group', backref='parent_bindings')


@append_to(__all__)
class GroupIntroductionBinding(db.Model):
    """ Position of an introduction paragraph in a group. """
    
    group_id = db.Column(db.ForeignKey('group.id'), primary_key=True)
    intro_id = db.Column(db.ForeignKey('introduction.id'), primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    # needs a composite uniqueness constraint
    
    group = db.relationship('Group', backref='intro_bindings')
    introduction = db.relationship('Introduction', backref='group_bindings')


@append_to(__all__)
class GroupQuestionBinding(db.Model):
    """ Clustering of single questions into question groups. """
    
    group_id = db.Column(db.ForeignKey('group.id'), primary_key=True)
    question_id = db.Column(db.ForeignKey('question.id'), primary_key=True)
    # might also need a reverse index
    order = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)
    
    group = db.relationship('Group', backref='question_bindings')
    question = db.relationship('Question', backref='group_bindings')


@append_to(__all__)
class Issue(db.Model):
    """ Ticket for any type of issue with any piece of content. """
    
    id = _integer_pkey()
    raised_id = db.Column(db.ForeignKey('revision.id'), nullable=False)
    resolved_id = db.Column(db.ForeignKey('revision.id'))  # null means open
    test_id = db.Column(db.ForeignKey('test.id'))
    groupnet_id = db.Column(db.ForeignKey('group_network.id'))
    questionnet_id = db.Column(db.ForeignKey('question_network.id'))
    figuretree_id = db.Column(db.ForeignKey('figure_tree.id'))
    assignee_id = db.Column(db.ForeignKey('person.id'))
    deadline = db.Column(db.DateTime)
    title = db.Column(db.Text, nullable=False)
    
    raised = db.relationship('Revision', backref='raised_issues')
    resolved = db.relationship('Revision', backref='resolved_issues')
    test = db.relationship('Test', backref='issues')
    groupnet = db.relationship('GroupNetwork', backref='issues')
    questionnet = db.relationship('QuestionNetwork', backref='issues')
    figuretree = db.relationship('FigureTree', backref='issues')
    assignee = db.relationship('Person', backref='assigned_issues')


@append_to(__all__)
class IssuePost(db.Model):
    """ Opening post of, or reply to, an issue. """
    
    id = _integer_pkey()
    issue_id = db.Column(db.ForeignKey('issue.id'), nullable=False)
    author_id = db.Column(db.ForeignKey('person.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    revision_id = db.Column(db.ForeignKey('revision.id'))  # optional reference
    message = db.Column(db.Text, nullable=False)
    
    issue = db.relationship('Issue', backref='posts')
    author = db.relationship('Person', backref='posts')
    revision = db.relationship('Revision', backref='revisions')


@append_to(__all__)
class Test(db.Model):
    """ A series of question groups, as presented to olympiad participants. """
    
    id = _integer_pkey()
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    topics = association_proxy('topic_bindings', 'topic')
    groups = association_proxy('group_bindings', 'group')


@append_to(__all__)
class TestTopicBinding(db.Model):
    """ Associates a test with a topic that is supposed to be covered. """
    
    test_id = db.Column(db.ForeignKey('test.id'), primary_key=True)
    topic_id = db.Column(db.ForeignKey('topic.id'), primary_key=True)
    # reverse index probably not necessary in this case
    
    test = db.relationship('Test', backref='topic_bindings')
    topic = db.relationship('Topic', backref='test_bindings')


@append_to(__all__)
class TestGroupBinding(db.Model):
    """ Order of a question group within a test. """
    
    test_id = db.Column(db.ForeignKey('test.id'), primary_key=True)
    group_id = db.Column(db.ForeignKey('group.id'), primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    
    test = db.relationship('Test', backref='group_bindings')
    group = db.relationship('Group', backref='test_bindings')

