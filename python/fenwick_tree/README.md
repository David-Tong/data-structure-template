# Fenwick tree

A Fenwick tree (binary indexed tree) maintains prefix sums using O(n) storage.
Point additions and prefix or range-sum queries take O(log n).

## Files

| File | Purpose |
| --- | --- |
| [Implementation](fenwick_tree/fenwick_tree.py) | FenwickTree class |
| [Example](fenwick_tree/example_for_fenwick_tree.py) | Point additions, assignments via deltas, and two-tree range additions |
| [Implementation guide](fenwick_tree/README.md) | API, internals, expected output, and test coverage |
| [Point-update tests](fenwick_tree/test_fenwick_tree.py) | Prefix and range sums, singleton and empty trees |
| [Range-update tests](fenwick_tree/test_range_update_range_query.py) | Two-tree additions and sums |

## Run the example

From the repository root, with no third-party dependencies:

```sh
python python/fenwick_tree/fenwick_tree/example_for_fenwick_tree.py
```

## When to use it

Use one tree for point additions and range sums. Use the two-tree technique
shown in the example for range additions and range sums.

An assignment requires the delta new_value - old_value. Inclusive range sums
are computed as sum(right) - sum(left - 1), with sum(-1) returning zero.

This implementation does not support general range min/max. Those aggregates
cannot be recovered by subtracting prefixes: [1, 5] and [1, 9] have identical
prefix minima but different minima on [1, 1].

Choose a [segment tree](../segment_tree/README.md) for point assignments with
custom associative aggregates, or a lazy segment tree for additive range
updates with min/max queries. The current two-tree and lazy-tree implementations
do not provide range assignment.

## Run the tests

Install pytest if needed with python -m pip install pytest, then run from the
repository root:

```sh
python -m pytest python/fenwick_tree/fenwick_tree -v
```

Expected outcome: **9 passed**. Add -s to see the overlapping-update test print
each expected range sum.

[Back to the Python catalog](../README.md)
