from functools import wraps
from typing import Generator, Callable, overload


class EnhancedGenerator[YT, ST, RT](Generator[YT, ST, RT]):
    __slots__ = ('gen', 'cnt', 'history')

    def throw(self, typ, val=None, tb=None, /):
        return self.gen.throw(typ, val, tb)

    def send(self, value, /):
        return self.gen.send(value)

    def close(self):
        return self.gen.close()

    def __init__(self, gen, history: bool = False):
        self.gen: Generator = gen
        self.cnt = -1
        self.history = [] if history else None

    def trace(self, val):
        if self.history is not None:
            self.history.append(val)

    def next(self, value=None):
        self.cnt += 1
        value = self.send(value)
        self.trace(value)
        return value

    def next_with_exception(self, exception: Exception):
        self.cnt += 1
        value = self.throw(type(exception), exception, exception.__traceback__)
        self.trace(value)
        return value

    def get(self, index):
        if index < self.cnt:
            if self.history is None:
                raise IndexError("Index out of range")
            else:
                return self.history[index]

        for i in range(index - self.cnt - 1):
            self.next()

        return self.next()

    def iter_slice(self, slice_: slice):
        start, stop, step = slice_.start or 0, slice_.stop, slice_.step or 1
        for i in range(start, stop, step):
            yield self.get(i)

    def iter_n(self, n: int):
        for i in range(n):
            yield self.next()

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.get(item)

        elif isinstance(item, slice):
            return list(self.iter_slice(item))

        else:
            raise TypeError("Invalid slice")



def enhanced_generator[YT, ST, RT](
        func: Callable[[...], Generator[YT, ST, RT]] = None,
        *,
        history: bool = False,
):
    def decorator(func: Callable[[...], Generator[YT, ST, RT]]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return EnhancedGenerator(
                func(*args, **kwargs), history=history
            )

        return wrapper

    if func is None:
        return decorator

    return decorator(func)
