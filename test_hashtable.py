import pytest
from pyht import HashTable, Pair


class TestCreate:
    def test_should_create_hashtable(self):
        assert HashTable(capacity=100) is not None

    def test_should_report_capacity(self):
        assert len(HashTable(capacity=100)) == 100

    def test_should_create_empty_value_slots(self):
        t = HashTable(capacity=3)
        assert t._pairs == [None] * 3

    def test_should_not_contain_none_values(self, t: HashTable):
        assert None not in t.values

    def test_should_return_duplicate_values(self, t: HashTable):
        value = 'Same Value'
        t[0] = value
        t[1] = value
        assert t.values == [value, value]


class TestInsert:
    def test_should_insert_key_value_pairs(self, t: HashTable, keys, values):
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            t[key] = value


class TestAccess:
    def test_should_return_existing_values_by_keys(self, t_with_values: HashTable, keys, values):
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            assert t_with_values[key] == value

    def test_should_report_contained_keys(self, t_with_values: HashTable, keys):
        for key in keys:
            assert key in t_with_values

    def test_should_report_contained_values(self, t_with_values: HashTable, values):
        for value in values:
            assert value in t_with_values.values

    def test_should_raise_key_error_on_missing_key(self, t: HashTable):
        key = 'Missing Key'
        with pytest.raises(KeyError) as exception:
            t[key]
        assert exception.value.args[0] == key

    def test_should_not_find_missing_key(self, t: HashTable):
        assert 'Missing Key' not in t

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
        assert l == len(t_with_values)

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
