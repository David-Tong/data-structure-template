# Segment Tree

## What can a Segment Tree do?

A segment tree is a binary tree built over an array that answers range queries and supports updates efficiently.

| Use case | Example problem |
|----------|----------------|
| Range max/min | What is the maximum value between index 2 and 7? |
| Range sum | What is the sum of elements from index 3 to 9? |
| Point update | Set index 5 to a new value, then query again |
| Range update | Add 3 to every element from index 1 to 6 (lazy only) |

Without a segment tree, a range query is O(n) and an update requires rebuilding. A segment tree reduces both to **O(log n)**.

---

## Interface

Each class is a self-contained file with no external dependencies — copy it directly into your project.

The public interface each class exposes:

| Class | Method | Signature | Description |
|-------|--------|-----------|-------------|
| `SegmentTree` | `update` | `update(idx, val)` | Set element at 0-based `idx` to `val` |
| `SegmentTree` | `range_query` | `range_query(ql, qr)` | Return aggregate over `[ql, qr]` |
| `SegmentTree` | `range_update` | `range_update(ql, qr, val)` | **Blocked** — raises `NotImplementedError`. Use `LazySegmentTree` instead. |
| `LazySegmentTree` | `update` | `update(ql, qr, val)` | Apply `val` to every element in `[ql, qr]` via `update_func` |
| `LazySegmentTree` | `range_update` | `range_update(ql, qr, val)` | Alias for `update` |
| `LazySegmentTree` | `range_query` | `range_query(ql, qr)` | Return aggregate over `[ql, qr]` |

The interface contract is documented as comments inside each class — look for the `--- Interface ---` and `--- Customisation points ---` sections in the docstring.

`update` and `range_update` sit together in the table to make the point/range distinction visible.

---

## `SegmentTree` — Point update, range query

### Constructor

```python
SegmentTree(nums, aggregate_func=max)
```

| Parameter | Description | Example |
|-----------|-------------|---------|
| `nums` | Input list | `[3, 1, 4, 1, 5]` |
| `aggregate_func` | Aggregate function over two values | `max`, `min`, `operator.add` |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `update` | `update(idx, val)` | Set element at index `idx` to `val` |
| `range_update` | `range_update(ql, qr, val)` | **Blocked** — raises `NotImplementedError`. Use `LazySegmentTree` instead. |
| `range_query` | `range_query(ql, qr)` | Return `func` aggregate over `[ql, qr]` |

### How to customise

Change `func` to control what `range_query` returns. Any associative binary function works.

**Range maximum** (default) — find the largest value in a range:
```python
temps = [30, 25, 35, 28, 40, 22, 38, 31]
st = SegmentTree(temps)               # aggregate_func=max by default
st.range_query(0, 4)                  # -> 40 (hottest in first 5 days)
st.update(4, 33)                      # correct a faulty sensor reading
st.range_query(0, 4)                  # -> 35
```

**Range minimum** — find the smallest value in a range:
```python
prices = [100, 95, 102, 88, 110, 76, 99, 105]
st = SegmentTree(prices, aggregate_func=min)
st.range_query(0, 7)                  # -> 76 (cheapest price overall)
st.range_query(0, 3)                  # -> 88 (cheapest in first 4 days)
```

**Range sum** — total up values in a range:
```python
import operator
sales = [200, 150, 300, 250, 400, 180, 220, 350]
st = SegmentTree(sales, aggregate_func=operator.add)
st.range_query(0, 3)                  # -> 900 (week 1 total)
st.range_query(4, 7)                  # -> 1150 (week 2 total)
st.update(2, 130)                     # correct a data entry error
st.range_query(0, 7)                  # -> 1880 (revised total)
```

**Custom function** — any associative `f(a, b)` works, e.g. range product:
```python
import operator
nums = [1, 2, 3, 4, 5]
st = SegmentTree(nums, aggregate_func=operator.mul)
st.range_query(0, 2)                  # -> 6   (1*2*3)
st.range_query(1, 4)                  # -> 120 (2*3*4*5)
```

See `segment_tree/test_segment_tree.py` for the full test suite.

### Original template use case

**Problem**: Given a list of numbers, repeatedly answer two kinds of queries:
1. What is the maximum value between index `ql` and `qr`?
2. Change the value at index `idx` to a new value.

A brute-force scan is O(n) per query. With a segment tree, both operations are O(log n).

**Concrete example**: You have 8 daily temperature readings. A weather app needs to answer "what was the hottest day between day 2 and day 6?" thousands of times, and sensor corrections arrive in between queries. Rebuilding from scratch each time is too slow — the segment tree makes every query and correction O(log n) instead.

The original template hardcoded `func=max`. Our template keeps the same default, so the call is identical:

