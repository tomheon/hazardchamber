"""
Responsible for destroying tiles after matches.

Handles clearing out rows / cols after 4+ matches, but not placing crits.

Also does not let tiles fall--gravity.py handles that.
"""

from board import EmptyTile
from constants import MIN_DESTROY_ROW_OR_COL
from match import find_matches


def destroy_tiles(board):
    """
    Return a copy of `board` with matched tiles (and rows / cols with 4+
    matches) destroyed.

    Does not modify `board` (which is important so that the original board,
    along with the returned list of destroyed tiles, can be used to figure out
    AP, traps, etc.)

    Note that this function will have no effect if there are no matches on the
    board.  It's up to other code to e.g. enforce that a move creates at least
    one match.

    Returns:

      - a new copy of the board with EmptyTiles in place of destroyed tiles

      - a sorted list of the squares (as (row, col) tuples) that were replaced
        with empty tiles
    """
    new_board = board.copy()
    matches = find_matches(new_board)

    destroyed = set()

    for match in matches:
        for (row, col) in match.squares:
            new_board.set_at(row, col, EmptyTile())
            destroyed.add((row, col))

        extents = match.max_extents

        for (row, col) in _destroy_rows(new_board, extents['rows']):
            new_board.set_at(row, col, EmptyTile())
            destroyed.add((row, col))

        for (row, col) in _destroy_cols(new_board, extents['cols']):
            new_board.set_at(row, col, EmptyTile())
            destroyed.add((row, col))

    return new_board, sorted(list(destroyed))


def _destroy_rows(board, row_extents):
        rows_to_destroy = (row
                           for (row, ext)
                           in row_extents.items()
                           if ext >= MIN_DESTROY_ROW_OR_COL)
        for row in rows_to_destroy:
            for col in range(board.side):
                yield (row, col)


def _destroy_cols(board, col_extents):
        cols_to_destroy = (col
                           for (col, ext)
                           in col_extents.items()
                           if ext >= MIN_DESTROY_ROW_OR_COL)
        for col in cols_to_destroy:
            for row in range(board.side):
                yield (row, col)
