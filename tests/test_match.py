from textwrap import dedent

from nose.tools import eq_, ok_

from parse import create_board_parser, parse_board
from match import find_matches, find_matches_at, find_left_match_at, \
    find_right_match_at, find_up_match_at, find_down_match_at, Match
from tutils import right_match, left_match, down_match, up_match


FOUR_SIDE_PARSER = create_board_parser(side=4)

FIVE_SIDE_PARSER = create_board_parser(side=5)

EIGHT_SIDE_PARSER = create_board_parser(side=8)


def _m(args, row, col):
    if args is None:
        return None
    elif isinstance(args, list):
        return sorted([a(row, col) for a in args])
    return args(row, col)


def test_find_left_match_at():
    board_s = dedent("""\
                     | Y | Y | Y | Y |
                     | R | R | R | Y |
                     | Y | G | G | G |
                     | E | E | E | E |
                     """)
    board = parse_board(board_s, FOUR_SIDE_PARSER)

    expected = [
        [None, None, left_match(3), left_match(4)],
        [None, None, left_match(3), None],
        [None, None, None, left_match(3)],
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
        [right_match(4), right_match(3), None, None],
        [right_match(3), None, None, None],
        [None, right_match(3), None, None],
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
        [down_match(4), None, down_match(3), None],
        [down_match(3), down_match(3), None, None],
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
        [up_match(3), None, up_match(3), None],
        [up_match(4), up_match(3), None, None],
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
        [[down_match(4), right_match(3)],
         [down_match(3)], [left_match(3)], []],
        [[down_match(3)], [], [], []],
        [[up_match(3)], [up_match(3)], [], []],
        [[up_match(4)], [right_match(3)], [], [left_match(3)]],
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
     [right_match(3)(0,
                     0).combine(down_match(4)(0,
                                              0)).combine(down_match(3)(0,
                                                                        1)),
      right_match(3)(3, 1)]),

    (dedent("""\
            | Y | Y | Y | Y |
            | G | G | E | E |
            | Y | Y | E | E |
            | Y | R | R | G |
            """),
     FOUR_SIDE_PARSER,
     [right_match(4)(0, 0)]),

    (dedent("""\
            | Y | Y | Y | G |
            | G | Y | E | E |
            | Y | Y | E | E |
            | Y | R | R | G |
            """),
     FOUR_SIDE_PARSER,
     [right_match(3)(0, 0).combine(down_match(3)(0, 1))]),

    (dedent("""\
            | Y | Y | Y | Y |
            | G | Y | E | E |
            | Y | Y | E | E |
            | Y | R | R | G |
            """),
     FOUR_SIDE_PARSER,
     [right_match(4)(0, 0).combine(down_match(3)(0, 1))]),

    (dedent("""\
            | Y | Y | Y | Y |
            | G | Y | E | E |
            | Y | Y | E | E |
            | Y | Y | Y | G |
            """),
     FOUR_SIDE_PARSER,
     [right_match(4)(0,
                     0).combine(down_match(4)(0,
                                              1)).combine(right_match(3)(3,
                                                                         0))]),

    (dedent("""\
            | Y | Y | Y | T | R |
            | R | R | R | R | R |
            | Y | Y | C | E | T |
            | Y | R | R | R | T |
            | T | R | T | R | T |
            """),
     FIVE_SIDE_PARSER,
     [right_match(3)(0, 0),
      right_match(3)(2, 0),
      right_match(5)(1, 0).combine(right_match(3)(
          3, 1)).combine(down_match(3)(1, 2)),
      down_match(3)(2, 4)]),

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
     [Match([(row, col) for row in range(4) for col in range(4)])]),

    (dedent("""\
            | Y | Y | Y | Y |
            | Y | Y | Y | Y |
            | Y | Y | Y | Y |
            | Y | Y | Y | Y |
            """),
     FOUR_SIDE_PARSER,
     [Match([(row, col) for row in range(4) for col in range(4)])]),

    # make sure our matching alg doesn't perform badly in worst case
    (dedent("""\
            | Y | Y | Y | Y | Y | Y | Y | Y |
            | Y | Y | Y | Y | Y | Y | Y | Y |
            | Y | Y | Y | Y | Y | Y | Y | Y |
            | Y | Y | Y | Y | Y | Y | Y | Y |
            | Y | Y | Y | Y | Y | Y | Y | Y |
            | Y | Y | Y | Y | Y | Y | Y | Y |
            | Y | Y | Y | Y | Y | Y | Y | Y |
            | Y | Y | Y | Y | Y | Y | Y | Y |
            """),
     EIGHT_SIDE_PARSER,
     [Match([(row, col) for row in range(8) for col in range(8)])]),

    # make sure our matching alg doesn't perform badly in worst case with
    # criticals, either
    (dedent("""\
            | C | C | C | C | C | C | C | C |
            | C | C | C | C | C | C | C | C |
            | C | C | C | C | C | C | C | C |
            | C | C | C | C | C | C | C | C |
            | C | C | C | C | C | C | C | C |
            | C | C | C | C | C | C | C | C |
            | C | C | C | C | C | C | C | C |
            | C | C | C | C | C | C | C | C |
            """),
     EIGHT_SIDE_PARSER,
     [Match([(row, col) for row in range(8) for col in range(8)])]),

    (dedent("""\
            | Y | Y | R | G |
            | Y | C | C | R |
            | R | G | P | G |
            | Y | R | Y | R |
            """),
     FOUR_SIDE_PARSER,
     [right_match(3)(1, 0),
      right_match(3)(1, 1)]),

    # cross 5 match
    (dedent("""\
            | Y | G | Y | T | R |
            | R | G | R | G | R |
            | Y | R | R | R | T |
            | Y | Y | R | Y | G |
            | T | R | T | R | T |
            """),
     FIVE_SIDE_PARSER,
     [Match([(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)])]),

    # T 5 match
    (dedent("""\
            | Y | G | Y | T | R |
            | R | G | Y | G | R |
            | Y | R | R | R | T |
            | Y | Y | R | Y | G |
            | T | T | R | T | T |
            """),
     FIVE_SIDE_PARSER,
     [Match([(2, 1), (2, 2), (2, 3), (3, 2), (4, 2)])]),

    ]


