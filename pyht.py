from collections.abc import Hashable
from typing import Any, Self, TypeAlias


Value: TypeAlias = Any
Key: TypeAlias = Hashable


class Pair:
    key: Key
    value: Value

    def __init__(self, key: Key, value: Value):
        self.key = key
        self.value = value

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Pair):
            return False
        return self.key == other.key and self.value == other.value


Pairs: TypeAlias = list[Pair]
MaybePair: TypeAlias = Pair | None
MaybePairs: TypeAlias = list[MaybePair]


class HashTable:
    def __init__(self, capacity: int):
        self._validate_capacity(capacity)
        self._slots: MaybePairs = [None] * capacity

    @staticmethod
    def _validate_capacity(capacity):
        if not isinstance(capacity, int):
            raise ValueError('`capacity` must be integer')
        if capacity <= 0:
            raise ValueError('`capacity` must be positive')

    @property
    def values(self) -> list[Value]:
        return [pair.value for pair in self._slots if pair]

    @property
    def pairs(self) -> Pairs:
        return [pair for pair in self._slots if pair]

    @property
    def capacity(self) -> int:
        return len(self._slots)

    def get(self, key: Key, default: Value = None) -> Value:
        pair = self._get_pair(key)
        if pair is not None:
            return pair.value
        return default

    def __len__(self) -> int:
        return len(self.pairs)

    def __getitem__(self, key: Hashable) -> Value:
        pair = self._get_pair(key)
        if pair is None:
            raise KeyError(key)
        return pair.value

    def __setitem__(self, key: Hashable, value: Any) -> Any:
        index = self._make_index(key)
        self._slots[index] = Pair(key, value)
        return value

    def __delitem__(self, key: Hashable) -> None:
        index = self._make_index(key)
        pair = self._slots[index]
        if pair is None:
            raise KeyError(key)
        self._slots[index] = None

    def __contains__(self, key: Hashable) -> bool:
        index = self._make_index(key)
        return self._slots[index] is not None

    def _get_pair(self, key: Hashable) -> MaybePair:
        index = self._make_index(key)
        return self._slots[index]

    def _make_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity
