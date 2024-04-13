from collections.abc import Sequence


def get_average(seq: Sequence[int | float]) -> float:
    """
    Simply calculate average value
    :param seq: Sequence of values
    :return: average in seq
    """
    try:
        return sum(seq) / len(seq)
    except ZeroDivisionError:
        print('Sequence can not be empty')


print(get_average([1, 2, 3, 4, 5]))
