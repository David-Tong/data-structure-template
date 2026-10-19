# Fenwick tree implementation

[fenwick_tree.py](fenwick_tree.py) implements a Fenwick tree (binary indexed
tree) for point additions and prefix sums. It uses only the Python standard
library. The two test files use `pytest`.

## Run the example

[example_for_fenwick_tree.py](example_for_fenwick_tree.py) has two demos:
`demonstrate_point_updates()` covers loading values, prefix and range sums,
and assignments via deltas; `demonstrate_range_updates()` covers two-tree
range additions. `main()` calls both. Comments show each array state and
expected result. No third-party dependencies are required.

From the repository root:

```sh
python python/fenwick_tree/fenwick_tree/example_for_fenwick_tree.py
```

From this folder, run `python example_for_fenwick_tree.py`. Expected output:

```text
=== demonstrate_point_updates() ===
Initial sales: [200, 150, 300, 250, 400]
Prefix sum [0..2]: 650
Range sum [1..3]: 700
Total sales: 1300
Empty prefix: 0
After adding 50 at index 1: [200, 200, 300, 250, 400]
Prefix sum [0..2]: 700
After setting index 2 to 130: [200, 200, 130, 250, 400]
Range sum [1..3]: 580
Total sales: 1180

=== demonstrate_range_updates() ===
Range updates using two Fenwick trees:
Start: [0, 0, 0, 0, 0]
After adding 3 to [1..3]: [0, 3, 3, 3, 0]
Total: 9
After adding -1 to [2..4]: [0, 3, 2, 2, -1]
Total: 6
After adding 2 to [0..4]: [2, 5, 4, 4, 1]
Total: 16
```

## Example walkthrough

The script's `if __name__ == "__main__":` block calls `main()` when you run
the file directly. `main()` runs the point-update demo first, then the
range-update demo. Each demo creates its own trees, so the second one starts
from zeros independently of the sales example.

### `demonstrate_point_updates()`

**Load the sales.** `FenwickTree(len(sales))` creates five zeros. The loop
`tree.add(index, value)` loads `[200, 150, 300, 250, 400]`, one value at a time.
The tree does not hold a reference to `sales`: the list is kept separately
to display values and remember the old value when assigning a new one.

**Query the initial array.** Every endpoint is inclusive:

| Code in the demo | Calculation | Printed result |
| --- | --- | --- |
| `tree.sum(2)` | 200 + 150 + 300 | 650 |
| `tree.sum(right) - tree.sum(left - 1)`, with `left=1`, `right=3` | 900 - 200 = 150 + 300 + 250 | 700 |
| `tree.sum(len(sales) - 1)` | Sum of all five values | 1300 |
| `tree.sum(-1)` | No elements | 0 |

**Add 50 at index 1.** `tree.add(1, 50)` changes 150 to 200. The following
`sales[1] += 50` keeps the display list in sync; changing the list alone would
not update the tree. The array is now `[200, 200, 300, 250, 400]`, and
`tree.sum(2)` prints `200 + 200 + 300 = 700`.

**Set index 2 to 130.** `add` takes a change, not a replacement value. The
demo calculates `new_value - sales[index] = 130 - 300 = -170`, adds that delta
to the tree, then sets `sales[index] = new_value`.

The final array is `[200, 200, 130, 250, 400]`. The range `[1..3]` sums to
`200 + 130 + 250 = 580`, and the total is `1180`. These results include the
earlier addition of 50 at index 1.

### `demonstrate_range_updates()`

