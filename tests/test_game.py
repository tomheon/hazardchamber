import random
import re
from textwrap import dedent

from nose.tools import eq_, ok_

from game import Game
from parse import create_board_parser, parse_board, unparse_board
from player import Player
from strategy import first_move_strat


FOUR_SIDE_PARSER = create_board_parser(side=4)


def test_stop_condition():
    stopped = [False]

    def _stop(_gs):
        stopped[0] = True
        return True

    g = Game(board=None,
             offense=None,
             defense=None,
             stop_condition=_stop)
    g.play()
    ok_(stopped[0])
    eq_(1, g.turn_count)
    eq_(0, g.move_count)


def _allow_one_move():
    # maintain this externally in case the game goes bad
    moves = [0]

    def _stop_cond(gs):
        if moves[0] >= 1:
            return True
        moves[0] = 1
        return False

    return _stop_cond


class TestPlayer(Player):

    def __init__(self, strategy):
        self.moves = 0
        self.reset_calls()
        Player.__init__(self, strategy)

    def reset_calls(self):
        self.update_destroyed_tile_calls = []
        self.update_tiles_swapped_calls = []
        self.update_tile_position_calls = []

    def pick_move(self, game_state):
        self.moves += 1
        return Player.pick_move(self, game_state)

    def update_destroyed_tile(self, row, col, board, destroyed_by_self):
        # ignoring the board for the moment
        self.update_destroyed_tile_calls.append((row, col, destroyed_by_self))
        Player.update_destroyed_tile(self, row, col, board, destroyed_by_self)

    def update_tiles_swapped(self, row_a, col_a, row_b, col_b):
        self.update_tiles_swapped_calls.append((row_a, col_a, row_b, col_b))

    def update_tile_position(self, old_row, old_col, new_row, new_col):
        self.update_tile_position_calls.append((old_row, old_col,
                                                new_row, new_col))


def test_one_turn_game():
    rand_state = random.getstate()
    try:
        random.seed(100)
        board_s = dedent("""\
                         | Y | G | BL | P |
                         | Y | R | BL | R |
                         | G | G | BK | G |
                         | Y | G | BL | P |
                         """)
        board = parse_board(board_s, FOUR_SIDE_PARSER)
        offense = TestPlayer(strategy=first_move_strat)
        defense = TestPlayer(strategy=first_move_strat)
        game = Game(board=board,
                    offense=offense,
                    defense=defense,
                    stop_condition=_allow_one_move())

        game.play()

        eq_(1, game.move_count)
        eq_(1, game.turn_count)
        eq_(1, offense.moves)
        eq_(0, defense.moves)
        eq_([(0, 1, 1, 1)],
            offense.update_tiles_swapped_calls)
        eq_([(0, 1, 1, 1)],
            defense.update_tiles_swapped_calls)
        eq_([(0, 1, 3, 1)],
            offense.update_tile_position_calls)
        eq_([(0, 1, 3, 1)],
            defense.update_tile_position_calls)
        eq_([(1, 1, True),
             (2, 1, True),
             (3, 1, True)],
            offense.update_destroyed_tile_calls)
        eq_([(1, 1, False),
             (2, 1, False),
             (3, 1, False)],
            defense.update_destroyed_tile_calls)
        eq_(dict(G=3), offense.ap)
        eq_(dict(), defense.ap)

        eq_(re.sub('\s', '',
                   dedent("""\
                          | Y | G  | BL | P |
                          | Y | P  | BL | R |
                          | G | BL | BK | G |
                          | Y | R  | BL | P |
                          """)),
            re.sub('\s', '', unparse_board(game.board)))

        game.stop_condition = _allow_one_move()
        offense.reset_calls()
        defense.reset_calls()

        game.play()

        eq_(2, game.move_count)
        eq_(2, game.turn_count)
        eq_(1, offense.moves)
        eq_(1, defense.moves)
        eq_([(2, 0, 3, 0)],
            offense.update_tiles_swapped_calls)
        eq_([(2, 0, 3, 0)],
            defense.update_tiles_swapped_calls)
        eq_([],
            offense.update_tile_position_calls)
        eq_([],
            defense.update_tile_position_calls)
        eq_([(0, 0, False),
             (1, 0, False),
             (2, 0, False)],
            offense.update_destroyed_tile_calls)
        eq_([(0, 0, True),
             (1, 0, True),
             (2, 0, True)],
            defense.update_destroyed_tile_calls)
        eq_(dict(G=3), offense.ap)
        eq_(dict(Y=3), defense.ap)

        eq_(re.sub('\s', '',
                   dedent("""\
                          | P | G  | BL | P |
                          | G | P  | BL | R |
                          | R | BL | BK | G |
                          | G | R  | BL | P |
                          """)),
            re.sub('\s', '', unparse_board(game.board)))
    finally:
        # be friendly to other downstream tests that actually want some
        # randomness
        random.setstate(rand_state)
