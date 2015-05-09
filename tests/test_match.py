from textwrap import dedent

from nose.tools import eq_

from parse import create_board_parser, parse_board
from match import find_matches, find_matches_at, find_left_match_at, \
    find_right_match_at, find_up_match_at, find_down_match_at, Match


FOUR_SIDE_PARSER = create_board_parser(side=4)


def _m(*args):
    return Match(args)


def test_find_left_match_at():
    board_s = dedent("""\
                     | Y | Y | Y | Y |
                     | R | R | R | Y |
                     | Y | G | G | G |
                     | E | E | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    eq_(None, find_left_match_at(0, 0, board))
    eq_(None, find_left_match_at(0, 1, board))
    eq_(None, find_left_match_at(1, 0, board))

    eq_(None, find_left_match_at(1, 3, board))

    eq_(None, find_left_match_at(2, 2, board))

    eq_(None, find_left_match_at(3, 3, board))

    eq_(_m((0, 0), (0, 1), (0, 2)), find_left_match_at(0, 2, board))
    eq_(_m((0, 0), (0, 1), (0, 2), (0, 3)), find_left_match_at(0, 3, board))

    eq_(_m((1, 0), (1, 1), (1, 2)), find_left_match_at(1, 2, board))

    eq_(_m((2, 1), (2, 2), (2, 3)), find_left_match_at(2, 3, board))
