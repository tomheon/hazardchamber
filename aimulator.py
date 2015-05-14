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
        moves = find_moves(game_state.board)
        moves = list(_explode_moves(moves))
        moves = _select_longest_straight(moves)
        moves = _select_preferred_colors(moves, colors, game_state.board)
        move = random.choice(moves)
        return (move[0], move[1])

    return _strat


def _explode_moves(moves):
    for t1, t2, matches in moves:
        for match in matches:
            yield t1, t2, match


def _longest_extent(move):
    t1, t2, match = move
    extents = match.max_extents
    col_extents = extents['cols'].values()
    row_extents = extents['rows'].values()
    return max(col_extents + row_extents)


def _select_longest_straight(moves):
    moves.sort(key=_longest_extent)
    moves.reverse()
    for _, moves in itertools.groupby(moves, _longest_extent):
        return list(moves)


def _select_preferred_colors(moves, colors, board):
    preferred = [move for move in moves if _has_color(move, colors, board)]
    if preferred:
        return preferred
    else:
        return moves


def _has_color(move, colors, board):
    match = move[2]
    return match.color(board) in colors
