"""
Utilities for finding matches in a board.
"""

import itertools
import operator

from constants import MIN_MATCH


class Match(object):

    def __init__(self, squares):
        self.squares = sorted(squares)

    def __str__(self):
        return "Match(%s)" % ", ".join([str(s) for s in self.squares])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, Match) and self.squares == other.squares

    def __hash__(self):
        return hash(tuple(self.squares))

    def __cmp__(self, other):
        return cmp(self.squares, other.squares)

    def subsumes_match(self, other):
        return set(self.squares) > set(other.squares)

    def __contains__(self, square_coord):
        return square_coord in self.squares

    @property
    def tile_count(self):
        return len(self.squares)

    @property
    def max_extents(self):
        """
        Returns a dict of the form:

        {
          'rows': { <row>: <extent>, <row>: <extent> },
          'cols': { <col>: <extent>, <col>: <extent> }
        }

        Where `extent` is the max number of contiguous tiles matches in that
        row or col.
        """
        squares = list(self.squares)

        _row = lambda s: s[0]
        _col = lambda s: s[1]

        rows_max_extents = {
            row: max_extent
            for row, max_extent
            in _max_extents(squares,
                            _row,
                            _col)
            if max_extent >= MIN_MATCH}
        cols_max_extents = {
            col: max_extent
            for col, max_extent
            in _max_extents(squares,
                            _col,
                            _row)
            if max_extent >= MIN_MATCH}

        return dict(rows=rows_max_extents,
                    cols=cols_max_extents)


def _max_extents(squares, group_key, extent_key):
    squares.sort(key=group_key)
    for g_key, g_squares in itertools.groupby(squares, group_key):
        exts = [extent_key(s) for s in g_squares]
        exts.sort()
        # shamelessly adapted from the python itertools recipes
        _ind_minus_elem = lambda (i, x): i - x
        yield (g_key,
               max([len(list(adj))
                    for (_, adj)
                    in itertools.groupby(enumerate(exts), _ind_minus_elem)]))


def find_matches(board):
    """
    Returns a sorted list of unique Match objects, one per 3-or-more match.

    Only the largest matches are returned in each case (e.g. the two 3 matches
    that make up a 4 match will not be returned, only the 4 match).

    If there are no matches, returns an empty list.
    """
    matches = set()
    for row in range(board.side):
        for col in range(board.side):
            matches.update(set(find_matches_at(row, col, board)))
    return sorted([m for m
                   in matches
                   if not any(o.subsumes_match(m) for o in matches)])


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
