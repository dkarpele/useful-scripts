from typing import Callable


def average_closure(counter: int = 0, summ: int = 0) -> Callable:
    """
    Calculate average with values sent on every function call. Use closures.
    :param summ: current summ
    :param counter: count function calls
    """
    def inner(value) -> float:
        nonlocal counter
        nonlocal summ
        summ += value
        counter += 1
        return summ / counter
    return inner


a = average_closure()
print(a(1))
print(a(2))
print(a(3))
print(a(4))
print(a(5))
