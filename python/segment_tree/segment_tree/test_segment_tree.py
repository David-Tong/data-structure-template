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
    # Original template use case: range max + point update
    nums = [2, 1, 5, 3, 6, 4, 8, 7]
    st = SegmentTree(nums)          # aggregate_func=max by default

    assert st.range_query(0, 2) == 5
    assert st.range_query(3, 6) == 8
    assert st.range_query(0, 7) == 8

    st.update(1, 9)
    assert st.range_query(0, 2) == 9
    assert st.range_query(0, 7) == 9


def test_range_maximum():
    # Daily temperatures: find the hottest day in a range, then correct a sensor
    temps = [30, 25, 35, 28, 40, 22, 38, 31]
    st = SegmentTree(temps)

    assert st.range_query(0, 4) == 40
    assert st.range_query(5, 7) == 38
    assert st.range_query(0, 7) == 40

    st.update(4, 33)               # correct faulty sensor at index 4
    assert st.range_query(0, 4) == 35
    assert st.range_query(0, 7) == 38


def test_range_minimum():
    # Stock prices: find the cheapest price in a date range
    prices = [100, 95, 102, 88, 110, 76, 99, 105]
    st = SegmentTree(prices, aggregate_func=min)

    assert st.range_query(0, 3) == 88
    assert st.range_query(4, 7) == 76
    assert st.range_query(0, 7) == 76

    st.update(5, 115)              # correct mis-recorded price at index 5
    assert st.range_query(4, 7) == 99
    assert st.range_query(0, 7) == 88


def test_range_sum():
    # Daily sales: total over any period, then correct a figure
    sales = [200, 150, 300, 250, 400, 180, 220, 350]
    st = SegmentTree(sales, aggregate_func=operator.add)

    assert st.range_query(0, 3) == 900    # week 1
    assert st.range_query(4, 7) == 1150   # week 2
    assert st.range_query(0, 7) == 2050   # all

    st.update(2, 130)                      # correct data entry error at index 2
    assert st.range_query(0, 3) == 730
    assert st.range_query(0, 7) == 1880


def test_range_product():
    # Find the product of all elements in a range
    nums = [1, 2, 3, 4, 5]
    st = SegmentTree(nums, aggregate_func=operator.mul)

    assert st.range_query(0, 2) == 6     # 1*2*3
    assert st.range_query(1, 4) == 120   # 2*3*4*5
    assert st.range_query(0, 4) == 120   # 1*2*3*4*5

    st.update(0, 3)                       # change index 0 from 1 to 3
    assert st.range_query(0, 2) == 18    # 3*2*3
    assert st.range_query(0, 4) == 360   # 3*2*3*4*5


def test_range_update_raises():
    # range_update is blocked on SegmentTree — use LazySegmentTree instead
    st = SegmentTree([1, 2, 3])
    try:
        st.range_update(0, 2, 1)
        assert False, "expected NotImplementedError"
    except NotImplementedError:
        pass
