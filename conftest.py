from collections.abc import Hashable
from typing import Any
import pytest

from pyht import HashTable


@pytest.fixture
def t() -> HashTable:
    return HashTable(capacity=100)


@pytest.fixture
def t_with_values(keys, values) -> HashTable:
    t = HashTable(capacity=100)
    for i in range(len(keys)):
        key = keys[i]
        value = values[i]
        t[key] = value
    return t


@pytest.fixture
def keys() -> tuple[Hashable, Hashable, Hashable, Hashable, Hashable]:
    return ('key', 10, 9.4, None, False)


@pytest.fixture
def values() -> tuple[Hashable, Hashable, Hashable, Hashable, Hashable]:
    return ('value', 10.0, 9, None, True)
