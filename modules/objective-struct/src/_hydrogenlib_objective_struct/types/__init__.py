import builtins

from .types import *


def get_ctype(cls):
    try:
        return cls.__ctype__
    except AttributeError:
        return {
            builtins.int: 'i',
            builtins.float: 'f',
            builtins.bool: '?',
        }[cls]
