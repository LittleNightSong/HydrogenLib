import struct
import typing
from collections.abc import Buffer
from typing import Any


class _CType(typing.Protocol):
    __ctype__: str


def to_format_string(format: tuple[str | _CType, ...]):
    format = ''.join(
        map(
            lambda x: x if isinstance(x, str) else x.__ctype__,
            format
        )
    )
    return format


def pack(format: tuple[str | _CType, ...], *data: Any) -> bytes:
    return struct.pack(to_format_string(format), *data)


def unpack(format: tuple[str | _CType], data: Buffer):
    return struct.unpack(to_format_string(format), data)
