"""
Various simple strategies.
"""

from collections import namedtuple
import random

from board import neighbors
import board_aware_cache
from match import find_matches
from square import sq


MoveWithMatches = namedtuple('MoveWithMatches',
                             '''
                             from_sq
                             to_sq
                             matches
                             ''')


def find_moves(board, stop_after=None):
    """
    Return all legal swap moves on the board as a sorted list of
    MoveWithMatches.

    Note that normally for each move from one square to the other, there will
    be a corresponding reverse move, as tiles can be swapped with either one
    being the 'touched' tile (by convention, that being the first listed in the
    tuple).  This is not always the case if passing `stop_after.`

    If `stop_after` is supplied, stop after that many moves are found.
    """
    cached = board_aware_cache.get('find_moves', board, stop_after)
    if cached:
        return cached

    moves_with_matches = []

    for (row, col) in board.squares_from_bottom_right():
        for row_n, col_n in neighbors(row, col, board.side):
            nb = board.copy()
            nb.swap(row, col, row_n, col_n)
            matches = find_matches(nb)
            if matches:
                moves_with_matches.append(
                    MoveWithMatches(from_sq=sq(row, col),
                                    to_sq=sq(row_n, col_n),
                                    matches=matches))
                if stop_after and len(moves_with_matches) >= stop_after:
                    sorted_moves_with_matches = sorted(moves_with_matches)
                    board_aware_cache.set('find_moves', board, stop_after,
                                          sorted_moves_with_matches)
                    return sorted_moves_with_matches

    sorted_moves_with_matches = sorted(moves_with_matches)
    board_aware_cache.set('find_moves', board, None, sorted_moves_with_matches)
    return sorted_moves_with_matches


def rand_move_strat(game_state):
    """
    Pick a random available move.

    Returns None if no moves are available.
    """
    moves_with_matches = find_moves(game_state.board)
    if not moves_with_matches:
        return None
    return random.choice([(m.from_sq, m.to_sq) for m in moves_with_matches])


def first_move_strat(game_state):
    """
    Pick the first available move,

    Returns None if no moves are available.
    """
    moves_with_matches = find_moves(game_state.board)
    if not moves_with_matches:
        return None
    move_with_match = moves_with_matches[0]
    return (move_with_match.from_sq, move_with_match.to_sq)


def no_move_strat(game_state):
    """
    Refuse to move, a la 3 minion teams.
    """
    return None
