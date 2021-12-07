from math import sqrt
from random import shuffle
from typing import Any, Dict, Iterable, List, Optional, TypeVar


def arithmetic_series(n: int, i: int=1, d: int=1) -> int:
    """Calculate the sum of a finite arithmetic progression."""
    max_ = i + (n - 1) * d
    return n * (i + max_) // 2


def inverse_arithmetic_series(arithmetic_series, i: int=1, d: int=1) -> int:
    """Find `n` of an arithmetic series from its summation."""
    # Solve arithmetic series by n:
    # -dn^2 + (d-2i)n + 2*arithmetic_series = 0
    D = (d - 2 * i) ** 2 + 8 * d * arithmetic_series
    if D < 0:
        raise ValueError('D < 0')
    n1 = ((2 * i - d) + sqrt(D)) // (-2 * d)
    if D == 0 or n1 > 0:
        return n1
    return ((2 * i - d) - sqrt(D)) // (-2 * d)


T = TypeVar('T')


def first_value(dict_: Dict[Any, T], default: Optional[T]=None) -> T:
    """Get the first value from a dictionary.
    
    Return `default` value if the dictionary is empty.
    """
    try:
        return next(iter(dict_.values()))
    except StopIteration:
        return default


def shuffled(iterable: Iterable[T]) -> List[T]:
    """Return a randomly shuffled list of an iterable."""
    copy = list(iterable)
    shuffle(copy)
    return copy
