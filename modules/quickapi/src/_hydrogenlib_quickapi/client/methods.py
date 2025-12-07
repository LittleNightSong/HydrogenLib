from __future__ import annotations

import inspect
from typing import Callable, Any

try:
    import typeguard
except ImportError:
    typeguard = None


class ValidateError(Exception):
    """
    参数验证失败
    """


def pre_validate[**P, T](*validators: Callable[[Any], bool]):
    """
    预处理
    :param validators:
    :return:
    """

    def decorator(func: Callable[P, T]):
        signature = inspect.signature(func)

        def wrapper(*args, **kwargs):
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()

            for validator in validators:
                if not validator(bound_args.arguments):
                    raise ValidateError(f"参数验证失败, 给定的参数有: {bound_args.arguments}")  # 操作中断

            return func(*args, **kwargs)

        return wrapper

    return decorator


def type_guard(value_preprocessor=None):
    def decorator(fun):
        signature = inspect.signature(fun)
        params_with_annotation = [(k, v.annotation) for k, v in signature.parameters.items() if
                                  v.annotation != inspect.Parameter.empty]

        def wrapper(*args, **kwargs):
            params = signature.bind(*args, **kwargs)

            for param, annotation in params_with_annotation:
                value = params.arguments[param]
                if value_preprocessor:
                    value = value_preprocessor(value)
                typeguard.check_type(value, annotation)

            return fun(*args, **kwargs)

        return wrapper

    return decorator