```python
nums = [2, 1, 5, 3, 6, 4, 8, 7]
st = SegmentTree(nums)       # aggregate_func=max by default
st.range_query(0, 2)         # -> 5   (max of indices 0, 1, 2)
st.update(1, 9)              # sensor correction: index 1 is now 9
st.range_query(0, 2)         # -> 9   (max updated)
```

---

## `LazySegmentTree` — Range update, range query

### Constructor

```python
LazySegmentTree(n, aggregate_func=max, update_func=None, identity=0, nums=None)
```

| Parameter | Description | Example |
|-----------|-------------|---------|
| `n` | Size of the array | `10` |
| `aggregate_func` | Aggregate function over two node values | `max`, `min`, `operator.add` |
| `update_func` | How a delta is applied to a node's aggregate value. Signature: `update_func(val, delta, size) -> new_val` where `size` is the number of elements the node covers. Default: `lambda val, delta, size: val + delta` (correct for max/min). For sum use `lambda val, delta, size: val + delta * size`. | `lambda val, delta, size: val * delta` |
| `identity` | Starting value of every node. Must be the neutral element for `aggregate_func`. See `identity` section below. | `0` |
| `nums` | Optional initial list of values loaded into the tree during construction. | `[3, 1, 4, 1, 5]` |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `update` | `update(ql, qr, val)` | Apply `val` to every element in `[ql, qr]` via `update_func` |
| `range_query` | `range_query(ql, qr)` | Return `func` aggregate over `[ql, qr]` |

### `identity` — starting value for every node

Every node is initialised to `identity` before any data is loaded. It must be the **neutral element** for `aggregate_func`: a value `e` where `aggregate_func(e, x) == x` for any `x`. Wrong choice means queries on uninitialised nodes return garbage.

| `aggregate_func` | correct `identity` | why |
|------------------|--------------------|-----|
| `max` | `0` (if all values ≥ 0) or `float('-inf')` | `max(e, x) == x` |
| `min` | `0` (if all values ≥ 0) or `float('inf')` | `min(e, x) == x` |
| `operator.add` | `0` | `0 + x == x` |
| `operator.mul` | `1` | `1 * x == x` |

**Second constraint — must survive `update_func`**: when you load initial values via `update(i, i, v)` (either manually or through `nums`), the tree calls `update_func(identity, v, 1)` on each leaf. That result must equal `v`, otherwise the loaded value is wrong from the start.

- Additive `update_func` (`val + delta`): `update_func(0, v, 1) = 0 + v = v` ✓ — use `identity=0`
- Multiplicative `update_func` (`val * delta`): `update_func(1, v, 1) = 1 * v = v` ✓ — use `identity=1`
- `identity=float('-inf')` with additive update: `float('-inf') + v = float('-inf')` ✗ — broken

### `nums` — initial values

`nums` is a convenience shortcut. Passing `nums=[a, b, c, ...]` is exactly equivalent to constructing the tree and then calling:

```python
for i, v in enumerate(nums):
    st.update(i, i, v)
```

The `identity` constraint above applies: the tree must be able to recover `v` from `update_func(identity, v, 1)`. With the default additive `update_func` and `identity=0` this always holds.

```python
# These two are identical:
st = LazySegmentTree(5, aggregate_func=max, identity=0, nums=[10, 20, 15, 30, 25])

st = LazySegmentTree(5, aggregate_func=max, identity=0)
for i, v in enumerate([10, 20, 15, 30, 25]):
    st.update(i, i, v)
```

### How to customise

| Goal | `aggregate_func` | `update_func` | needs `size`? | `identity` |
|------|-----------------|---------------|---------------|------------|
| Range sum + range add | `operator.add` | `lambda val, delta, size: val + delta * size` | **yes** — sum grows by `delta` per element | `0` |
| Range max + range add | `max` | `lambda val, delta, size: val + delta` | no — max shifts by `delta` regardless of count | `0` |
| Range min + range add | `min` | `lambda val, delta, size: val + delta` | no — min shifts by `delta` regardless of count | `0` |
| Range sum + range multiply | `operator.add` | `lambda val, delta, size: val * delta` | no — sum scales by `delta` regardless of count | `1` |

**When does `update_func` need `size`?** It depends on the combination of `update_func` and `aggregate_func` — not either one alone:

> Does applying the update to each element change the aggregate by a **fixed amount**, or by an amount that **scales with the number of elements**?

Node covering `[1..3]`, original values `[4, 7, 2]`, `delta=3`, `size=3`.

**Add delta=3 to every element, aggregate=sum**
```
values: [4, 7, 2]  ->  [7, 10, 5]
sum before: 13
sum after:  22 = 13 + 3*3    # delta added 3 times, once per element -> needs size
update_func: lambda val, delta, size: val + delta * size
```

