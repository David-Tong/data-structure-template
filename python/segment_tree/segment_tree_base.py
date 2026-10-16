from abc import ABC, abstractmethod


class SegmentTreeBase(ABC):
    """
    Abstract base class for segment tree implementations.

    Subclasses must implement _build, update, and range_query.
    Signatures differ per subclass:
      - SegmentTree:     update(idx, val),    range_query(start, end)
      - LazySegmentTree: update(ql, qr, val), range_query(ql, qr, target)
    """

    def __init__(self, n):
        self.N = n
        self.tree = [0] * (4 * n)
        self._build()

    @abstractmethod
    def _build(self):
        """Construct the internal tree. Called once by __init__."""
        pass

    @abstractmethod
    def range_query(self, ql, qr):
        """Query over [ql, qr]. Raises TypeError if not overridden in subclass."""
        pass

    @abstractmethod
    def update(self, idx, val):
        """Update element(s) in the tree. Raises TypeError if not overridden in subclass."""
        pass

    def range_update(self, ql, qr, val):
        """Raises NotImplementedError — use LazySegmentTree for O(log n) range update."""
        raise NotImplementedError(
            "range_update is O(n log n) on SegmentTree. Use LazySegmentTree instead."
        )
