import functools
from types import FunctionType
from typing import Any, Protocol

from .function import get_name


class Descriptor(Protocol):
    def __get__(self, instance, owner): ...

    def __set__(self, instance, value): ...

    def __delete__(self, instance): ...

    def __set_name__(self, owner, name): ...


def mixin(typ: type[Any], *, name=None, sync=True, wrap=False):
    def decorator(func: FunctionType):
        nonlocal name
        name = name or get_name(func)

        final_func = func
        if wrap:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            final_func = wrapper

        elif sync:
            if original_func := getattr(typ, name, None):
                functools.update_wrapper(final_func, original_func)

            else:
                final_func.__dict__.update({
                    '__name__': name,
                    '__qualname__': typ.__name__ + '.' + name,
                    '__module__': typ.__module__,
                })

        setattr(typ, name, final_func)
        return func

    return decorator


def mixin_descriptor(typ: type[Any], name: str, descriptor: Descriptor, call_set_name: bool = True):
    setattr(
        typ, name, descriptor
    )
    if call_set_name and (set_name := getattr(typ, '__set_name__', None)):
        set_name(typ, name)
