from unittest.mock import patch

import pytest
from pytest_unordered import unordered

from pyht import HashTable, Pair


class TestSetup:
    def test_keys_and_values_are_of_same_size(self, keys, values):
        assert len(keys) == len(values)


class TestCreate:
    def test_should_create_hashtable(self):
        assert HashTable(capacity=100) is not None

    def test_should_create_empty_value_slots(self):
        t = HashTable(capacity=3)
        assert t._slots == [None] * 3

    def test_should_not_contain_none_values(self, t: HashTable):
        assert None not in t.values

    def test_should_raise_valueerror_when_capacity_is_zero(self):
        with pytest.raises(ValueError):
            HashTable(capacity=0)

    def test_should_raise_valueerror_when_capacity_not_integer(self):
        with pytest.raises(ValueError):
            HashTable(capacity='Not an integer')  # pyright: ignore

    def test_should_not_create_hashtable_with_negative_capacity(self):
        with pytest.raises(ValueError):
            HashTable(capacity=-1)

    def test_should_add_values_when_collision_happens(self):
        t = HashTable(capacity=2)
        value = 'Some Value'
        with patch('builtins.hash', return_value=0):
            t[0] = value
            t[1] = value
        assert unordered(t.values) == [value, value]


class TestInsert:
    def test_should_insert_key_value_pairs(self, t: HashTable, keys, values):
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            t[key] = value

    def test_should_return_duplicate_values(self):
        t = HashTable(capacity=2)
        value = 'Same Value'
        t[0] = value
        t[1] = value
        assert t.values == [value, value]


class TestAccess:
    def test_should_return_existing_values_by_keys(self, t_with_values: HashTable, keys, values):
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            assert t_with_values[key] == value

    def test_should_raise_key_error_on_missing_key(self, t: HashTable):
        key = 'Missing Key'
        with pytest.raises(KeyError) as exception:
            t[key]
        assert exception.value.args[0] == key

    def test_should_not_find_missing_key(self, t: HashTable):
        assert 'Missing Key' not in t


class TestKeys:
    def test_should_report_contained_keys(self, t_with_values: HashTable, keys):
        for key in keys:
            assert key in t_with_values

    def test_should_return_copy_of_keys(self, t_with_values: HashTable):
        assert t_with_values.keys is not t_with_values.keys


class TestValues:
    def test_should_report_contained_values(self, t_with_values: HashTable, values):
        for value in values:
            assert value in t_with_values.values

    def test_should_return_copy_of_values(self, t_with_values: HashTable):
        assert t_with_values.keys is not t_with_values.keys


class TestPairs:
    def test_should_report_contained_kv_pairs(self, t_with_values: HashTable, keys, values):
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            found = False
            expected_pair = Pair(key, value)
            for pair in t_with_values.pairs:
                if pair == expected_pair:
                    found = True
            assert found

    def test_should_return_copy_of_pairs(self, t_with_values: HashTable):
        assert t_with_values.pairs is not t_with_values.pairs

    def test_should_not_contain_none_pairs(self, t_with_values: HashTable):
        assert None not in t_with_values.pairs


class TestMetrics:
    def test_should_report_length(self, t_with_values: HashTable, values):
        assert len(t_with_values) == len(values)

    def test_should_report_length_of_empty_hashtable(self):
        assert len(HashTable(capacity=100)) == 0

    def test_should_report_representation(self, t_with_values: HashTable, keys, values):
        expected_pair_reprs = self._get_pair_reprs(keys, values)
        representation = str(t_with_values)
        pair_reprs = self._get_pair_reprs_from_hashtable_representation(representation)
        assert unordered(pair_reprs) == expected_pair_reprs
        assert representation[0] == '{'
        assert representation[-1] == '}'

    @staticmethod
    def _get_pair_reprs(keys, values):
        pair_reprs = []
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            pair_repr = f'{key}: {value}'
            pair_reprs.append(pair_repr)
        return pair_reprs

    @staticmethod
    def _get_pair_reprs_from_hashtable_representation(representation: str):
        representation = representation[1:-1]
        return representation.split(', ')


class TestIterate:
    def test_should_iterate_over_keys(self, t_with_values: HashTable, keys):
        keys = list(keys)
        for key in t_with_values.keys:
            assert key in keys
            keys.pop(keys.index(key))
        assert not keys

    def test_should_iterate_over_values(self, t_with_values: HashTable, values):
        values = list(values)
        for value in t_with_values.values:
            assert value in values
            values.pop(values.index(value))
        assert not values

    def test_should_iterate_over_kv_pairs(self, t_with_values: HashTable):
        for key, value in t_with_values.pairs:
            assert key in t_with_values.keys
            assert value in t_with_values.values
            del t_with_values[key]

    def test_should_iterate_over_hashtable_as_by_keys(self, t_with_values: HashTable):
        for key in t_with_values:
            assert key in t_with_values.keys
            del t_with_values[key]


class TestGet:
    def test_should_return_existing_values_by_keys(self, t_with_values: HashTable, keys, values):
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            assert t_with_values.get(key) == value

    def test_should_return_none_on_missing_key(self, t: HashTable):
        key = 'key'
        assert t.get(key) is None

    def test_should_return_default_on_missing_key(self, t: HashTable):
        key = 'key'
        default = 'value'
        assert t.get(key, default) is default


class TestDelete:
    def test_should_delete_existing_keys(self, t_with_values: HashTable, keys):
        l = len(t_with_values)
        for key in keys:
            del t_with_values[key]
            assert key not in t_with_values
        assert l - len(keys) == len(t_with_values)

    def test_should_delete_existing_values(self, t_with_values: HashTable, keys, values):
        for key in keys:
            del t_with_values[key]

        for value in values:
            assert value not in t_with_values.values

    def test_should_raise_key_error_on_missing_key(self, t: HashTable):
        key = 'Missing Key'
        with pytest.raises(KeyError) as exception:
            del t[key]
        assert exception.value.args[0] == key


class TestUpdate:
    def test_should_update_existing_values(self, t_with_values: HashTable, keys):
        new_value = "New Value"
        for key in keys:
            t_with_values[key] = new_value
            assert t_with_values[key] == new_value


class TestFromdict:
    def test_creates_hashtable_from_dict(self, keys, values):
        d = {keys[i]: values[i] for i in range(len(keys))}
        t = HashTable.from_dict(d)
        assert unordered(t.keys) == list(d.keys())
        assert unordered(t.values) == list(d.values())
