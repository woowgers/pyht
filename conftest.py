import pytest

from pyht import HashTable, Key, Value
from utils import random_integer, random_unique_values


@pytest.fixture
def t(n_values: int) -> HashTable:
    return HashTable(capacity=n_values)


@pytest.fixture
def t_with_values(n_values: int, keys, values) -> HashTable:
    t = HashTable(capacity=n_values)
    for i in range(len(keys)):
        key = keys[i]
        value = values[i]
        t[key] = value
    return t


@pytest.fixture
def n_values() -> int:
    return 1 + abs(random_integer()) % 100


@pytest.fixture
def keys(n_values: int) -> list[Key]:
    return random_unique_values(n_values)


@pytest.fixture
def values(n_values: int) -> list[Value]:
    return random_unique_values(n_values)
