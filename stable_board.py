"""
Generate a guaranteed stable board (for the beginning of a game).
"""

from parse import unparse_board
from board import Board
from constants import BOARD_SIDE
from match import find_matches_at
from strategy import find_moves
from tiles import new_rand_tile, EmptyTile


# Max times we'll try a random tile in an empty square before declaring a
# problem
MAX_TRIES = 100


def rand_stable_board(board_side=BOARD_SIDE, no_teamups=False):
    """
    Generate a random stable board (meaning with no current matches) of side
    `board_side`.

    The board will have at least one legal move.

    Throws an exception if it can't randomly and stably fill a given square in
    MAX_TRIES tries, or can't generate a board with at least one move after
    MAX_TRIES tries.
    """
    board_tries = 0
    while True:
        board_tries += 1
        if board_tries >= MAX_TRIES:
            raise Exception(
                "No moves on stable board after %d tries" % MAX_TRIES)

        board = empty_board(board_side)
        for (row, col) in board.squares_from_bottom_right():
            sq_tries = 0
            while True:
                sq_tries += 1
                if sq_tries >= MAX_TRIES:
                    raise Exception(
                        "Unstable cell (%d, %d) after %d tries %s" %
                        (row, col, MAX_TRIES, unparse_board(board)))
                board.set_at(row, col, new_rand_tile(no_teamups=no_teamups))

                if not find_matches_at(row, col, board):
                    break
        if find_moves(board, stop_after=1):
            return board


def empty_board(board_side):
    """
    Since this has some pitfalls with references, pull it out to a function.
    """
    rows = []

    for _rows in range(board_side):
        row = []
        for _cols in range(board_side):
            row.append(EmptyTile())
        rows.append(row)

    return Board(rows)
