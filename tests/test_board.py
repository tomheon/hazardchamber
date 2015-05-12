from nose.tools import eq_, ok_

from board import EmptyTile, ColoredTile, CriticalTile, TeamupTile, StrikeTile, \
    AttackTile, ProtectTile, CountdownTile, new_rand_tile, Board

YELLOW = ColoredTile('Y')
YELLOW2 = ColoredTile('Y')
RED = ColoredTile('R')

YELLOW_STRIKE_123_OFFENSE = StrikeTile(color='Y', strength=123, direction='<')
YELLOW_STRIKE_124_OFFENSE = StrikeTile(color='Y', strength=124, direction='<')
YELLOW_STRIKE_123_DEFENSE = StrikeTile(color='Y', strength=123, direction='>')
RED_STRIKE_123_OFFENSE = StrikeTile(color='R', strength=123, direction='<')

YELLOW_ATTACK_123_OFFENSE = AttackTile(color='Y', strength=123, direction='<')
YELLOW_ATTACK_124_OFFENSE = AttackTile(color='Y', strength=124, direction='<')
YELLOW_ATTACK_123_DEFENSE = AttackTile(color='Y', strength=123, direction='>')
RED_ATTACK_123_OFFENSE = AttackTile(color='R', strength=123, direction='<')

YELLOW_PROTECT_123_OFFENSE = ProtectTile(color='Y',
                                         strength=123, direction='<')
YELLOW_PROTECT_124_OFFENSE = ProtectTile(color='Y',
                                         strength=124, direction='<')
YELLOW_PROTECT_123_DEFENSE = ProtectTile(color='Y',
                                         strength=123, direction='>')
RED_PROTECT_123_OFFENSE = ProtectTile(color='R', strength=123, direction='<')

YELLOW_COUNTDOWN_5 = CountdownTile(color='Y', turns_left=5)
YELLOW_COUNTDOWN_6 = CountdownTile(color='Y', turns_left=6)
RED_COUNTDOWN_5 = CountdownTile(color='R', turns_left=5)

EMPTY = EmptyTile()
EMPTY2 = EmptyTile()

CRITICAL = CriticalTile()
CRITICAL2 = CriticalTile()
TEAMUP = TeamupTile()
TEAMUP2 = TeamupTile()

# (t1, t2, should_match)
TILE_MATCH_TESTS = [
    # basic colors
    (YELLOW, YELLOW, True),
    (YELLOW, YELLOW2, True),
    (YELLOW, RED, False),

    # strike colors
    (YELLOW, YELLOW_STRIKE_123_OFFENSE, True),
    (YELLOW_STRIKE_123_OFFENSE, RED, False),
    (YELLOW_STRIKE_123_OFFENSE, YELLOW_STRIKE_124_OFFENSE, True),
    (YELLOW_STRIKE_123_OFFENSE, YELLOW_STRIKE_123_OFFENSE, True),
    (YELLOW_STRIKE_123_OFFENSE, RED_STRIKE_123_OFFENSE, False),

    # attack colors
    (YELLOW, YELLOW_ATTACK_123_OFFENSE, True),
    (YELLOW_ATTACK_123_OFFENSE, RED, False),
    (YELLOW_ATTACK_123_OFFENSE, YELLOW_ATTACK_124_OFFENSE, True),
    (YELLOW_ATTACK_123_OFFENSE, YELLOW_ATTACK_123_DEFENSE, True),
    (YELLOW_ATTACK_123_OFFENSE, RED_ATTACK_123_OFFENSE, False),
    (YELLOW_STRIKE_124_OFFENSE, YELLOW_ATTACK_123_DEFENSE, True),

    # protect colors
    (YELLOW, YELLOW_PROTECT_123_OFFENSE, True),
    (YELLOW_PROTECT_123_OFFENSE, RED, False),
    (YELLOW_PROTECT_123_OFFENSE, YELLOW_PROTECT_124_OFFENSE, True),
    (YELLOW_PROTECT_123_OFFENSE, YELLOW_PROTECT_123_DEFENSE, True),
    (YELLOW_PROTECT_123_OFFENSE, RED_PROTECT_123_OFFENSE, False),
    (YELLOW_STRIKE_124_OFFENSE, YELLOW_PROTECT_123_DEFENSE, True),
    (YELLOW_ATTACK_124_OFFENSE, YELLOW_PROTECT_123_DEFENSE, True),

    # countdown colors
    (YELLOW, YELLOW_COUNTDOWN_5, True),
    (YELLOW_COUNTDOWN_5, RED, False),
    (YELLOW_COUNTDOWN_5, YELLOW_COUNTDOWN_6, True),
    (YELLOW_COUNTDOWN_5, YELLOW_COUNTDOWN_5, True),
    (YELLOW_COUNTDOWN_5, RED_COUNTDOWN_5, False),
    (YELLOW_STRIKE_123_OFFENSE, YELLOW_COUNTDOWN_5, True),
    (YELLOW_ATTACK_123_OFFENSE, YELLOW_COUNTDOWN_5, True),
    (YELLOW_PROTECT_123_OFFENSE, YELLOW_COUNTDOWN_5, True),

    # empty tiles
    (EMPTY, EMPTY, False),
    (EMPTY, EMPTY2, False),
    (EMPTY, YELLOW, False),
    (EMPTY, YELLOW_STRIKE_123_OFFENSE, False),
    (EMPTY, YELLOW_ATTACK_123_OFFENSE, False),
    (EMPTY, YELLOW_PROTECT_123_OFFENSE, False),
    (EMPTY, YELLOW_COUNTDOWN_5, False),
    (EMPTY, CRITICAL, False),
    (EMPTY, TEAMUP, False),

    # criticals
    (CRITICAL, CRITICAL, True),
    (CRITICAL, CRITICAL2, True),
    (CRITICAL, YELLOW, True),
    (CRITICAL, RED, True),
    (CRITICAL, YELLOW_COUNTDOWN_6, True),
    (CRITICAL, YELLOW_STRIKE_123_OFFENSE, True),
    (CRITICAL, YELLOW_ATTACK_123_OFFENSE, True),
    (CRITICAL, YELLOW_PROTECT_123_OFFENSE, True),

    # teamup
    (TEAMUP, TEAMUP, True),
    (TEAMUP, TEAMUP2, True),
    (TEAMUP, CRITICAL, True),
    (TEAMUP, YELLOW, False),
    (TEAMUP, RED, False),
    (TEAMUP, YELLOW_COUNTDOWN_6, False),
    (TEAMUP, YELLOW_STRIKE_123_OFFENSE, False),
    (TEAMUP, YELLOW_ATTACK_123_OFFENSE, False),
    (TEAMUP, YELLOW_PROTECT_123_OFFENSE, False),
]


