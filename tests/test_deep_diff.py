"""Test suite for deep_diff functionality."""

from deep_diff import diff


class TestEquality:
    """Test cases for equal items."""

    def test_equal_dicts(self) -> None:
        """Test that equal dicts return None."""
        dict1 = {"a": 1}
        dict2 = {"a": 1}
        result = diff(dict1, dict2)
        assert result is None

    def test_equal_sets(self) -> None:
        """Test that equal sets return None."""
        set1 = {1, 2, 3}
        set2 = {3, 2, 1}  # Sets are unordered
        result = diff(set1, set2)
        assert result is None

    def test_equal_lists(self) -> None:
        """Test that equal lists return None."""
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        result = diff(list1, list2)
        assert result is None

    def test_equal_scalars(self) -> None:
        """Test that equal scalar values return None."""
        result = diff(42, 42)
        assert result is None

    def test_equal_strings(self) -> None:
        """Test that equal strings return None."""
        result = diff("hello", "hello")
        assert result is None


class TestDictDifferences:
    """Test cases for dictionary differences."""

    def test_added_key(self) -> None:
        """Test detection of added key."""
        dict1 = {"a": 1}
        dict2 = {"a": 1, "b": 2}
        result = diff(dict1, dict2)
        assert result == [{"kind": "N", "path": ["b"], "rhs": 2}]

    def test_deleted_key(self) -> None:
        """Test detection of deleted key."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"a": 1}
        result = diff(dict1, dict2)
        assert result == [{"kind": "D", "path": ["b"], "lhs": 2}]

    def test_modified_value(self) -> None:
        """Test detection of modified value."""
        dict1 = {"a": 1}
        dict2 = {"a": 2}
        result = diff(dict1, dict2)
        assert result == [{"kind": "E", "path": ["a"], "lhs": 1, "rhs": 2}]

    def test_nested_dict_difference(self) -> None:
        """Test detection of differences in nested dictionaries."""
        dict1 = {"a": {"b": 1}}
        dict2 = {"a": {"b": 2}}
        result = diff(dict1, dict2)
        assert result == [{"kind": "E", "path": ["a", "b"], "lhs": 1, "rhs": 2}]

    def test_multiple_changes(self) -> None:
        """Test detection of multiple changes."""
        dict1 = {"a": 1}
        dict2 = {"a": 1, "b": 2, "c": 3}
        result = diff(dict1, dict2)
        assert len(result) == 2
        assert {"kind": "N", "path": ["b"], "rhs": 2} in result
        assert {"kind": "N", "path": ["c"], "rhs": 3} in result


class TestListDifferences:
    """Test cases for list differences."""

    def test_modified_element(self) -> None:
        """Test detection of modified list element."""
        list1 = [1, 2, 3]
        list2 = [1, 5, 3]
        result = diff(list1, list2)
        assert result == [{"kind": "E", "path": [1], "lhs": 2, "rhs": 5}]

    def test_added_element(self) -> None:
        """Test detection of added list element."""
        list1 = [1, 2]
        list2 = [1, 2, 3]
        result = diff(list1, list2)
        assert len(result) == 1
        assert result[0]["kind"] == "A"
        assert result[0]["index"] == 2

    def test_deleted_element(self) -> None:
        """Test detection of deleted list element."""
        list1 = [1, 2, 3]
        list2 = [1, 2]
        result = diff(list1, list2)
        assert len(result) == 1
        assert result[0]["kind"] == "A"
        assert result[0]["index"] == 2
        assert result[0]["item"]["kind"] == "D"

    def test_nested_list_difference(self) -> None:
        """Test detection of differences in nested lists."""
        list1 = [[1, 2], [3, 4]]
        list2 = [[1, 2], [3, 5]]
        result = diff(list1, list2)
        assert result == [{"kind": "E", "path": [1, 1], "lhs": 4, "rhs": 5}]


class TestSetDifferences:
    """Test cases for set differences."""

    def test_elements_removed(self) -> None:
        """Test detection of removed set elements."""
        set1 = {1, 2, 3, 4, 5}
        set2 = {6, 5, 4, 3, 2}
        result = diff(set1, set2)
        assert len(result) == 2
        assert {"kind": "D", "path": [], "lhs": {1}} in result
        assert {"kind": "N", "path": [], "rhs": {6}} in result

    def test_elements_added(self) -> None:
        """Test detection of added set elements."""
        set1 = {1, 2}
        set2 = {1, 2, 3}
        result = diff(set1, set2)
        assert result == [{"kind": "N", "path": [], "rhs": {3}}]

    def test_elements_removed_only(self) -> None:
        """Test detection when only elements are removed."""
        set1 = {1, 2, 3}
        set2 = {2, 3}
        result = diff(set1, set2)
        assert result == [{"kind": "D", "path": [], "lhs": {1}}]


class TestMixedTypes:
    """Test cases for mixed data structures."""

    def test_dict_with_list(self) -> None:
        """Test comparison of dict containing lists."""
        dict1 = {"items": [1, 2, 3]}
        dict2 = {"items": [1, 2, 4]}
        result = diff(dict1, dict2)
        assert result == [{"kind": "E", "path": ["items", 2], "lhs": 3, "rhs": 4}]

    def test_dict_with_nested_dict(self) -> None:
        """Test comparison of nested dicts."""
        dict1 = {"user": {"name": "Alice", "age": 30}}
        dict2 = {"user": {"name": "Alice", "age": 31}}
        result = diff(dict1, dict2)
        assert result == [{"kind": "E", "path": ["user", "age"], "lhs": 30, "rhs": 31}]

    def test_type_change(self) -> None:
        """Test detection when type changes."""
        dict1 = {"value": 42}
        dict2 = {"value": "42"}
        result = diff(dict1, dict2)
        assert result == [{"kind": "E", "path": ["value"], "lhs": 42, "rhs": "42"}]


class TestExceptions:
    """Test cases for exception paths."""

    def test_exclude_single_key(self) -> None:
        """Test excluding a single key from diff."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"a": 1, "b": 999}
        result = diff(dict1, dict2, exceptions=[["b"]])
        assert result is None

    def test_exclude_nested_key(self) -> None:
        """Test excluding nested keys from diff."""
        dict1 = {"data": {"id": 1, "name": "old"}}
        dict2 = {"data": {"id": 2, "name": "new"}}
        result = diff(dict1, dict2, exceptions=[["data", "id"]])
        assert result == [{"kind": "E", "path": ["data", "name"], "lhs": "old", "rhs": "new"}]

    def test_exclude_multiple_paths(self) -> None:
        """Test excluding multiple paths from diff."""
        dict1 = {"a": 1, "b": 2, "c": 3}
        dict2 = {"a": 999, "b": 999, "c": 3}
        result = diff(dict1, dict2, exceptions=[["a"], ["b"]])
        assert result is None


