"""
Play a game vs. the AI, where the offense tries to maximize certain AP in a
strict order.

In this case, the AP the AI and the offense is going after is exactly the same
(as if they had the same team).
"""

from argparse import ArgumentParser
import random

from aimulator import create_ai_strat
from game import Game
from player import Player
from stable_board import rand_stable_board
from strategy import create_ap_seeking_strat


def one_hundred_turns(game_state):
    return game_state.turn_count > 10


def _ap_state(p_letter, player):
    return 'AP %s: %s' % (p_letter,
                          ' '.join(['%s=%s' % item
                                    for item
                                    in sorted(player.ap.items())]))


def print_ap(game_state):
    print "Turn %d, move %d" % (game_state.turn_count, game_state.move_count)
    print _ap_state('O', game_state.offense)
    print _ap_state('D', game_state.defense)
    print '---'


def main():
    parser = ArgumentParser()
    parser.add_argument('random_seed', type=int)
    args = parser.parse_args()
    random.seed(args.random_seed)
    board = rand_stable_board()
    colors = ['G', 'Y', 'R', 'B', 'P', 'T']
    defense_colors = ['G', 'Y', 'R', 'B', 'P', 'T']
    offense = Player(strategy=create_ap_seeking_strat(colors))
    defense = Player(strategy=create_ai_strat(defense_colors))
    game = Game(board=board,
                offense=offense,
                defense=defense,
                pre_move=print_ap,
                stop_condition=one_hundred_turns)
    print "O colors: %s" % ' '.join(colors)
    print "D colors: %s" % ' '.join(defense_colors)
    print "---"
    game.play()


if __name__ == '__main__':
    main()
