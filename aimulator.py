"""
Emulate the MPQ AI.
"""

import itertools
import random

from strategy import find_moves


def create_ai_strat(colors):
    """
    Return an AI strat function for a team with (active) abilities
    corresponding to the supplied `colors`.

    - `colors`: an iterable of letter codes (e.g. 'P', 'BL')
    """
    colors = set(colors)

    def _strat(game_state):
        moves_with_matches = find_moves(game_state.board)
        moves_with_match = list(_explode_moves(moves_with_matches))
        moves_with_match = _select_longest_straight(moves_with_match)
        moves_with_match = _select_preferred_colors(moves_with_match,
                                                    colors,
                                                    game_state.board)
        move_with_match = random.choice(moves_with_match)
        return (move_with_match[0], move_with_match[1])

    return _strat


def _explode_moves(moves_with_matches):
    for from_sq, to_sq, matches in moves_with_matches:
        for match in matches:
            yield from_sq, to_sq, match


def _longest_extent(move_with_match):
    from_sq, to_sq, match = move_with_match
    extents = match.max_extents
    col_extents = extents['cols'].values()
    row_extents = extents['rows'].values()
    return max(col_extents + row_extents)


def _select_longest_straight(moves_with_match):
    moves_with_match.sort(key=_longest_extent)
    moves_with_match.reverse()
    for _, m in itertools.groupby(moves_with_match, _longest_extent):
        return list(m)


def _select_preferred_colors(moves_with_match, colors, board):
    preferred = [move_with_match
                 for move_with_match
                 in moves_with_match
                 if _has_color(move_with_match, colors, board)]
    if preferred:
        return preferred
    else:
        return moves_with_match


def _has_color(move_with_match, colors, board):
    _from_sq, _to_sq, match = move_with_match
    return match.color(board) in colors