class TestEdgeCases:
    """Test cases for edge cases."""

    def test_empty_dicts(self) -> None:
        """Test comparison of empty dicts."""
        result = diff({}, {})
        assert result is None

    def test_empty_lists(self) -> None:
        """Test comparison of empty lists."""
        result = diff([], [])
        assert result is None

    def test_empty_sets(self) -> None:
        """Test comparison of empty sets."""
        result = diff(set(), set())
        assert result is None

    def test_none_values(self) -> None:
        """Test comparison of None values."""
        dict1 = {"value": None}
        dict2 = {"value": None}
        result = diff(dict1, dict2)
        assert result is None

    def test_none_vs_value(self) -> None:
        """Test comparison of None vs actual value."""
        dict1 = {"value": None}
        dict2 = {"value": 0}
        result = diff(dict1, dict2)
        assert result == [{"kind": "E", "path": ["value"], "lhs": None, "rhs": 0}]

    def test_boolean_vs_int(self) -> None:
        """Test comparison of boolean vs int (equality issue)."""
        # Note: In Python, True == 1 and False == 0, so these are "equal"
        dict1 = {"value": True}
        dict2 = {"value": 1}
        # This might return None due to Python's equality rules
        result = diff(dict1, dict2)
        # True == 1 in Python, so result should be None
        assert result is None

    def test_deep_nesting(self) -> None:
        """Test detection in deeply nested structures."""
        dict1 = {"a": {"b": {"c": {"d": 1}}}}
        dict2 = {"a": {"b": {"c": {"d": 2}}}}
        result = diff(dict1, dict2)
        assert result == [{"kind": "E", "path": ["a", "b", "c", "d"], "lhs": 1, "rhs": 2}]

    def test_complex_structure(self) -> None:
        """Test comparison of complex nested structure."""
        dict1 = {
            "users": [
                {"id": 1, "name": "Alice", "tags": {"admin", "user"}},
                {"id": 2, "name": "Bob", "tags": {"user"}},
            ]
        }
        dict2 = {
            "users": [
                {"id": 1, "name": "Alice", "tags": {"admin", "user"}},
                {"id": 2, "name": "Bob", "tags": {"user"}},
            ]
        }
        result = diff(dict1, dict2)
        assert result is None
