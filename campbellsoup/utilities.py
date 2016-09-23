# (c) 2014, 2016 Julian Gonggrijp

"""
    Useful abstractions that don't belong anywhere else.
"""

import re

camelcase_regex = re.compile(r'[A-Z][a-z0-9]*')


def un_camelcase(name):
    """
        Turn a camelcased name into a lowercase name with underscore separators.
    """
    return '_'.join(camelcase_regex.findall(name)).lower()


def append_to(__all__):
    """
        Class and function decorator to include the name in __all__.
        
        A common use case for __all__ is to mark a group of classes or
        functions that have something in common for wildcard export,
        while other classes or functions defined in the same module
        are to be exported, but not included in the wildcard. The set
        of to be included objects can be quite large and explicitly
        listing their names in __all__ means repeating yourself; this
        decorator solves that by automatically adding their names to
        __all__.

        Take note that the decorator can only be used for functions
        defined with def and for classes.
        
        >>> # module "wild"
        >>> __all__ = []
        >>> class Example (object):
        ...     pass
        >>> @append_to(__all__)
        ... class Illustration (object):
        ...     pass
        >>> @append_to(__all__)
        ... def foo():
        ...     pass
        >>> def bar():
        ...     pass
        >>> # from wild import *
        >>> # will only import Illustration and foo.
        >>> # To import everything from this module, do
        >>> # from wild import Example, bar, *
    """
    def wrap(obj):
        assert hasattr(obj, '__name__'), "Decorated object must have a __name__."
        __all__.append(obj.__name__)
        return obj
    return wrap
