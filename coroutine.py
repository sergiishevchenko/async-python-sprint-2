
from functools import wraps


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        fn.send(None)
        return fn

    return inner