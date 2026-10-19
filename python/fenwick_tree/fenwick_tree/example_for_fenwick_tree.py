# -*- coding: utf-8 -*-
"""Run from the repository root:

    python python/fenwick_tree/fenwick_tree/example_for_fenwick_tree.py

No third-party dependencies are required. Indices are 0-based and inclusive.
"""
from __future__ import print_function

from fenwick_tree import FenwickTree


def demonstrate_point_updates():
    print("=== demonstrate_point_updates() ===")
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
    print("=== demonstrate_range_updates() ===")
    # Start:                       [0, 0, 0, 0, 0]
    # Add 3 to indices 1 through 3: [0, 3, 3, 3, 0]
    # Subtract 1 from 2 through 4:  [0, 3, 2, 2, -1]
    # Add 2 to all elements:        [2, 5, 4, 4, 1]
    # Expected totals after updates: 9, 6, 16.
    n = 5
    # Store differences D[i] in b1 and i * D[i] in b2.
    b1, b2 = FenwickTree(n), FenwickTree(n)

    def prefix_sum(index):
        # sum(A[0..index]) = (index+1)*sum(D[j]) - sum(j*D[j])
        # D[j] at position j contributes to elements j through index,
        # so it appears (index - j + 1) times in the prefix sum.
        # Split that count into (index+1) copies minus j copies:
        #   (index+1)*b1.sum(index) supplies the first term,
        #   b2.sum(index) supplies the correction j*D[j].
        return (index + 1) * b1.sum(index) - b2.sum(index)

    def range_sum(left, right):
        # Subtract the prefix ending just before left from the prefix ending at right.
        # prefix_sum(-1) returns 0, so this also works when left == 0.
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


def demonstrate_order_statistics():
    print("=== demonstrate_order_statistics() ===")
    # Find the k-th smallest element using a frequency Fenwick tree.
    #
    # Instead of storing values at array positions, store counts at value
    # positions: freq.add(v - 1, 1) increments how many times value v appears.
    # freq.sum(i) then returns how many elements have value <= i+1.
    # The k-th smallest is the smallest value v where freq.sum(v-1) >= k.
    #
    # Values must lie in a known range [1..max_val].
    # Insert: O(log max_val). K-th query: O(log^2 max_val) with binary search.
    values = [3, 1, 4, 1, 5, 2, 3, 3]
    max_val = 5  # all values are in [1..5]
    freq = FenwickTree(max_val)
    for v in values:
        freq.add(v - 1, 1)  # value v stored at 0-based index v-1

    # freq counts (0-based indices 0..4 represent values 1..5):
    #   index 0 (value 1): 2   index 1 (value 2): 1   index 2 (value 3): 3
    #   index 3 (value 4): 1   index 4 (value 5): 1
    # Sorted: [1, 1, 2, 3, 3, 3, 4, 5]

    def kth_smallest(k):
        # Binary search: find smallest 0-based index i where freq.sum(i) >= k,
        # then return i+1 as the 1-based value.
        lo, hi = 0, max_val - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if freq.sum(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo + 1

    print("Values: {}".format(values))
    print("Sorted: [1, 1, 2, 3, 3, 3, 4, 5]")
    print("1st smallest: {}".format(kth_smallest(1)))  # 1
    print("3rd smallest: {}".format(kth_smallest(3)))  # 2
    print("4th smallest: {}".format(kth_smallest(4)))  # 3
    print("8th smallest: {}".format(kth_smallest(8)))  # 5


def main():
    demonstrate_point_updates()
    print()
    demonstrate_range_updates()
    print()
    demonstrate_order_statistics()


if __name__ == "__main__":
    main()
