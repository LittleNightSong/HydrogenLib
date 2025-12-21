import builtins as bt

from _hydrogenlib_core.typefunc import alias, get_type_name
from .base import AbstractCType

from ctypes import *


class pytype(AbstractCType):
    pytp = alias['__real_type__'](mode=alias.mode.read_write)
    ctype = alias['__real_ctype__'](mode=alias.mode.read_write)

    def __init__(self, pytype, ctype=None):
        self.pytp = pytype
        self.ctype = ctype

    def __str__(self):
        return get_type_name(self.pytp)

    def __convert_ctype__(self, obj):
        origin = obj.__class__
        match self.pytp:
            case bt.str:
                match origin:
                    case bt.str:
                        return obj
                    case bt.bytes:
                        return obj.decode()
                    case bt.memoryview:
                        return obj.to_bytes().decode()
                    case _:
                        raise TypeError(f'{origin} cannot convert to {self.pytp}')
            case bt.bytes:
                match origin:
                    case bt.bytes:
                        return obj
                    case bt.str:
                        return obj.encode()
                    case bt.memoryview:
                        return obj.to_bytes()
                    case _:
                        raise TypeError(f'{origin} cannot convert to {self.pytp}')

            case bt.memoryview:
                match origin:
                    case bt.memoryview:
                        return obj
                    case bt.bytes:
                        return memoryview(obj)
                    case bt.str:
                        return memoryview(obj.encode())
                    case _:
                        raise TypeError(f'{origin} cannot convert to {self.pytp}')

            case x:
                return x(obj)


int = pytype[int, c_int]
float = pytype[float, c_float]
str = pytype[str, c_wchar_p]
bytes = pytype[bytes, c_char_p]
memoryview = pytype[memoryview, c_void_p]
bytearray = pytype[bytearray, c_void_p]
list = pytype[list, c_void_p]
tuple = pytype[tuple, c_void_p]
dict = pytype[dict, c_void_p]
set = pytype[set, c_void_p]
