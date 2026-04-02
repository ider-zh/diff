"""Deep diff tool for comparing dict, list, and set data structures."""

from typing import Any, Dict, List, Optional, Set, Union

__version__ = "0.1.0"
__all__ = ["diff"]

# Type aliases for clarity
Comparable = Union[Dict[str, Any], List[Any], Set[Any], Any]
DiffRecord = Dict[str, Any]


def _diff_set(set1: Set[Any], set2: Set[Any]) -> List[DiffRecord]:
    """Compare two sets and return differences.

    Args:
        set1: The first set to compare.
        set2: The second set to compare.

    Returns:
        A list of difference records.
    """
    diff_records: List[DiffRecord] = []
    removed = set1 - set2
    added = set2 - set1

    if removed:
        diff_records.append({"kind": "D", "path": [], "lhs": removed})
    if added:
        diff_records.append({"kind": "N", "path": [], "rhs": added})

    return diff_records


def _diff_list(list1: List[Any], list2: List[Any]) -> List[DiffRecord]:
    """Compare two lists and return differences.

    Args:
        list1: The first list to compare.
        list2: The second list to compare.

    Returns:
        A list of difference records.
    """
    diff_records: List[DiffRecord] = []

    # Compare common elements
    for i, (item1, item2) in enumerate(zip(list1, list2)):
        _router(item1, item2, diff_records, i)

    # Handle length differences
    if len(list1) > len(list2):
        for i in range(len(list2), len(list1)):
            diff_records.append(
                {"kind": "A", "path": [], "index": i, "item": {"kind": "D", "lhs": list1[i]}}
            )
    elif len(list1) < len(list2):
        for i in range(len(list1), len(list2)):
            diff_records.append(
                {"kind": "A", "path": [], "index": i, "item": {"kind": "N", "rhs": list2[i]}}
            )

    return diff_records


def _diff_dict(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> List[DiffRecord]:
    """Compare two dictionaries and return differences.

    Args:
        dict1: The first dictionary to compare.
        dict2: The second dictionary to compare.

    Returns:
        A list of difference records.
    """
    diff_records: List[DiffRecord] = []

    # Keys only in dict1 (deleted)
    for key in sorted(set(dict1.keys()) - set(dict2.keys())):
        diff_records.append({"kind": "D", "path": [key], "lhs": dict1[key]})

    # Keys only in dict2 (new)
    for key in sorted(set(dict2.keys()) - set(dict1.keys())):
        diff_records.append({"kind": "N", "path": [key], "rhs": dict2[key]})

    # Common keys
    for key in sorted(dict1.keys()):
        if key in dict2:
            _router(dict1[key], dict2[key], diff_records, key)

    return diff_records


def _router(
    item1: Any,
    item2: Any,
    diff_records: List[DiffRecord],
    path_key: Optional[Union[str, int]] = None,
) -> None:
    """Route comparison based on item types.

    Args:
        item1: The first item to compare.
        item2: The second item to compare.
        diff_records: List to accumulate difference records.
        path_key: The current key/index in the path.
    """
    if isinstance(item1, dict) and isinstance(item2, dict):
        ret_list = _diff_dict(item1, item2)
        if path_key is not None:
            for record in ret_list:
                record["path"].insert(0, path_key)
        diff_records.extend(ret_list)

    elif isinstance(item1, list) and isinstance(item2, list):
        ret_list = _diff_list(item1, item2)
        if path_key is not None:
            for record in ret_list:
                record["path"].insert(0, path_key)
        diff_records.extend(ret_list)

    elif isinstance(item1, set) and isinstance(item2, set):
        ret_list = _diff_set(item1, item2)
        if path_key is not None:
            for record in ret_list:
                record["path"].insert(0, path_key)
        diff_records.extend(ret_list)

    elif item1 != item2:
        if path_key is not None:
            diff_records.append({"kind": "E", "path": [path_key], "lhs": item1, "rhs": item2})
        else:
            diff_records.append({"kind": "E", "path": [], "lhs": item1, "rhs": item2})


def _is_path_in_exceptions(
    diff_record: DiffRecord, exception_paths: List[List[Union[str, int]]]
) -> bool:
    """Check if a diff record path matches any exception paths.

    Args:
        diff_record: The difference record to check.
        exception_paths: List of paths to exclude from diff.

    Returns:
        True if the record should be excluded, False otherwise.
    """

    def _is_subset(prefix: List[Any], path: List[Any]) -> bool:
        """Check if prefix matches the first elements of path."""
        if len(prefix) > len(path):
            return False
        for p_elem, path_elem in zip(prefix, path):
            if p_elem != path_elem:
                return False
        return True

    # Filter out non-integer path elements for matching
    diff_path = [p for p in diff_record["path"] if not isinstance(p, int)]

    for exception in exception_paths:
        if exception == diff_path:
            return True
        if len(exception) < len(diff_path) and _is_subset(exception, diff_path):
            return True

    return False


def diff(
    item1: Comparable, item2: Comparable, exceptions: Optional[List[List[Union[str, int]]]] = None
) -> Optional[List[DiffRecord]]:
    """Compare two items and return their differences.

    Compares two items (dict, list, set, or scalar values) and returns
    a list of difference records. Each record indicates what changed,
    where it changed, and what the values were.

    Args:
        item1: The first item to compare.
        item2: The second item to compare.
        exceptions: Optional list of paths to exclude from the diff.

    Returns:
        A list of difference records, or None if items are equal.

    Example:
        >>> diff({'a': 1, 'c': 1}, {'b': 1, 'c': 1})
        [{'kind': 'D', 'path': ['a'], 'lhs': 1},
         {'kind': 'N', 'path': ['b'], 'rhs': 1}]
    """
    if item1 == item2:
        return None

    diff_records: List[DiffRecord] = []
    _router(item1, item2, diff_records)

    # Filter out exceptions if provided
    if exceptions:
        diff_records = [rec for rec in diff_records if not _is_path_in_exceptions(rec, exceptions)]

    return diff_records if diff_records else None
