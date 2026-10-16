import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from segment_tree_base import SegmentTreeBase


class Node(object):
    __slots__ = ['val', 'lazy']

    def __init__(self, identity):
        self.val = identity   # aggregate value for this node's range
        self.lazy = 0         # pending update not yet pushed to children


class LazySegmentTree(SegmentTreeBase):
    """
    Generic lazy segment tree supporting range update and range query in O(log n).
    Index is 0-based externally.

    Parameters:
      n           -- size of the array
      aggregate_func -- aggregate function over two node values, e.g. max, min, operator.add
      update_func    -- how a lazy delta is applied to a node value (default: additive)
                        signature: update_func(current_val, delta) -> new_val
      identity       -- neutral element for aggregate_func, e.g. 0 for sum, float('-inf') for max
    """

    def __init__(self, n, aggregate_func=max, update_func=None, identity=0):
        self.aggregate_func = aggregate_func
        self.update_func = update_func if update_func is not None else lambda val, delta: val + delta
        self.identity = identity
        self.nodes = [Node(identity) for _ in range(4 * (n + 1))]
        super(LazySegmentTree, self).__init__(n)

    # --- Public ---

    def update(self, ql, qr, val):
        """Apply val to every element in [ql, qr] (0-based, inclusive) via update_func."""
        self._update_node(1, 0, self.N - 1, ql, qr, val)

    def range_query(self, ql, qr):
        """Return aggregate over [ql, qr] (0-based, inclusive)."""
        return self._query_node(1, 0, self.N - 1, ql, qr)

    # --- Private ---

    def _build(self):
        pass  # all nodes initialise to identity by default in Node.__init__

    def _apply(self, node, delta):
        """Apply delta to a node and record it as a pending lazy update."""
        self.nodes[node].val = self.update_func(self.nodes[node].val, delta)
        self.nodes[node].lazy += delta

    def _push_down(self, node):
        """Push pending lazy update from node to its two children."""
        if self.nodes[node].lazy == 0:
            return
        self._apply(2 * node, self.nodes[node].lazy)
        self._apply(2 * node + 1, self.nodes[node].lazy)
        self.nodes[node].lazy = 0

    def _pull_up(self, node):
        """Recalculate node's aggregate from its two children after an update."""
        self.nodes[node].val = self.aggregate_func(self.nodes[2 * node].val, self.nodes[2 * node + 1].val)

    def _update_node(self, node, left, right, ql, qr, delta):
        if ql <= left and qr >= right:
            self._apply(node, delta)
            return
        self._push_down(node)
        mid = (left + right) // 2
        if ql <= mid:
            self._update_node(2 * node, left, mid, ql, qr, delta)
        if qr > mid:
            self._update_node(2 * node + 1, mid + 1, right, ql, qr, delta)
        self._pull_up(node)

    def _query_node(self, node, left, right, ql, qr):
        if ql <= left and qr >= right:
            return self.nodes[node].val
        self._push_down(node)
        mid = (left + right) // 2
        if qr <= mid:
            return self._query_node(2 * node, left, mid, ql, qr)
        if ql > mid:
            return self._query_node(2 * node + 1, mid + 1, right, ql, qr)
        left_val = self._query_node(2 * node, left, mid, ql, mid)
        right_val = self._query_node(2 * node + 1, mid + 1, right, mid + 1, qr)
        return self.aggregate_func(left_val, right_val)
