from textwrap import dedent

from nose.tools import eq_

from parse import create_board_parser, parse_board
from match import find_matches, find_matches_at, find_left_match_at, \
    find_right_match_at, find_up_match_at, find_down_match_at, Match


FOUR_SIDE_PARSER = create_board_parser(side=4)

FIVE_SIDE_PARSER = create_board_parser(side=5)


def _m(args, row, col):
    if args is None:
        return None
    elif isinstance(args, list):
        return sorted([a(row, col) for a in args])
    return args(row, col)


def LEFT(num_squares):
    def _left(row, col):
        return Match([(row, col - i) for i in range(num_squares)])
    return _left


def RIGHT(num_squares):
    def _right(row, col):
        return Match([(row, col + i) for i in range(num_squares)])
    return _right


def DOWN(num_squares):
    def _down(row, col):
        return Match([(row + i, col) for i in range(num_squares)])
    return _down


def UP(num_squares):
    def _up(row, col):
        return Match([(row - i, col) for i in range(num_squares)])
    return _up


def test_find_left_match_at():
    board_s = dedent("""\
                     | Y | Y | Y | Y |
                     | R | R | R | Y |
                     | Y | G | G | G |
                     | E | E | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    expected = [
        [None, None, LEFT(3), LEFT(4)],
        [None, None, LEFT(3), None],
        [None, None, None, LEFT(3)],
        [None, None, None, None],
        ]
    for row in range(board.side):
        for col in range(board.side):
            yield (_verify_find_single_match,
                   board, row, col, expected[row][col],
                   find_left_match_at)


def test_find_right_match_at():
    board_s = dedent("""\
                     | Y | Y | Y | Y |
                     | R | R | R | Y |
                     | Y | G | G | G |
                     | E | E | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    expected = [
        [RIGHT(4), RIGHT(3), None, None],
        [RIGHT(3), None, None, None],
        [None, RIGHT(3), None, None],
        [None, None, None, None],
        ]
    for row in range(board.side):
        for col in range(board.side):
            yield (_verify_find_single_match,
                   board, row, col, expected[row][col],
                   find_right_match_at)


def test_find_down_match_at():
    board_s = dedent("""\
                     | Y | Y | G | E |
                     | Y | R | G | E |
                     | Y | R | G | E |
                     | Y | R | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    expected = [
        [DOWN(4), None, DOWN(3), None],
        [DOWN(3), DOWN(3), None, None],
        [None, None, None, None],
        [None, None, None, None],
        ]
    for row in range(board.side):
        for col in range(board.side):
            yield (_verify_find_single_match,
                   board, row, col, expected[row][col],
                   find_down_match_at)


def test_find_up_match_at():
    board_s = dedent("""\
                     | Y | Y | G | E |
                     | Y | R | G | E |
                     | Y | R | G | E |
                     | Y | R | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    expected = [
        [None, None, None, None],
        [None, None, None, None],
        [UP(3), None, UP(3), None],
        [UP(4), UP(3), None, None],
        ]
    for row in range(board.side):
        for col in range(board.side):
            yield (_verify_find_single_match,
                   board, row, col, expected[row][col],
                   find_up_match_at)


def test_find_matches_at():
    board_s = dedent("""\
                     | Y | Y | Y | E |
                     | Y | Y | E | E |
                     | Y | Y | E | E |
                     | Y | R | R | R |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    expected = [
        [[DOWN(4), RIGHT(3)], [DOWN(3)], [LEFT(3)], []],
        [[DOWN(3)], [], [], []],
        [[UP(3)], [UP(3)], [], []],
        [[UP(4)], [RIGHT(3)], [], [LEFT(3)]],
        ]
    for row in range(board.side):
        for col in range(board.side):
            yield (_verify_find_single_match,
                   board, row, col, expected[row][col],
                   find_matches_at)


def _verify_find_single_match(board, row, col, expected, find_under_test):
    expected = _m(expected, row, col)
    eq_(expected, find_under_test(row, col, board))


def test_critical_as_second_match_tile():
    """
    It would be easy to mistakenly call:

    | C | Y | R |

    or the like a match, if you were to only use matches() against the first
    tile in the potential match.

    Test against that.
    """
    board_s = dedent("""\
                     | C | Y | R | Y |
                     | R | R | R | Y |
                     | Y | G | G | G |
                     | E | E | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)
    eq_(None, find_right_match_at(0, 0, board))


def test_match_subsumes():
    cases = [
        ([], [], False),
        ([(0, 1)], [(0, 1)], False),
        ([(0, 1)], [], True),
        ([(0, 1), (0, 2)], [(0, 1)], True),
        ([(0, 1), (0, 2)], [(0, 2)], True),
        ([], [(0, 1)], False),
        ([(0, 1)], [(0, 1), (0, 2)], False),
        ([(0, 2)], [(0, 1), (0, 2)], False),
        ]
    for (a, b, subsumes) in cases:
        yield _verify_match_subsumes, a, b, subsumes


def _verify_match_subsumes(a, b, subsumes):
    eq_(subsumes, Match(a).subsumes_match(Match(b)))


def test_square_in_match():
    cases = [
        ([], (0, 0), False),
        ([(0, 0)], (0, 0), True),
        ([(0, 0), (0, 1)], (0, 0), True),
        ([(0, 0), (0, 1)], (0, 1), True),
        ([(0, 0), (0, 1)], (0, 2), False),
        ([(0, 0), (0, 1)], (1, 0), False),
        ]
    for (match, square, includes) in cases:
        yield _verify_square_in_match, match, square, includes


def _verify_square_in_match(match, square, includes):
    eq_(includes, square in Match(match))


# (board_s, parser, expected matches)
FIND_MATCHES_CASES = [
    (dedent("""\
            | Y | Y | Y | E |
            | Y | Y | E | E |
            | Y | Y | E | E |
            | Y | R | R | R |
            """),
     FOUR_SIDE_PARSER,
     [RIGHT(3)(0, 0),
      DOWN(4)(0, 0),
      DOWN(3)(0, 1),
      RIGHT(3)(3, 1)]),

    (dedent("""\
            | Y | Y | Y | T | R |
            | R | R | R | R | R |
            | Y | Y | C | E | T |
            | Y | R | R | R | T |
            | T | R | T | R | T |
            """),
     FIVE_SIDE_PARSER,
     [RIGHT(3)(0, 0),
      RIGHT(5)(1, 0),
      RIGHT(3)(2, 0),
      RIGHT(3)(3, 1),
      DOWN(3)(1, 2),
      DOWN(3)(2, 4)
      ]),

    (dedent("""\
            | Y | Y | R | G |
            | Y | R | G | R |
            | R | Y | R | G |
            | Y | R | Y | R |
            """),
     FOUR_SIDE_PARSER,
     []),

    (dedent("""\
            | C | C | C | C |
            | C | C | C | C |
            | C | C | C | C |
            | C | C | C | C |
            """),
     FOUR_SIDE_PARSER,
     [RIGHT(4)(0, 0),
      RIGHT(4)(1, 0),
      RIGHT(4)(2, 0),
      RIGHT(4)(3, 0),
      DOWN(4)(0, 0),
      DOWN(4)(0, 1),
      DOWN(4)(0, 2),
      DOWN(4)(0, 3)
      ]),

    (dedent("""\
            | Y | Y | Y | Y |
            | Y | Y | Y | Y |
            | Y | Y | Y | Y |
            | Y | Y | Y | Y |
            """),
     FOUR_SIDE_PARSER,
     [RIGHT(4)(0, 0),
      RIGHT(4)(1, 0),
      RIGHT(4)(2, 0),
      RIGHT(4)(3, 0),
      DOWN(4)(0, 0),
      DOWN(4)(0, 1),
      DOWN(4)(0, 2),
      DOWN(4)(0, 3)
      ]),

    (dedent("""\
            | Y | Y | R | G |
            | Y | C | C | R |
            | R | G | P | G |
            | Y | R | Y | R |
            """),
     FOUR_SIDE_PARSER,
     [RIGHT(3)(1, 0),
      RIGHT(3)(1, 1)]),
    ]


def test_find_matches():
    for (board_s, parser, expected) in FIND_MATCHES_CASES:
        board = parse_board(board_s, parser)
        yield _verify_find_matches, board, expected


def _verify_find_matches(board, expected):
    eq_(sorted(expected), find_matches(board))
