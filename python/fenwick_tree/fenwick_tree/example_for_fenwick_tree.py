# -*- coding: utf-8 -*-
"""Run from the repository root:

    python python/fenwick_tree/fenwick_tree/example_for_fenwick_tree.py

No third-party dependencies are required. Indices are 0-based and inclusive.
"""
from __future__ import print_function

from fenwick_tree import FenwickTree


def demonstrate_point_updates():
    # Start:                      [0, 0, 0, 0, 0]
    # Load initial sales:         [200, 150, 300, 250, 400]
    # Add 50 at index 1:          [200, 200, 300, 250, 400]
    # Set index 2 to 130 (-170):  [200, 200, 130, 250, 400]
    # Initially: prefix [0..2] = 650, range [1..3] = 700, total = 1300.
    # After adding 50: prefix [0..2] = 200 + 200 + 300 = 700.
    # After setting index 2: range [1..3] = 200 + 130 + 250 = 580;
    # total = 200 + 200 + 130 + 250 + 400 = 1180.
    # The empty prefix sum(-1) is always 0.

    # Load a nonzero array by adding each value to an initially zero tree.
    sales = [200, 150, 300, 250, 400]
    tree = FenwickTree(len(sales))
    for index, value in enumerate(sales):
        tree.add(index, value)

    print("Initial sales: {}".format(sales))
    print("Prefix sum [0..2]: {}".format(tree.sum(2)))  # Expected: 650

    # Remove the prefix before the left endpoint to get an inclusive range.
    left, right = 1, 3
    total = tree.sum(right) - tree.sum(left - 1)
    print("Range sum [1..3]: {}".format(total))  # Expected: 700
    print("Total sales: {}".format(tree.sum(len(sales) - 1)))  # Expected: 1300
    print("Empty prefix: {}".format(tree.sum(-1)))  # Expected: 0

    # add changes the value by a delta, rather than replacing it.
    tree.add(1, 50)
    sales[1] += 50
    print("After adding 50 at index 1: {}".format(sales))
    print("Prefix sum [0..2]: {}".format(tree.sum(2)))  # Expected: 700

    # To assign a value, subtract its old value to calculate the delta.
    index, new_value = 2, 130
    tree.add(index, new_value - sales[index])
    sales[index] = new_value
    print("After setting index 2 to 130: {}".format(sales))
    total = tree.sum(right) - tree.sum(left - 1)
    print("Range sum [1..3]: {}".format(total))  # Expected: 580
    print("Total sales: {}".format(tree.sum(len(sales) - 1)))  # Expected: 1180


def demonstrate_range_updates():
    # Start:                       [0, 0, 0, 0, 0]
    # Add 3 to indices 1 through 3: [0, 3, 3, 3, 0]
    # Subtract 1 from 2 through 4:  [0, 3, 2, 2, -1]
    # Add 2 to all elements:        [2, 5, 4, 4, 1]
    # Expected totals after updates: 9, 6, 16.
    n = 5
    # Store differences D[i] in b1 and i * D[i] in b2.
    b1, b2 = FenwickTree(n), FenwickTree(n)

    def prefix_sum(index):
        return (index + 1) * b1.sum(index) - b2.sum(index)

    def range_sum(left, right):
        return prefix_sum(right) - prefix_sum(left - 1)

    print("Range updates using two Fenwick trees:")
    print("Start: [0, 0, 0, 0, 0]")
    for left, right, delta in [(1, 3, 3), (2, 4, -1), (0, 4, 2)]:
        # Start the addition at left and stop it just after right.
        b1.add(left, delta)
        b2.add(left, left * delta)
        if right + 1 < n:
            b1.add(right + 1, -delta)
            b2.add(right + 1, -(right + 1) * delta)

        # Query each element to display the array represented by the trees.
        values = [range_sum(i, i) for i in range(n)]
        print("After adding {} to [{}..{}]: {}".format(delta, left, right, values))
        print("Total: {}".format(range_sum(0, n - 1)))


def main():
    demonstrate_point_updates()
    demonstrate_range_updates()


if __name__ == "__main__":
    main()
