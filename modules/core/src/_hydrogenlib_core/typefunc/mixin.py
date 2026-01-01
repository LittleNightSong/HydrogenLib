from typing import Any, Protocol
from .function import get_name
from types import FunctionType
import functools


class Descriptor(Protocol):
    def __get__(self, instance, owner): ...
    def __set__(self, instance, value): ...
    def __delete__(self, instance): ...
    def __set_name__(self, owner, name): ...



def mixin(typ: type[Any], *, name=None, sync=True):
    def decorator(func: FunctionType):
        nonlocal name
        name = name or get_name(func)

        if sync:
            functools.update_wrapper(func, getattr(typ, name))

        setattr(typ, name, func)
        return func

    return decorator


def mixin_descriptor(typ: type[Any], name: str, descriptor: Descriptor, call_set_name: bool = True):
    setattr(
        typ, name, descriptor
    )
    if call_set_name and (set_name := getattr(typ, '__set_name__', None)):
        set_name(typ, name)

