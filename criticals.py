"""
Code to support locating criticals.
"""

import random

from board import neighbors
from constants import MIN_CREATE_CRITICAL


def calc_critical_square(match):
    """
    Calculate which square in a match should be a critical tile.

    Rules are as follows:

    - in a straight match of odd number of tiles, take the center tile

    - in a stright match of even number tiles, take the left center tile
      (horiz) or top center tile (vert)

    - in any t, cross, or u like match, take the bottomest, toppest
      'intersection'

    Otherwise return a random tile in the match.

    These rules are currently an approximation of the real ones, which I
    believe are more complex.

    If the size of the match is < MIN_CREATE_CRITICAL, returns None.
    """
    if match.tile_count < MIN_CREATE_CRITICAL:
        return None

    if _is_straight_row_match(match) or _is_straight_col_match(match):
        return _middle(match)

    intersections = _find_intersections(match)
    if intersections:
        return sorted(intersections)[0]

    return random.choice(match.squares)


def _is_straight_row_match(match):
    rows = [row for row, col in match.squares]
    return len(set(rows)) == 1


def _is_straight_col_match(match):
    cols = [col for row, col in match.squares]
    return len(set(cols)) == 1


def _middle(match):
    return match.squares[(len(match.squares) - 1) / 2]


def _find_intersections(match):
    # just fake out a grid bigger than our match to calc neighbors
    side = max(max([s[0] for s in match.squares]),
               max([s[1] for s in match.squares])) + 1
    intersections = []
    for row, col in match.squares:
        ns = [n for n in neighbors(row, col, side) if n in match.squares]
        if any(n[0] == row for n in ns) and any(n[1] == col for n in ns):
            intersections.append((row, col))
    return intersections
