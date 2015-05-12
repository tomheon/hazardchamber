"""
An offensive or defensive player.

Eventually this will also embed teams, etc.

For the moment, it just holds a move strategy.
"""


class Player(object):

    def __init__(self, strategy):
        self.strategy = strategy

    def pick_move(self, game_state):
        """
        Return a tuple of:

        ((row, col), (row, col))

        indicating the tiles the player wishes to swap.

        The first tile is considered the 'touched' tile.

        Return None if the player does not wish to / cannot make a move.

        - `game_state`: a game.GameState namedtuple containing the current
          state of the game.
        """
        return self.strategy(game_state)

    def update_destroyed_tile(self, row, col, destroyed_by_self):
        """
        Called (by the game or a player) when a tile is destroyed.

        - `destroyed_by_self`: True if this player destroyed the tile

        TODO: need to work AP in eventually for abilities that do / don't
        generate.
        """
        pass

    def update_tile_position(self, old_row, old_col, new_row, new_col):
        """
        Called when a tile's position changes.
        """
        pass

    def update_tiles_swapped(self, row_a, col_a, row_b, col_b):
        """
        Called when two tiles are swapped.
        """
        pass
