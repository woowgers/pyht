from collections.abc import Hashable
from typing import Any, Self, TypeAlias

Value: TypeAlias = Any
Key: TypeAlias = Hashable


class Pair:
    key: Key
    value: Value

    __Deleted = object()

    @classmethod
    @property
    def deleted(cls):
        return cls.__Deleted

    def __init__(self, key: Key, value: Value):
        self.key = key
        self.value = value

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Pair):
            return False
        return self.key == other.key and self.value == other.value

    def __getitem__(self, index: int) -> Key | Value:
        if index not in (0, 1):
            raise IndexError(f'{self.__class__.__name__} only allows 0 and 1 indices ({index} given).')
        if index == 0:
            return self.key
        return self.value

    def __str__(self) -> str:
        return f'{self.key}: {self.value}'


Pairs: TypeAlias = list[Pair]
MaybePair: TypeAlias = Pair | Any
MaybePairs: TypeAlias = list[MaybePair]


class HashTable:
    def __init__(self, capacity: int):
        self._validate_capacity(capacity)
        self._slots: MaybePairs = [None] * capacity

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        capacity = len(d) * 10
        t = HashTable(capacity)
        for key, value in d.items():
            t[key] = value
        return t

    @staticmethod
    def _validate_capacity(capacity):
        if not isinstance(capacity, int):
            raise ValueError('`capacity` must be integer')
        if capacity <= 0:
            raise ValueError('`capacity` must be positive')

    def _probe(self, key: Key):
        index = self._make_index(key)
        for _ in range(self.capacity):
            yield index, self._slots[index]
            index = (index + 1) % self.capacity

    @property
    def keys(self) -> list[Key]:
        return [pair.key for pair in self._slots if pair not in (None, Pair.deleted)]

    @property
    def values(self) -> list[Value]:
        return [pair.value for pair in self._slots if pair not in (None, Pair.deleted)]

    @property
    def pairs(self) -> Pairs:
        return [pair for pair in self._slots if pair not in (None, Pair.deleted)]

    @property
    def capacity(self) -> int:
        return len(self._slots)

    def get(self, key: Key, default: Value = None) -> Value:
        for _, pair in self._probe(key):
            if pair not in (None, Pair.deleted) and pair.key == key:
                return pair.value
        return default

    def __len__(self) -> int:
        return len(self.pairs)

    def __getitem__(self, key: Hashable) -> Value:
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is Pair.deleted:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        for index, pair in self._probe(key):
            if pair is Pair.deleted:
                continue
            if pair is None or pair.key == key:
                self._slots[index] = Pair(key, value)
                break
        else:
            raise MemoryError('Not enough capacity')

    def __delitem__(self, key: Hashable) -> None:
        for index, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is Pair.deleted:
                continue
            if pair.key == key:
                self._slots[index] = Pair.deleted
                break
        else:
            raise KeyError(key)

    def __contains__(self, key: Hashable) -> bool:
        index = self._make_index(key)
        return self._slots[index] not in (None, Pair.deleted)

    def __iter__(self):
        return iter(self.keys)

    def __str__(self) -> str:
        return '{' + ', '.join(map(str, self.pairs)) + '}'

    def _get_pair(self, key: Hashable) -> MaybePair:
        index = self._make_index(key)
        for index, pair in self._probe(key):
            if pair is Pair.deleted:
                continue
            return self._slots[index]

    def _make_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity
