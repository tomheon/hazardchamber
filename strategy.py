"""
Various simple strategies.
"""

from collections import namedtuple
import itertools
import random

from board import neighbors
import board_aware_cache
from criticals import calc_critical_square
from gravity import apply_gravity
from match import find_matches
from square import sq
from tile_destroyer import destroy_tiles
from tiles import CriticalTile


MoveWithMatches = namedtuple('MoveWithMatches',
                             '''
                             from_sq
                             to_sq
                             matches
                             ''')


def find_moves(board, stop_after=None):
    """
    Return all legal swap moves on the board as a sorted list of
    MoveWithMatches.

    Note that normally for each move from one square to the other, there will
    be a corresponding reverse move, as tiles can be swapped with either one
    being the 'touched' tile (by convention, that being the first listed in the
    tuple).  This is not always the case if passing `stop_after.`

    If `stop_after` is supplied, stop after that many moves are found.
    """
    cached = board_aware_cache.get('find_moves', board, stop_after)
    if cached:
        return cached

    moves_with_matches = []

    for (row, col) in board.squares_from_bottom_right():
        for row_n, col_n in neighbors(row, col, board.side):
            nb = board.copy()
            nb.swap(row, col, row_n, col_n)
            matches = find_matches(nb)
            if matches:
                moves_with_matches.append(
                    MoveWithMatches(from_sq=sq(row, col),
                                    to_sq=sq(row_n, col_n),
                                    matches=matches))
                if stop_after and len(moves_with_matches) >= stop_after:
                    sorted_moves_with_matches = sorted(moves_with_matches)
                    board_aware_cache.set('find_moves', board, stop_after,
                                          sorted_moves_with_matches)
                    return sorted_moves_with_matches

    sorted_moves_with_matches = sorted(moves_with_matches)
    board_aware_cache.set('find_moves', board, None, sorted_moves_with_matches)
    return sorted_moves_with_matches


def rand_move_strat(game_state):
    """
    Pick a random available move.

    Returns None if no moves are available.
    """
    moves_with_matches = find_moves(game_state.board)
    if not moves_with_matches:
        return None
    return random.choice([(m.from_sq, m.to_sq) for m in moves_with_matches])


def first_move_strat(game_state):
    """
    Pick the first available move,

    Returns None if no moves are available.
    """
    moves_with_matches = find_moves(game_state.board)
    if not moves_with_matches:
        return None
    move_with_match = moves_with_matches[0]
    return (move_with_match.from_sq, move_with_match.to_sq)


def no_move_strat(game_state):
    """
    Refuse to move, a la 3 minion teams.
    """
    return None


def _ap(from_sq, to_sq, matches, colors, board):
    """
    Return a list, the same length as `colors`, with each element being the
    number of ap in that color earned by `match`.
    """
    ap = [0] * len(colors)

    # later, do prob. ev of tiles that fall

    board = board.copy()
    board.swap(from_sq[0], from_sq[1], to_sq[0], to_sq[1])

    while find_matches(board):
        new_board, destroyed_sqs = destroy_tiles(board)
        for s in destroyed_sqs:
            sq_ap = board.at(s[0], s[1]).ap()
            if sq_ap and sq_ap[0] in colors:
                ap[colors.index(sq_ap[0])] += sq_ap[1]
        for match in matches:
            crit = calc_critical_square(match)
            if crit:
                new_board.set_at(crit[0], crit[1], CriticalTile())
        board, _ = apply_gravity(new_board)

    return ap


def create_ap_seeking_strat(colors):
    """
    Return a strategy that seeks AP in `colors`, preferring those earlier in
    `colors` to those later.

    Will select the match that generates the most AP in the most preferred
    color, breaking any ties with reference to the next most preferred etc.

    Ties are broken with reference to the lexically earliest swapped tiles.
    """
    colors = list(colors)

    def _ap_seeking_strat(game_state):
        moves_with_matches = find_moves(game_state.board)
        ap_plus_move = [(_ap(mwm.to_sq,
                             mwm.from_sq,
                             mwm.matches,
                             colors,
                             game_state.board),
                         (mwm.to_sq, mwm.from_sq))
                        for mwm
                        in moves_with_matches]
        ap_plus_move.sort(reverse=True)
        for _, moves in itertools.groupby(ap_plus_move, lambda t: t[0]):
            return sorted(moves)[0][1]
        return None

    return _ap_seeking_strat
