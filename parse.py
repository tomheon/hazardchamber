"""
Parsing (and unparsing) boards, teams, games, etc.
"""

from pyparsing import Keyword, Word, nums, Or, Optional, Group

import board
from constants import BOARD_SIDE
import tiles


def create_board_parser(side):
    Edge = Keyword('|')

    Yellow = Keyword('Y')
    Blue = Keyword('BL')
    Black = Keyword('BK')
    Purple = Keyword('P')
    Red = Keyword('R')
    Green = Keyword('G')

    Color = Or([Yellow, Blue, Black, Purple, Red, Green])

    Direction = Or([Keyword('>'), Keyword('<')])
    Strength = Word(nums)
    Strike = Keyword('S') + Direction + Strength
    Attack = Keyword('A') + Direction + Strength
    Protect = Keyword('P') + Direction + Strength

    TurnsLeft = Word(nums)
    Countdown = Keyword('CD') + TurnsLeft

    Special = Or([Strike, Attack, Protect, Countdown])

    Colored = Color + Optional(Special)

    Teamup = Keyword('T')
    Critical = Keyword('C')
    Empty = Keyword('E')

    Uncolored = Or([Teamup, Critical, Empty])

    Square = Group(Optional(Or([Colored, Uncolored]),
                            default='*') + Edge)
    Row = Group(Edge + (Square * side))
    Board = Row * side
    return Board


STANDARD_BOARD_PARSER = create_board_parser(BOARD_SIDE)


def strip_pipes(sq):
    return [c for c in sq if c != '|']


def to_tile(s):
    if len(s) == 1:
        t = s[0]
        if t == '*':
            return tiles.NullTile()
        elif t == 'C':
            return tiles.CriticalTile()
        elif t == 'T':
            return tiles.TeamupTile()
        elif t == 'E':
            return tiles.EmptyTile()
        else:
            return tiles.ColoredTile(color=t)
    else:
        sub = s[1]
        if sub == 'P':
            return tiles.ProtectTile(color=s[0],
                                     strength=s[3],
                                     direction=s[2])
        elif sub == 'A':
            return tiles.AttackTile(color=s[0],
                                    strength=s[3],
                                    direction=s[2])
        elif sub == 'S':
            return tiles.StrikeTile(color=s[0],
                                    strength=s[3],
                                    direction=s[2])
        elif sub == 'CD':
            return tiles.CountdownTile(color=s[0],
                                       turns_left=s[2])
        else:
            raise Exception("Bad subtype: %s" % s)

    return s


def parse_row(row):
    stripped = [strip_pipes(s) for s in row if s != '|']
    return [to_tile(s) for s in stripped]


def parse_board(s_board, parser=STANDARD_BOARD_PARSER):
    rows = parser.parseString(s_board)
    return board.Board([parse_row(row) for row in rows])


def unparse_board(board):
    return str(board)
