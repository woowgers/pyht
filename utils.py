from random import choice, choices, randint
from string import ascii_letters
from typing import Any


def random_integer() -> int:
    return randint(-10000, 10000)


def random_positive() -> int:
    return randint(1, 10000)


def random_float() -> float:
    return random_integer() / random_positive()


def random_boolean() -> bool:
    return choice((True, False))


def random_string() -> str:
    length = abs(random_integer()) % 20
    return ''.join(choices(ascii_letters, k=length))


def random_none() -> None:
    return None


def random_value():
    random_functions = (
        random_integer,
        random_float,
        random_string,
        random_none,
    )
    get_random_value = choice(random_functions)
    return get_random_value()


def random_unique_values(n_values: int) -> list[Any]:
    def append_random_value(lst: list):
        while True:
            value = random_value()
            if value not in lst:
                lst.append(value)
                return

    random_values = []
    for _ in range(n_values):
        append_random_value(random_values)
    return random_values
