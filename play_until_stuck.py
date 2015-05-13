"""
Play a game with a (for now) single random player and single non-moving player,
and print the number of moves until stuck board to stdout.
"""

from argparse import ArgumentParser
import random
import sys

from game import Game
from parse import unparse_board
from player import Player
from stable_board import rand_stable_board
from strategy import no_move_strat, rand_move_strat, find_moves


def stop_when_stuck(game_state):
    return not find_moves(game_state.board, stop_after=1)


def print_board(game_state):
    print
    print >> sys.stderr, '***'
    print >> sys.stderr, unparse_board(game_state.board)
    print >> sys.stderr, game_state.board.md5()
    print >> sys.stderr, '***'
    print


def main():
    parser = ArgumentParser()
    parser.add_argument('--random-seed', type=int)
    parser.add_argument('--print-board',
                        action='store_true')
    args = parser.parse_args()
    if args.random_seed:
        random.seed(args.random_seed)
    pre_move = None
    if args.print_board:
        pre_move = print_board
    board = rand_stable_board()
    offense = Player(strategy=rand_move_strat)
    defense = Player(strategy=no_move_strat)
    game = Game(board=board,
                offense=offense,
                defense=defense,
                stop_condition=stop_when_stuck,
                pre_move=pre_move)
    game.play()
    print game.turn_count


if __name__ == '__main__':
    main()
