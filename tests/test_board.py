from nose.tools import eq_

from board import EmptyTile, ColoredTile, CriticalTile, TeamupTile, StrikeTile, \
    AttackTile, ProtectTile, CountdownTile

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

YELLOW_PROTECT_123_OFFENSE = ProtectTile(color='Y', strength=123, direction='<')
YELLOW_PROTECT_124_OFFENSE = ProtectTile(color='Y', strength=124, direction='<')
YELLOW_PROTECT_123_DEFENSE = ProtectTile(color='Y', strength=123, direction='>')
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
    eq_(should_match, t2.matches(t1))


def test_tile_matches():
    for t1, t2, should_match in TILE_MATCH_TESTS:
        yield _verify_tile_match, t1, t2, should_match
