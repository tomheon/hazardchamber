import re
from textwrap import dedent

from nose.tools import eq_

from parse import create_board_parser, parse_board, unparse_board
from gravity import apply_gravity

FOUR_SIDE_PARSER = create_board_parser(side=4)

# (board before, parser, board after, moved)
TEST_CASES = [
    (dedent("""\
            | Y | Y | Y | Y |
            | R | R | R | Y |
            | Y | G | G | G |
            | G | G | Y | P |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | Y | Y | Y | Y |
            | R | R | R | Y |
            | Y | G | G | G |
            | G | G | Y | P |
            """),
     []),

    (dedent("""\
            | Y | Y | E | Y |
            | R | R | R | Y |
            | Y | G | G | G |
            | G | G | Y | P |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | Y | Y | E | Y |
            | R | R | R | Y |
            | Y | G | G | G |
            | G | G | Y | P |
            """),
     []),

    (dedent("""\
            | Y | Y | E | Y |
            | R | R | E | Y |
            | Y | G | E | G |
            | G | G | E | P |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | Y | Y | E | Y |
            | R | R | E | Y |
            | Y | G | E | G |
            | G | G | E | P |
            """),
     []),

    (dedent("""\
            | Y | Y | Y | Y |
            | R | R | E | Y |
            | Y | G | G | G |
            | G | G | Y | P |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | Y | Y | E | Y |
            | R | R | Y | Y |
            | Y | G | G | G |
            | G | G | Y | P |
            """),
     [((0, 2), (1, 2))]),

    (dedent("""\
            | Y | Y | Y | Y |
            | R | R | E | Y |
            | Y | G | E | G |
            | G | G | Y | P |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | Y | Y | E | Y |
            | R | R | E | Y |
            | Y | G | Y | G |
            | G | G | Y | P |
            """),
     [((0, 2), (2, 2))]),

    (dedent("""\
            | Y | Y | G | Y |
            | R | E | G | Y |
            | Y | G | Y | G |
            | G | E | Y | P |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | Y | E | G | Y |
            | R | E | G | Y |
            | Y | Y | Y | G |
            | G | G | Y | P |
            """),
     [((0, 1), (2, 1)), ((2, 1), (3, 1))]),

    (dedent("""\
            | Y | Y | G | E |
            | R | E | G | Y |
            | E | G | Y | G |
            | G | E | Y | P |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | E | E | G | E |
            | Y | E | G | Y |
            | R | Y | Y | G |
            | G | G | Y | P |
            """),
     [((0, 1), (2, 1)), ((2, 1), (3, 1)),
      ((0, 0), (1, 0)), ((1, 0), (2, 0))]),
    ]


def test_apply_gravity():
    for board_s, parser, exp_board_s, exp_moved in TEST_CASES:
        board = parse_board(board_s, parser)
        yield _verify_apply_gravity, board, exp_board_s, exp_moved


def _verify_apply_gravity(board, exp_board_s, exp_moved):
    post_g_board, moved = apply_gravity(board)
    eq_(re.sub('\s', '', exp_board_s),
        re.sub('\s', '', unparse_board(post_g_board)))
    eq_(sorted(exp_moved), moved)

    # verify that gravity is idempotent
    post_gg_board, gg_moved = apply_gravity(post_g_board)
    eq_(re.sub('\s', '', unparse_board(post_g_board)),
        re.sub('\s', '', unparse_board(post_gg_board)))
    eq_([], gg_moved)
