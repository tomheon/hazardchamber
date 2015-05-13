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

import copy
import random


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
    return "| %s |" % " | ".join([str(s).ljust(3, ' ') for s in row])


NEW_TILES = [
    lambda: ColoredTile('Y'),
    lambda: ColoredTile('BL'),
    lambda: ColoredTile('BK'),
    lambda: ColoredTile('P'),
    lambda: ColoredTile('R'),
    lambda: ColoredTile('G'),
    TeamupTile
    ]


def new_rand_tile():
    """
    Return a new random color or teamup tile.
    """
    return random.choice(NEW_TILES)()


class Board(object):

    def __init__(self, rows):
        assert all(len(rows) == len(row) for row in rows)
        self.rows = rows

    def __str__(self):
        return '\n'.join([_format_row(row) for row in self.rows])

    def __eq__(self, other):
        return isinstance(other, Board) and self.rows == other.rows

    def hash(self):
        return hash(tuple([tuple(r) for r in self.rows]))

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

    def is_in_bounds(self, row, col):
        return all(0 <= n < self.side for n in [row, col])

    def set_at(self, row, col, tile):
        self.rows[row][col] = tile

    def copy(self):
        return copy.deepcopy(self)

    @property
    def side(self):
        return len(self.rows)

    def swap(self, row_one, col_one, row_two, col_two):
        """
        Swap the tiles at (row_one, col_one) and (row_two, col_two).
        """
        self.rows[row_one][col_one], self.rows[row_two][col_two] = \
            self.rows[row_two][col_two], self.rows[row_one][col_one]

    def squares_from_bottom_right(self):
        """
        Generate (row, col) from each square, starting at the bottom (right) of
        the board.

        E.g. the first yielded value in a 8x8 board would be (7, 7), the second
        (7, 6).
        """
        for row in reversed(range(self.side)):
            for col in reversed(range(self.side)):
                yield row, col


def neighbors(row, col, side):
    """
    Return all legal neighbors for the square at `row`, `col` on a board of
    side `side`, sorted.
    """
    n = []
    if row + 1 < side:
        n.append((row + 1, col))
    if row > 0:
        n.append((row - 1, col))
    if col + 1 < side:
        n.append((row, col + 1))
    if col > 0:
        n.append((row, col - 1))

    return sorted(n)
