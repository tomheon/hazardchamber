"""
Code for dealing with tiles.
"""

import random

from termcolor import colored


class NullTile(object):
    """
    Used in tests only, to make the tiles we care about more visible.  Doesn't
    match anything, but behaves like a normal tile under gravity.
    """

    def __str__(self):
        return " "

    def matches(self, tile):
        return False

    def is_empty(self):
        return False

    def is_critical(self):
        return False

    def is_color(self):
        return False

    def is_game_tile(self):
        return False

    def is_teamup(self):
        return False

    def protection(self, direction):
        return 0

    def ap(self):
        return None

    def as_fancy_str(self, ljust):
        return str(self).ljust(ljust, ' ')

    def copy(self):
        return self


class EmptyTile(object):

    def __str__(self):
        return "E"

    def matches(self, tile):
        return False

    def is_empty(self):
        return True

    def is_critical(self):
        return False

    def is_color(self):
        return False

    def is_game_tile(self):
        return False

    def is_teamup(self):
        return False

    def ap(self):
        return None

    def as_fancy_str(self, ljust):
        return str(self).ljust(ljust, ' ')

    def copy(self):
        return self

    def protection(self, direction):
        return 0


class GameTile(object):

    def is_empty(self):
        return False

    def is_critical(self):
        return False

    def is_color(self):
        return False

    def is_game_tile(self):
        return True

    def is_teamup(self):
        return False

    def ap(self):
        return None

    def as_fancy_str(self, ljust):
        return str(self).ljust(ljust, ' ')

    def copy(self):
        return self

    def protection(self, direction):
        return 0


class ColoredTile(GameTile):

    def __init__(self, color=None):
        self.color = color

    def __str__(self):
        return self.color

    def matches(self, tile):
        return tile.is_critical() or (tile.is_color()
                                      and tile.color == self.color)

    def is_color(self):
        return True

    def ap(self):
        return (self.color, 1)

    def as_fancy_str(self, ljust):
        return _color(str(self).ljust(ljust, ' '), self.color)

    def protection(self, direction):
        return 0


def _color(s, color):
    color_to_str = dict(Y='yellow',
                        R='red',
                        G='green',
                        BL='cyan',
                        BK='grey',
                        P='magenta')
    return colored(s, color_to_str[color])


class CriticalTile(GameTile):

    def __str__(self):
        return "C"

    def matches(self, tile):
        return tile.is_game_tile()

    def is_critical(self):
        return True


class TeamupTile(GameTile):

    def __str__(self):
        return "T"

    def matches(self, tile):
        return tile.is_teamup() or tile.is_critical()

    def is_teamup(self):
        return True

    def ap(self):
        return ('T', 1)


class StrikeTile(ColoredTile):

    def __init__(self, color=None, strength=None, direction=None):
        super(StrikeTile, self).__init__(color=color)
        self.strength = strength
        self.direction = direction

    def __str__(self):
        return "%s S %s %s" % (self.color, self.direction, self.strength)


class AttackTile(ColoredTile):

    def __init__(self, color=None, strength=None, direction=None):
        super(AttackTile, self).__init__(color=color)
        self.strength = strength
        self.direction = direction

    def __str__(self):
        return "%s A %s %s" % (self.color, self.direction, self.strength)


class ProtectTile(ColoredTile):

    def __init__(self, color=None, strength=None, direction=None):
        super(ProtectTile, self).__init__(color=color)
        self.strength = strength
        self.direction = direction

    def __str__(self):
        return "%s P %s %s" % (self.color, self.direction, self.strength)

    def protection(self, direction):
        if self.direction == direction:
            return self.strength
        else:
            return 0


class CountdownTile(ColoredTile):

    def __init__(self, color=None, turns_left=None, on_countdown=None):
        """
        - `on_countdown` is a callable that will be invoked (with no arguments)
          when the countdown fires
        """
        super(CountdownTile, self).__init__(color=color)
        self.turns_left = turns_left
        self.on_countdown = on_countdown

    def __str__(self):
        return "%s CD %s" % (self.color, self.turns_left)

    def copy(self):
        return CountdownTile(color=self.color,
                             turns_left=self.turns_left,
                             on_countdown=self.on_countdown)


NEW_TILES = [
    lambda: ColoredTile('Y'),
    lambda: ColoredTile('BL'),
    lambda: ColoredTile('BK'),
    lambda: ColoredTile('P'),
    lambda: ColoredTile('R'),
    lambda: ColoredTile('G'),
    TeamupTile
    ]


def new_rand_tile(no_teamups=False):
    """
    Return a new random color or teamup tile (unless no_teamups is True).
    """
    while True:
        tile = random.choice(NEW_TILES)()
        if not tile.is_teamup() or not no_teamups:
            return tile
