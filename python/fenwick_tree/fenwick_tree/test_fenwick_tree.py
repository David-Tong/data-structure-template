# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from fenwick_tree import FenwickTree


# All indices are 0-based (same as Python lists).
# Run with: pytest test_fenwick_tree.py -v


def test_prefix_sums_after_updates():
    # Compare every prefix with a plain list after each point addition.
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
    sales = [200, 150, 300, 250, 400]
    tree = FenwickTree(len(sales))
    for i, value in enumerate(sales):
        tree.add(i, value)

    for left in range(len(sales)):
        for right in range(left, len(sales)):
            assert tree.sum(right) - tree.sum(left - 1) == sum(sales[left:right + 1])


def test_single_element():
    tree = FenwickTree(1)
    tree.add(0, 7)
    tree.add(0, -10)
    assert tree.sum(0) == -3
    assert tree.sum(-1) == 0


def test_empty_tree():
    assert FenwickTree(0).sum(-1) == 0
