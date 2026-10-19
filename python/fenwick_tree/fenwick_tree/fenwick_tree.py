# -*- coding: utf-8 -*-
class FenwickTree(object):
    """
    Fenwick tree supporting point additions and prefix sums in O(log n).
    Index is 0-based externally. All n elements start at zero.
    Construction and storage are O(n).

    --- Interface ---
      add(idx, delta) -- add delta to element idx, where 0 <= idx < n
      sum(idx)        -- return the sum over [0..idx], where -1 <= idx < n
                       sum(-1) returns 0 (the empty prefix)

    For an inclusive range [left..right], use sum(right) - sum(left - 1).
    Indices are assumed valid; bounds are not checked.
    """

    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, delta):
        """Add delta to element idx (0-based)."""
        idx += 1
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx):
        """Return the prefix sum over [0, idx] (0-based, inclusive)."""
        idx += 1
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx -= idx & -idx
        return s
