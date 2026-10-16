# -*- coding: utf-8 -*-
class LazySegmentTree(object):
    """
    Generic lazy segment tree supporting range update and range query in O(log n).
    Index is 0-based externally.

    --- Interface ---
    To adapt this template, supply aggregate_func, update_func, and identity
    at construction time:

      update(ql, qr, val)   -- apply val to every element in [ql..qr] via update_func
      range_query(ql, qr)   -- return aggregate_func result over [ql..qr]

    --- Customisation points ---
      aggregate_func  -- how to combine two node values: max, min, operator.add, ...

      update_func     -- how a lazy delta is applied to a node's aggregate value.
                         signature: update_func(current_val, delta, size) -> new_val
                         size = number of elements covered by the node.
                         The size argument is what makes sum correct for range updates:
                           max/min: lambda val, delta, size: val + delta
                           sum:     lambda val, delta, size: val + delta * size
                         Default is the max/min variant (val + delta).

      identity        -- starting value for every node (neutral element for aggregate_func).
                         Use 0 when all elements are initialised via additive update(i, i, v),
                         since 0 + v = v. float('-inf') / float('inf') are only appropriate
                         when you need to represent "no element" distinctly from zero.
    """

    class Node(object):
        __slots__ = ['val', 'lazy']

        def __init__(self, identity):
            self.val = identity   # aggregate value for this node's range
            self.lazy = 0         # pending update not yet pushed to children

    def __init__(self, n, aggregate_func=max, update_func=None, identity=0):
        self.N = n
        self.aggregate_func = aggregate_func
        self.update_func = update_func if update_func is not None \
            else lambda val, delta, size: val + delta
        self.identity = identity
        self.nodes = [self.Node(identity) for _ in range(4 * (n + 1))]

    # --- Public ---

    def update(self, ql, qr, val):
        """Apply val to every element in [ql, qr] (0-based, inclusive) via update_func."""
        self._update_node(1, 0, self.N - 1, ql, qr, val)

    def range_query(self, ql, qr):
        """Return aggregate over [ql, qr] (0-based, inclusive)."""
        return self._query_node(1, 0, self.N - 1, ql, qr)

    # --- Private ---

    def _apply(self, node, delta, size):
        """Apply delta to a node (covering `size` elements) and record as pending lazy."""
        self.nodes[node].val = self.update_func(self.nodes[node].val, delta, size)
        self.nodes[node].lazy += delta

    def _push_down(self, node, left, right):
        """Push pending lazy update from node to its two children."""
        if self.nodes[node].lazy == 0:
            return
        mid = (left + right) // 2
        self._apply(2 * node, self.nodes[node].lazy, mid - left + 1)
        self._apply(2 * node + 1, self.nodes[node].lazy, right - mid)
        self.nodes[node].lazy = 0

    def _pull_up(self, node):
        """Recalculate node's aggregate from its two children after an update."""
        self.nodes[node].val = self.aggregate_func(
            self.nodes[2 * node].val, self.nodes[2 * node + 1].val)

    def _update_node(self, node, left, right, ql, qr, delta):
        if ql <= left and qr >= right:
            self._apply(node, delta, right - left + 1)
            return
        self._push_down(node, left, right)
        mid = (left + right) // 2
        if ql <= mid:
            self._update_node(2 * node, left, mid, ql, qr, delta)
        if qr > mid:
            self._update_node(2 * node + 1, mid + 1, right, ql, qr, delta)
        self._pull_up(node)

    def _query_node(self, node, left, right, ql, qr):
        if ql <= left and qr >= right:
            return self.nodes[node].val
        self._push_down(node, left, right)
        mid = (left + right) // 2
        if qr <= mid:
            return self._query_node(2 * node, left, mid, ql, qr)
        if ql > mid:
            return self._query_node(2 * node + 1, mid + 1, right, ql, qr)
        left_val = self._query_node(2 * node, left, mid, ql, mid)
        right_val = self._query_node(2 * node + 1, mid + 1, right, mid + 1, qr)
        return self.aggregate_func(left_val, right_val)
