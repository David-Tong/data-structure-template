import operator
from lazy_segment_tree import LazySegmentTree

# =============================================================================
# LazySegmentTree — Range update, range query
# All indices are 0-based (same as Python lists).
# =============================================================================
#
# HOW IT WORKS
# ------------
# LazySegmentTree extends SegmentTree with efficient range updates using
# lazy propagation — pending updates are deferred until actually needed.
#
#   update(ql, qr, delta)  -> apply delta to every element in [ql..qr] in O(log n)
#   range_query(ql, qr)    -> query over [ql..qr] in O(log n)
#
# Three parameters control behaviour:
#
#   func        -- how to combine two node values for a query
#                  e.g. max, min, operator.add
#
#   update_func -- how a delta is applied to a node value
#                  signature: update_func(current_val, delta) -> new_val
#                  default (additive): lambda val, delta: val + delta
#
#   identity    -- the starting value of every node (neutral element for func)
#                  func=operator.add -> identity=0         (0 + x = x)
#                  func=max          -> identity=float('-inf')
#                  func=min          -> identity=float('inf')
#                  func=operator.mul -> identity=1         (1 * x = x)
#
# NOTE ON find_first
# ------------------
# The original LazySegmentTree template tracked both min and max per node
# and provided find_first(ql, qr, target) — returning the leftmost index
# in [ql..qr] whose value equals target.
#
# This generic template uses a single aggregate value per node instead,
# which does not support find_first directly. If you need find_first,
# you can replicate it by tracking min and max with two separate trees:
#
#   st_min = LazySegmentTree(n, func=min, identity=float('inf'))
#   st_max = LazySegmentTree(n, func=max, identity=float('-inf'))
#
# Then a range [ql..qr] contains target if and only if:
#   st_min.range_query(ql, qr) <= target <= st_max.range_query(ql, qr)
#
# See Example 0 below for the full find_first workaround.
#
# =============================================================================

def show(label, st, n):
    """Print current logical array state by querying each element."""
    vals = [st.range_query(i, i) for i in range(n)]
    print(label)
    print("  index:", list(range(n)))
    print("  value:", vals)
    print()


# -----------------------------------------------------------------------------
# Example 0 — Original template use case: range additive update + find_first
#
# The original LazySegmentTree tracked min and max per node so that
# find_first(ql, qr, target) could find the leftmost index whose value
# equals target.
#
# Workaround using two generic trees (one for min, one for max):
#   - apply the same updates to both trees
#   - a range contains target iff min <= target <= max
#   - walk left-to-right to find the leftmost matching index
# -----------------------------------------------------------------------------
print("=" * 60)
print("Example 0: Original use case — range add + find_first workaround")
print("=" * 60)

n = 5
# Initial values: [0, 0, 0, 0, 0]
#        index:    0  1  2  3  4
st_min = LazySegmentTree(n, aggregate_func=min, identity=float('inf'))
st_max = LazySegmentTree(n, aggregate_func=max, identity=float('-inf'))

def range_add(ql, qr, delta):
    """Apply additive delta to both trees."""
    st_min.update(ql, qr, delta)
    st_max.update(ql, qr, delta)

