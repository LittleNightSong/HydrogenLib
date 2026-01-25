import inspect

from typing_extensions import Literal

from _hydrogenlib_core.typefunc import get_name
from ._types import Prototype


def c_function(
        maybe_func=None, *,
        name: str = None,
        functype: Literal['c', 'py'] = 'c'
):
    def decorator(func):
        nonlocal name
        if name is None:
            name = get_name(func)

        signature = inspect.signature(func)

        restype = signature.return_annotation

        if restype is signature.empty:
            restype = None

        argtypes = [
            param.annotation
            for param in signature.parameters.values()
        ]

        return Prototype(restype, *argtypes, protocol=functype)

    return decorator if not maybe_func else decorator(maybe_func)
