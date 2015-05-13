from textwrap import dedent

from nose.tools import eq_, ok_

from game import GameState
from match import Match
from parse import create_board_parser, parse_board
from strategy import find_moves, rand_move_strat, first_move_strat, \
    no_move_strat
from tutils import right_match, down_match

FOUR_SIDE_PARSER = create_board_parser(side=4)

# (board_s, parser, exp_moves_non_sym)
FIND_MOVES_CASES = [
    (dedent("""\
            | Y | P | P | Y |
            | R | G | R | Y |
            | Y | G | R | G |
            | R | Y | P | G |
            """),
     FOUR_SIDE_PARSER,
     []),

    (dedent("""\
            | Y | P | P | Y |
            | R | G | R | P |
            | Y | G | R | G |
            | R | Y | P | G |
            """),
     FOUR_SIDE_PARSER,
     [((0, 3),
       (1, 3),
       [right_match(3)(0, 1)])]),

    (dedent("""\
            | R | P | P | Y |
            | R | G | R | Y |
            | Y | G | R | G |
            | C | Y | P | G |
            """),
     FOUR_SIDE_PARSER,
     [((2, 0),
       (3, 0),
       [down_match(3)(0, 0)]),
      ((3, 0),
       (3, 1),
       [down_match(3)(1, 1)])]),

    (dedent("""\
            | Y | R | P | Y |
            | R | G | R | Y |
            | Y | G | R | G |
            | G | Y | Y | G |
            """),
     FOUR_SIDE_PARSER,
     [((0, 1),
       (0, 2),
       [down_match(3)(0, 2)]),
      ((0, 1),
       (1, 1),
       [right_match(3)(1, 0)]),
      ((2, 0),
       (3, 0),
       [Match([(3, 0), (3, 1), (3, 2)])]),
      ((3, 0),
       (3, 1),
       [down_match(3)(1, 1)])])
    ]


def test_find_moves():
    for board_s, parser, exp_moves_non_sym in FIND_MOVES_CASES:
        board = parse_board(board_s, parser)
        yield _verify_find_moves, board, exp_moves_non_sym
        for num_moves in range(1, (len(exp_moves_non_sym) * 2) + 1):
            yield (_verify_find_moves_with_stop, board, exp_moves_non_sym,
                   num_moves)


def _verify_find_moves(board, exp_moves_non_sym):
    moves = find_moves(board)
    exp_moves = exp_moves_non_sym + [(b, a, m)
                                     for a, b, m
                                     in exp_moves_non_sym]
    eq_(sorted(exp_moves), moves)


def _verify_find_moves_with_stop(board, exp_moves_non_sym, num_moves):
    moves = find_moves(board, stop_after=num_moves)
    eq_(num_moves, len(moves))


def test_rand_move_strat():
    for board_s, parser, exp_moves_non_sym in FIND_MOVES_CASES:
        board = parse_board(board_s, parser)
        for _ in range(10):
            yield _verify_rand_move_strat, board, exp_moves_non_sym


def _verify_rand_move_strat(board, exp_moves_non_sym):
    move = rand_move_strat(_game_state(board))
    if not exp_moves_non_sym:
        eq_(None, move)
    else:
        exp_moves = exp_moves_non_sym + [(b, a, m)
                                         for a, b, m
                                         in exp_moves_non_sym]
        ok_(move in [(a, b) for a, b, m in exp_moves])


def test_first_move_strat():
    for board_s, parser, exp_moves_non_sym in FIND_MOVES_CASES:
        board = parse_board(board_s, parser)
        yield _verify_first_move_strat, board, exp_moves_non_sym


def _verify_first_move_strat(board, exp_moves_non_sym):
    move = first_move_strat(_game_state(board))
    if not exp_moves_non_sym:
        eq_(None, move)
    else:
        exp_moves = exp_moves_non_sym + [(b, a, m)
                                         for a, b, m
                                         in exp_moves_non_sym]
        exp_moves.sort()
        eq_((exp_moves[0][0], exp_moves[0][1]), move)


def test_no_move_strat():
    for board_s, parser, exp_moves_non_sym in FIND_MOVES_CASES:
        board = parse_board(board_s, parser)
        yield _verify_no_move_strat, board


def _verify_no_move_strat(board):
    eq_(None, no_move_strat(_game_state(board)))


def _game_state(board):
    return GameState(board=board,
                     offense=None,
                     defense=None,
                     turn_count=1,
                     move_count=1,
                     to_move=None)