def find_first(ql, qr, target):
    """Return leftmost index in [ql..qr] whose value equals target, or -1."""
    # check if target exists anywhere in [ql..qr]
    if not (st_min.range_query(ql, qr) <= target <= st_max.range_query(ql, qr)):
        return -1
    # narrow to the leftmost matching index
    lo, hi = ql, qr
    while lo < hi:
        mid = (lo + hi) // 2
        if st_min.range_query(lo, mid) <= target <= st_max.range_query(lo, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

show("Initial (all zeros):", st_min, n)

range_add(0, 2, 3)     # [3, 3, 3, 0, 0]
print("After range_add([0..2], 3):")
show("", st_min, n)
print("find_first([0..4], target=3):", find_first(0, 4, 3))   # 0
print("find_first([0..4], target=0):", find_first(0, 4, 0))   # 3
print("find_first([0..4], target=9):", find_first(0, 4, 9))   # -1

range_add(1, 3, 2)     # [3, 5, 5, 2, 0]
print("\nAfter range_add([1..3], 2):")
show("", st_min, n)
print("find_first([0..4], target=5):", find_first(0, 4, 5))   # 1
print("find_first([0..4], target=2):", find_first(0, 4, 2))   # 3
print("find_first([2..4], target=5):", find_first(2, 4, 5))   # 2
print("find_first([3..4], target=5):", find_first(3, 4, 5))   # -1


# -----------------------------------------------------------------------------
# Example 1 — Range Sum with range add (default update_func)
# Problem: employees have base salaries; give everyone in a department a raise,
#          then query the total salary bill for any group.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 1: Range Sum with range add")
print("=" * 60)

n = 6
# Salaries: [5000, 4000, 4500, 6000, 5500, 4800]
#    index:   0     1     2     3     4     5
salaries = [5000, 4000, 4500, 6000, 5500, 4800]
st = LazySegmentTree(n, aggregate_func=operator.add, identity=0)
for i, s in enumerate(salaries):
    st.update(i, i, s)

show("Initial salaries:", st, n)
print("Total salary [0..5]:", st.range_query(0, 5))   # 29800
print("Total salary [2..4]:", st.range_query(2, 4))   # 16000

st.update(1, 3, 500)   # give department [1..3] a 500 raise
print("\nAfter giving [1..3] a 500 raise:")
show("", st, n)
print("Total salary [0..5]:", st.range_query(0, 5))   # 31300
print("Total salary [1..3]:", st.range_query(1, 3))   # 17500

st.update(0, 5, 200)   # give everyone a 200 raise
print("After giving everyone [0..5] a 200 raise:")
show("", st, n)
print("Total salary [0..5]:", st.range_query(0, 5))   # 32500


# -----------------------------------------------------------------------------
# Example 2 — Range Max with range add
# Problem: players have scores; add bonus points to a range of players,
#          then find the highest score in any range.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 2: Range Max with range add")
print("=" * 60)

n = 6
# Scores: [10, 20, 15, 30, 25, 18]
#  index:   0   1   2   3   4   5
scores = [10, 20, 15, 30, 25, 18]
st_max = LazySegmentTree(n, aggregate_func=max, identity=float('-inf'))
for i, s in enumerate(scores):
    st_max.update(i, i, s)

show("Initial scores:", st_max, n)
print("Highest score [0..5]:", st_max.range_query(0, 5))  # 30
print("Highest score [0..2]:", st_max.range_query(0, 2))  # 20

st_max.update(2, 4, 10)   # award 10 bonus points to players [2..4]
print("After adding 10 bonus to [2..4]:")
show("", st_max, n)
print("Highest score [0..5]:", st_max.range_query(0, 5))  # 40
print("Highest score [0..2]:", st_max.range_query(0, 2))  # 25


# -----------------------------------------------------------------------------
# Example 3 — Range Min with range add
# Problem: items have prices; apply a discount to a range,
#          then find the cheapest item in any range.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 3: Range Min with range add")
print("=" * 60)

n = 5
# Prices: [100, 80, 120, 90, 110]
#  index:   0   1    2   3    4
prices = [100, 80, 120, 90, 110]
st_min = LazySegmentTree(n, aggregate_func=min, identity=float('inf'))
for i, p in enumerate(prices):
    st_min.update(i, i, p)

show("Initial prices:", st_min, n)
print("Cheapest in [0..4]:", st_min.range_query(0, 4))   # 80
print("Cheapest in [2..4]:", st_min.range_query(2, 4))   # 90

st_min.update(1, 3, -15)   # apply -15 discount to items [1..3]
print("After applying -15 discount to [1..3]:")
show("", st_min, n)
print("Cheapest in [0..4]:", st_min.range_query(0, 4))   # 65
print("Cheapest in [2..4]:", st_min.range_query(2, 4))   # 75


# -----------------------------------------------------------------------------
# Example 4 — Custom update_func: range multiply
# Problem: scale values in a range by a multiplier, then query the total sum.
#
# Three parameters work together:
#   aggregate_func=operator.add          -- query returns the SUM of a range
#   update_func=lambda val, d: val * d   -- each element is MULTIPLIED by delta
#   identity=1                           -- neutral element for multiplication
#                                           (1 * x = x), so unset nodes start
#                                           at 1 and update(i, i, v) gives
#                                           1 * v = v correctly
#
# Why identity=1 and not 0?
#   update_func(0, v) = 0 * v = 0 — every element would stay zero forever.
#
# Limitation: the internal lazy accumulator uses lazy += delta (additive).
# If two multiplicative range updates overlap on the same node before the
# lazy value is pushed down, the deltas are added instead of multiplied,
# giving a wrong result. This example is safe because the single range
# update st.update(1, 3, 2) does not overlap with itself. Do not stack
# overlapping range-multiply updates without a custom _apply/_push_down.
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Example 4: Custom update_func — Range Multiply")
print("=" * 60)

n = 5
# Values: [2, 3, 4, 5, 6]
#  index:  0  1  2  3  4
values = [2, 3, 4, 5, 6]
st_mul = LazySegmentTree(
    n,
    aggregate_func=operator.add,
    update_func=lambda val, delta: val * delta,
    identity=1
)
for i, v in enumerate(values):
    st_mul.update(i, i, v)

show("Initial values:", st_mul, n)
print("Sum [0..4]:", st_mul.range_query(0, 4))   # 20

st_mul.update(1, 3, 2)   # double every element in [1..3]
print("After multiplying [1..3] by 2:")
show("", st_mul, n)
# values now: [2, 6, 8, 10, 6]
print("Sum [0..4]:", st_mul.range_query(0, 4))   # 32
print("Sum [1..3]:", st_mul.range_query(1, 3))   # 24
