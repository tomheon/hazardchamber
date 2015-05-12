from nose.tools import eq_

from criticals import calc_critical_square
from tutils import right_match, down_match

# (match, exp_crit_sq)
CASES = [
    (right_match(5)(0, 1), (0, 3)),
    (right_match(6)(0, 1), (0, 3)),
    (down_match(5)(1, 1), (3, 1)),
    (down_match(6)(1, 1), (3, 1)),
    (down_match(3)(0, 1).combine(right_match(3)(1, 0)),
     (1, 1)),
    (down_match(3)(0, 1).combine(right_match(3)(0, 0)),
     (0, 1)),
    (down_match(3)(0, 1).combine(right_match(3)(0, 1)),
     (0, 1))
    ]


def test_calc_critical_square():
    for match, exp_crit_square in CASES:
        yield _verify_calc_critical_square, match, exp_crit_square


def _verify_calc_critical_square(match, exp_crit_square):
    eq_(exp_crit_square, calc_critical_square(match))
