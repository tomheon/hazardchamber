from nose.tools import eq_

from tutils import random_midgame_board_s

from parse import parse_board, unparse_board


def _verify_parse_and_unparse(board_s):
    eq_(board_s, unparse_board(parse_board(board_s)))


def test_parse_and_unparse_randoms():
    for _ in range(100):
        yield _verify_parse_and_unparse, random_midgame_board_s()
