import dataclasses
import struct
import typing
from collections.abc import Buffer
from typing import Self, Generator, Any, ClassVar


class CType(typing.Protocol):
    __ctype__: str


class Struct(CType):
    """
    Base class for creating structured data with a defined format, suitable for packing and unpacking binary data.

    This class allows the creation of a structure that can be used to pack and unpack binary data according to a
    specified format. It supports type annotations for defining the fields of the structure.
    The class automatically generates the necessary format string for the `struct` module based on the provided
    field types. It also provides methods for comparing instances, packing and unpacking data,
    and converting the structure to a dictionary representation.

    Usage:
        class MyStruct(Struct):
            a: int
            b: bool
            c: float
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
    def iter_unpack_reused(cls, buffer) -> Generator[Self, None, None]:
        ...

    def update_from(self, buffer: Buffer, offset=0) -> None:
        ...

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
