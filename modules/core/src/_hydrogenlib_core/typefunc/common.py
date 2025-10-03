from typing import Literal, Protocol

from .function import get_signature

builtin_types = (
    int, float, str, bool,
    None, list, tuple, dict, set,
    bytes, bytearray, memoryview, slice, type
)


def int_to_bytes(num: int, lenght, byteorder: Literal["little", "big"] = 'little'):
    try:
        byte = num.to_bytes(lenght, byteorder)
    except OverflowError as e:
        raise e
    return byte


def int_to_bytes_nonelength(num: int):
    length = len(hex(num))
    length = max(length // 2 - 1, 1)  # 十六进制下,每两个字符占一个字节
    return num.to_bytes(length, 'little')


def bytes_to_int(data: bytes, byteorder: Literal["little", "big"] = 'little'):
    if len(data) == 0:
        return
    return int.from_bytes(data, byteorder)


def get_vaild_data(data: bytes) -> bytes:
    """
    100100 -> vaild = 1001
    111100 -> vaild = 1111
    :param data:
    :return:
    """
    # 找到第一个有效数据（逆序），他的后面就是无效数据
    after_data = data[::-1]
    for index, value in enumerate(after_data):
        if value != 0:
            last_invaild = len(data) - index
            return data[:last_invaild]
    return b''


def is_error(exception) -> bool:
    return isinstance(exception, Exception)


def get_attr_by_path(obj, path):
    """
    :param path: 引用路径
    :param obj: 起始对象

    """
    path_ls = path.split(".")
    cur = obj
    for attr in path_ls:
        cur = getattr(cur, attr)
    return cur


def set_attr_by_path(obj, path, value):
    path_ls = path.split(".")
    cur = obj
    for i, attr in path_ls[:-1]:
        cur = getattr(cur, attr)

    setattr(cur, path_ls[-1], value)


def del_attr_by_path(obj, path):
    path_ls = path.split(".")
    cur = obj
    for i, attr in path_ls[:-1]:
        cur = getattr(cur, attr)
    delattr(cur, path_ls[-1])


def get_type_name(type_or_obj):
    if isinstance(type_or_obj, type):
        return type_or_obj.__name__
    return type_or_obj.__class__.__name__


def get_parameters(func):
    return get_signature(func).parameters


def as_address_string(int_id: int):
    return '0x' + format(int_id, '016X')


class AsyncIO[T](Protocol):
    @property
    async def mode(self) -> str:
        ...

    @property
    async def name(self) -> str:
        ...

    async def close(self) -> None:
        ...

    @property
    async def closed(self) -> bool: ...

    def fileno(self) -> int: ...

    def isatty(self) -> bool: ...

    async def read(self, n: int = -1) -> T:
        ...

    def readable(self) -> bool: ...

    async def readline(self, limit: int = -1) -> T:
        ...

    async def readlines(self, hint: int = -1) -> list[T]:
        ...

    async def seek(self, offset: int, whence: int = 0) -> int:
        ...

    def seekable(self) -> bool: ...

    def tell(self) -> int:
        ...

    def truncate(self, size: int = 0) -> int:
        ...

    async def write(self, b: bytes) -> int:
        ...

    def writable(self) -> bool: ...

    def writelines(self, lines: list[T]) -> None:
        ...

    def __enter__(self) -> 'AsyncIO[T]':
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
