# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from fenwick_tree import FenwickTree


# All indices are 0-based (same as Python lists).
# Run with: pytest test_fenwick_tree.py -v


def test_prefix_sums_after_updates():
    # Expected sum(0)..sum(4), in update order:
    # Start:          [0, 0, 0, 0, 0]
    # Add 3 at 0:     [3, 3, 3, 3, 3]
    # Add 5 at 4:     [3, 3, 3, 3, 8]
    # Add 4 at 2:     [3, 3, 7, 7, 12]
    # Subtract 6 at 2:[3, 3, 1, 1, 6]
    # Add 0 at 0:     [3, 3, 1, 1, 6]
    # Subtract 5 at 4:[3, 3, 1, 1, 1]
    # Expected sum(-1) after every update: 0.
    # Start:              [0, 0, 0, 0, 0]
    # Add 3 at index 0:    [3, 0, 0, 0, 0]
    # Add 5 at index 4:    [3, 0, 0, 0, 5]
    # Add 4 at index 2:    [3, 0, 4, 0, 5]
    # Subtract 6 at 2:     [3, 0, -2, 0, 5]
    # Add 0 at index 0:    [3, 0, -2, 0, 5]
    # Subtract 5 at 4:     [3, 0, -2, 0, 0]
    # After each step, compare every prefix sum with the list.
    # Final prefix sums: [3, 3, 1, 1, 1]. The empty prefix is always 0.
    values = [0] * 5
    tree = FenwickTree(len(values))
    assert [tree.sum(i) for i in range(5)] == values

    for index, delta in [(0, 3), (4, 5), (2, 4), (2, -6), (0, 0), (4, -5)]:
        values[index] += delta
        tree.add(index, delta)
        for i in range(len(values)):
            assert tree.sum(i) == sum(values[:i + 1])
        assert tree.sum(-1) == 0


def test_range_sum():
    # Expected range sums: each group fixes left = 0, 1, 2, 3, 4;
    # within each group, right runs from left through 4 (inclusive).
    # Loaded sales: [200, 350, 650, 900, 1300] | [150, 450, 700, 1100] | [300, 550, 950] | [250, 650] | [400]
    # Load sales: [200, 150, 300, 250, 400]
    # Prefix sums: [200, 350, 650, 900, 1300]
    # Example: indices 1 through 3 contain [150, 300, 250].
    # Their sum is 900 - 200 = 700. Check every range against the list.
    sales = [200, 150, 300, 250, 400]
    tree = FenwickTree(len(sales))
    for i, value in enumerate(sales):
        tree.add(i, value)

    for left in range(len(sales)):
        for right in range(left, len(sales)):
            assert tree.sum(right) - tree.sum(left - 1) == sum(sales[left:right + 1])


def test_single_element():
    # Expected query results, in assertion order: -3, 0.
    # Start: [0] -> add 7: [7] -> subtract 10: [-3]
    # Expect sum(0) = -3 and sum(-1) = 0 (no elements).
    tree = FenwickTree(1)
    tree.add(0, 7)
    tree.add(0, -10)
    assert tree.sum(0) == -3
    assert tree.sum(-1) == 0


def test_empty_tree():
    # Expected sum(-1): 0.
    # Array: []
    # The prefix ending at -1 contains []. Its sum should be 0.
    assert FenwickTree(0).sum(-1) == 0
