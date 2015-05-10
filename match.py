"""
Utilities for finding matches in a board.
"""

import operator

from constants import MIN_MATCH


class Match(object):

    def __init__(self, squares):
        self.squares = sorted(squares)

    def __str__(self):
        return ", ".join([str(s) for s in self.squares])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, Match) and self.squares == other.squares

    def __cmp__(self, other):
        return cmp(self.squares, other.squares)


def find_matches(board):
    """
    Returns a list of Match objects, one per 3-or-more match.

    If there are no matches, returns an empty list.
    """
    matches = []
    for row in range(board.side):
        for col in range(board.side):
            matches.extend(find_matches_at(row, col, board))


def find_matches_at(row, col, board):
    matches = [find_left_match_at(row, col, board),
               find_right_match_at(row, col, board),
               find_down_match_at(row, col, board),
               find_up_match_at(row, col, board)]
    return sorted([m for m in matches if m])


def find_left_match_at(row, col, board):
    return _find_match_col(row, col, board, 0, operator.ge, -1)


def find_right_match_at(row, col, board):
    return _find_match_col(row, col, board, board.side, operator.lt, 1)


def find_up_match_at(row, col, board):
    return _find_match_row(row, col, board, 0, operator.ge, -1)


def find_down_match_at(row, col, board):
    return _find_match_row(row, col, board, board.side, operator.lt, 1)


def _find_match_col(row, col, board, lim, cmp_lim, incr):
    so_far = [(row, col)]
    cur_col = col + incr
    while cmp_lim(cur_col, lim):
        if all(board.at(r, c).matches(board.at(row, cur_col))
               for r, c in so_far):
            so_far.append((row, cur_col))
            cur_col += incr
        else:
            break
    if len(so_far) >= MIN_MATCH:
        return Match(so_far)
    else:
        return None


def _find_match_row(row, col, board, lim, cmp_lim, incr):
    so_far = [(row, col)]
    cur_row = row + incr
    while cmp_lim(cur_row, lim):
        if all(board.at(r, c).matches(board.at(cur_row, col))
               for r, c in so_far):
            so_far.append((cur_row, col))
            cur_row += incr
        else:
            break
    if len(so_far) >= MIN_MATCH:
        return Match(so_far)
    else:
        return None
