# python/ — Python 2 Templates

Python 2.7 compatible data structure templates.

## Folder Structure

```
python/
├── segment_tree/
│   ├── segment_tree/
│   │   ├── segment_tree.py           # SegmentTree class
│   │   └── segment_tree_example.py   # Usage examples
│   └── lazy_segment_tree/
│       ├── lazy_segment_tree.py      # LazySegmentTree class
│       └── lazy_segment_tree_example.py  # Usage examples
└── README.md
```

## Segment Tree

### `segment_tree/segment_tree/segment_tree.py`

#### `SegmentTree`
- Point update, range query (e.g. range sum, range min/max)
- Constructor takes the input list and a binary `func` (e.g. `min`, `max`, `operator.add`)
- `O(n)` build, `O(log n)` update and query

### `segment_tree/lazy_segment_tree/lazy_segment_tree.py`

#### `LazySegmentTree`
- Range update, range query
- Supports additive range updates with a configurable aggregate function
- `O(n)` build, `O(log n)` update and query
