from typing import Callable, Generator

AverageCoroType = Generator[None, int, float]


def init_coro(func: Callable) -> Callable:
    """
    Initialize coroutine with None.
    :param func: Reference to generator
    :return: Callable
    """

    def inner(*args, **kwargs) -> Generator:
        generator: Generator = func(*args, **kwargs)
        generator.send(None)
        return generator

    return inner


def average_coro() -> AverageCoroType:
    """
    Sub generator that returns average value
    :return: average
    """
    summ_: int = 0
    counter_: int = 0
    while True:
        try:
            value = yield
            summ_ += value
        except StopIteration:
            return summ_ / counter_
        counter_ += 1
        # yield summ_ / counter_
        # print(summ_/counter_)


@init_coro
def delegator(subgen: AverageCoroType) -> Generator[None, None, float]:
    """
    Delegator function that loops over the sub generator.
    :param subgen: Sub generator
    :return:
    """
    res = yield from subgen
    return res


g: Generator = delegator(average_coro())
for i in range(1, 6):
    g.send(i)

try:
    g.throw(StopIteration)
except StopIteration as e:
    print(e.value)
