from functools import wraps


def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args]=func(*args)
        return cache[args]
    return wrap


@memo
def fib(i):
    if i<2: return 1
    return fib(i-1)+fib(i-2)


def fib_iter(n):
    if n < 2:
        return 1
    a, b = 1,1
    while n >= 2:
        c = a+b
        a = b
        b = c
        n = n-1
    return c


import time
print('start: ', time.time())
print(fib_iter(10000000))
print('end: ', time.time())