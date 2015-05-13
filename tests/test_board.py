from nose.tools import eq_, ok_

from board import Board, neighbors
from stable_board import empty_board


def test_is_in_bounds():
    board = empty_board(8)
    for row in range(8):
        for col in range(8):
            yield _verify_is_in_bounds, board, row, col, True

    out_of_bounds = [(-1, 0), (0, -1), (-1, -1),
                     (8, 0), (0, 8), (8, 8),
                     (9, 0), (0, 9), (9, 9)]

    for (row, col) in out_of_bounds:
        yield _verify_is_in_bounds, board, row, col, False


def _verify_is_in_bounds(board, row, col, expected):
    eq_(expected, board.is_in_bounds(row, col))


def test_at():
    board = Board([['A', 'B'], ['C', 'D']])
    cases = [
        ((0, 0), 'A'),
        ((0, 1), 'B'),
        ((1, 0), 'C'),
        ((1, 1), 'D')
        ]
    for ((row, col), expected) in cases:
        yield _verify_at, board, row, col, expected


def _verify_at(board, row, col, expected):
    eq_(expected, board.at(row, col))


def test_set_at():
    board = Board([['A', 'B'], ['C', 'D']])
    ok_('M' != board.at(0, 1))
    board.set_at(0, 1, 'M')
    eq_('M', board.at(0, 1))


class Modifiable(object):

    def __init__(self, data):
        self.data = data


def test_copy_isolates_changes():
    board = Board([[Modifiable('A'), Modifiable('B')],
                   [Modifiable('C'), Modifiable('D')]])
    eq_('A', board.at(0, 0).data)
    new_board = board.copy()
    eq_('A', board.at(0, 0).data)
    for row in range(1):
        for col in range(1):
            eq_(board.at(row, col).data, new_board.at(row, col).data)
    new_board.set_at(0, 0, Modifiable('M'))
    eq_('M', new_board.at(0, 0).data)
    eq_('A', board.at(0, 0).data)
    new_board.at(0, 1).data = 'X'
    eq_('X', new_board.at(0, 1).data)
    eq_('B', board.at(0, 1).data)


def test_squares_from_bottom_right():
    board = Board([[0, 1], [2, 3]])
    eq_([3, 2, 1, 0],
        [board.at(row, col) for row, col in board.squares_from_bottom_right()])


def test_swap():
    board = Board([[0, 1], [2, 3]])
    board.swap(0, 0, 1, 0)
    eq_(Board([[2, 1], [0, 3]]), board)


def test_neighbors():
    # (row, col, side, exp_neighbors)
    cases = [
        (0, 0, 3, [(0, 1), (1, 0)]),
        (0, 1, 3, [(0, 0), (0, 2), (1, 1)]),
        (0, 2, 3, [(0, 1), (1, 2)]),

        (1, 0, 3, [(0, 0), (2, 0), (1, 1)]),
        (1, 1, 3, [(0, 1), (1, 0), (1, 2), (2, 1)]),
        (1, 2, 3, [(0, 2), (1, 1), (2, 2)]),

        (2, 0, 3, [(1, 0), (2, 1)]),
        (2, 1, 3, [(2, 0), (1, 1), (2, 2)]),
        (2, 2, 3, [(2, 1), (1, 2)]),
        ]

    for row, col, side, expected in cases:
        yield _verify_neighbors, row, col, side, expected


def _verify_neighbors(row, col, side, expected):
    eq_(sorted(expected), neighbors(row, col, side))
