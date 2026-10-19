# -*- coding: utf-8 -*-
import sys
import os
import operator
sys.path.insert(0, os.path.dirname(__file__))
from segment_tree import SegmentTree


# =============================================================================
# SegmentTree — Point update, range query
# All indices are 0-based (same as Python lists).
#
# Run with:  pytest test_segment_tree.py -v
# =============================================================================


def test_range_maximum_original_use_case():
    # Expected query results, in assertion order: 5, 8, 8, 9, 9.
    # Before: [2, 1, 5, 3, 6, 4, 8, 7]
    # Indices 0 through 2: [2, 1, 5] -> largest = 5.
    # Indices 3 through 6: [3, 6, 4, 8] -> largest = 8.
    # Set index 1 to 9:
    # After:  [2, 9, 5, 3, 6, 4, 8, 7]
    # The largest value in indices 0 through 2 and the whole array is now 9.
    nums = [2, 1, 5, 3, 6, 4, 8, 7]
    st = SegmentTree(nums)          # aggregate_func=max by default

    assert st.range_query(0, 2) == 5
    assert st.range_query(3, 6) == 8
    assert st.range_query(0, 7) == 8

    st.update(1, 9)
    assert st.range_query(0, 2) == 9
    assert st.range_query(0, 7) == 9


def test_range_maximum():
    # Expected query results, in assertion order: 40, 38, 40, 35, 38.
    # Before: [30, 25, 35, 28, 40, 22, 38, 31]
    # Largest in indices 0 through 4 = 40; in 5 through 7 = 38; overall = 40.
    # Set index 4 to 33:
    # After:  [30, 25, 35, 28, 33, 22, 38, 31]
    # Largest in indices 0 through 4 = 35; overall = 38.
    temps = [30, 25, 35, 28, 40, 22, 38, 31]
    st = SegmentTree(temps)

    assert st.range_query(0, 4) == 40
    assert st.range_query(5, 7) == 38
    assert st.range_query(0, 7) == 40

    st.update(4, 33)               # correct faulty sensor at index 4
    assert st.range_query(0, 4) == 35
    assert st.range_query(0, 7) == 38


def test_range_minimum():
    # Expected query results, in assertion order: 88, 76, 76, 99, 88.
    # Before: [100, 95, 102, 88, 110, 76, 99, 105]
    # Smallest in indices 0 through 3 = 88; in 4 through 7 = 76; overall = 76.
    # Set index 5 to 115:
    # After:  [100, 95, 102, 88, 110, 115, 99, 105]
    # Smallest in indices 4 through 7 = 99; overall = 88.
    prices = [100, 95, 102, 88, 110, 76, 99, 105]
    st = SegmentTree(prices, aggregate_func=min)

    assert st.range_query(0, 3) == 88
    assert st.range_query(4, 7) == 76
    assert st.range_query(0, 7) == 76

    st.update(5, 115)              # correct mis-recorded price at index 5
    assert st.range_query(4, 7) == 99
    assert st.range_query(0, 7) == 88


def test_range_sum():
    # Expected query results, in assertion order: 900, 1150, 2050, 730, 1880.
    # Before: [200, 150, 300, 250, 400, 180, 220, 350]
    # First four sum to 900; last four sum to 1150; total = 2050.
    # Set index 2 to 130:
    # After:  [200, 150, 130, 250, 400, 180, 220, 350]
    # First four sum to 730; total = 1880.
    sales = [200, 150, 300, 250, 400, 180, 220, 350]
    st = SegmentTree(sales, aggregate_func=operator.add)

    assert st.range_query(0, 3) == 900    # week 1
    assert st.range_query(4, 7) == 1150   # week 2
    assert st.range_query(0, 7) == 2050   # all

    st.update(2, 130)                      # correct data entry error at index 2
    assert st.range_query(0, 3) == 730
    assert st.range_query(0, 7) == 1880


def test_range_product():
    # Expected query results, in assertion order: 6, 120, 120, 18, 360.
    # Before: [1, 2, 3, 4, 5]
    # First three multiply to 6; last four and all five multiply to 120.
    # Set index 0 to 3:
    # After:  [3, 2, 3, 4, 5]
    # First three multiply to 18; all five multiply to 360.
    nums = [1, 2, 3, 4, 5]
    st = SegmentTree(nums, aggregate_func=operator.mul)

    assert st.range_query(0, 2) == 6     # 1*2*3
    assert st.range_query(1, 4) == 120   # 2*3*4*5
    assert st.range_query(0, 4) == 120   # 1*2*3*4*5

    st.update(0, 3)                       # change index 0 from 1 to 3
    assert st.range_query(0, 2) == 18    # 3*2*3
    assert st.range_query(0, 4) == 360   # 3*2*3*4*5


def test_range_update_raises():
    # Expected outcome: range_update(0, 2, 1) raises NotImplementedError.
    # Start: [1, 2, 3]
    # Requested change: add 1 to all three -> [2, 3, 4].
    # This operation is unsupported: expect NotImplementedError instead.
    # SegmentTree only allows changing one element at a time.
    st = SegmentTree([1, 2, 3])
    try:
        st.range_update(0, 2, 1)
        assert False, "expected NotImplementedError"
    except NotImplementedError:
        pass
