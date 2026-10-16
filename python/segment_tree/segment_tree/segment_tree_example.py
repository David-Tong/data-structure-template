import operator
from segment_tree import SegmentTree

# =============================================================================
# SegmentTree — Point update, range query
# All indices are 0-based (same as Python lists).
# =============================================================================
#
# HOW IT WORKS
# ------------
# Given an array, SegmentTree builds an internal binary tree so that:
#   - update(idx, val)    -> change one element in O(log n)
#   - range_query(ql, qr) -> query over [ql..qr] in O(log n)
#
# The aggregate function (func) decides what "query" means:
#   func=max          -> range maximum
#   func=min          -> range minimum
#   func=operator.add -> range sum
#   func=<any f(a,b)> -> any associative binary function
#
# =============================================================================

def print_array(label, arr):
    print(label)
    print("  index:", list(range(len(arr))))
    print("  value:", arr)
    print()


# -----------------------------------------------------------------------------
# Example 0 — Original template use case: Range Maximum with point update
#
# This directly replicates what the original SegmentTree template was built for:
#   - build from a list of numbers
#   - point update a single element
#   - query the maximum over any range
#
# The original template hardcoded func=max. Our template makes it configurable
# but func=max is still the default, so the call is identical.
# -----------------------------------------------------------------------------
print("=" * 60)
print("Example 0: Original use case — Range Maximum, Point Update")
print("=" * 60)

nums = [2, 1, 5, 3, 6, 4, 8, 7]
#  idx:  0  1  2  3  4  5  6  7
print_array("Initial array:", nums)

st = SegmentTree(nums)           # func=max by default, same as original template

# Range max queries
print("Max [0..2]:", st.range_query(0, 2))   # 5
print("Max [3..6]:", st.range_query(3, 6))   # 8
print("Max [0..7]:", st.range_query(0, 7))   # 8

# Point update: set index 1 to 9
st.update(1, 9)
nums[1] = 9
print_array("\nAfter update(1, 9):", nums)
print("Max [0..2]:", st.range_query(0, 2))   # 9
print("Max [0..7]:", st.range_query(0, 7))   # 9


# -----------------------------------------------------------------------------
# Example 1 — Range Maximum (real-world context)
# Problem: given daily temperatures, find the hottest day in any range,
#          then update a reading and query again.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 1: Range Maximum")
print("=" * 60)

temps = [30, 25, 35, 28, 40, 22, 38, 31]
#  idx:   0   1   2   3   4   5   6   7
print_array("Initial temperatures:", temps)

st = SegmentTree(temps)

print("Hottest in [0..4]:", st.range_query(0, 4))   # 40
print("Hottest in [5..7]:", st.range_query(5, 7))   # 38
print("Hottest in [0..7]:", st.range_query(0, 7))   # 40

# Sensor at index 4 was faulty — correct it to 33
st.update(4, 33)
temps[4] = 33
print_array("\nAfter correcting index 4 to 33:", temps)
print("Hottest in [0..4]:", st.range_query(0, 4))   # 35
print("Hottest in [0..7]:", st.range_query(0, 7))   # 38


# -----------------------------------------------------------------------------
# Example 2 — Range Minimum
# Problem: given stock prices, find the cheapest price in a date range.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 2: Range Minimum")
print("=" * 60)

prices = [100, 95, 102, 88, 110, 76, 99, 105]
#   idx:   0    1    2   3    4   5   6    7
print_array("Stock prices:", prices)

st_min = SegmentTree(prices, aggregate_func=min)

print("Cheapest in [0..3]:", st_min.range_query(0, 3))  # 88
print("Cheapest in [4..7]:", st_min.range_query(4, 7))  # 76
print("Cheapest in [0..7]:", st_min.range_query(0, 7))  # 76

# Price at index 5 was mis-recorded — correct it to 115
st_min.update(5, 115)
prices[5] = 115
print_array("\nAfter correcting index 5 to 115:", prices)
print("Cheapest in [4..7]:", st_min.range_query(4, 7))  # 99
print("Cheapest in [0..7]:", st_min.range_query(0, 7))  # 88


# -----------------------------------------------------------------------------
# Example 3 — Range Sum
# Problem: given daily sales figures, find the total sales over any period,
#          then correct a figure and re-query.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 3: Range Sum")
print("=" * 60)

sales = [200, 150, 300, 250, 400, 180, 220, 350]
#  idx:   0    1    2    3    4    5    6    7
print_array("Daily sales:", sales)

st_sum = SegmentTree(sales, aggregate_func=operator.add)

print("Total [0..3] (week 1):", st_sum.range_query(0, 3))  # 900
print("Total [4..7] (week 2):", st_sum.range_query(4, 7))  # 1150
print("Total [0..7] (all)   :", st_sum.range_query(0, 7))  # 2050

# Day 2 (index 2) had a data entry error — correct from 300 to 130
st_sum.update(2, 130)
sales[2] = 130
print_array("\nAfter correcting index 2 from 300 to 130:", sales)
print("Total [0..3] (week 1):", st_sum.range_query(0, 3))  # 730
print("Total [0..7] (all)   :", st_sum.range_query(0, 7))  # 1880


# -----------------------------------------------------------------------------
# Example 4 — Custom function: range product
# Problem: find the product of all elements in a range.
# Any associative binary function works as func.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 4: Custom function — Range Product")
print("=" * 60)

nums = [1, 2, 3, 4, 5]
#  idx:  0  1  2  3  4
print_array("Numbers:", nums)

st_prod = SegmentTree(nums, aggregate_func=operator.mul)

print("Product [0..2]:", st_prod.range_query(0, 2))   # 6   (1*2*3)
print("Product [1..4]:", st_prod.range_query(1, 4))   # 120 (2*3*4*5)
print("Product [0..4]:", st_prod.range_query(0, 4))   # 120 (1*2*3*4*5)

st_prod.update(0, 3)   # change index 0 from 1 to 3
nums[0] = 3
print_array("\nAfter updating index 0 to 3:", nums)
print("Product [0..2]:", st_prod.range_query(0, 2))   # 18  (3*2*3)
print("Product [0..4]:", st_prod.range_query(0, 4))   # 360 (3*2*3*4*5)
