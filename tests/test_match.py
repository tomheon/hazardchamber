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

    expected = [
        [None, None, ((0, 0), (0, 1), (0, 2)), ((0, 0), (0, 1), (0, 2), (0, 3))],
        [None, None, ((1, 0), (1, 1), (1, 2)), None],
        [None, None, None, ((2, 1), (2, 2), (2, 3))],
        [None, None, None, None],
        ]
    for row in range(board.side):
        for col in range(board.side):
            yield (_verify_find_single_match,
                   board, row, col, expected[row][col],
                   find_left_match_at)


def test_find_right_match_at():
    board_s = dedent("""\
                     | Y | Y | Y | Y |
                     | R | R | R | Y |
                     | Y | G | G | G |
                     | E | E | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    expected = [
        [((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 1), (0, 2), (0, 3)), None, None],
        [((1, 0), (1, 1), (1, 2)), None, None, None],
        [None, ((2, 1), (2, 2), (2, 3)), None, None],
        [None, None, None, None],
        ]
    for row in range(board.side):
        for col in range(board.side):
            yield (_verify_find_single_match,
                   board, row, col, expected[row][col],
                   find_right_match_at)


def _verify_find_single_match(board, row, col, expected, find_under_test):
    if expected:
        expected = _m(*expected)
    eq_(expected, find_under_test(row, col, board))


def test_critical_as_second_match_tile():
    """
    It would be easy to mistakenly call:

    | C | Y | R |

    or the like a match, if you were to only use matches() against the first
    tile in the potential match.

    Test against that.
    """
    board_s = dedent("""\
                     | C | Y | R | Y |
                     | R | R | R | Y |
                     | Y | G | G | G |
                     | E | E | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)
    eq_(None, find_right_match_at(0, 0, board))


