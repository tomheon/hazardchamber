import re
from textwrap import dedent

from nose.tools import eq_

from parse import create_board_parser, unparse_board, parse_board
from tile_destroyer import destroy_tiles


FOUR_SIDE_PARSER = create_board_parser(side=4)

SIX_SIDE_PARSER = create_board_parser(side=6)

# (board, parser, new_board, destroyed squares)
CASES = [
    (dedent("""\
            | Y | Y  | R   | Y |
            | R | R  | Y   | Y |
            | Y | G  | BL  | G |
            | P | BL | BK  | G |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | Y | Y  | R   | Y |
            | R | R  | Y   | Y |
            | Y | G  | BL  | G |
            | P | BL | BK  | G |
            """),
     []),

    (dedent("""\
            | Y | Y  | Y  | Y |
            | R | R  | R  | Y |
            | Y | G  | G  | G |
            | P | BL | BK | G |
            """),
     FOUR_SIDE_PARSER,
     dedent("""\
            | E | E  | E  | E |
            | E | E  | E  | Y |
            | Y | E  | E  | E |
            | P | BL | BK | G |
            """),
     [(0, 0), (0, 1), (0, 2), (0, 3),
      (1, 0), (1, 1), (1, 2),
      (2, 1), (2, 2), (2, 3)]),


    (dedent("""\
            | Y | Y  | Y  | Y | G | G |
            | R | R  | R  | R | R | G |
            | Y | G  | Y  | G | Y | Y |
            | P | BL | BK | G | Y | Y |
            | G | BK | BL | Y | G | G |
            | P | BL | BK | G | Y | Y |
            """),
     SIX_SIDE_PARSER,
     dedent("""\
            | E | E  | E  | E | E | E |
            | E | E  | E  | E | E | E |
            | Y | G  | Y  | G | Y | Y |
            | P | BL | BK | G | Y | Y |
            | G | BK | BL | Y | G | G |
            | P | BL | BK | G | Y | Y |
            """),
     [(0, c) for c in range(6)] + [(1, c) for c in range(6)]),

    (dedent("""\
            | Y | R  | Y  | Y | G | G |
            | Y | R  | R  | P | R | G |
            | Y | R  | Y  | G | Y | Y |
            | Y | R  | BK | G | Y | Y |
            | P | R  | BL | Y | G | G |
            | P | BL | BK | G | Y | Y |
            """),
     SIX_SIDE_PARSER,
     dedent("""\
            | E | E | Y  | Y | G | G |
            | E | E | R  | P | R | G |
            | E | E | Y  | G | Y | Y |
            | E | E | BK | G | Y | Y |
            | E | E | BL | Y | G | G |
            | E | E | BK | G | Y | Y |
            """),
     [(r, 0) for r in range(6)] + [(r, 1) for r in range(6)]),


    (dedent("""\
            | G | R | Y  | Y | G | G |
            | Y | R | R  | P | R | G |
            | Y | R | Y  | G | Y | Y |
            | G | R | BK | G | Y | Y |
            | Y | G | BL | Y | G | G |
            | Y | Y | Y  | Y | Y | Y |
            """),
     SIX_SIDE_PARSER,
     dedent("""\
            | G | E | Y  | Y | G | G |
            | Y | E | R  | P | R | G |
            | Y | E | Y  | G | Y | Y |
            | G | E | BK | G | Y | Y |
            | Y | E | BL | Y | G | G |
            | E | E | E  | E | E | E |
            """),
     [(r, 1) for r in range(6)] + [(5, c) for c in range(6)])
    ]


def test_destroy_tiles():
    for board_s, parser, new_board_s, destroyed in CASES:
        yield _verify_destroy_tiles, board_s, parser, new_board_s, destroyed


def _verify_destroy_tiles(board_s, parser, e_new_board_s, e_destroyed):
    board = parse_board(board_s, parser)
    new_board, destroyed = destroy_tiles(board)
    eq_(sorted(list(set(e_destroyed))), destroyed)
    eq_(re.sub('\s', '', e_new_board_s),
        re.sub('\s', '', unparse_board(new_board)))
