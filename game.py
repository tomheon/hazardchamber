"""
The game itself, with turns and back and forth and all that.
"""

from collections import namedtuple
from itertools import cycle

from board import new_rand_tile, CriticalTile
from criticals import calc_critical_square
from constants import MIN_MOVE_AGAIN, MIN_CREATE_CRITICAL
from gravity import apply_gravity
from match import find_matches
from tile_destroyer import destroy_tiles


GameState = namedtuple('GameState',
                       '''
                       board
                       offense
                       defense
                       to_move
                       move_count
                       turn_count
                       ''')


class Game(object):

    def __init__(self, board, offense, defense, stop_condition):
        """
        - `board`: a Board object containing the initial position

        - `offense`: a Player object (will move first)

        - `defense`: a Player object (will move second)

        - `stop_condition`: a callable(GameState) which will be called after
          each move.  The game will end if it returns True.
        """
        self.board = board
        self.offense = offense
        self.defense = defense
        self.players = cycle([offense, defense])
        self.to_move = next(self.players)
        self.stop_condition = stop_condition
        self.move_count = 0
        self.turn_count = 1

    def play(self):
        while not self.stop_condition(self._game_state()):
            self.move()

    def move(self):
        self.move_count += 1

        matched_five = False
        to_swap = self.to_move.pick_move(self._game_state())

        if to_swap:
            self._apply_swap(to_swap)

            while True:
                matches = find_matches(self.board)
                if not matches:
                    break
                matched_five = matched_five or _has_five_match(matches)
                self._destroy_tiles()
                self._place_criticals(matches)
                self._apply_gravity()
                self._fill_empty_squares()

            if not matched_five:
                self.to_move = next(self.players)
                if self.to_move == self.offense:
                    self.turn_count += 1

    def _destroy_tiles(self):
        new_board, destroyed_squares = destroy_tiles(self.board)

        for row, col in destroyed_squares:
            self.offense.update_destroyed_tile(
                row, col,
                self.to_move == self.offense)
            self.defense.update_destroyed_tile(
                row, col,
                self.to_move == self.defense)

        self.board = new_board

    def _place_criticals(self, matches):
        for match in matches:
            if match.has_extent_at_least(MIN_CREATE_CRITICAL):
                row, col = calc_critical_square(match)
                self.board.set_at(row, col, CriticalTile())

    def _apply_gravity(self):
        new_board, tiles_moved = apply_gravity(self.board)

        for ((old_row, old_col), (new_row, new_col)) in tiles_moved:
            self.offense.update_tile_position(old_row, old_col,
                                              new_row, new_col)
            self.defense.update_tile_position(old_row, old_col,
                                              new_row, new_col)

        self.board = new_board

    def _fill_empty_squares(self):
        for (row, col) in self.board.squares_from_bottom_right():
            if self.board.at(row, col).is_empty():
                self.board.set_at(row, col, new_rand_tile())

    def _apply_swap(self, to_swap):
        self.board.swap(to_swap[0][0],
                        to_swap[0][1],
                        to_swap[1][0],
                        to_swap[1][1])

        self.offense.update_tiles_swapped(to_swap[0][0],
                                          to_swap[0][1],
                                          to_swap[1][0],
                                          to_swap[1][1])

        self.defense.update_tiles_swapped(to_swap[0][0],
                                          to_swap[0][1],
                                          to_swap[1][0],
                                          to_swap[1][1])

    def _game_state(self):
        return GameState(board=self.board,
                         offense=self.offense,
                         defense=self.defense,
                         to_move=self.to_move,
                         move_count=self.move_count,
                         turn_count=self.turn_count)


def _has_five_match(matches):
    return any(m.has_extent_at_least(MIN_MOVE_AGAIN) for m in matches)