def _verify_tile_match(t1, t2, should_match):
    eq_(should_match, t1.matches(t2))


def test_tile_matches():
    for t1, t2, should_match in TILE_MATCH_TESTS:
        yield _verify_tile_match, t1, t2, should_match
        yield _verify_tile_match, t2, t1, should_match


def test_new_rand_tile():
    for _ in range(100):
        yield _verify_legal_rand_tile, new_rand_tile()


def _verify_legal_rand_tile(tile):
    ok_(isinstance(tile, ColoredTile) or
        isinstance(tile, TeamupTile))


def test_is_in_bounds():
    board = Board([[EmptyTile()] * 8] * 8)
    for row in range(8):
        for col in range(8):
            yield _verify_is_in_bounds, board, row, col, True

    out_of_bounds = [(-1, 0), (0, -1), (-1, -1),
                     (8, 0), (0, 8), (8, 8),
                     (9, 0), (0, 9), (9, 9)]

    for (row, col) in out_of_bounds:
        yield _verify_is_in_bounds, board, row, col, False


def _verify_is_in_bounds(board, row, col, expected):
    eq_(expected, board.is_in_bounds(row, col))


def test_at():
    board = Board([['A', 'B'], ['C', 'D']])
    cases = [
        ((0, 0), 'A'),
        ((0, 1), 'B'),
        ((1, 0), 'C'),
        ((1, 1), 'D')
        ]
    for ((row, col), expected) in cases:
        yield _verify_at, board, row, col, expected


def _verify_at(board, row, col, expected):
    eq_(expected, board.at(row, col))


def test_set_at():
    board = Board([['A', 'B'], ['C', 'D']])
    ok_('M' != board.at(0, 1))
    board.set_at(0, 1, 'M')
    eq_('M', board.at(0, 1))


class Modifiable(object):

    def __init__(self, data):
        self.data = data


def test_copy_isolates_changes():
    board = Board([[Modifiable('A'), Modifiable('B')],
                   [Modifiable('C'), Modifiable('D')]])
    eq_('A', board.at(0, 0).data)
    new_board = board.copy()
    eq_('A', board.at(0, 0).data)
    for row in range(1):
        for col in range(1):
            eq_(board.at(row, col).data, new_board.at(row, col).data)
    new_board.set_at(0, 0, Modifiable('M'))
    eq_('M', new_board.at(0, 0).data)
    eq_('A', board.at(0, 0).data)
    new_board.at(0, 1).data = 'X'
    eq_('X', new_board.at(0, 1).data)
    eq_('B', board.at(0, 1).data)
