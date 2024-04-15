def average_closure(start=0, summ=0):
    def inner(value):
        nonlocal start
        nonlocal summ
        summ += value
        start += 1
        return summ / start

    return inner


a = average_closure()
print(a(1))
print(a(2))
print(a(3))
