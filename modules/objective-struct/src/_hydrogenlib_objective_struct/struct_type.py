import dataclasses
import struct
import typing
from collections.abc import Buffer
from typing import Self, Generator, Any, ClassVar


class CType(typing.Protocol):
    __ctype__: str


class Struct(CType):
    """
    代表C语言结构体的Python类。
    提供了将结构体对象与字节序列之间互相转换的功能，
    包括打包、解包、更新等操作。
    """

    __cfields__: ClassVar[tuple[dataclasses.Field]]
    __cstruct__: ClassVar[struct.Struct]
    __cendian__: ClassVar[str]

    def pack(self) -> bytes:
        ...

    def pack_into(self, buffer: Buffer, offset=0) -> None:
        ...

    @classmethod
    def unpack(cls, buffer) -> Self:
        ...

    @classmethod
    def unpack_from(cls, buffer, offset=0) -> Self:
        ...

    @classmethod
    def iter_unpack(cls, buffer) -> Generator[Self, None, None]:
        ...

    @classmethod
    def iter_update(cls, buffer) -> Generator[Self, None, None]:
        ...

    def update(self, buffer: Buffer) -> None:
        ...

    def update_from(self, buffer: Buffer, offset=0) -> None:
        ...

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
