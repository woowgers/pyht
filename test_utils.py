from types import NoneType

from pytest_unordered import unordered

from utils import (
    random_boolean,
    random_float,
    random_integer,
    random_none,
    random_positive,
    random_string,
    random_unique_values,
    random_value,
)


class TestInteger:
    def test_returns_integer(self):
        value = random_integer()
        assert isinstance(value, int)


class TestBool:
    def test_returns_boolean(self):
        value = random_boolean()
        assert isinstance(value, bool)


class TestFloat:
    def test_returns_float(self):
        value = random_float()
        assert isinstance(value, float)


class TestString:
    def test_returns_string(self):
        value = random_string()
        assert isinstance(value, str)


class TestNone:
    def test_returns_none(self):
        value = random_none()
        assert value is None


class TestValue:
    def test_returns_value(self):
        value = random_value()
        classes = (NoneType, int, str, float)
        assert type(value) in classes


class TestPositive:
    def test_returns_positive(self):
        value = random_positive()
        assert value > 0


class TestUniqueValues:
    def test_returns_unique_values(self):
        n_values = random_positive() % 100
        values = random_unique_values(n_values)
        unique = unordered(list(set(values)))
        assert unique == values
