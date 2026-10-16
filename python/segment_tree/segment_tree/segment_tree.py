# -*- coding: utf-8 -*-
class SegmentTree(object):
    """
    Segment tree with configurable aggregate function.
    Supports point update and range query in O(log n).

    External API is 0-based: idx, ql, qr all accept 0..N-1.
    Internally tree nodes are 1-based (root=1, children=2*node, 2*node+1),
    and the input array is shifted by +1 so position 0 maps to internal index 1.

    --- Interface ---
    To adapt this template, override aggregate_func at construction time:

      update(idx, val)      -- set element at 0-based idx to val
      range_query(ql, qr)   -- return aggregate_func result over [ql..qr]

    --- Customisation points ---
      aggregate_func        -- any associative f(a, b): max, min, operator.add, ...
    """

    def __init__(self, nums, aggregate_func=max):
        self.N = len(nums)
        self.aggregate_func = aggregate_func
        self._nums = [0] + nums  # internal shift: _nums[1..N] maps to nums[0..N-1]
        self.tree = [0] * (4 * self.N)
        self._build()

    # --- Public ---

    def update(self, idx, val):
        """Update position idx (0-based) to val."""
        self._update_node(1, 1, self.N, idx + 1, val)

    def range_query(self, ql, qr):
        """Return aggregate over [ql, qr] (0-based, inclusive)."""
        return self._query_node(1, 1, self.N, ql + 1, qr + 1)

    def range_update(self, ql, qr, val):
        """Blocked — O(n log n) on SegmentTree. Use LazySegmentTree instead."""
        raise NotImplementedError(
            "range_update is O(n log n) on SegmentTree. Use LazySegmentTree instead."
        )

    # --- Private ---

    def _build(self):
        self._build_node(1, 1, self.N)

    def _build_node(self, node, left, right):
        if left == right:
            self.tree[node] = self._nums[left]
            return
        mid = (left + right) // 2
        self._build_node(2 * node, left, mid)
        self._build_node(2 * node + 1, mid + 1, right)
        self.tree[node] = self.aggregate_func(self.tree[2 * node], self.tree[2 * node + 1])

    def _update_node(self, node, left, right, idx, val):
        if left == right:
            self.tree[node] = val
            return
        mid = (left + right) // 2
        if idx <= mid:
            self._update_node(2 * node, left, mid, idx, val)
        else:
            self._update_node(2 * node + 1, mid + 1, right, idx, val)
        self.tree[node] = self.aggregate_func(self.tree[2 * node], self.tree[2 * node + 1])

    def _query_node(self, node, left, right, ql, qr):
        if left == ql and right == qr:
            return self.tree[node]
        mid = (left + right) // 2
        if qr <= mid:
            return self._query_node(2 * node, left, mid, ql, qr)
        if ql > mid:
            return self._query_node(2 * node + 1, mid + 1, right, ql, qr)
        left_val = self._query_node(2 * node, left, mid, ql, mid)
        right_val = self._query_node(2 * node + 1, mid + 1, right, mid + 1, qr)
        return self.aggregate_func(left_val, right_val)