**Add delta=3 to every element, aggregate=max**
```
values: [4, 7, 2]  ->  [7, 10, 5]
max before: 7
max after:  10 = 7 + 3       # max just shifts by delta regardless of how many elements
update_func: lambda val, delta, size: val + delta
```

**Multiply every element by delta=3, aggregate=sum**
```
values: [4, 7, 2]  ->  [12, 21, 6]
sum before: 13
sum after:  39 = 13 * 3      # whole sum scales by delta regardless of how many elements
update_func: lambda val, delta, size: val * delta
```

**Multiply every element by delta=3, aggregate=max**
```
values: [4, 7, 2]  ->  [12, 21, 6]
max before: 7
max after:  21 = 7 * 3       # max scales by delta regardless of how many elements
update_func: lambda val, delta, size: val * delta
```

`size` is only needed in one case: **additive update + sum aggregate**.

**What is `size` in `update_func`?**

A segment tree node stores the *aggregate of a range*, not individual elements. When a range update covers a node exactly, the tree skips visiting each element and applies `delta` once to the stored aggregate instead (lazy propagation). `size` — the number of original array elements in the node's range — lets `update_func` compute the correct new aggregate without touching each element individually.

For max/min, shifting every element by `delta` shifts the aggregate by exactly `delta`, regardless of range width. For sum, `delta` is added once per element, so the total increases by `delta * size`. Without the `* size`, a range update over 100 elements would only add `delta` once to the node's sum instead of 100 times.

**Why does range multiply not need `size`?** Multiplication distributes cleanly over any aggregate:

```
(a*δ) + (b*δ) + (c*δ) = (a+b+c) * δ   →  sum * delta,  no size needed
max(a*δ, b*δ, c*δ)    = max(a,b,c) * δ →  max * delta,  no size needed
```

The stored aggregate just gets scaled by `delta` regardless of how many elements are in the range. Addition does not have this property — adding `delta` to each element increases the sum by `delta * size`, not `delta * 1`.

**Range sum with range add** — total salaries, apply raises to a department:
```python
import operator
st = LazySegmentTree(6, aggregate_func=operator.add,
                     update_func=lambda val, delta, size: val + delta * size,
                     identity=0)
st.update(0, 5, 200)    # give everyone a 200 raise
st.update(1, 3, 500)    # give department [1..3] an extra 500
st.range_query(0, 5)    # -> total salary bill
st.range_query(1, 3)    # -> department [1..3] total
```

**Range max with range add** — player scores, add bonus points to a group:
```python
st = LazySegmentTree(6, aggregate_func=max, identity=0)
st.update(2, 4, 10)     # award 10 bonus points to players [2..4]
st.range_query(0, 5)    # -> highest score overall
st.range_query(0, 2)    # -> highest score in [0..2]
```

**Range min with range add** — item prices, apply a discount to a range:
```python
st = LazySegmentTree(5, aggregate_func=min, identity=0)
st.update(1, 3, -15)    # apply -15 discount to items [1..3]
st.range_query(0, 4)    # -> cheapest item overall
st.range_query(2, 4)    # -> cheapest item in [2..4]
```

**Custom update_func: range multiply** — scale values in a range by a multiplier:

The default `update_func` adds a delta to each node value. For multiplication you replace it with `lambda val, delta, size: val * delta`.

Three parameters work together:

| Parameter | Value | Why |
|-----------|-------|-----|
| `aggregate_func` | `operator.add` | you want the *sum* of the range after multiplying |
| `update_func` | `lambda val, delta, size: val * delta` | each element is *multiplied* by delta |
| `identity` | `1` | neutral element for multiplication — see `identity` section above |

```python
import operator
values = [2, 3, 4, 5, 6]
#  index:  0  1  2  3  4
st = LazySegmentTree(5, aggregate_func=operator.add,
                     update_func=lambda val, delta, size: val * delta,
                     identity=1)
for i, v in enumerate(values):
    st.update(i, i, v)         # initialise: each element set via 1 * v = v

st.range_query(0, 4)           # -> 20  (2+3+4+5+6)
st.update(1, 3, 2)             # double every element in [1..3]: [2,6,8,10,6]
st.range_query(0, 4)           # -> 32  (2+6+8+10+6)
st.range_query(1, 3)           # -> 24  (6+8+10)
```

**Limitation**: the internal lazy accumulator is additive (`lazy += delta`). If two multiplicative range updates overlap on the same node before the lazy value is pushed down, the second delta is added to the first instead of multiplied — giving a wrong result. Range multiply is therefore safe only when range updates do not overlap. For full correctness with overlapping range multiplies you would need a custom subclass that overrides `_apply` and `_push_down` to combine lazy values multiplicatively.

See `lazy_segment_tree/test_lazy_segment_tree.py` for the full test suite.

### Original template use case and find_first

