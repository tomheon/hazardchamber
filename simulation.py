"""
Useful code for running simulations.
"""


def stop_after_n_turns(n):
    def _stop(game_state):
        return game_state.turn_count > n
    return _stop
