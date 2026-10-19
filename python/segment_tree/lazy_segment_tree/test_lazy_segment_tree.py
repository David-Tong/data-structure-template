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


def test_find_first_workaround():
    # Expected search results, in assertion order: 0, 3, -1, 1, 3, 2, -1.
    # Start:                       [0, 0, 0, 0, 0]
    # Add 3 to indices 0 through 2: [3, 3, 3, 0, 0]
    # First 3 is at index 0; first 0 is at index 3; 9 is absent (-1).
    # Add 2 to indices 1 through 3: [3, 5, 5, 2, 0]
    # First 5 is at index 1; first 2 is at index 3.
    # Within indices 2 through 4, [5, 2, 0], the first 5 is at index 2.
    # Within indices 3 through 4, [2, 0], there is no 5 (-1).
    # This search is not correct for every array: [1, 3] has no 2,
    # even though 2 lies between its smallest and largest values.
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
    # Expected query results, in assertion order: 29800, 16000, 31300, 16000, 32500.
    # Start:                         [5000, 4000, 4500, 6000, 5500, 4800]
    # Add 500 to indices 1 through 3: [5000, 4500, 5000, 6500, 5500, 4800]
    # Add 200 to all six:             [5200, 4700, 5200, 6700, 5700, 5000]
    # Totals after these steps: 29800 -> 31300 -> 32500.
    # After the first raise, indices 1 through 3 are [4500, 5000, 6500], sum = 16000.
    salaries = [5000, 4000, 4500, 6000, 5500, 4800]
    st = LazySegmentTree(len(salaries), aggregate_func=operator.add,
                         update_func=lambda val, delta, size: val + delta * size,
                         identity=0, nums=salaries)

    assert st.range_query(0, 5) == 29800
    assert st.range_query(2, 4) == 16000

    st.update(1, 3, 500)           # give department [1..3] a 500 raise
    # [1..3]: 4000+500=4500, 4500+500=5000, 6000+500=6500 -> sum=16000
    assert st.range_query(0, 5) == 31300
    assert st.range_query(1, 3) == 16000

    st.update(0, 5, 200)           # give everyone a 200 raise
    assert st.range_query(0, 5) == 32500


def test_range_max_with_range_add():
    # Expected query results, in assertion order: 30, 20, 40, 25.
    # Before: [10, 20, 15, 30, 25, 18]
    # Add 10 to indices 2 through 4:
    # After:  [10, 20, 25, 40, 35, 18]
    # Largest overall: 30 -> 40.
    # Largest in indices 0 through 2: 20 -> 25.
    scores = [10, 20, 15, 30, 25, 18]
    st = LazySegmentTree(len(scores), aggregate_func=max, identity=0, nums=scores)

    assert st.range_query(0, 5) == 30
    assert st.range_query(0, 2) == 20

    st.update(2, 4, 10)            # award 10 bonus points to players [2..4]
    assert st.range_query(0, 5) == 40
    assert st.range_query(0, 2) == 25


def test_range_min_with_range_add():
    # Expected query results, in assertion order: 80, 90, 65, 75.
    # Before: [100, 80, 120, 90, 110]
    # Subtract 15 from indices 1 through 3:
    # After:  [100, 65, 105, 75, 110]
    # Smallest overall: 80 -> 65.
    # Smallest in indices 2 through 4: 90 -> 75.
    prices = [100, 80, 120, 90, 110]
    st = LazySegmentTree(len(prices), aggregate_func=min, identity=0, nums=prices)

    assert st.range_query(0, 4) == 80
    assert st.range_query(2, 4) == 90

    st.update(1, 3, -15)           # apply -15 discount to items [1..3]
    assert st.range_query(0, 4) == 65
    assert st.range_query(2, 4) == 75


def test_range_update_alias():
    # Expected point-query results for BOTH trees, i = 0..4: [10, 25, 20, 35, 25].
    # Expected range_query(0, 4) for BOTH trees: 35.
    # Both trees start with: [10, 20, 15, 30, 25]
    # Add 5 to indices 1 through 3 using update on one tree
    # and range_update on the other.
    # Both should represent: [10, 25, 20, 35, 25]
    # Compare every value and the largest value in the whole array.
    vals = [10, 20, 15, 30, 25]
    st_a = LazySegmentTree(len(vals), aggregate_func=max, identity=0, nums=vals)
    st_b = LazySegmentTree(len(vals), aggregate_func=max, identity=0, nums=vals)

    st_a.update(1, 3, 5)
    st_b.range_update(1, 3, 5)

    for i in range(len(vals)):
        assert st_a.range_query(i, i) == st_b.range_query(i, i)
    assert st_a.range_query(0, 4) == st_b.range_query(0, 4)


def test_range_multiply_no_overlap():
    # Expected query results, in assertion order: 20, 32, 24.
    # Before: [2, 3, 4, 5, 6] -> total = 20.
    # Double indices 1 through 3:
    # After:  [2, 6, 8, 10, 6] -> total = 32.
    # Indices 1 through 3 contain [6, 8, 10] -> sum = 24.
    # Only one multiplication update is tested. Repeated updates on overlapping
    # ranges can give wrong answers: pending update values are added, not multiplied.
    values = [2, 3, 4, 5, 6]
    st = LazySegmentTree(len(values), aggregate_func=operator.add,
                         update_func=lambda val, delta, size: val * delta,
                         identity=1, nums=values)

    assert st.range_query(0, 4) == 20  # 2+3+4+5+6

    st.update(1, 3, 2)                 # double every element in [1..3]: [2,6,8,10,6]
    assert st.range_query(0, 4) == 32  # 2+6+8+10+6
    assert st.range_query(1, 3) == 24  # 6+8+10
