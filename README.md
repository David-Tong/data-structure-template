# Data structure templates

Self-contained Python data structures for competitive programming. Copy an
implementation file into your project, run its example to learn the API, and
use its tests to check behavior.

## Choose a structure

| Structure | Updates | Queries | Guide |
| --- | --- | --- | --- |
| Fenwick tree | Point addition; range addition with two trees | Prefix and range sums | [Fenwick tree](python/fenwick_tree/README.md) |
| Segment tree | Point assignment | Sum, min, max, or another associative aggregate | [Segment trees](python/segment_tree/README.md) |
| Lazy segment tree | Range addition | Sum, min, max | [Lazy segment tree](python/segment_tree/lazy_segment_tree/README.md) |

All public indices are 0-based and ranges include both endpoints. Each
implementation uses O(n) storage. Supported updates and queries take O(log n).

## Run the examples

Use Python 3 for the commands below, from the repository root. The implementation
and example files retain Python 2.7-compatible syntax. Examples require no
third-party dependencies.

```sh
python python/fenwick_tree/fenwick_tree/example_for_fenwick_tree.py
python python/segment_tree/segment_tree/example_for_segment_tree.py
python python/segment_tree/lazy_segment_tree/example_for_lazy_segment_tree.py
```

Each example has separate demonstration functions called by main(), comments
showing array states, and printed query results. Expected output is documented
in its implementation guide.

## Run the tests

```sh
python -m pip install pytest
python -m pytest python -v
```

Expected outcome: **21 passed**. Add -s to display output printed by tests.
On Windows, substitute py -3 for python if that is your Python launcher.

## Repository layout

- [Python catalog](python/README.md): implementation and example links.
- [Fenwick tree](python/fenwick_tree/README.md): sums and additive updates.
- [Segment trees](python/segment_tree/README.md): point assignment and range addition.
- [License](LICENSE).

Implementation folders contain the class, an example_for_*.py script, test_*.py
files, and a README with usage, implementation details, and test coverage.
