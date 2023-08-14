import pytest

from pyht import Pair


class TestCreate:
    def test_creates_pair(self):
        pair = Pair('key', 'value')
        assert type(pair) == Pair


class TestDeleted:
    def test_returns_private_deleted_attribute(self):
        expected = Pair._Pair__Deleted  # pyright: ignore
        deleted = Pair.deleted
        assert deleted is expected


class TestEquals:
    def test_equals_if_equal_key_and_values(self):
        p1 = Pair(1, 2)
        p2 = Pair(1, 2)
        assert p1 == p2

    def test_not_equals_if_not_equal_keys(self):
        p1 = Pair(1, 2)
        p2 = Pair(0, 2)
        assert p1 != p2

    def test_not_equals_if_not_equal_values(self):
        p1 = Pair(1, 2)
        p2 = Pair(1, 0)
        assert p1 != p2


class TestAccess:
    def test_first_index_returns_key(self):
        p = Pair(1, 0)
        assert p[0] == 1

    def test_second_index_returns_index(self):
        p = Pair(1, 0)
        assert p[1] == 0

    def test_third_index_raises_indexerror(self):
        with pytest.raises(IndexError):
            p = Pair(1, 0)
            p[2]


class TestStr:
    def test_returns_string_representation(self):
        p = Pair(1, 2)
        assert str(p) == '1: 2'
