"""
Various simple strategies.
"""

import random

from board import neighbors
import board_aware_cache
from match import find_matches


def find_moves(board, stop_after=None):
    """
    Return all legal swap moves on the board as a sorted list of:

    [((row1, col1), (row2, col2), matches), ...]

    Note that normally for each ((row1, col1), (row2, col2)) tuple, there will
    be a corresponding ((row2, col2), (row1, col1)) tuple, as tiles can be
    swapped with either one being the 'touched' tile (by convention, that being
    the first listed in the tuple).  This is not always the case if passing
    `stop_after.`

    If `stop_after` is supplied, stop after that many moves are found.
    """
    cached = board_aware_cache.get('find_moves', board, stop_after)
    if cached:
        return cached

    moves = []

    for (row, col) in board.squares_from_bottom_right():
        for row_n, col_n in neighbors(row, col, board.side):
            nb = board.copy()
            nb.swap(row, col, row_n, col_n)
            matches = find_matches(nb)
            if matches:
                moves.append(((row, col), (row_n, col_n), matches))
            if stop_after is not None and len(moves) >= stop_after:
                sorted_moves = sorted(moves)
                board_aware_cache.set('find_moves', board, stop_after,
                                      sorted_moves)
                return sorted_moves

    sorted_moves = sorted(moves)
    board_aware_cache.set('find_moves', board, None, sorted_moves)
    return sorted_moves


def rand_move_strat(game_state):
    """
    Pick a random available move.

    Returns None if no moves are available.
    """
    moves = find_moves(game_state.board)
    if not moves:
        return None
    return random.choice([(t1, t2) for t1, t2, _ in moves])


def first_move_strat(game_state):
    """
    Pick the first available move,

    Returns None if no moves are available.
    """
    moves = find_moves(game_state.board)
    if not moves:
        return None
    move = moves[0]
    return (move[0], move[1])


def no_move_strat(game_state):
    """
    Refuse to move, a la 3 minion teams.
    """
    return None
