# rework to just bring tiles down


def apply_gravity(board):
    """
    Returns (new_board, tiles_moved)

    Where:

      - `new_board` is the board with gravity having been applied

      - `tiles_moved` is a sorted list of ((old_row, old_col), (new_row,
        new_col)) tuples for each tile in new_board which was in a different
        square in the original board.
    """
    board = board.copy()
    moved = dict()

    # start from the bottom, then we only have to move once--look above until
    # non-empty, if ever, and swap
    for row, col in board.squares_from_bottom_right():
        if board.at(row, col).is_empty():
            for r in reversed(range(row)):
                if not board.at(r, col).is_empty():
                    board.swap(row, col, r, col)
                    moved[(r, col)] = (row, col)
                    break

    return board, sorted(list(moved.items()))
