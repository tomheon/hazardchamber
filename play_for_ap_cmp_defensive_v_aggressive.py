"""
Play a game vs. the AI, either trying to minimize AP gains or maximize one's
own.
"""

from argparse import ArgumentParser
import random

from aimulator import create_ai_strat
from game import Game
from player import Player
from stable_board import rand_stable_board
from strategy import create_ap_seeking_strat
from simulation import stop_after_n_turns


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
    parser.add_argument('--num-turns', type=int, default=50)
    parser.add_argument('--play-defense', action="store_true", default=False)
    parser.add_argument('random_seed', type=int)
    args = parser.parse_args()
    random.seed(args.random_seed)
    board = rand_stable_board()
    defense_colors = ['G', 'Y', 'R', 'BL', 'P', 'T']
    offense_play_colors = ['BK', 'R', 'Y', 'P']
    offense_judged_by_colors = ['BK', 'R', 'Y', 'P']
    if args.play_defense:
        offense_play_colors = ['Y', 'R', 'G', 'P', 'BL', 'BK']
    offense = Player(strategy=create_ap_seeking_strat(offense_play_colors))
    defense = Player(strategy=create_ai_strat(defense_colors))
    game = Game(board=board,
                offense=offense,
                defense=defense,
                pre_move=print_ap,
                stop_condition=stop_after_n_turns(args.num_turns))
    print "O judged by colors: %s" % ' '.join(offense_judged_by_colors)
    print "O play colors: %s" % ' '.join(offense_play_colors)
    print "D colors: %s" % ' '.join(defense_colors)
    print "---"
    game.play()


if __name__ == '__main__':
    main()
