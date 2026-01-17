import builtins
import collections.abc
from typing import Iterable, Self, ClassVar


class c_types:
    pad = None

    char = builtins.bytes

    byte = \
        ubyte = builtins.int

    bool = builtins.bool

    short = \
        ushort = \
        int = \
        uint = \
        long = \
        ulong = \
        llong = \
        ullong = builtins.int

    short_float = \
        float = \
        double = builtins.float

    ssize_t = builtins.int
    size_t = builtins.int

    string = builtins.bytes
    bytearray = builtins.bytearray

    pointer = builtins.int


class Struct:
    format: ClassVar[str]
    size: ClassVar[int]

    def __init__(self, *args, **kwargs): ...

    @property
    def field_values(self) -> tuple: ...

    def pack(self) -> bytes: ...

    def pack_into(self, buffer: collections.abc.Buffer) -> None: ...

    @classmethod
    def unpack(cls, buffer: collections.abc.Buffer) -> Self: ...

    @classmethod
    def unpack_from(cls, buffer: collections.abc.Buffer, offset=0) -> Self: ...

    @classmethod
    def iter_unpack(cls, buffer: collections.abc.Buffer) -> Iterable[Self]: ...

    @property
    def format(self) -> str: ...

    @property
    def size(self) -> int: ...
