from textwrap import dedent

from nose.tools import eq_

from aimulator import create_ai_strat
from game import GameState
from parse import create_board_parser, parse_board


FOUR_SIDE_PARSER = create_board_parser(side=4)


# (desc, board_s, parser, ai colors, exp move)
CASES = [

    ("AI prefers 4 matches to 3 of its own colors",
     dedent("""\
            | Y | Y |   | Y |
            | R | R | Y | R |
            | T | T | G | T |
            |   |   |   |   |
            """),
     FOUR_SIDE_PARSER,
     ['T', 'R'],
     ((1, 2), (0, 2))),

    ("AI prefers 4 matches of its own colors to 3 of non",
     dedent("""\
            | Y | Y |   | Y |
            | R | R | Y | R |
            | T | T | G | T |
            |   |   |   |   |
            """),
     FOUR_SIDE_PARSER,
     ['Y'],
     ((1, 2), (0, 2))),

    ("AI prefers 4 matches of its own colors to 3 of own",
     dedent("""\
            | Y | Y |   | Y |
            | R | R | Y | R |
            | T | T | G | T |
            |   |   |   |   |
            """),
     FOUR_SIDE_PARSER,
     ['Y', 'R', 'T'],
     ((1, 2), (0, 2))),

    ("AI prefers 3 matches of its own colors to 3 of non",
     dedent("""\
            | Y | Y |   | R |
            | R | R | Y | R |
            | T | T |   | T |
            |   |   |   |   |
            """),
     FOUR_SIDE_PARSER,
     ['R'],
     ((1, 3), (1, 2))),

    ("AI sees only straight matches",
     dedent("""\
            |   |   | G |   |
            | G | G |   |   |
            |   |   | G |   |
            |   |   | G |   |
            """),
     FOUR_SIDE_PARSER,
     ['Y'],
     ((1, 1), (1, 2))),

    ]


def test_aimulator():
    for desc, board_s, parser, colors, exp_move in CASES:
        board = parse_board(board_s, parser)
        yield _verify_aimulator, desc, board, colors, exp_move


def _verify_aimulator(desc, board, colors, exp_move):
    strat = create_ai_strat(colors)
    game_state = GameState(board=board,
                           offense=None,
                           defense=None,
                           to_move=None,
                           move_count=None,
                           turn_count=None)
    # sort the moves since we're not currently differentiating on which tile
    # was touched for the AI
    eq_(sorted(exp_move), sorted(strat(game_state)))
