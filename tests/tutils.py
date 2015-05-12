import random

from board import EmptyTile, ColoredTile, CriticalTile, TeamupTile, StrikeTile, \
    AttackTile, ProtectTile, CountdownTile, Board
from constants import BOARD_SIDE
from match import Match


def _rand_color():
    return random.choice(['Y', 'R', 'P', 'BL', 'BK', 'G'])


def _rand_direction():
    return random.choice('<>')


def _rand_strength():
    return random.randint(1, 124)


def _rand_turns_left():
    return random.randint(1, 20)


TILE_FUNCS = [EmptyTile,
              CriticalTile,
              TeamupTile,
              lambda: ColoredTile(_rand_color()),
              lambda: StrikeTile(_rand_color(),
                                 _rand_strength(),
                                 _rand_direction()),
              lambda: AttackTile(_rand_color(),
                                 _rand_strength(),
                                 _rand_direction()),
              lambda: ProtectTile(_rand_color(),
                                  _rand_strength(),
                                  _rand_direction()),
              lambda: CountdownTile(_rand_color(),
                                    _rand_turns_left())]


def _rand_tile():
    return random.choice(TILE_FUNCS)()


def _rand_row():
    return [_rand_tile() for _ in range(BOARD_SIDE)]


def random_midgame_board():
    """
    Note: not guaranteed stable, may contain strike tiles etc.
    """
    return Board([_rand_row() for _ in range(BOARD_SIDE)])


def random_midgame_board_s():
    """
    Note: not guaranteed stable, may contain strike tiles etc.
    """
    return str(random_midgame_board())


def left_match(num_squares):
    def _left(row, col):
        return Match([(row, col - i) for i in range(num_squares)])
    return _left


def right_match(num_squares):
    def _right(row, col):
        return Match([(row, col + i) for i in range(num_squares)])
    return _right


def down_match(num_squares):
    def _down(row, col):
        return Match([(row + i, col) for i in range(num_squares)])
    return _down


def up_match(num_squares):
    def _up(row, col):
        return Match([(row - i, col) for i in range(num_squares)])
    return _up
