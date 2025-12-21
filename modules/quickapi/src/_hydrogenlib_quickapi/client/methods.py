from __future__ import annotations
import functools


class ValidateError(Exception):
    """
    参数验证失败
    """


def validators(**validators):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for name, validator in validators.items():
                kwargs[name] = validator(kwargs[name])
            return await func(*args, **kwargs)

        return wrapper

    return decorator
