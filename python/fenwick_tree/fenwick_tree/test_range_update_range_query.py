# -*- coding: utf-8 -*-
"""Range addition and range sum queries using two Fenwick trees.

Run from the repository root:
    python -m pytest python/fenwick_tree/fenwick_tree/test_range_update_range_query.py -v

All indices are 0-based and ranges are inclusive. The array starts at zero.
Negative additions and overlapping updates are supported.

How it works:
    Define differences D[0] = A[0], D[j] = A[j] - A[j - 1].
    Adding delta to A[left..right] changes just two differences:
        D[left] += delta
        D[right + 1] -= delta   (when right + 1 < n)
    A prefix sum of D gives a single A[i], not a prefix sum of A.

    For a prefix sum of A, each D[j] appears in A[j] through A[p],
    so its contribution is (p - j + 1) * D[j]:
        sum(A[0..p]) = (p + 1) * sum(D[0..p]) - sum(j * D[j], j=0..p)
    Store D[j] in b1 and j * D[j] in b2 to evaluate this in O(log n).
    Subtract two prefix sums to obtain any range sum.

Construction and storage: O(n). Each update or query: O(log n).
This technique supports addition and sums, not range assignment or min/max.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from fenwick_tree import FenwickTree


def test_overlapping_range_additions_and_range_sums():
    # Start:                       [0, 0, 0, 0, 0]
    # Add 3 to indices 1 through 3: [0, 3, 3, 3, 0]
    # Subtract 1 from 2 through 4:  [0, 3, 2, 2, -1]
    # Add 2 to all elements:        [2, 5, 4, 4, 1]
    # This checks overlapping updates, subtraction, and updates reaching the end.
    n = 5
    b1, b2 = FenwickTree(n), FenwickTree(n)
    cases = [(1, 3, 3, [0, 3, 3, 3, 0]),
             (2, 4, -1, [0, 3, 2, 2, -1]),
             (0, 4, 2, [2, 5, 4, 4, 1])]
    for left, right, delta, expected in cases:
        # Record where the addition starts in both trees.
        b1.add(left, delta)
        b2.add(left, left * delta)
        # Stop the addition after right, if another element follows.
        if right + 1 < n:
            b1.add(right + 1, -delta)
            b2.add(right + 1, -(right + 1) * delta)
        print("After adding {} to [{}..{}]: {}".format(delta, left, right, expected))
        for start in range(n):
            for end in range(start, n):
                # Take the sum up to end and subtract the sum before start.
                prefix_end = (end + 1) * b1.sum(end) - b2.sum(end)
                prefix_before = start * b1.sum(start - 1) - b2.sum(start - 1)
                expected_sum = sum(expected[start:end + 1])
                print("Expected sum[{}..{}] = {}".format(start, end, expected_sum))
                assert prefix_end - prefix_before == expected_sum


def test_initialize_nonzero_array():
    # Expected query results: sum[0..3] = 10; sum[1..2] = 5.
    # Intermediate prefixes: sum[0..2] = 7; sum[0..0] = 2.
    # Initial values:       [2, 1, 4, 3]
    # Differences D:         [2, -1, 3, -1]
    # Index times D:         [0, -1, 6, -3]
    # Store D in the first tree and index times D in the second.
    # Expect total = 2 + 1 + 4 + 3 = 10.
    # Indices 1 through 2 contain [1, 4], so their sum should be 5.
    values = [2, 1, 4, 3]
    b1, b2 = FenwickTree(len(values)), FenwickTree(len(values))
    for i, value in enumerate(values):
        difference = value - (values[i - 1] if i > 0 else 0)
        b1.add(i, difference)
        b2.add(i, i * difference)
    assert 4 * b1.sum(3) - b2.sum(3) == 10
    prefix_2 = 3 * b1.sum(2) - b2.sum(2)
    prefix_0 = b1.sum(0) - b2.sum(0)
    assert prefix_2 - prefix_0 == 5


def test_range_updates_against_plain_list():
    # Expected range sums: each group fixes left = 0, 1, 2, 3, 4;
    # within each group, right runs from left through 4 (inclusive).
    # Start (all zero): [0, 0, 0, 0, 0] | [0, 0, 0, 0] | [0, 0, 0] | [0, 0] | [0]
    # Add 2 to [0..4]: [2, 4, 6, 8, 10] | [2, 4, 6, 8] | [2, 4, 6] | [2, 4] | [2]
    # Add 5 to [1..3]: [2, 9, 16, 23, 25] | [7, 14, 21, 23] | [7, 14, 16] | [7, 9] | [2]
    # Subtract 3 from [2..4]: [2, 9, 13, 17, 16] | [7, 11, 15, 14] | [4, 8, 7] | [4, 3] | [-1]
    # Subtract 4 at 0: [-2, 5, 9, 13, 12] | [7, 11, 15, 14] | [4, 8, 7] | [4, 3] | [-1]
    # Add 7 at 4: [-2, 5, 9, 13, 19] | [7, 11, 15, 21] | [4, 8, 14] | [4, 10] | [6]
    # Add 0 to [1..2]: [-2, 5, 9, 13, 19] | [7, 11, 15, 21] | [4, 8, 14] | [4, 10] | [6]
    # Expected empty-prefix result after every update: 0.
    # Start:                       [0, 0, 0, 0, 0]
    # Add 2 to indices 0 through 4: [2, 2, 2, 2, 2]
    # Add 5 to indices 1 through 3: [2, 7, 7, 7, 2]
    # Subtract 3 from 2 through 4:  [2, 7, 4, 4, -1]
    # Subtract 4 at index 0:        [-2, 7, 4, 4, -1]
    # Add 7 at index 4:             [-2, 7, 4, 4, 6]
    # Add 0 to indices 1 through 2: [-2, 7, 4, 4, 6]
    # After each step, compare every range sum with the updated list.
    # The empty prefix [] should always have sum 0.
    values = [0] * 5
    n = len(values)
    b1, b2 = FenwickTree(n), FenwickTree(n)
    for left, right, delta in [(0, 4, 2), (1, 3, 5), (2, 4, -3),
                               (0, 0, -4), (4, 4, 7), (1, 2, 0)]:
        b1.add(left, delta)
        b2.add(left, left * delta)
        if right + 1 < n:
            b1.add(right + 1, -delta)
            b2.add(right + 1, -(right + 1) * delta)
        for i in range(left, right + 1):
            values[i] += delta
        for start in range(n):
            for end in range(start, n):
                prefix_end = (end + 1) * b1.sum(end) - b2.sum(end)
                prefix_before = start * b1.sum(start - 1) - b2.sum(start - 1)
                assert prefix_end - prefix_before == sum(values[start:end + 1])
        assert 0 * b1.sum(-1) - b2.sum(-1) == 0


def test_single_element():
    # Expected final sum[0..0]: -3.
    # Start: [0] -> add 7: [7] -> subtract 10: [-3]
    # The only range, indices 0 through 0, should have sum -3.
    # There is no element after this range, so no end marker is needed.
    b1, b2 = FenwickTree(1), FenwickTree(1)
    for delta in [7, -10]:
        b1.add(0, delta)
        b2.add(0, 0 * delta)
    assert b1.sum(0) - b2.sum(0) == -3


def test_empty_tree():
    # Expected empty-prefix result: 0.
    # Array: []; both difference arrays are also [].
    # The prefix ending at -1 contains no elements.
    # The two-tree sum formula should return 0.
    b1, b2 = FenwickTree(0), FenwickTree(0)
    assert 0 * b1.sum(-1) - b2.sum(-1) == 0
