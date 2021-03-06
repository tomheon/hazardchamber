"""
Simulate 64 strength 1 protect tiles v. 1 strength 64 and everything in
between.
"""

from argparse import ArgumentParser
import random

from aimulator import create_ai_strat
import board_aware_cache
from game import Game
from player import Player
from stable_board import rand_stable_board
from strategy import rand_move_strat, create_protect_protects_strat
from simulation import stop_after_n_turns
from tiles import ProtectTile


def _to_protect_tile(tile, strength):
    return ProtectTile(color=tile.color,
                       strength=strength,
                       direction='<')


def mk_print_protection(sim_id, num_protect_tiles):
    def print_protection(game_state):
        print "%s,%d,%d,%s" % (sim_id,
                               num_protect_tiles,
                               game_state.move_count,
                               game_state.board.protection('<'))
    return print_protection


def run_sim(sim_id, num_protect_tiles, num_turns, use_protect_protects):
    strength = 64.0 / num_protect_tiles
    board = rand_stable_board(no_teamups=True)
    squares = list(board.squares_from_bottom_right())
    random.shuffle(squares)

    for square in squares[:num_protect_tiles]:
        tile = board.at(square[0], square[1])
        pt = _to_protect_tile(tile, strength)
        board.set_at(square[0], square[1], pt)

    defense_colors = ['G', 'Y', 'R', 'B', 'P', 'T']
    if use_protect_protects:
        offense = Player(strategy=create_protect_protects_strat('<'))
    else:
        offense = Player(strategy=rand_move_strat)
    defense = Player(strategy=create_ai_strat(defense_colors))

    game = Game(board=board,
                offense=offense,
                defense=defense,
                pre_move=mk_print_protection(sim_id, num_protect_tiles),
                stop_condition=stop_after_n_turns(num_turns))

    board_aware_cache.clear()

    game.play()


def run_sims(trial, max_protect_tiles, num_turns, use_protect_protects):
    for i in range(max_protect_tiles):
        num_protect_tiles = i + 1
        run_sim("%s-%s" % (num_protect_tiles, trial),
                num_protect_tiles, num_turns, use_protect_protects)


def main():
    parser = ArgumentParser()
    parser.add_argument('--num-turns', type=int, default=20)
    parser.add_argument('--num-trials', type=int, default=1000)
    parser.add_argument('--max-protect-tiles', type=int, default=64)
    parser.add_argument('--offense-protects-protects',
                        default=False,
                        action='store_true')
    parser.add_argument('random_seed', type=int)
    args = parser.parse_args()
    random.seed(args.random_seed)

    for i in range(args.num_trials):
        run_sims(i, args.max_protect_tiles, args.num_turns,
                 args.offense_protects_protects)


if __name__ == '__main__':
    main()
