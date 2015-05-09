"""
Code for dealing with the board.

As much as possible, this code is stupid and isolated from more game-like
concerns.  For example, even though a trap or countdown tile usually 'belongs'
to a character in some way that requires tile modification upon the character's
downing, it keeps no direct reference to the character (even though this
somewhat complicates board transitions).

Further to keeping it dumb, any special behaviors (e.g. upon countdown) are
expressed as callbacks.
"""


class EmptyTile(object):

    def __str__(self):
        return "E"

    def matches(self, tile):
        return False


class GameTile(object):

    pass


class ColoredTile(GameTile):

    def __init__(self, color=None):
        self.color = color

    def __str__(self):
        return self.color

    def matches(self, tile):
        return (isinstance(tile, CriticalTile)
                or
                (isinstance(tile, ColoredTile)
                 and tile.color == self.color))


class CriticalTile(GameTile):

    def __str__(self):
        return "C"

    def matches(self, tile):
        return isinstance(tile, GameTile)


class TeamupTile(GameTile):

    def __str__(self):
        return "T"

    def matches(self, tile):
        return (isinstance(tile, TeamupTile) or
                isinstance(tile, CriticalTile))


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


def _format_row(row):
    return "| %s |" % " | ".join([str(s) for s in row])


class Board(object):

    def __init__(self, rows):
        assert all(len(rows) == len(row) for row in rows)
        self.rows = rows

    def __str__(self):
        return '\n'.join([_format_row(row) for row in self.rows])

    def at(self, row, col):
        """
        Return the tile at `row` `col`.

        Raise an exception if out of bounds.
        """
        if len(self.rows) <= row:
            raise Exception("Bad row num: %s" % row)

        if len(self.rows[0]) <= col:
            raise Exception("Bad col num: %s" % col)

        return self.rows[row][col]

    @property
    def side(self):
        return len(self.rows)
