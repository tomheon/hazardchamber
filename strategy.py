"""
Various simple strategies.
"""

import random

from match import find_matches


def find_moves(board, stop_after=None):
    """
    Return all legal swap moves on the board as a sorted list of:

    [((row1, col1), (row2, col2)), ...]

    Note that normally for each ((row1, col1), (row2, col2)) tuple, there will
    be a corresponding ((row2, col2), (row1, col1)) tuple, as tiles can be
    swapped with either one being the 'touched' tile (by convention, that being
    the first listed in the tuple).  This is not always the case if passing
    `stop_after.`

    If `stop_after` is supplied, stop after that many moves are found.
    """
    moves = []

    for (row, col) in board.squares_from_bottom_right():
        neighbors = _neighbors(row, col, board.side)
        for row_n, col_n in neighbors:
            nb = board.copy()
            nb.swap(row, col, row_n, col_n)
            if find_matches(nb):
                moves.append(((row, col), (row_n, col_n)))
            if stop_after is not None and len(moves) >= stop_after:
                return sorted(moves)

    return sorted(moves)


def rand_move_strat(game_state):
    """
    Pick a random available move.

    Returns None if no moves are available.
    """
    moves = find_moves(game_state.board)
    if not moves:
        return None
    return random.choice(moves)


def first_move_strat(game_state):
    """
    Pick the first available move,

    Returns None if no moves are available.
    """
    moves = find_moves(game_state.board)
    if not moves:
        return None
    return moves[0]


def _neighbors(row, col, side):
    if row + 1 < side:
        yield (row + 1, col)
    if row > 0:
        yield (row - 1, col)
    if col + 1 < side:
        yield (row, col + 1)
    if col > 0:
        yield (row, col - 1)
