# Python templates

The implementations and examples use Python 2.7-compatible syntax and run with
Python 3. Use Python 3 for the test commands documented here. Each implementation
is self-contained; examples use only the standard library, and tests use pytest.

## Implementations

| Structure | Source | Runnable example | Detailed guide |
| --- | --- | --- | --- |
| Fenwick tree | [fenwick_tree.py](fenwick_tree/fenwick_tree/fenwick_tree.py) | [Point and range additions](fenwick_tree/fenwick_tree/example_for_fenwick_tree.py) | [Guide](fenwick_tree/fenwick_tree/README.md) |
| Segment tree | [segment_tree.py](segment_tree/segment_tree/segment_tree.py) | [Point assignments and aggregates](segment_tree/segment_tree/example_for_segment_tree.py) | [Guide](segment_tree/segment_tree/README.md) |
| Lazy segment tree | [lazy_segment_tree.py](segment_tree/lazy_segment_tree/lazy_segment_tree.py) | [Range additions and aggregates](segment_tree/lazy_segment_tree/example_for_lazy_segment_tree.py) | [Guide](segment_tree/lazy_segment_tree/README.md) |

## Shared conventions

All public indices are 0-based and query ranges are inclusive. Callers must
supply valid indices; the classes do not check bounds.

| Class | Update meaning | Initialization |
| --- | --- | --- |
| FenwickTree | add(i, delta) increments one value | O(n) for zeros; O(n log n) to load values with repeated additions |
| SegmentTree | update(i, value) assigns one value | O(n) from a nonempty list |
| LazySegmentTree | update(left, right, delta) adds across a range with the documented additive configuration | O(n) for zeros; O(n log n) when loading nums |

Supported updates and queries take O(log n); storage is O(n). The segment
trees require a nonempty array. FenwickTree(0) supports the empty-prefix query.

## Use an implementation

Copy the class file beside your script and import its class, for example:

```python
from fenwick_tree import FenwickTree

tree = FenwickTree(3)
tree.add(1, 5)
print(tree.sum(2))  # 5
```

Follow the example links above for complete programs and expected output.
The [repository guide](../README.md) lists commands to run all three examples.

## Run the tests

From the repository root:

```sh
python -m pip install pytest
python -m pytest python -v
```

Expected outcome: **21 passed**: nine Fenwick tests, six segment-tree tests,
and six lazy-segment-tree tests. Each detailed guide describes its individual
tests. Add -s to display printed output.