**Problem**: You have an array of values that receive frequent **range updates** (e.g. add 3 to every element from index 1 to 6). After each batch of updates, you need to find the **leftmost index** in a range whose value equals a specific target.

A concrete scenario: you have `n` seats, each with a "score" initialised to 0. Events add points to ranges of seats. After each event, you need to find the first seat whose total score has reached exactly some threshold — for example, the first seat that has received exactly 5 points total.

The original template tracked both `min` and `max` per node so it could prune the search tree: if the target is outside `[min, max]` for a node's range, that whole subtree can be skipped. It exposed `find_first(ql, qr, target)` — returning the leftmost index in `[ql..qr]` whose value equals `target`, or `-1` if none exists.

This generic template uses a single aggregate value per node instead, which does not support `find_first` directly.

**Why two trees?**

The original template stored both `min` and `max` in every node. This let it answer the question "does target exist somewhere in this node's range?" in O(1) per node — if `target < min` or `target > max`, the whole subtree is skipped. That is how it achieved O(log n) for `find_first`.

Our generic template stores only one aggregate value per node. A single `min` tree tells you the smallest value in a range but not whether `target` is present. A single `max` tree tells you the largest but not whether `target` is present. You need **both** to reconstruct the same pruning condition: `min <= target <= max` means target could exist in this range.

**Why binary search?**

The original template had `find_first` built into the recursive tree traversal — it walked left before right and returned as soon as it found the leftmost match, all in one O(log n) pass.

Our generic `range_query` only returns an aggregate, not a position. To find the leftmost index, we binary search over `[ql..qr]`: at each step we check whether the left half contains the target (using both trees), and narrow accordingly. Each check is O(log n) and we do O(log n) checks, so the total is **O(log² n)** — slightly worse than the original O(log n) but acceptable for most use cases.

To replicate it, use **two trees** — one tracking `min`, one tracking `max` — and apply every update to both:

```python
st_min = LazySegmentTree(n, aggregate_func=min, identity=0)
st_max = LazySegmentTree(n, aggregate_func=max, identity=0)

# A range [ql..qr] contains target iff:
#   st_min.range_query(ql, qr) <= target <= st_max.range_query(ql, qr)

def find_first(ql, qr, target):
    if not (st_min.range_query(ql, qr) <= target <= st_max.range_query(ql, qr)):
        return -1
    lo, hi = ql, qr
    while lo < hi:
        mid = (lo + hi) // 2
        if st_min.range_query(lo, mid) <= target <= st_max.range_query(lo, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

See `lazy_segment_tree/test_lazy_segment_tree.py` `test_find_first_workaround` for the full runnable version.

---

## Indexing

All public methods (`update`, `range_query`) use **0-based indexing** — consistent with standard Python arrays.

| | External (caller) | Internal (tree nodes) |
|--|-------------------|-----------------------|
| Array positions | 0-based: `0..N-1` | 1-based: `1..N` (shifted by +1) |
| Tree nodes | hidden | 1-based: root=1, children=`2*node`, `2*node+1` |

The internal +1 shift is an implementation detail. Callers never see it — `idx`, `ql`, and `qr` always mean 0-based positions into the original array.

---

## Why separate `update` signatures

The two classes serve different use cases:

- `SegmentTree` — point update `update(idx, val)`, range aggregate query
- `LazySegmentTree` — range update `update(ql, qr, val)`, range aggregate query

Forcing identical signatures would require `*args`/`**kwargs` and lose clarity. Each class owns its own signature and documents it in the `--- Interface ---` comment block in its docstring.

---

## Range Update — Normal vs Lazy Segment Tree

Range update is possible in a normal segment tree but is not efficient:

| Operation | Normal Segment Tree | Lazy Segment Tree |
|-----------|--------------------|--------------------|
| Point update | O(log n) | O(log n) |
| Range update | O(n log n) — loop point update over each index | O(log n) — lazy propagation defers work |
| Range query | O(log n) | O(log n) |

`SegmentTree.range_update()` is intentionally blocked and raises `NotImplementedError`. Use `LazySegmentTree` when range update is a core operation.

---

## Running tests

```bash
# run all tests from the segment_tree/ folder
pytest segment_tree/ lazy_segment_tree/ -v

# or run one suite at a time
pytest segment_tree/test_segment_tree.py -v
pytest lazy_segment_tree/test_lazy_segment_tree.py -v
```

Each test function maps to one customisation scenario described in this README.

---

## File Structure

```
segment_tree/
├── README.md
├── segment_tree/
│   ├── segment_tree.py              # SegmentTree — self-contained, no dependencies
│   └── test_segment_tree.py         # pytest test suite (examples + assertions)
└── lazy_segment_tree/
    ├── lazy_segment_tree.py         # LazySegmentTree — self-contained, no dependencies
    └── test_lazy_segment_tree.py    # pytest test suite (examples + assertions)
```
