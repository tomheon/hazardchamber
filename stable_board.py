"""
Generate a guaranteed stable board (for the beginning of a game).
"""

from parse import unparse_board
from board import Board, new_rand_tile, EmptyTile
from constants import BOARD_SIDE
from match import find_matches_at


# Max times we'll try a random tile in an empty square before declaring a
# problem
MAX_TRIES = 100


def rand_stable_board(board_side=BOARD_SIDE):
    """
    Generate a random stable board (meaning with no current matches) of side
    `board_side`.

    Throws an exception if it can't randomly and stably fill a given square in
    MAX_TRIES tries.
    """
    board = empty_board(board_side)
    for (row, col) in board.squares_from_bottom_right():
        tries = 0
        while True:
            tries += 1
            if tries >= MAX_TRIES:
                raise Exception(
                    "Unstable cell (%d, %d) after %d tries %s" %
                    (row, col, MAX_TRIES, unparse_board(board)))
            board.set_at(row, col, new_rand_tile())

            if not find_matches_at(row, col, board):
                break
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
