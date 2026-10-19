# Segment trees

Segment trees store aggregates over array intervals. Choose the implementation
based on whether updates affect one element or an entire range.

## Choose an implementation

| Feature | SegmentTree | LazySegmentTree |
| --- | --- | --- |
| Update | Assign one element | Add a delta to a range |
| Query | Any associative binary aggregate | Sum, min, or max with the documented additive configuration |
| Build | O(n) from a list | O(n) for zeros; O(n log n) to load nums |
| Update / query | O(log n) | O(log n) |
| Storage | O(n) | O(n) |
| Guide | [Point assignments](segment_tree/README.md) | [Range additions](lazy_segment_tree/README.md) |
| Source | [segment_tree.py](segment_tree/segment_tree.py) | [lazy_segment_tree.py](lazy_segment_tree/lazy_segment_tree.py) |
| Example | [example_for_segment_tree.py](segment_tree/example_for_segment_tree.py) | [example_for_lazy_segment_tree.py](lazy_segment_tree/example_for_lazy_segment_tree.py) |

Both classes use 0-based public indices and inclusive ranges. Supply nonempty
arrays and valid indices.

## Run the examples

From the repository root, with no third-party dependencies:

```sh
python python/segment_tree/segment_tree/example_for_segment_tree.py
python python/segment_tree/lazy_segment_tree/example_for_lazy_segment_tree.py
```

Each script has separate demo functions called by main(), array-state comments,
and printed results. The detailed guides include the complete expected output.

## Update and query behavior

SegmentTree.update(index, value) replaces an element. Its aggregate_func
defaults to max; use min, operator.add, operator.mul, or another associative
binary function. Its range_update method raises NotImplementedError.

LazySegmentTree.update(left, right, delta) and its range_update alias apply
the configured update across a range. For additive updates, use identity=0:

| Aggregate | aggregate_func | update_func |
| --- | --- | --- |
| Sum | operator.add | lambda value, delta, size: value + delta * size |
| Minimum | min | Default: value + delta |
| Maximum | max | Default: value + delta |

For sum queries, a node covering size elements gains delta * size. Min/max
shift by delta regardless of the number of elements. Both classes query with
range_query(left, right).

## Limitations

The lazy implementation combines pending tags with addition. Replacing only
update_func does not implement general multiplication or assignment; those
operations also need different tag composition.

The min/max search workaround in the tests is not a general value search.
For example, [1, 3] has a minimum below 2 and a maximum above 2, but contains
no 2. The class does not expose a find_first method.

For sums with additive updates, a [Fenwick tree](../fenwick_tree/README.md)
offers a simpler alternative. Use the segment-tree implementations when you
need the aggregates described above.

## Run the tests

Install pytest if needed with python -m pip install pytest, then run from the
repository root:

```sh
python -m pytest python/segment_tree -v
```

Expected outcome: **12 passed**. The implementation guides describe all six
tests in each suite and their expected results.

[Back to the Python catalog](../README.md)
