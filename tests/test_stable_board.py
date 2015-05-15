from nose.tools import eq_, ok_

from match import find_matches
from stable_board import rand_stable_board
from strategy import find_moves
from tiles import TeamupTile, ColoredTile


def test_rand_stable_board():
    for _ in range(3):
        yield _verify_rand_stable_board, rand_stable_board()


def _verify_rand_stable_board(board):
    eq_([], find_matches(board))
    ok_(find_moves(board))

    for row, col in board.squares_from_bottom_right():
        tile = board.at(row, col)
        ok_(isinstance(tile, (ColoredTile, TeamupTile)))
