"""
Code for dealing with the board.
"""

import hashutils


def _format_row(row):
    return "| %s |" % " | ".join([str(s).ljust(3, ' ') for s in row])


class Board(object):

    def __init__(self, rows):
        assert all(len(rows) == len(row) for row in rows)
        self.rows = rows

    def __str__(self):
        # TODO: find longest tile and pad to that instead of 3
        return '\n'.join([_format_row(row) for row in self.rows])

    def __iter__(self):
        for row, col in self.squares_from_bottom_right():
            yield self.at(row, col)

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
        return Board([[t.copy() for t in row] for row in self.rows])

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

    def md5(self):
        return hashutils.md5(str(self))

    def as_fancy_str(self):
        # TODO: find longest tile and pad to that instead of 3
        FILL_FACTOR = 3
        spacer = '-' * (self.side * (FILL_FACTOR + 3) + 1)
        lines = [spacer]
        for row in self.rows:
            lines.append("| %s |" % " | ".join([t.as_fancy_str(3)
                                                for t in row]))
            lines.append(spacer)
        return '\n'.join(lines)


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
