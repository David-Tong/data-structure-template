# Segment tree implementation

[segment_tree.py](segment_tree.py) supports point assignments and inclusive
range queries. Public indices are 0-based. Supply a nonempty list and valid
indices: `0 <= left <= right < len(values)`. Bounds are not checked.

## Run the example

From the repository root, run this script without third-party dependencies:

```sh
python python/segment_tree/segment_tree/example_for_segment_tree.py
```

From this folder, use `python example_for_segment_tree.py`.
[The script](example_for_segment_tree.py) has separate functions for point
assignments, min/max queries, and a custom product aggregate. `main()` calls
them all. Each function includes array-state comments and expected results.

Expected output:

```text
Initial sales: [200, 150, 300, 250, 400]
Range sum [1..3]: 700
Total: 1300
After setting index 2 to 130: [200, 150, 130, 250, 400]
Range sum [1..3]: 530
Total: 1130
Initial values: [10, 20, 15, 30, 25]
Minimum: 10
Maximum: 30
After setting index 3 to 5: [10, 20, 15, 5, 25]
Minimum: 5
Maximum: 25
Initial product [0..2]: 6
Product [0..2] after setting index 0 to 3: 18
```

## Interface

Import `SegmentTree` from `segment_tree` when your script is beside the module.
Construct it with `SegmentTree(values, aggregate_func=max)`. Choose `min`,
`operator.add`, or another associative binary function to change the aggregate.
`update(index, value)` assigns a value directly; `range_query(left, right)`
returns the aggregate including both endpoints.

| Operation | Result | Cost |
| --- | --- | --- |
| `SegmentTree(values, aggregate_func=max)` | Build from a nonempty list | O(n) |
| `update(index, value)` | Assign one element; returns `None` | O(log n) |
| `range_query(left, right)` | Aggregate over the inclusive range | O(log n) |

## Implementation

The tree recursively splits the input into halves. Leaves hold individual
values; each parent merges its two children. Nodes use a list of size `4 * n`,
with root 1 and children `2 * node` and `2 * node + 1`. Array positions are
shifted internally by one.

An assignment replaces one leaf and recomputes its ancestors. A query returns
fully covered nodes and combines results when it crosses a midpoint.
Construction and storage are O(n); assignments and range queries are O(log n).
`range_update` raises `NotImplementedError`; use
[LazySegmentTree](../lazy_segment_tree/README.md) for range additions.

## Tests

[test_segment_tree.py](test_segment_tree.py) contains six tests. Query results
below are in assertion order, before and after the documented assignments.

| Test | Expected results |
| --- | --- |
| `test_range_maximum_original_use_case` | 5, 8, 8, 9, 9 |
| `test_range_maximum` | 40, 38, 40, 35, 38 |
| `test_range_minimum` | 88, 76, 76, 99, 88 |
| `test_range_sum` | 900, 1150, 2050, 730, 1880 |
| `test_range_product` | 6, 120, 120, 18, 360 |
| `test_range_update_raises` | `NotImplementedError` |

### Run the tests

Install pytest and run from the repository root:

```sh
python -m pip install pytest
python -m pytest python/segment_tree/segment_tree/test_segment_tree.py -v
```

Expected outcome: **6 passed**. From this folder, use `python -m pytest -v`.
The example prints results for learning; the tests use assertions to check
correctness.

[Back to the segment trees overview](../README.md)
