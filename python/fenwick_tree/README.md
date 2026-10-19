# Fenwick Tree

A Fenwick tree (binary indexed tree) supports point additions and prefix sums in
**O(log n)**, with **O(n)** construction and storage.

The implementation in `fenwick_tree/fenwick_tree.py` is self-contained and
compatible with Python 2.7. Copy it directly into your project.

## Interface

| Method | Description |
|--------|-------------|
| `FenwickTree(n)` | Create `n` elements initialised to zero; `n >= 0` |
| `add(i, delta)` | Add `delta` to the element at 0-based index `i` |
| `sum(i)` | Return the inclusive prefix sum over `[0, i]` |

For `add`, use `0 <= i < n`. For `sum`, use `-1 <= i < n`;
`sum(-1)` returns zero for the empty prefix. Bounds are not checked.

## Usage

```python
sales = [200, 150, 300, 250, 400]
tree = FenwickTree(len(sales))
for i, value in enumerate(sales):
    tree.add(i, value)

tree.sum(2)                     # -> 650 (indices 0 through 2)
tree.sum(4) - tree.sum(1)       # -> 950 (indices 2 through 4)

tree.add(2, -170)               # change sales at index 2 from 300 to 130
tree.sum(2)                     # -> 480
tree.sum(4)                     # -> 1130
```

`add` increments an element; to assign a new value, pass `new_value - old_value`.
For any inclusive range `[left, right]`, use `sum(right) - sum(left - 1)`.

Run the tests from the repository root:

```sh
python -m pytest python/fenwick_tree/fenwick_tree/test_fenwick_tree.py -v
```
