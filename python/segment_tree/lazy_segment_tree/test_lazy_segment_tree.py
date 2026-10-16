# -*- coding: utf-8 -*-
import sys
import os
import operator
sys.path.insert(0, os.path.dirname(__file__))
from lazy_segment_tree import LazySegmentTree


# =============================================================================
# LazySegmentTree — Range update, range query
# All indices are 0-based (same as Python lists).
#
# Run with:  pytest test_lazy_segment_tree.py -v
# =============================================================================


def _make_st(n, vals, aggregate_func=max, update_func=None, identity=0):
    """Helper: build a LazySegmentTree and initialise it element by element."""
    st = LazySegmentTree(n, aggregate_func=aggregate_func,
                         update_func=update_func, identity=identity)
    for i, v in enumerate(vals):
        st.update(i, i, v)   # size=1 for a single element, so update_func(0, v, 1) = v
    return st


def test_find_first_workaround():
    # Original template use case: range additive update + find_first.
    # Workaround: two trees (min + max) and binary search.
    # All elements start at 0 (identity=0). range_add accumulates onto that base.
    # identity=0 is correct here: 0 + delta = delta, so additive init works.
    n = 5
    st_min = LazySegmentTree(n, aggregate_func=min, identity=0)
    st_max = LazySegmentTree(n, aggregate_func=max, identity=0)

    def range_add(ql, qr, delta):
        st_min.update(ql, qr, delta)
        st_max.update(ql, qr, delta)

    def find_first(ql, qr, target):
        """Leftmost index in [ql..qr] whose value equals target, or -1."""
        if not (st_min.range_query(ql, qr) <= target <= st_max.range_query(ql, qr)):
            return -1
        lo, hi = ql, qr
        while lo < hi:
            mid = (lo + hi) // 2
            if st_min.range_query(lo, mid) <= target <= st_max.range_query(lo, mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

    # Initial: [0, 0, 0, 0, 0]
    range_add(0, 2, 3)             # [3, 3, 3, 0, 0]
    assert find_first(0, 4, 3) == 0
    assert find_first(0, 4, 0) == 3
    assert find_first(0, 4, 9) == -1

    range_add(1, 3, 2)             # [3, 5, 5, 2, 0]
    assert find_first(0, 4, 5) == 1
    assert find_first(0, 4, 2) == 3
    assert find_first(2, 4, 5) == 2
    assert find_first(3, 4, 5) == -1


def test_range_sum_with_range_add():
    # Employees have base salaries; apply raises to a department, then query totals.
    salaries = [5000, 4000, 4500, 6000, 5500, 4800]
    n = len(salaries)
    # For sum, update_func must scale delta by size so a range update adds
    # delta to each element, not just once to the node's aggregate.
    st = _make_st(n, salaries, aggregate_func=operator.add,
                  update_func=lambda val, delta, size: val + delta * size,
                  identity=0)

    assert st.range_query(0, 5) == 29800
    assert st.range_query(2, 4) == 16000

    st.update(1, 3, 500)           # give department [1..3] a 500 raise
    # [1..3]: 4000+500=4500, 4500+500=5000, 6000+500=6500 -> sum=16000
    assert st.range_query(0, 5) == 31300
    assert st.range_query(1, 3) == 16000

    st.update(0, 5, 200)           # give everyone a 200 raise
    assert st.range_query(0, 5) == 32500


def test_range_max_with_range_add():
    # Players have scores; add bonus points to a range, then find the highest score.
    scores = [10, 20, 15, 30, 25, 18]
    n = len(scores)
    # identity=0: nodes start at 0, update(i,i,v) adds v -> node gets v
    st = _make_st(n, scores, aggregate_func=max, identity=0)

    assert st.range_query(0, 5) == 30
    assert st.range_query(0, 2) == 20

    st.update(2, 4, 10)            # award 10 bonus points to players [2..4]
    assert st.range_query(0, 5) == 40
    assert st.range_query(0, 2) == 25


def test_range_min_with_range_add():
    # Items have prices; apply a discount to a range, then find the cheapest.
    prices = [100, 80, 120, 90, 110]
    n = len(prices)
    # identity=0: nodes start at 0, update(i,i,v) adds v -> node gets v
    st = _make_st(n, prices, aggregate_func=min, identity=0)

    assert st.range_query(0, 4) == 80
    assert st.range_query(2, 4) == 90

    st.update(1, 3, -15)           # apply -15 discount to items [1..3]
    assert st.range_query(0, 4) == 65
    assert st.range_query(2, 4) == 75


def test_range_multiply_no_overlap():
    # Scale values in a range by a multiplier, then query the total sum.
    # update_func is multiplicative; identity=1 so 1*v=v on initialisation.
    # Safe here because the single range update does not overlap itself.
    values = [2, 3, 4, 5, 6]
    n = len(values)
    st = _make_st(n, values,
                  aggregate_func=operator.add,
                  update_func=lambda val, delta, size: val * delta,
                  identity=1)

    assert st.range_query(0, 4) == 20  # 2+3+4+5+6

    st.update(1, 3, 2)                 # double every element in [1..3]: [2,6,8,10,6]
    assert st.range_query(0, 4) == 32  # 2+6+8+10+6
    assert st.range_query(1, 3) == 24  # 6+8+10
