# (c) 2014 Julian Gonggrijp (j.gonggrijp@gmail.com)

"""
    Queries into the database, as abstracted by (Flask-)SQLAlchemy.
"""

from datetime import date

from .models import *


# 3. De voorgeschiedenis van een vraag kan opgezocht worden. Dat wil
# zeggen dat oude versies opgevraagd kunnen worden. Wanneer vragen
# samengevoegd zijn moet dit hiermee ook duidelijk worden.

def familynet(question):
    pass
    # will have to be recursive and rely both on a set and a graph
    # datastructure (i.e. a dictionary of lists)


def lastused(question):
    pass
    # will need to rely on familynet(question) and memoize its result
    # for the entire network


# 2. Er kunnen vragen gezocht worden die als inspiratiebron voor
# nieuwe vragen kunnen dienen. (zoeken op: thema, niveau, auteur)

def question_filter_query(final_only = False, initial_only = False, **kwargs):
    q = Question.query
    if 'topics' in kwargs:
        q = q.filter(Question.topics.any(Topic.in_(kwargs['topics'])))
    if 'authors' in kwargs:
        q = q.filter(Question.author.in_(kwargs['authors']))
    if 'levels' in kwargs:
        q = q.filter(Question.level.in_(kwargs['levels']))
    if 'qualities' in kwargs:
        q = q.filter(Question.quality.in_(kwargs['qualities']))
    if 'categories' in kwargs:
        q = q.filter(Question.category.in_(kwargs['categories']))
    if final_only:
        q = (
            q.outer_join(*Question.descendants.attr, aliased = True)
            .filter(Question.id == None)  # no descendants
            .reset_joinpoint()
        )
    if initial_only:
        q = (
            q.outer_join(*Questions.ancestors.attr, aliased = True)
            .filter(Question.id == None)  # no descendants
            .reset_joinpoint()
        )
    if 'word' in kwargs:
        q = q.filter(Question.text.like('%' + kwargs['word'] + '%'))
    if 'source' in kwargs:
        q = q.filter(Question.bibliography.like('%' + kwargs['source'] + '%'))
    return q


# 1. Bruikbare oude vragen kunnen gezocht worden voor hergebruik in
# nieuwe toetsen. (zoeken op: lang niet gebruikt, onderwerp/hoofdstuk,
# niveau van een vraag)

def filter_reusable(query, date_limit):
    candidates = query.all()
    shortlist = []
    for c in candidates:
        if lastused(c) < date_limit:
            shortlist.append(c)
    return shortlist
