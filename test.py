#! /usr/bin/env python2
# (c) 2014 Julian Gonggrijp (j.gonggrijp@gmail.com)

"""
    Doctest module for the campbellsoup package.
"""

from doctest import testmod

import campbellsoup as cs

if __name__ == '__main__':
    testmod(cs)
    testmod(cs.models)
    testmod(cs.queries)
    testmod(cs.utilities)
