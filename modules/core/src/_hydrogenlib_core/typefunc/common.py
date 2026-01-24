from typing import Protocol, Self

builtin_types = (
    int, float, str, bool,
    None, list, tuple, dict, set,
    bytes, bytearray, memoryview, slice, type, frozenset
)


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


def as_address_string(int_id: int):
    return '0x' + format(int_id, '016X')


def getitems(obj, *items):
    for item in items:
        yield obj[item]


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

    def __enter__(self) -> Self:
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
