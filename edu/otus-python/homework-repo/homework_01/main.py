"""
Домашнее задание №1
Функции и структуры данных
"""

from typing import Iterable, List


def power_numbers(*numbers: int) -> List[int]:
    """Возвращает список квадратов переданных чисел.

    >>> power_numbers(1, 2, 5, 7)
    [1, 4, 25, 49]
    """

    return [number ** 2 for number in numbers]


# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"


def is_prime(number: int) -> bool:
    """Проверяет, является ли число простым."""

    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for divider in range(3, int(number ** 0.5) + 1, 2):
        if number % divider == 0:
            return False
    return True


def filter_numbers(numbers: Iterable[int], filter_type: str) -> List[int]:
    """Возвращает числа из ``numbers`` согласно типу фильтрации.

    :param numbers: последовательность целых чисел
    :param filter_type: тип фильтрации (ODD, EVEN или PRIME)
    """

    if filter_type == ODD:
        func = lambda x: x % 2 != 0
    elif filter_type == EVEN:
        func = lambda x: x % 2 == 0
    elif filter_type == PRIME:
        func = is_prime
    else:
        raise ValueError("Unsupported filter type")
    return list(filter(func, numbers))