This demo adds a delta to several adjacent elements at once. It uses `b1` for
differences between neighboring values and `b2` for the corrections needed
to calculate prefix sums. The [two-tree explanation](#range-additions-with-two-trees)
below derives the formula used by its helpers:

| Helper | Purpose |
| --- | --- |
| `prefix_sum(index)` | Return the sum from 0 through `index` using `(index + 1) * b1.sum(index) - b2.sum(index)` |
| `range_sum(left, right)` | Subtract the prefix before `left` from the prefix ending at `right` |

The loop reads each tuple as `(left, right, delta)` and applies the updates
in order:

| Update tuple | Meaning | Array afterward | Printed total |
| --- | --- | --- | --- |
| `(1, 3, 3)` | Add 3 at indices 1, 2, and 3 | `[0, 3, 3, 3, 0]` | 9 |
| `(2, 4, -1)` | Subtract 1 at indices 2, 3, and 4 | `[0, 3, 2, 2, -1]` | 6 |
| `(0, 4, 2)` | Add 2 to every element | `[2, 5, 4, 4, 1]` | 16 |

For each tuple, `b1.add(left, delta)` marks where the addition starts, and
`b2.add(left, left * delta)` records its correction. If an element follows
the range, the two calls at `right + 1` cancel the addition from there onward.
For the first update, cancellation happens at index 4. The other two updates
reach the last element, so the `if right + 1 < n` block is skipped.

Finally, `[range_sum(i, i) for i in range(n)]` queries each individual element
to print the current array. Unlike the sales list in the first demo, this
display list is reconstructed from the trees after every update.
`range_sum(0, n - 1)` then prints the total. Each update or range query takes
O(log n); displaying all `n` elements takes O(n log n).

## Interface

All public indices are **0-based**, and query ranges include both endpoints.

| Operation | Result | Cost |
| --- | --- | --- |
| `FenwickTree(n)` | Create an array of `n` zeros | O(n) |
| `tree.add(i, delta)` | Add `delta` to element `i`; returns `None` | O(log n) |
| `tree.sum(i)` | Sum of elements from index 0 through `i` | O(log n) |
| `tree.sum(right) - tree.sum(left - 1)` | Sum over `[left, right]` | O(log n) |

Storage is O(n). Use `n >= 0`, `0 <= i < n` for updates, and
`-1 <= i < n` for prefix queries. `sum(-1)` returns 0. Indices are assumed
valid; the implementation does not check bounds. An empty tree supports only
the empty-prefix query.

## Implementation

The internal `bit` list has `n + 1` entries and uses **1-based** indices;
`bit[0]` is unused. Each method adds 1 to the public index before traversing it.

For an internal index `j`, `j & -j` extracts its lowest set bit, which is the
size of the block summarized by `bit[j]`. That entry stores the sum of internal
positions `j - (j & -j) + 1` through `j`.

- `add` increments the current block sum, then moves to `j + (j & -j)`.
  This visits the larger blocks containing the changed element.
- `sum` accumulates the current block sum, then moves to `j - (j & -j)`.
  This visits disjoint blocks that together cover the requested prefix.

For example, with eight elements, updating public index 2 visits internal
indices 3, 4, and 8. Querying the prefix ending at public index 6 visits internal
indices 7, 6, and 4: blocks of sizes 1, 2, and 4 cover the seven elements.
Each traversal takes O(log n) steps.

Subtracting the prefix before `left` from the prefix ending at `right` leaves
exactly the inclusive range sum. The empty-prefix result makes the same formula
work when `left` is 0.

Loading a nonzero list with repeated `add` calls takes O(n log n).
`add` changes a value by a delta; it does not assign a value or update an entire
range. To assign a value, pass `new_value - old_value`, as shown in the example.
Copy `fenwick_tree.py` beside your script and import with
`from fenwick_tree import FenwickTree`.

## Range additions with two trees

The runnable example and
[test_range_update_range_query.py](test_range_update_range_query.py) combine
two instances for range additions and range sums. These helper operations
are not methods on `FenwickTree`.

We want to add a number to many adjacent elements and then ask for their sum.
Updating each element separately would take O(k log n) for a range of length
`k`. Two Fenwick trees let us update the range in O(log n).

### 1. Record where an addition starts and stops

Start with five zeros and add 3 to indices 1 through 3:

```text
Index:       0   1   2   3   4
Array A:     0   3   3   3   0
Changes D:   0  +3   0   0  -3
```

The `+3` means "start adding 3 here." The `-3` at index 4 means "stop adding
3 here." Walking from left to right and keeping a running total of `D`
reconstructs `A`: `0, 3, 3, 3, 0`.

This `D` is called a **difference array**: `D[0] = A[0]`, and each later
`D[j] = A[j] - A[j - 1]`. Adding `delta` to `[left, right]` needs only two
changes:

- Add `delta` to `D[left]`.
- Subtract `delta` from `D[right + 1]`, if that index exists.

Store these changes in the first Fenwick tree, `b1`. Now `b1.sum(p)` gives
the value of **one element**, `A[p]`. For example, `b1.sum(3) = 3`.
But we want the sum of **all elements** from 0 through 3, which is 9.

### 2. Count how many times each change contributes

The change `+3` at index 1 contributes to three elements in the prefix ending
at index 3:

```text
A[0] = D[0]
A[1] = D[0] + D[1]
A[2] = D[0] + D[1] + D[2]
A[3] = D[0] + D[1] + D[2] + D[3]
```

Adding these rows counts `D[0]` four times, `D[1]` three times, `D[2]` twice,
and `D[3]` once. In general, a change at index `j` appears `p + 1 - j` times
in the prefix ending at `p`.

We can calculate that in two parts: count every change `p + 1` times, then
subtract the extra `j` copies of each change. The second tree, `b2`, stores
`j * D[j]` to supply that correction.

| Tree | Values it represents | What its prefix query returns |
| --- | --- | --- |
| `b1` | `D[j]` | Sum of changes through `p`, equal to `A[p]` |
| `b2` | `j * D[j]` | Sum of the corrections through `p` |

These are the logical values stored through point additions, not the trees'
internal `bit` lists. The resulting formula is:

```text
sum of A[0..p] = (p + 1) * b1.sum(p) - b2.sum(p)
```

For our array `[0, 3, 3, 3, 0]`:

| Prefix end `p` | `b1.sum(p)` | `b2.sum(p)` | Array prefix sum |
| --- | --- | --- | --- |
| 2 | 3 | 1 * 3 = 3 | 3 * 3 - 3 = 6 |
| 3 | 3 | 1 * 3 = 3 | 4 * 3 - 3 = 9 |
| 4 | 3 - 3 = 0 | 1 * 3 + 4 * (-3) = -9 | 5 * 0 - (-9) = 9 |

The final row shows why we need the second tree: the value at index 4 is zero,
but the sum of the array is still 9.

### 3. Subtract two prefixes to query a range

As with an ordinary Fenwick tree, remove the prefix before the left endpoint:

```text
sum of A[left..right] = prefix_sum(right) - prefix_sum(left - 1)
```

`prefix_sum(-1)` is zero, so this also works for ranges starting at index 0.
Here is the complete code, starting from an array of zeros:

```python
from fenwick_tree import FenwickTree

n = 5
b1, b2 = FenwickTree(n), FenwickTree(n)

def range_add(left, right, delta):
    # Start the addition at left; record its correction in b2 too.
    b1.add(left, delta)
    b2.add(left, left * delta)
    # Stop after right, unless the range reaches the end of the array.
    if right + 1 < n:
        b1.add(right + 1, -delta)
        b2.add(right + 1, -(right + 1) * delta)

def prefix_sum(p):
    # Count each change p + 1 times, then remove its extra copies.
    return (p + 1) * b1.sum(p) - b2.sum(p)

def range_sum(left, right):
    return prefix_sum(right) - prefix_sum(left - 1)

range_add(1, 3, 3)                  # [0, 3, 3, 3, 0]
print(range_sum(1, 3))              # 9
range_add(2, 4, -1)                 # [0, 3, 2, 2, -1]
print(range_sum(0, 4))              # 6
range_add(0, 4, 2)                  # [2, 5, 4, 4, 1]
print(range_sum(0, 4))              # 16
```

Each range update or query takes O(log n); the two trees use O(n) storage.
This technique supports additive updates, including negative and overlapping
updates, but does not implement range assignment or range min/max.

## Tests

In [test_fenwick_tree.py](test_fenwick_tree.py):

| Test | Expected behavior |
| --- | --- |
| `test_prefix_sums_after_updates` | Check every prefix against a plain list after each positive, negative, or zero update; final prefixes are `[3, 3, 1, 1, 1]` |
| `test_range_sum` | Check all 15 inclusive ranges of `[200, 150, 300, 250, 400]`; for example, `[1..3]` sums to 700 |
| `test_single_element` | Adding 7 then -10 gives `sum(0) == -3` and `sum(-1) == 0` |
| `test_empty_tree` | A zero-length tree returns 0 for `sum(-1)` |

In [test_range_update_range_query.py](test_range_update_range_query.py):

| Test | Expected behavior |
| --- | --- |
| `test_overlapping_range_additions_and_range_sums` | Check all 15 ranges after each of three updates; arrays become `[0, 3, 3, 3, 0]`, `[0, 3, 2, 2, -1]`, and `[2, 5, 4, 4, 1]`; print each expected range sum |
| `test_initialize_nonzero_array` | Initialize from differences of `[2, 1, 4, 3]`; total is 10 and `[1..2]` sums to 5 |
| `test_range_updates_against_plain_list` | Check every range after each of six updates, including endpoint and zero updates; final array is `[-2, 7, 4, 4, 6]`, with total 19 |
| `test_single_element` | Two-tree updates of 7 then -10 give a final sum of -3 |
| `test_empty_tree` | The two-tree empty-prefix formula returns 0 |

The assertions compare results against explicit values or sums computed from
plain Python lists. Printed expected results are explanatory; assertions decide
whether a test passes.

### Run the tests

Install the test dependency in your Python environment:

```sh
python -m pip install pytest
```

From the repository root, run both files:

```sh
python -m pytest python/fenwick_tree/fenwick_tree -v
```

The expected outcome is **9 passed**. To display the overlapping-update test's
printed arrays and expected sums, disable pytest's output capture with `-s`:

```sh
python -m pytest python/fenwick_tree/fenwick_tree/test_range_update_range_query.py -v -s
```

To run just that test:

```sh
python -m pytest python/fenwick_tree/fenwick_tree/test_range_update_range_query.py::test_overlapping_range_additions_and_range_sums -v -s
```

From this implementation folder, the shorter command is
`python -m pytest -v -s`. On Windows, use `py -3` instead of `python` if that
is how your working Python installation is launched.

[Back to the Fenwick tree overview](../README.md)
