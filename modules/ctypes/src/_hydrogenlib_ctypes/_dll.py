import ctypes
import functools

from _hydrogenlib_core.typefunc import alias
from ._types import CType, Prototype


class _DLLMeta(type):
    def __getattr__(self, item) -> 'DLL':
        if item.startswith('_'):
            raise AttributeError(f'{self.__name__} has no attribute {item!r}')
        return self(item)


class DLL(metaclass=_DLLMeta):
    def __init__(self, name: str):
        self._name = name
        self._dll = ctypes.CDLL(self._name)

    def value(self, name: str, type):
        type = CType.as_ctype(type)
        return type.in_dll(self._dll, name)

    def __call__(self, maybe_func=None, *, name: str = None, output_param=None):
        def decorator(func):
            nonlocal name
            name = name or func.__name__

            prototype = Prototype.from_pyfunc(func)
            if output_param:
                prototype = prototype.replace(output_param=output_param)

            wrapper = functools.update_wrapper(prototype.bind(self, name), func)

            return wrapper

        return decorator if not maybe_func else decorator(maybe_func)

    _as_parameter_ = __cobj__ = alias['_dll']
