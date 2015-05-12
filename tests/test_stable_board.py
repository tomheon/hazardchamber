from nose.tools import eq_, ok_

from board import TeamupTile, ColoredTile
from match import find_matches
from stable_board import rand_stable_board


def test_rand_stable_board():
    for _ in range(20):
        yield _verify_rand_stable_board, rand_stable_board()


def _verify_rand_stable_board(board):
    for row, col in board.squares_from_bottom_right():
        tile = board.at(row, col)
        ok_(isinstance(tile, (ColoredTile, TeamupTile)))
        eq_([], find_matches(board))
