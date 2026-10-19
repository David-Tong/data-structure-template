# Lazy segment tree implementation

[lazy_segment_tree.py](lazy_segment_tree.py) supports range additions and
inclusive range queries. Public indices are 0-based. Use `n > 0` and valid
ranges `0 <= left <= right < n`; bounds are not checked. When supplying
`nums`, use a list of length `n`.

## Run the example

From the repository root, run this script without third-party dependencies:

```sh
python python/segment_tree/lazy_segment_tree/example_for_lazy_segment_tree.py
```

From this folder, use `python example_for_lazy_segment_tree.py`.
[The script](example_for_lazy_segment_tree.py) separates range-sum and min/max
demonstrations into functions called by `main()`. Comments show the array at
each step and the expected results.

Expected output:

```text
=== demonstrate_range_updates() ===
Start: [0, 0, 0, 0, 0]
After adding 3 to [1..3]: [0, 3, 3, 3, 0]
Total: 9
Range sum [1..3]: 9
After adding -1 to [2..4]: [0, 3, 2, 2, -1]
Total: 6
Range sum [1..3]: 7
After adding 2 to [0..4]: [2, 5, 4, 4, 1]
Total: 16
Range sum [1..3]: 13

=== demonstrate_min_max_queries() ===
Initial values: [10, 20, 15, 30, 25]
Minimum: 10
Maximum: 30
After subtracting 15 from [1..3]: [10, 5, 0, 15, 25]
Minimum: 0
Maximum: 25
```

## Interface

Import `LazySegmentTree` from `lazy_segment_tree` when your script is beside
the module. For additive updates, initialize with `identity=0` and optionally
`nums=values`:

| Query | `aggregate_func` | `update_func` |
| --- | --- | --- |
| Sum | `operator.add` | `lambda value, delta, size: value + delta * size` |
| Minimum | `min` | Default: `value + delta` |
| Maximum | `max` | Default: `value + delta` |

`update(left, right, delta)` adds the delta across the inclusive range with
these configurations. `range_update` is an alias for it.
`range_query(left, right)` returns the configured aggregate. To update one
element, use equal endpoints; this still adds a delta rather than assigning.

| Operation | Result | Cost |
| --- | --- | --- |
| `LazySegmentTree(n, ...)` | Initialize zeros with `identity=0` | O(n) |
| `LazySegmentTree(n, ..., nums=values)` | Load values using point updates | O(n log n) |
| `update(left, right, delta)` | Add to the range with the configuration above; returns `None` | O(log n) |
| `range_update(left, right, delta)` | Alias for `update` | O(log n) |
| `range_query(left, right)` | Aggregate over the inclusive range | O(log n) |

## Implementation

Each node stores an aggregate and a pending additive update. A fully covered
node updates its aggregate immediately and accumulates `lazy += delta`.
Before descending into a partially covered node, the tree pushes its pending
update to both children. After updating children, it merges their aggregates.
For sums, adding to every element changes a node by `delta * size`; min/max
shift only by `delta`.

Storage and zero initialization are O(n). Loading `nums` uses repeated point
updates and takes O(n log n). Each range addition or query takes O(log n).
Printing all individual values in the example takes O(n log n).

The current lazy tags compose by addition. Changing `update_func` alone does
not provide general range multiplication or assignment. The runnable example
uses additive updates, which support overlapping ranges and negative deltas.

## Tests

[test_lazy_segment_tree.py](test_lazy_segment_tree.py) contains six tests.
Results below follow assertion order.

| Test | Expected results and scope |
| --- | --- |
| `test_find_first_workaround` | Indices 0, 3, -1, 1, 3, 2, -1 for the specific arrays tested; min/max bounds do not establish membership for arbitrary arrays |
| `test_range_sum_with_range_add` | 29800, 16000, 31300, 16000, 32500 |
| `test_range_max_with_range_add` | 30, 20, 40, 25 |
| `test_range_min_with_range_add` | 80, 90, 65, 75 |
| `test_range_update_alias` | Both trees agree on points `[10, 25, 20, 35, 25]` and maximum 35 |
| `test_range_multiply_no_overlap` | 20, 32, 24 for one multiplication update; does not establish general multiplication support |

### Run the tests

Install pytest and run from the repository root:

```sh
python -m pip install pytest
python -m pytest python/segment_tree/lazy_segment_tree/test_lazy_segment_tree.py -v
```

Expected outcome: **6 passed**. From this folder, use `python -m pytest -v`.
The example prints results for learning; the tests use assertions to check
correctness.

[Back to the segment trees overview](../README.md)
