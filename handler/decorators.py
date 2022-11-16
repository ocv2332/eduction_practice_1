import functools


def check_argument(condition, message):
    def wrapper(function):
        @functools.wraps(function)
        def inner(*args, **kwargs):
            assert condition(*args, **kwargs), message
            return function(*args, **kwargs)

        return inner

    return wrapper
