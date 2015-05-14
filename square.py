"""
Just keeps track of a row and col.
"""

from collections import namedtuple


Square = namedtuple('Square', 'row col')


def sq(row, col):
    """
    Just a shortcut since Squares are so common.
    """
    return Square(row=row, col=col)
