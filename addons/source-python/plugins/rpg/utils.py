# Python imports
from math import sqrt
from random import shuffle
from typing import Any, Dict, Iterable, List, Optional, TypeVar


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
