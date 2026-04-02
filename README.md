# deep-diff

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green)](LICENSE)

A Python tool to perform deep comparisons of complex data structures (dictionaries, lists, sets) and identify differences. Inspired by the npm package [deep-diff](https://www.npmjs.com/package/deep-diff).

## Features

- 🔍 **Deep Comparison**: Compare nested dictionaries, lists, and sets
- 📊 **Detailed Diff Output**: Get structured difference records with paths to changed elements
- 🎯 **Exception Paths**: Exclude specific paths from comparison
- 🏷️ **Type-Safe**: Full type hints for better IDE support
- ✨ **Modern Python**: Requires Python 3.8+

## Installation

```bash
pip install deep-diff
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Dictionary Comparison

```python
from deep_diff import diff

result = diff(
    {'a': 1, 'c': 1},
    {'b': 1, 'c': 1}
)
print(result)
# Output:
# [{'kind': 'D', 'path': ['a'], 'lhs': 1},
#  {'kind': 'N', 'path': ['b'], 'rhs': 1}]
```

### Excluding Paths

```python
from deep_diff import diff

result = diff(
    {'a': 1, 'c': 1},
    {'b': 1, 'c': 1},
    exceptions=[['a'], ['b']]
)
print(result)  # None - all differences are excluded
```

## Difference Record Format

Each difference record contains:

| Field | Type | Description |
|-------|------|-------------|
| `kind` | str | Type of change: `'N'` (new), `'D'` (deleted), `'E'` (edited), `'A'` (array change) |
| `path` | list | Path to the changed property (e.g., `['user', 'name']`) |
| `lhs` | any | Left-hand side value (undefined if kind == 'N') |
| `rhs` | any | Right-hand side value (undefined if kind == 'D') |
| `index` | int | Array index (only when kind == 'A') |
| `item` | dict | Nested change record (only when kind == 'A') |

### Change Types

- **`'N'`** - New property/element added
- **`'D'`** - Property/element deleted
- **`'E'`** - Property/element edited/modified
- **`'A'`** - Change within an array element at specific index

## Examples

### Dictionary Changes

```python
from deep_diff import diff

# Modified value
diff({'a': 1}, {'a': 2})
# [{'kind': 'E', 'path': ['a'], 'lhs': 1, 'rhs': 2}]

# Nested structure
diff(
    {'user': {'name': 'Alice', 'age': 30}},
    {'user': {'name': 'Alice', 'age': 31}}
)
# [{'kind': 'E', 'path': ['user', 'age'], 'lhs': 30, 'rhs': 31}]
```

### List Changes

```python
from deep_diff import diff

# Modified element
diff([1, 2, 3], [1, 5, 3])
# [{'kind': 'E', 'path': [1], 'lhs': 2, 'rhs': 5}]

# Added element
diff([1, 2], [1, 2, 3])
# [{'kind': 'A', 'path': [], 'index': 2, 'item': {'kind': 'N', 'rhs': 3}}]
```

### Set Changes

```python
from deep_diff import diff

# Added elements
diff({1, 2}, {1, 2, 3})
# [{'kind': 'N', 'path': [], 'rhs': {3}}]

# Removed elements
diff({1, 2, 3}, {2, 3})
# [{'kind': 'D', 'path': [], 'lhs': {1}}]
```

### Complex Structures

```python
from deep_diff import diff

result = diff(
    {
        'name': 'my object',
        'details': {'with': ['elements']}
    },
    {
        'name': 'updated object',
        'details': {'with': ['more', 'elements']}
    }
)
# Returns detailed differences for each level
```

## API Reference

### `diff(item1, item2, exceptions=None)`

Compare two items and return their differences.

**Parameters:**

- `item1` (any): The first item to compare
- `item2` (any): The second item to compare
- `exceptions` (list, optional): List of paths to exclude from comparison. Each path is a list of keys/indices.

**Returns:**

- `None` if items are equal
- List of difference records if differences exist

**Example:**

```python
from deep_diff import diff

# Equal items
diff([1, 2, 3], [1, 2, 3])  # Returns None

# Different items
diff([1, 2, 3], [1, 2, 4])
# [{'kind': 'E', 'path': [2], 'lhs': 3, 'rhs': 4}]

# With exceptions
diff(
    {'a': 1, 'b': 2},
    {'a': 10, 'b': 20},
    exceptions=[['a']]
)
# [{'kind': 'E', 'path': ['b'], 'lhs': 2, 'rhs': 20}]
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/ider-zh/diff.git
cd diff

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=deep_diff

# Run specific test file
pytest tests/test_deep_diff.py::TestDictDifferences
```

### Code Quality

```bash
# Format code with black
black deep_diff tests

# Lint with ruff
ruff check deep_diff tests

# Type checking with mypy
mypy deep_diff
```

## License

BSD 3-Clause License - see [LICENSE](LICENSE) file for details

## Author

**ider** - [GitHub](https://github.com/ider-zh)

Email: 326737833@qq.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### Version 0.1.0 (Current)

- Complete modernization of the codebase
- Added full type hints
- Migrated to pyproject.toml
- Moved to pytest for testing
- Added comprehensive test suite
- Improved documentation
- Added GitHub Actions CI/CD
- Better code quality with ruff and black