def test_find_matches():
    for (board_s, parser, expected) in FIND_MATCHES_CASES:
        board = parse_board(board_s, parser)
        yield _verify_find_matches, board, expected


def _verify_find_matches(board, expected):
    eq_(sorted(expected), find_matches(board))


def test_find_matches_with_stop_after():
    for (board_s, parser, expected) in FIND_MATCHES_CASES:
        board = parse_board(board_s, parser)
        for stop_after in range(1, len(expected) + 1):
            yield (_verify_find_matches_with_stop_after, board,
                   expected, stop_after)


def _verify_find_matches_with_stop_after(board, expected, stop_after):
    matches = find_matches(board, stop_after=stop_after)
    eq_(stop_after, len(matches))
    for match in matches:
        # we can't do a simple in, since we're preventing combining by doing a
        # stop_after.
        ok_(any(m.contains_match(match) for m in expected))


def test_count_tiles_in_match():
    cases = [
        ([], 0),
        ([(0, 0)], 1),
        ([(0, 0), (0, 1), (0, 2)], 3)
        ]

    for (squares, expected) in cases:
        yield _verify_count_tiles_in_match, squares, expected


def _verify_count_tiles_in_match(squares, expected):
    eq_(expected, Match(squares).tile_count)


def test_max_extents():
    cases = [
        ([(0, 1), (0, 2), (0, 3)], {0: 3}, {}),
        ([(1, 1), (2, 1), (3, 1)], {}, {1: 3}),
        ([(0, 0), (1, 0), (2, 0), (3, 0)], {}, {0: 4}),
        ([(0, 2), (1, 1), (1, 2), (1, 3), (2, 2)],
         {1: 3}, {2: 3})
        ]

    for match_args, row_extents, col_extents in cases:
        yield _verify_max_extent, match_args, row_extents, col_extents


def _verify_max_extent(match_args, row_extents, col_extents):
    eq_(dict(rows=row_extents, cols=col_extents),
        Match(match_args).max_extents)


def test_combine():
    cases = [
        ([], [], []),
        ([(0, 0)], [], [(0, 0)]),
        ([(0, 0)], [(0, 1)], [(0, 0), (0, 1)]),
        ([(0, 0)], [(0, 0), (0, 1)], [(0, 0), (0, 1)]),
        ]
    for m1, m2, expected in cases:
        yield _verify_combine, m1, m2, expected
        yield _verify_combine, m2, m1, expected


def _verify_combine(m1, m2, expected):
    eq_(Match(expected), Match(m1).combine(Match(m2)))


def test_has_extent_at_least():
    cases = [
        ([(0, 1), (0, 2), (0, 3)], 3),
        ([(0, 0), (1, 0), (2, 0), (3, 0)], 4),
        ([(0, 2), (1, 0), (1, 1), (1, 2), (1, 3), (2, 2)], 4)
        ]

    for match_args, max_extent in cases:
        for ext in range(max_extent):
            yield _verify_has_extent_at_least, match_args, ext, True
        yield _verify_has_extent_at_least, match_args, max_extent, True
        yield _verify_has_extent_at_least, match_args, max_extent + 1, False


def _verify_has_extent_at_least(match_args, extent, expected):
    eq_(expected, Match(match_args).has_extent_at_least(extent))


def test_contains_match():
    cases = [
        (right_match(4)(0, 0), right_match(3)(0, 0), True),
        (right_match(4)(0, 0), right_match(3)(0, 1), True),
        (right_match(3)(0, 1), right_match(3)(0, 1), True),
        (right_match(3)(0, 1), right_match(3)(1, 0), False),
        (right_match(3)(0, 1), down_match(3)(0, 1), False),
        ]

    for m1, m2, contains in cases:
        yield _verify_contains_match, m1, m2, contains


def _verify_contains_match(m1, m2, contains):
    eq_(contains, m1.contains_match(m2))
