# -*- coding: utf-8 -*-
"""Run: python python/segment_tree/lazy_segment_tree/example_for_lazy_segment_tree.py

No third-party dependencies. All indices are 0-based and ranges are inclusive.
"""
from __future__ import print_function

import operator
from lazy_segment_tree import LazySegmentTree


def demonstrate_range_updates():
    print("=== demonstrate_range_updates() ===")
    # Start:                       [0, 0, 0, 0, 0]
    # Add 3 to indices 1 through 3: [0, 3, 3, 3, 0]
    # Subtract 1 from 2 through 4:  [0, 3, 2, 2, -1]
    # Add 2 to all elements:        [2, 5, 4, 4, 1]
    # Expected totals after updates: 9, 6, 16.
    # Expected sums [1..3] after updates: 9, 7, 13.
    # A sum increases by delta once per element in the covered node.
    tree = LazySegmentTree(5, aggregate_func=operator.add,
                           update_func=lambda value, delta, size: value + delta * size,
                           identity=0)
    print("Start: [0, 0, 0, 0, 0]")
    for left, right, delta in [(1, 3, 3), (2, 4, -1), (0, 4, 2)]:
        # update adds delta throughout the range; it does not assign values.
        tree.update(left, right, delta)
        values = [tree.range_query(i, i) for i in range(5)]
        print("After adding {} to [{}..{}]: {}".format(delta, left, right, values))
        print("Total: {}".format(tree.range_query(0, 4)))
        print("Range sum [1..3]: {}".format(tree.range_query(1, 3)))


def demonstrate_min_max_queries():
    print("=== demonstrate_min_max_queries() ===")
    # Start:                         [10, 20, 15, 30, 25]
    # Subtract 15 from 1 through 3:   [10, 5, 0, 15, 25]
    # Overall minimum: 10 -> 0; overall maximum: 30 -> 25.
    values = [10, 20, 15, 30, 25]
    # For min/max, the default update function shifts the aggregate by delta.
    minimum = LazySegmentTree(5, aggregate_func=min, identity=0, nums=values)
    maximum = LazySegmentTree(5, aggregate_func=max, identity=0, nums=values)
    print("Initial values: {}".format(values))
    print("Minimum: {}".format(minimum.range_query(0, 4)))  # Expected: 10
    print("Maximum: {}".format(maximum.range_query(0, 4)))  # Expected: 30
    # range_update is an alias for update. Apply the change to both trees.
    minimum.range_update(1, 3, -15)
    maximum.range_update(1, 3, -15)
    values = [minimum.range_query(i, i) for i in range(5)]
    print("After subtracting 15 from [1..3]: {}".format(values))
    print("Minimum: {}".format(minimum.range_query(0, 4)))  # Expected: 0
    print("Maximum: {}".format(maximum.range_query(0, 4)))  # Expected: 25


def main():
    demonstrate_range_updates()
    print()
    demonstrate_min_max_queries()


if __name__ == "__main__":
    main()
