"""
Parsing (and unparsing) boards, teams, games, etc.
"""

from pyparsing import Keyword, Word, nums, Or, Optional, Group

import board


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

Square = Group(Optional(Edge) + Or([Colored, Uncolored]) + Edge)
Row = Group(Square * 8)
Board = Row * 8


def strip_pipes(sq):
    return [c for c in sq if c != '|']


def to_tile(s):
    if len(s) == 1:
        t = s[0]
        if t == 'C':
            return board.CriticalTile()
        elif t == 'T':
            return board.TeamupTile()
        elif t == 'E':
            return board.EmptyTile()
        else:
            return board.ColoredTile(color=t)
    else:
        sub = s[1]
        if sub == 'P':
            return board.ProtectTile(color=s[0],
                                     strength=s[3],
                                     direction=s[2])
        elif sub == 'A':
            return board.AttackTile(color=s[0],
                                    strength=s[3],
                                    direction=s[2])
        elif sub == 'S':
            return board.StrikeTile(color=s[0],
                                    strength=s[3],
                                    direction=s[2])
        elif sub == 'CD':
            return board.CountdownTile(color=s[0],
                                       turns_left=s[2])
        else:
            raise Exception("Bad subtype: %s" % s)

    return s


def parse_row(row):
    stripped = [strip_pipes(s) for s in row]
    return [to_tile(s) for s in stripped]


def parse_board(s_board):
    rows = Board.parseString(s_board)
    return board.Board([parse_row(row) for row in rows])


def unparse_board(board):
    return str(board)
