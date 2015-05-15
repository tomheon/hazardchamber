import re
from textwrap import dedent

from nose.tools import eq_

from parse import parse_board, unparse_board, create_board_parser
from tutils import random_midgame_board_s


def _verify_parse_and_unparse(board_s):
    eq_(board_s, unparse_board(parse_board(board_s)))


def test_parse_and_unparse_randoms():
    for _ in range(100):
        yield _verify_parse_and_unparse, random_midgame_board_s()


def test_nulls():
    board_s = dedent("""\
                     |   | R | R |
                     | Y |   | G |
                     | Y | R |   |
                     """)
    parser = create_board_parser(side=3)
    eq_(re.sub('\s', '', board_s),
        re.sub('\s', '', unparse_board(parse_board(board_s, parser))))
