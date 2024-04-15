import itertools

summ = 0
counter = itertools.count(1)


def average_global_var(value: int) -> float:
    """
    Calculate average with values sent on every function call.
    :param value: Value added to the list
    :return: Current average
    """
    global summ
    summ += value
    return summ / next(counter)


print(average_global_var(1))
print(average_global_var(2))
print(average_global_var(3))
print(average_global_var(4))
print(average_global_var(10))
