"""Tests for celery call JSON argument parsing."""
import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from celery.bin.base import JSON_ARRAY, JSON_OBJECT


@pytest.fixture(autouse=True)
def clean_os_environ():
    with patch.dict(os.environ, clear=True):
        yield


class test_JsonArray:
    """Tests for the JSON_ARRAY parameter type."""

    def test_valid_json_array(self):
        result = JSON_ARRAY.convert('[1, 2, 3]', None, None)
        assert result == [1, 2, 3]

    def test_valid_json_array_strings(self):
        result = JSON_ARRAY.convert('["a", "b"]', None, None)
        assert result == ["a", "b"]

    def test_single_quoted_strings(self):
        """Single-quoted Python-style array should be accepted."""
        result = JSON_ARRAY.convert("['1', '2']", None, None)
        assert result == ["1", "2"]

    def test_single_quoted_mixed(self):
        """Single-quoted array with mixed types should be accepted."""
        result = JSON_ARRAY.convert("['hello', 1, True]", None, None)
        assert result == ["hello", 1, True]

    def test_already_a_list(self):
        value = [1, 2, 3]
        result = JSON_ARRAY.convert(value, None, None)
        assert result is value

    def test_invalid_value_raises(self):
        with pytest.raises(Exception):
            JSON_ARRAY.convert("not-an-array", None, None)

    def test_object_not_accepted_as_array(self):
        with pytest.raises(Exception):
            JSON_ARRAY.convert('{"a": 1}', None, None)


class test_JsonObject:
    """Tests for the JSON_OBJECT parameter type."""

    def test_valid_json_object(self):
        result = JSON_OBJECT.convert('{"x": 1}', None, None)
        assert result == {"x": 1}

    def test_single_quoted_object(self):
        """Single-quoted Python-style dict should be accepted."""
        result = JSON_OBJECT.convert("{'x': 1}", None, None)
        assert result == {"x": 1}

    def test_single_quoted_keys_and_values(self):
        result = JSON_OBJECT.convert("{'key': 'value'}", None, None)
        assert result == {"key": "value"}

    def test_already_a_dict(self):
        value = {"a": 1}
        result = JSON_OBJECT.convert(value, None, None)
        assert result is value

    def test_invalid_value_raises(self):
        with pytest.raises(Exception):
            JSON_OBJECT.convert("not-an-object", None, None)

    def test_array_not_accepted_as_object(self):
        with pytest.raises(Exception):
            JSON_OBJECT.convert('[1, 2]', None, None)
