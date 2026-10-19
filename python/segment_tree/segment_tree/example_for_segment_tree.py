# -*- coding: utf-8 -*-
"""Run: python python/segment_tree/segment_tree/example_for_segment_tree.py

No third-party dependencies. All indices are 0-based and ranges are inclusive.
"""
from __future__ import print_function

import operator
from segment_tree import SegmentTree


def demonstrate_point_updates():
    print("=== demonstrate_point_updates() ===")
    # Start:                 [200, 150, 300, 250, 400]
    # Set index 2 to 130:    [200, 150, 130, 250, 400]
    # Initially: sum [1..3] = 700, total = 1300.
    # After assignment: sum [1..3] = 530, total = 1130.
    sales = [200, 150, 300, 250, 400]
    tree = SegmentTree(sales, aggregate_func=operator.add)
    print("Initial sales: {}".format(sales))
    print("Range sum [1..3]: {}".format(tree.range_query(1, 3)))  # Expected: 700
    print("Total: {}".format(tree.range_query(0, 4)))  # Expected: 1300

    # Unlike FenwickTree.add, update assigns the new value directly.
    tree.update(2, 130)
    sales[2] = 130
    print("After setting index 2 to 130: {}".format(sales))
    print("Range sum [1..3]: {}".format(tree.range_query(1, 3)))  # Expected: 530
    print("Total: {}".format(tree.range_query(0, 4)))  # Expected: 1130


def demonstrate_min_max_queries():
    print("=== demonstrate_min_max_queries() ===")
    # Start:                [10, 20, 15, 30, 25]
    # Set index 3 to 5:     [10, 20, 15, 5, 25]
    # Overall minimum: 10 -> 5; overall maximum: 30 -> 25.
    values = [10, 20, 15, 30, 25]
    minimum = SegmentTree(values, aggregate_func=min)
    maximum = SegmentTree(values)  # The default aggregate is max.
    print("Initial values: {}".format(values))
    print("Minimum: {}".format(minimum.range_query(0, 4)))  # Expected: 10
    print("Maximum: {}".format(maximum.range_query(0, 4)))  # Expected: 30
    # Each independent tree must receive the assignment.
    minimum.update(3, 5)
    maximum.update(3, 5)
    values[3] = 5
    print("After setting index 3 to 5: {}".format(values))
    print("Minimum: {}".format(minimum.range_query(0, 4)))  # Expected: 5
    print("Maximum: {}".format(maximum.range_query(0, 4)))  # Expected: 25


def demonstrate_custom_aggregate():
    print("=== demonstrate_custom_aggregate() ===")
    # Start:                [1, 2, 3, 4, 5]
    # Set index 0 to 3:     [3, 2, 3, 4, 5]
    # Product [0..2]: 1 * 2 * 3 = 6 -> 3 * 2 * 3 = 18.
    # The merge function must be associative; multiplication is one example.
    tree = SegmentTree([1, 2, 3, 4, 5], aggregate_func=operator.mul)
    print("Initial product [0..2]: {}".format(tree.range_query(0, 2)))  # Expected: 6
    tree.update(0, 3)
    print("Product [0..2] after setting index 0 to 3: {}".format(
        tree.range_query(0, 2)))  # Expected: 18


def main():
    demonstrate_point_updates()
    print()
    demonstrate_min_max_queries()
    print()
    demonstrate_custom_aggregate()


if __name__ == "__main__":
    main()
